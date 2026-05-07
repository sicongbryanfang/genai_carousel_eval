"""
Compare prompt_v4_no_rationale_thinking_1024 vs genai_v2_thinking_1024 broken
down by consumer-level label groups (IS_SPARSE_ORDER, IS_SPARSE_BROWSE) fetched
from Snowflake.

Runs Wilcoxon signed-rank + Holm-Bonferroni + Cohen's d for each of the 4
subgroups (IS_SPARSE_ORDER={T,F} × IS_SPARSE_BROWSE={T,F}) plus an overall
section.

Usage:
    python carousel_eval/10k_eval/significance_by_label.py \
        --csv_a carousel_eval/10k_eval/eval_user_prompt_4_no_rationale_think_1024.csv \
        --csv_b carousel_eval/10k_eval/eval_user_v2_1024thinking.csv \
        --label_a no_rationale_think_1024 \
        --label_b genai_v2_think_1024 \
        --output carousel_eval/10k_eval/significance_by_label_report.md
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import snowflake.connector

from significance_test import (
    METRIC_COLS,
    METRIC_DISPLAY,
    LOWER_IS_BETTER,
    holm_bonferroni,
    run_test,
    cohens_d,
    d_label,
)


LABEL_COLS = ["is_sparse_order", "is_sparse_browse"]


# ============================================================================
# Snowflake
# ============================================================================

def fetch_labels(consumer_ids: list[int], token: str | None = None) -> pd.DataFrame:
    params = dict(
        account=os.environ.get("SNOWFLAKE_ACCOUNT", "doordash"),
        user=os.environ.get("SNOWFLAKE_USER", "SICONGBRYAN.FANG"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "ADHOC_ETL"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "PRODDB"),
    )
    if token:
        params["token"] = token
        params["authenticator"] = "PROGRAMMATIC_ACCESS_TOKEN"
    else:
        params["authenticator"] = "externalbrowser"

    print("[snowflake] Connecting ...")
    conn = snowflake.connector.connect(**params)
    try:
        ids_str = ", ".join(str(c) for c in consumer_ids)
        sql = f"""
            SELECT CONSUMER_ID, IS_SPARSE_ORDER, IS_SPARSE_BROWSE
            FROM PRODDB.ANDYPARK.cx_carousel_v3_prompt_test_enriched
            WHERE CONSUMER_ID IN ({ids_str})
        """
        print("[snowflake] Fetching labels ...")
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0].lower() for d in cur.description]
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=cols)
        print(f"[snowflake] Got {len(df):,} rows")
        return df
    finally:
        conn.close()


# ============================================================================
# Report formatting
# ============================================================================

def format_section(
    results: list[dict],
    label_a: str,
    label_b: str,
    total_pairs: int,
    group_desc: str,
    alpha: float = 0.05,
) -> str:
    lines = []
    lines.append(f"### {group_desc}  (n={total_pairs:,} pairs)")
    lines.append("")
    lines.append(
        f"| Metric | Mean {label_a} | Mean {label_b} | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |")

    for r in results:
        display = METRIC_DISPLAY.get(r["metric"], r["metric"])
        sig = "Yes" if r["adj_p"] < alpha else "No"
        if r["metric"] == "composite_quality_score":
            display = f"**{display}**"
            sig = f"**{sig}**"

        def fmt_p(p):
            return f"{p:.2e}" if p < 0.001 else f"{p:.4f}"

        sign = "+" if r["mean_diff"] > 0 else ""
        lines.append(
            f"| {display} "
            f"| {r['mean_a']:.4f} "
            f"| {r['mean_b']:.4f} "
            f"| {sign}{r['mean_diff']:.4f} "
            f"| {r['cohens_d']:+.4f} "
            f"| {r['d_label']} "
            f"| {fmt_p(r['adj_p'])} "
            f"| {sig} |"
        )

    # Brief interpretation bullet
    lines.append("")
    sig_a, sig_b, no_sig = [], [], []
    for r in results:
        display = METRIC_DISPLAY.get(r["metric"], r["metric"])
        if r["adj_p"] >= alpha:
            no_sig.append(display)
            continue
        better_a = (
            r["mean_diff"] < 0 if r["metric"] in LOWER_IS_BETTER else r["mean_diff"] > 0
        )
        entry = f"{display} (d={r['cohens_d']:+.3f})"
        (sig_a if better_a else sig_b).append(entry)

    if sig_a:
        lines.append(f"**{label_a} better:** " + ", ".join(sig_a))
    if sig_b:
        lines.append(f"**{label_b} better:** " + ", ".join(sig_b))
    if no_sig:
        lines.append(f"**No significant difference:** " + ", ".join(no_sig))
    lines.append("")

    return "\n".join(lines)


def run_group(
    merged: pd.DataFrame,
    label_a: str,
    label_b: str,
    group_desc: str,
    alpha: float = 0.05,
) -> str:
    results = []
    for metric in METRIC_COLS:
        r = run_test(merged, metric, alpha)
        if r is not None:
            results.append(r)

    if not results:
        return f"### {group_desc}\n\n_No data._\n\n"

    raw_p = {r["metric"]: r["wilcoxon_p"] for r in results}
    adj_p = holm_bonferroni(raw_p)
    for r in results:
        r["adj_p"] = adj_p[r["metric"]]

    return format_section(results, label_a, label_b, len(merged), group_desc, alpha)


# ============================================================================
# Main
# ============================================================================

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--csv_a", required=True)
    p.add_argument("--csv_b", required=True)
    p.add_argument("--label_a", default="A")
    p.add_argument("--label_b", default="B")
    p.add_argument("--output", required=True)
    p.add_argument("--token", default=None, help="Snowflake PAT (omit for browser SSO)")
    p.add_argument("--alpha", type=float, default=0.05)
    return p.parse_args()


def main():
    args = parse_args()

    print(f"[load] Reading {args.csv_a} ...")
    df_a = pd.read_csv(args.csv_a)
    print(f"[load] Reading {args.csv_b} ...")
    df_b = pd.read_csv(args.csv_b)

    merged = df_a.merge(df_b, on=["consumer_id", "day_part"], suffixes=("_a", "_b"))
    print(f"[load] Common (consumer, daypart) pairs: {len(merged):,}")

    # Fetch labels for all consumers in merged
    consumer_ids = sorted(merged["consumer_id"].unique().tolist())
    print(f"[load] Fetching labels for {len(consumer_ids):,} consumers ...")
    df_labels = fetch_labels(consumer_ids, token=args.token)
    df_labels.columns = [c.lower() for c in df_labels.columns]

    # Deduplicate labels per consumer (take first row if duplicates)
    df_labels = df_labels.drop_duplicates(subset=["consumer_id"])

    # Join labels onto merged
    merged = merged.merge(df_labels, on="consumer_id", how="left")
    missing = merged[LABEL_COLS].isna().any(axis=1).sum()
    if missing:
        print(f"[warn] {missing:,} rows missing label data — excluded from label-group analysis")

    # Build report
    lines = [
        f"# Significance Report: {args.label_a} vs {args.label_b}",
        "",
        f"- **Test**: Wilcoxon signed-rank (two-sided), Holm-Bonferroni correction, α={args.alpha}",
        f"- **Effect size**: Cohen's d (paired). |d|<0.2=negligible, 0.2–0.5=small, 0.5–0.8=medium, >0.8=large",
        f"- **Positive mean diff** = {args.label_a} higher; **negative** = {args.label_b} higher",
        f"- **Label source**: `PRODDB.ANDYPARK.cx_carousel_v3_prompt_test_enriched`",
        "",
        "## Overall",
        "",
        run_group(merged, args.label_a, args.label_b, "All consumers", args.alpha),
    ]

    for label_col in LABEL_COLS:
        display_col = label_col.upper()
        lines.append(f"## Breakdown by {display_col}")
        lines.append("")
        for val in [True, False]:
            mask = merged[label_col] == val
            sub = merged[mask].copy()
            group_desc = f"{display_col} = {val}  ({len(sub['consumer_id'].unique()):,} consumers)"
            if len(sub) < 10:
                lines.append(f"### {group_desc}\n\n_Not enough data._\n")
                continue
            print(f"[group] {display_col}={val}: {len(sub):,} pairs")
            lines.append(run_group(sub, args.label_a, args.label_b, group_desc, args.alpha))

    report = "\n".join(lines)

    with open(args.output, "w") as f:
        f.write(report)
    print(f"\n[done] Saved {args.output}")


if __name__ == "__main__":
    main()
