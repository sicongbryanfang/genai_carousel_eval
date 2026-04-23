"""
Extract V2 carousels from datalake parquet files for the same 10k consumers
used in the original 10k eval (from 10k_user_promp4.csv).

READ-ONLY on DBFS: This script only reads parquet files from the datalake.
It does NOT write, modify, or delete any data on DBFS. Output is written
to a local directory only.

Run this script in Databricks to read parquet files from DBFS and export
a CSV compatible with run_10k_eval_v2.py.

Usage (Databricks):
    python carousel_eval/10k_eval_v2/extract_v2_carousels.py \
        --consumer_csv carousel_eval/10k_eval/10k_user_promp4.csv \
        --output_dir /tmp/10k_eval_v2
"""

from __future__ import annotations

import argparse
import os

import pandas as pd
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


PARQUET_PATHS = [
    "/mnt/doordash-datalake/test_tmp/yangyu/genai_v2_tier12/genai_carousel_v2_carousel_generation_batch_download_carousels_v319_0",
    "/mnt/doordash-datalake/test_tmp/yangyu/genai_v2_tier12/genai_carousel_v2_carousel_generation_batch_download_carousels_v319_1",
    "/mnt/doordash-datalake/test_tmp/yangyu/genai_v2_tier12/genai_carousel_v2_carousel_generation_batch_download_carousels_v319_2",
    "/mnt/doordash-datalake/test_tmp/yangyu/genai_v2_tier12/genai_carousel_v2_carousel_generation_batch_download_carousels_v319_3_4_5",
    "/mnt/doordash-datalake/test_tmp/yangyu/genai_v2_tier12/genai_carousel_v2_carousel_generation_batch_download_carousels_v319_6",
    "/mnt/doordash-datalake/test_tmp/yangyu/genai_v2_tier12/genai_carousel_v2_carousel_generation_batch_download_carousels_v319_7_8_9",
    "/mnt/doordash-datalake/test_tmp/yangyu/genai_v2_tier12/genai_carousel_v2_carousel_generation_batch_download_carousels_v319_combined_round2",
]


def main():
    p = argparse.ArgumentParser(description="Extract V2 carousels for existing 10k consumers")
    p.add_argument("--consumer_csv", required=True,
                   help="Path to existing 10k eval CSV with CONSUMER_ID column "
                        "(e.g. carousel_eval/10k_eval/10k_user_promp4.csv)")
    p.add_argument("--output_dir", default="/tmp/10k_eval_v2",
                   help="Local output directory (NOT on DBFS)")
    args = p.parse_args()

    spark = SparkSession.builder.getOrCreate()

    # Load target consumer IDs from existing 10k eval
    print(f"[load] Reading consumer IDs from {args.consumer_csv} ...")
    pdf_consumers = pd.read_csv(args.consumer_csv, usecols=["CONSUMER_ID"])
    target_ids = sorted(pdf_consumers["CONSUMER_ID"].unique().tolist())
    print(f"[load] {len(target_ids):,} target consumers from existing 10k eval")

    # Broadcast target IDs as a Spark DataFrame for filtering
    df_target = spark.createDataFrame(
        [(int(cid),) for cid in target_ids], ["_target_consumer_id"]
    )

    # Read and union all parquet sources
    print(f"\n[load] Reading {len(PARQUET_PATHS)} parquet paths ...")
    dfs = []
    for path in PARQUET_PATHS:
        try:
            df = spark.read.parquet(path)
            n = df.count()
            print(f"  {path.split('/')[-1]}: {n:,} rows")
            dfs.append(df)
        except Exception as e:
            print(f"  [WARN] Failed to read {path}: {e}")

    if not dfs:
        print("[ERROR] No data loaded from any path.")
        return

    df_all = dfs[0]
    for df in dfs[1:]:
        df_all = df_all.unionByName(df, allowMissingColumns=True)

    # Show schema for debugging
    print("\n[schema]")
    df_all.printSchema()

    total_rows = df_all.count()
    print(f"\n[load] Total rows after union: {total_rows:,}")

    # Identify consumer ID column (try common names)
    cols_lower = {c.lower(): c for c in df_all.columns}
    consumer_col = None
    for candidate in ["consumer_id", "consumerid", "cx_id", "user_id"]:
        if candidate in cols_lower:
            consumer_col = cols_lower[candidate]
            break

    if consumer_col is None:
        print(f"[ERROR] Cannot find consumer ID column. Available: {df_all.columns}")
        return

    print(f"[info] Using consumer ID column: '{consumer_col}'")

    n_consumers = df_all.select(consumer_col).distinct().count()
    print(f"[info] Total unique consumers in V2 data: {n_consumers:,}")

    # Filter to target consumers only
    df_filtered = df_all.join(
        df_target,
        df_all[consumer_col] == df_target["_target_consumer_id"],
        how="inner",
    ).drop("_target_consumer_id")

    # Deduplicate by consumer (keep first occurrence)
    df_dedup = df_filtered.dropDuplicates([consumer_col])

    matched = df_dedup.count()
    print(f"[filter] Matched {matched:,} of {len(target_ids):,} target consumers in V2 data")

    if matched == 0:
        print("[ERROR] No target consumers found in V2 data.")
        return

    # Identify carousel column
    carousel_col = None
    for candidate in ["normalized_carousels", "carousels", "carousel_json",
                       "NORMALIZED_CAROUSELS", "CAROUSELS"]:
        if candidate in cols_lower:
            carousel_col = cols_lower[candidate]
            break

    # Select output columns: CONSUMER_ID, NORMALIZED_CAROUSELS
    if carousel_col:
        df_out = df_dedup.select(
            F.col(consumer_col).alias("CONSUMER_ID"),
            F.col(carousel_col).alias("NORMALIZED_CAROUSELS"),
        )
    else:
        print(f"[WARN] No carousel column auto-detected. Exporting all columns.")
        print(f"[WARN] Available columns: {df_all.columns}")
        print(f"[WARN] You may need to manually rename the carousel column to NORMALIZED_CAROUSELS.")
        df_out = df_dedup.withColumnRenamed(consumer_col, "CONSUMER_ID")

    # Save as CSV
    os.makedirs(args.output_dir, exist_ok=True)
    out_path = os.path.join(args.output_dir, "10k_v2_carousels.csv")

    print(f"\n[save] Writing to {out_path} ...")
    pdf = df_out.toPandas()
    pdf.to_csv(out_path, index=False)
    print(f"[save] Saved {len(pdf):,} rows to {out_path}")

    # Report coverage
    missing = set(target_ids) - set(pdf["CONSUMER_ID"].unique())
    if missing:
        print(f"\n[WARN] {len(missing):,} consumers from the original 10k eval "
              f"are NOT present in V2 data.")


if __name__ == "__main__":
    main()
