"""
Evaluate carousels from the 10k user prompt CSV format.

Input CSV columns:
  - CONSUMER_ID
  - NORMALIZED_CAROUSELS: JSON array of daypart objects, each with
    {"daypart_name": {"carousels": [{"title": ..., "cuisine_filter": [...]}]}}

Order history: Snowflake-exported CSV via fetch_orders.py (--orders_csv), with
columns: consumer_id, day_part, item_id, item_name, description, is_cng,
cuisine_tags_from_menu.

Since carousels lack food_type/tags, FCS food_type checks and TMC will be
computed with empty food_type lists.

Usage:
    python carousel_eval/10k_eval/run_10k_eval.py \
        --input carousel_eval/10k_eval/10k_user_promp4.csv \
        --orders_csv carousel_eval/10k_eval/10k_orders.csv \
        --output_dir carousel_eval/10k_eval \
        --source_name user_prompt4
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, List

import numpy as np
import pandas as pd

# Add parent dir so we can import from local_eval_test
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from local_eval_test import (
    METRIC_COLS,
    compute_all_metrics,
    embed_carousels,
    embed_items,
    generate_report,
    get_embedding_model,
    normalize_order_history,
    run_evaluation,
    DEFAULT_THETA,
)


# ============================================================================
# Parsing
# ============================================================================


def parse_carousels(consumer_id: int, normalized_carousels_json: str) -> pd.DataFrame:
    """Parse NORMALIZED_CAROUSELS JSON into a flat DataFrame."""
    rows = []
    try:
        carousel_list = json.loads(normalized_carousels_json)
    except (json.JSONDecodeError, TypeError):
        return pd.DataFrame(columns=[
            "consumer_id", "day_part", "carousel_rank",
            "title", "food_type", "cuisine_type",
        ])

    for dp_obj in carousel_list:
        for day_part, dp_data in dp_obj.items():
            if not isinstance(dp_data, dict):
                continue
            carousels = dp_data.get("carousels", [])
            for rank, c in enumerate(carousels, 1):
                cuisine_filter = c.get("cuisine_filter", []) or []
                cuisine_type = [
                    ct.capitalize()
                    for ct in cuisine_filter
                    if ct and ct != "unknown"
                ]
                rows.append({
                    "consumer_id": consumer_id,
                    "day_part": day_part,
                    "carousel_rank": rank,
                    "title": c.get("title", ""),
                    "food_type": [],
                    "cuisine_type": cuisine_type,
                })

    return pd.DataFrame(rows)


# ============================================================================
# Main
# ============================================================================


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run eval on 10k user prompt CSV",
    )
    p.add_argument(
        "--input", required=True,
        help="Path to the input CSV with NORMALIZED_CAROUSELS",
    )
    p.add_argument(
        "--orders_csv", required=True,
        help="Path to Snowflake-exported orders CSV (from fetch_orders.py)",
    )
    p.add_argument("--output_dir", default=".")
    p.add_argument("--source_name", default="user_prompt")
    p.add_argument("--sample_limit", type=int, default=0)
    p.add_argument("--sr_theta", type=float, default=DEFAULT_THETA)
    p.add_argument(
        "--embed_mode",
        choices=["title_only", "title_metadata"],
        default="title_metadata",
    )
    return p.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # Load carousel input
    print(f"[load] Reading {args.input} ...")
    df_input = pd.read_csv(args.input)
    print(f"[load] {len(df_input):,} rows")

    # Load Snowflake orders
    print(f"[load] Reading orders from {args.orders_csv} ...")
    df_orders_raw = pd.read_csv(args.orders_csv)
    df_orders_raw.columns = [c.strip().lower() for c in df_orders_raw.columns]
    print(f"[load] {len(df_orders_raw):,} order rows")

    # Find common consumers
    carousel_consumers = set(df_input["CONSUMER_ID"].unique())
    order_consumers = set(df_orders_raw["consumer_id"].unique())
    common = sorted(carousel_consumers & order_consumers)

    if args.sample_limit > 0:
        common = common[:args.sample_limit]

    print(f"[load] Carousel consumers: {len(carousel_consumers):,}, "
          f"Order consumers: {len(order_consumers):,}, "
          f"Common: {len(common):,}")

    if not common:
        print("[ERROR] No common consumers found.")
        return

    common_set = set(common)

    # Parse carousels for common consumers
    print("[parse] Parsing carousels ...")
    df_input_filtered = df_input[
        df_input["CONSUMER_ID"].isin(common_set)
    ]
    carousel_dfs = []
    for _, row in df_input_filtered.iterrows():
        c_df = parse_carousels(
            row["CONSUMER_ID"],
            row.get("NORMALIZED_CAROUSELS", ""),
        )
        if not c_df.empty:
            carousel_dfs.append(c_df)

    if not carousel_dfs:
        print("[ERROR] No carousels parsed.")
        return

    df_carousel = pd.concat(carousel_dfs, ignore_index=True)

    # Filter and normalize orders
    df_orders_raw = df_orders_raw[
        df_orders_raw["consumer_id"].isin(common_set)
    ]
    df_orders = normalize_order_history(df_orders_raw)
    print(f"[norm] Carousels: {len(df_carousel):,}, "
          f"Orders: {len(df_orders):,}")

    # Embed
    model = get_embedding_model()
    df_carousel = embed_carousels(model, df_carousel, args.embed_mode)
    df_orders = embed_items(model, df_orders, args.embed_mode)

    # Evaluate
    source = args.source_name
    print(f"\n[eval] Running {source} evaluation ...")
    metrics = run_evaluation(
        df_carousel, df_orders, source, args.sr_theta,
    )

    # Report & save
    generate_report(metrics, source)
    out_path = os.path.join(args.output_dir, f"eval_{source}.csv")
    metrics.to_csv(out_path, index=False)
    print(f"\n[done] Saved {out_path} ({len(metrics):,} rows)")


if __name__ == "__main__":
    main()
