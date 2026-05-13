"""
Evaluate EBR carousels for v2 consumers and compare against v2 baseline.

Steps:
  1. Find consumers in both 10k_v2_carousels.csv and EBR table
  2. Fetch EBR carousels (with LAST_UPDATE_DATE) for overlap consumers
  3. Fetch fresh 90-day order history ending eval_date (default 2026-05-07)
  4. Embed (title_only) and run evaluation -> eval_ebr.csv
  5. Compare against eval_v2.csv with Wilcoxon signed-rank test
  6. Correlate metric deltas with LAST_UPDATE_DATE age

Usage:
    python carousel_eval/10k_eval_v2/run_ebr_eval.py \
        --token <PAT> \
        --eval_date 2026-05-07 \
        --output_dir carousel_eval/10k_eval_v2
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import snowflake.connector
from scipy.stats import spearmanr, wilcoxon

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from local_eval_test import (
    DEFAULT_THETA,
    embed_carousels,
    embed_items,
    generate_report,
    get_embedding_model,
    normalize_ebr,
    normalize_order_history,
    run_evaluation,
)

# Reuse V2 carousel parser from run_10k_eval_v2.py
sys.path.insert(0, os.path.dirname(__file__))
from run_10k_eval_v2 import parse_carousels as parse_v2_carousels

ORDER_LOOKBACK_DAYS = 90
EBR_TABLE = "proddb.ml.cx_profile_generated_carousels_ebr"

# Match significance_by_label.py — TMC and FCS excluded
METRIC_COLS = [
    "mms", "sr_at_3", "sr_at_5", "sr_at_10",
    "ccr", "ild", "tcd", "redundancy_rate",
    "ohcd", "composite_quality_score",
]

LOWER_IS_BETTER = {"redundancy_rate"}


# ---------------------------------------------------------------------------
# Snowflake helpers
# ---------------------------------------------------------------------------

def get_connection(user: str, token: str) -> snowflake.connector.SnowflakeConnection:
    return snowflake.connector.connect(
        account=os.environ.get("SNOWFLAKE_ACCOUNT", "doordash"),
        user=user,
        token=token,
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "ADHOC_ETL"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "PRODDB"),
        authenticator="PROGRAMMATIC_ACCESS_TOKEN",
    )


def query_to_df(conn, sql: str) -> pd.DataFrame:
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [d[0].lower() for d in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=cols)
    finally:
        cur.close()


def fetch_ebr_carousels(conn, consumer_ids: List[int], batch_size: int = 2000) -> pd.DataFrame:
    chunks = []
    total = (len(consumer_ids) + batch_size - 1) // batch_size
    for i in range(0, len(consumer_ids), batch_size):
        batch = consumer_ids[i: i + batch_size]
        id_list = ", ".join(str(c) for c in batch)
        sql = f"""
        SELECT consumer_id, day_part, carousel_rank, title, tags, last_update_date
        FROM {EBR_TABLE}
        WHERE consumer_id IN ({id_list})
        """
        batch_num = i // batch_size + 1
        print(f"  [ebr] Batch {batch_num}/{total} ({len(batch)} consumers) ...")
        chunk = query_to_df(conn, sql)
        chunks.append(chunk)
        print(f"    -> {len(chunk):,} rows")
    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()


def fetch_orders(conn, consumer_ids: List[int], eval_date: str, batch_size: int = 1000) -> pd.DataFrame:
    start_date = (
        datetime.strptime(eval_date, "%Y-%m-%d") - timedelta(days=ORDER_LOOKBACK_DAYS)
    ).strftime("%Y-%m-%d")

    chunks = []
    total = (len(consumer_ids) + batch_size - 1) // batch_size
    for i in range(0, len(consumer_ids), batch_size):
        batch = consumer_ids[i: i + batch_size]
        id_list = ", ".join(str(c) for c in batch)
        sql = f"""
        WITH base_order_items AS (
            SELECT
                a.creator_id                AS consumer_id,
                a.store_id,
                a.item_id,
                a.item_name,
                a.description,
                EXTRACT(HOUR FROM CONVERT_TIMEZONE('UTC', a.timezone, a.actual_delivery_time)) AS local_hour,
                DAYOFWEEKISO(CONVERT_TIMEZONE('UTC', a.timezone, a.actual_delivery_time)) AS day_of_week
            FROM public.dimension_order_item a
            WHERE a.created_at::DATE BETWEEN '{start_date}' AND '{eval_date}'
              AND a.order_cart_id IS NOT NULL
              AND a.is_filtered_core = TRUE
              AND a.removed_at IS NULL
              AND a.is_group_order = 0
              AND a.creator_id IN ({id_list})
        ),
        daypart_map AS (
            SELECT DISTINCT local_hour, day_part_regroup
            FROM static.hour_to_daypart_mapping
        )
        SELECT DISTINCT
            b.consumer_id,
            CASE WHEN b.day_of_week <= 5 THEN 'weekday' ELSE 'weekend' END || '_' || dm.day_part_regroup AS day_part,
            b.item_id,
            b.item_name,
            COALESCE(b.description, '') AS description,
            ds.is_cng,
            dmu.cuisine_tags AS cuisine_tags_from_menu
        FROM base_order_items b
        INNER JOIN daypart_map dm ON b.local_hour = dm.local_hour
        INNER JOIN edw.merchant.dimension_store ds ON b.store_id = ds.store_id
        LEFT  JOIN edw.merchant.dimension_menu dmu ON b.store_id = dmu.store_id
        WHERE ds.is_cng = 0
        """
        batch_num = i // batch_size + 1
        print(f"  [orders] Batch {batch_num}/{total} ({len(batch)} consumers) ...")
        chunk = query_to_df(conn, sql)
        chunks.append(chunk)
        print(f"    -> {len(chunk):,} rows")
    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()


# ---------------------------------------------------------------------------
# Statistical comparison (Wilcoxon + Holm-Bonferroni + Cohen's d)
# ---------------------------------------------------------------------------

def cohens_d(diffs: np.ndarray) -> float:
    std = diffs.std(ddof=1)
    return 0.0 if std == 0 else float(diffs.mean() / std)


def d_label(d: float) -> str:
    ad = abs(d)
    if ad < 0.2:
        return "negligible"
    if ad < 0.5:
        return "small"
    if ad < 0.8:
        return "medium"
    return "large"


def holm_bonferroni(p_values: Dict[str, float]) -> Dict[str, float]:
    items = sorted(p_values.items(), key=lambda x: x[1])
    m = len(items)
    adjusted, max_so_far = {}, 0.0
    for i, (name, p) in enumerate(items):
        adj_p = max(min(p * (m - i), 1.0), max_so_far)
        max_so_far = adj_p
        adjusted[name] = adj_p
    return adjusted


def compare_metrics(df_a: pd.DataFrame, df_b: pd.DataFrame, label_a: str, label_b: str) -> str:
    merged = df_a.merge(df_b, on=["consumer_id", "day_part"], suffixes=("_a", "_b"))
    print(f"\n[compare] Paired rows: {len(merged):,}")

    results = []
    raw_p = {}
    for m in METRIC_COLS:
        col_a, col_b = f"{m}_a", f"{m}_b"
        if col_a not in merged.columns or col_b not in merged.columns:
            continue
        valid = merged[[col_a, col_b]].dropna()
        if len(valid) < 10:
            continue
        vals_a, vals_b = valid[col_a].values, valid[col_b].values
        diffs = vals_a - vals_b
        if np.all(diffs == 0):
            p = 1.0
            d = 0.0
        else:
            _, p = wilcoxon(diffs, alternative="two-sided")
            d = cohens_d(diffs)
        results.append({
            "metric": m, "n": len(valid),
            "mean_a": float(vals_a.mean()), "mean_b": float(vals_b.mean()),
            "mean_diff": float(diffs.mean()), "cohens_d": d,
            "d_label": d_label(d), "wilcoxon_p": float(p),
        })
        raw_p[m] = float(p)

    adj_p = holm_bonferroni(raw_p)
    for r in results:
        r["adj_p"] = adj_p.get(r["metric"], 1.0)

    lines = [
        f"# EBR vs V2 Comparison: {label_a} vs {label_b}",
        "",
        f"- **Test**: Wilcoxon signed-rank (two-sided, paired)",
        f"- **Correction**: Holm-Bonferroni",
        f"- **Paired rows**: {len(merged):,}",
        "",
        f"| Metric | N | Mean({label_a}) | Mean({label_b}) | Diff | Cohen's d | Effect | adj-p | Sig |",
        f"|--------|---|---------|---------|------|-----------|--------|-------|-----|",
    ]
    for r in sorted(results, key=lambda x: x["adj_p"]):
        m = r["metric"]
        sig = "✓" if r["adj_p"] < 0.05 else ""
        higher_better = m not in LOWER_IS_BETTER
        diff_str = f"{r['mean_diff']:+.4f}"
        lines.append(
            f"| {m} | {r['n']} | {r['mean_a']:.4f} | {r['mean_b']:.4f} | "
            f"{diff_str} | {r['cohens_d']:.3f} | {r['d_label']} | "
            f"{r['adj_p']:.4f} | {sig} |"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Latest_update_date correlation analysis
# ---------------------------------------------------------------------------

def analyze_freshness_correlation(
    metrics_ebr: pd.DataFrame,
    metrics_v2: pd.DataFrame,
    ebr_raw: pd.DataFrame,
    eval_date: str,
) -> str:
    # Compute per-(consumer_id, day_part) last update date
    ebr_dates = (
        ebr_raw.groupby(["consumer_id", "day_part"])["last_update_date"]
        .max()
        .reset_index()
    )
    ebr_dates["last_update_date"] = pd.to_datetime(ebr_dates["last_update_date"], errors="coerce")
    ref_date = pd.Timestamp(eval_date)
    ebr_dates["age_days"] = (ref_date - ebr_dates["last_update_date"]).dt.days

    merged = metrics_ebr.merge(
        metrics_v2, on=["consumer_id", "day_part"], suffixes=("_ebr", "_v2")
    ).merge(ebr_dates[["consumer_id", "day_part", "age_days"]], on=["consumer_id", "day_part"])

    lines = [
        "",
        "# Freshness Correlation (Spearman ρ: metric delta vs EBR entry age)",
        "",
        f"- **EBR entry age** = days between `last_update_date` and eval_date ({eval_date})",
        f"- **metric delta** = EBR metric − v2 metric (positive = EBR is better)",
        f"- **N** = {len(merged):,} paired (consumer_id, day_part) rows",
        "",
        "| Metric | ρ | p-value | Interpretation |",
        "|--------|---|---------|----------------|",
    ]

    for m in METRIC_COLS:
        col_ebr, col_v2 = f"{m}_ebr", f"{m}_v2"
        if col_ebr not in merged.columns or col_v2 not in merged.columns:
            continue
        valid = merged[["age_days", col_ebr, col_v2]].dropna()
        if len(valid) < 10:
            continue
        delta = valid[col_ebr].values - valid[col_v2].values
        rho, p = spearmanr(valid["age_days"].values, delta)
        if abs(rho) >= 0.2 and p < 0.05:
            interp = "older EBR -> larger delta" if rho > 0 else "older EBR -> smaller delta"
        else:
            interp = "no clear trend"
        lines.append(f"| {m} | {rho:.3f} | {p:.4f} | {interp} |")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--token", default=os.environ.get("SNOWFLAKE_TOKEN"), help="Snowflake PAT token")
    p.add_argument("--user", default="SICONGBRYAN.FANG")
    p.add_argument("--eval_date", default="2026-05-07")
    p.add_argument("--v2_carousels", default="carousel_eval/10k_eval_v2/10k_v2_carousels.csv")
    p.add_argument("--v2_eval", default="carousel_eval/10k_eval_v2/eval_v2.csv")
    p.add_argument("--output_dir", default="carousel_eval/10k_eval_v2")
    p.add_argument("--sample_limit", type=int, default=0, help="Limit consumers for testing")
    p.add_argument("--skip_fetch", action="store_true", help="Reuse saved ebr_carousels_raw.csv and ebr_orders.csv")
    return p.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    ebr_raw_path = os.path.join(args.output_dir, "ebr_carousels_raw.csv")
    orders_path = os.path.join(args.output_dir, "ebr_orders.csv")

    if not args.skip_fetch:
        if not args.token:
            raise ValueError("--token or SNOWFLAKE_TOKEN env var required")

        print("[connect] Connecting to Snowflake ...")
        conn = get_connection(args.user, args.token)
        print("[connect] Connected!")

        # Step 1: consumer overlap (v2 carousels ∩ EBR)
        print(f"\n[load] Reading v2 consumer IDs from {args.v2_carousels} ...")
        df_v2 = pd.read_csv(args.v2_carousels, usecols=["CONSUMER_ID"])
        v2_consumers = set(df_v2["CONSUMER_ID"].unique())
        print(f"  v2 consumers: {len(v2_consumers):,}")

        print("[query] Fetching EBR consumer IDs ...")
        df_ebr_ids = query_to_df(conn, f"SELECT DISTINCT consumer_id FROM {EBR_TABLE}")
        ebr_consumers = set(df_ebr_ids["consumer_id"].unique())
        print(f"  EBR consumers: {len(ebr_consumers):,}")

        common = sorted(v2_consumers & ebr_consumers)
        print(f"  Overlap (v2 ∩ EBR): {len(common):,}")

        if args.sample_limit > 0:
            common = common[:args.sample_limit]
            print(f"  [sample] Limited to {len(common):,} consumers")

        if not common:
            print("[ERROR] No common consumers found.")
            conn.close()
            return

        # Step 2: Fetch EBR carousels
        print("\n[fetch] Fetching EBR carousels ...")
        df_ebr_raw = fetch_ebr_carousels(conn, common)
        df_ebr_raw.to_csv(ebr_raw_path, index=False)
        print(f"  Saved {len(df_ebr_raw):,} rows -> {ebr_raw_path}")

        # Step 3: Fetch fresh order history
        start_date = (
            datetime.strptime(args.eval_date, "%Y-%m-%d") - timedelta(days=ORDER_LOOKBACK_DAYS)
        ).strftime("%Y-%m-%d")
        print(f"\n[fetch] Fetching orders (window: {start_date} to {args.eval_date}) ...")
        df_orders_raw = fetch_orders(conn, common, args.eval_date)
        df_orders_raw.to_csv(orders_path, index=False)
        print(f"  Saved {len(df_orders_raw):,} rows -> {orders_path}")

        conn.close()
    else:
        print(f"[skip_fetch] Loading from {ebr_raw_path} and {orders_path} ...")
        df_ebr_raw = pd.read_csv(ebr_raw_path)
        df_orders_raw = pd.read_csv(orders_path)
        common = sorted(df_ebr_raw["consumer_id"].unique().tolist())
        print(f"  EBR rows: {len(df_ebr_raw):,}, Order rows: {len(df_orders_raw):,}, Consumers: {len(common):,}")

    # Step 4: Normalize & embed EBR carousels (title_only)
    print("\n[norm] Normalizing EBR carousels ...")
    df_carousel = normalize_ebr(df_ebr_raw)
    print(f"  Carousel rows: {len(df_carousel):,}")

    print("[norm] Normalizing order history ...")
    df_orders = normalize_order_history(df_orders_raw)
    print(f"  Order rows: {len(df_orders):,}")

    # Filter to consumers present in both
    common_set = set(df_carousel["consumer_id"].unique()) & set(df_orders["consumer_id"].unique())
    df_carousel = df_carousel[df_carousel["consumer_id"].isin(common_set)]
    df_orders = df_orders[df_orders["consumer_id"].isin(common_set)]
    print(f"  After filtering to consumers with both carousels & orders: {len(common_set):,}")

    model = get_embedding_model()

    print("[embed] Embedding EBR carousels (title_only) ...")
    df_carousel = embed_carousels(model, df_carousel, "title_only")

    print("[embed] Embedding order items (title_only) ...")
    df_orders = embed_items(model, df_orders, "title_only")

    # Step 5: Run evaluation
    print("\n[eval] Running EBR evaluation ...")
    metrics_ebr = run_evaluation(df_carousel, df_orders, "ebr", DEFAULT_THETA)
    generate_report(metrics_ebr, "ebr")

    eval_ebr_path = os.path.join(args.output_dir, "eval_ebr.csv")
    metrics_ebr.to_csv(eval_ebr_path, index=False)
    print(f"[save] {eval_ebr_path} ({len(metrics_ebr):,} rows)")

    # Step 6: Re-evaluate V2 carousels with the SAME order history for a fair comparison
    print(f"\n[v2] Parsing V2 carousels from {args.v2_carousels} ...")
    df_v2_input = pd.read_csv(args.v2_carousels)
    df_v2_input = df_v2_input[df_v2_input["CONSUMER_ID"].isin(common_set)]
    v2_carousel_dfs = []
    for _, row in df_v2_input.iterrows():
        c_df = parse_v2_carousels(row["CONSUMER_ID"], row.get("NORMALIZED_CAROUSELS", ""))
        if not c_df.empty:
            v2_carousel_dfs.append(c_df)
    df_v2_carousel = pd.concat(v2_carousel_dfs, ignore_index=True) if v2_carousel_dfs else pd.DataFrame()
    print(f"  V2 carousel rows: {len(df_v2_carousel):,}")

    print("[embed] Embedding V2 carousels (title_only) ...")
    df_v2_carousel = embed_carousels(model, df_v2_carousel, "title_only")

    print("[eval] Running V2 re-evaluation ...")
    metrics_v2 = run_evaluation(df_v2_carousel, df_orders, "v2", DEFAULT_THETA)
    generate_report(metrics_v2, "v2")

    eval_v2_reeval_path = os.path.join(args.output_dir, "eval_v2_reeval.csv")
    metrics_v2.to_csv(eval_v2_reeval_path, index=False)
    print(f"[save] {eval_v2_reeval_path} ({len(metrics_v2):,} rows)")

    comparison_md = compare_metrics(metrics_ebr, metrics_v2, "ebr", "v2")
    print("\n" + comparison_md)

    # Step 7: Freshness correlation
    freshness_md = analyze_freshness_correlation(metrics_ebr, metrics_v2, df_ebr_raw, args.eval_date)
    print("\n" + freshness_md)

    # Save report
    report_path = os.path.join(args.output_dir, "eval_ebr_vs_v2_report.md")
    with open(report_path, "w") as f:
        f.write(comparison_md)
        f.write("\n\n")
        f.write(freshness_md)
    print(f"\n[save] {report_path}")


if __name__ == "__main__":
    main()
