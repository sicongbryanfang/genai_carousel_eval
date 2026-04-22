"""
Fetch 90-day order history from Snowflake for consumers in the 10k eval CSV.

Uses browser-based SSO for authentication.

Usage:
    python carousel_eval/10k_eval/fetch_orders.py \
        --input carousel_eval/10k_eval/10k_user_promp4.csv \
        --output carousel_eval/10k_eval/10k_orders.csv
"""

from __future__ import annotations

import argparse
import os

import pandas as pd
import snowflake.connector


EVAL_DATE = "2026-02-03"
ORDER_LOOKBACK_DAYS = 90


def get_connection(user: str = None, token: str = None):
    params = dict(
        account=os.environ.get("SNOWFLAKE_ACCOUNT", "doordash"),
        user=user or os.environ.get("SNOWFLAKE_USER", "SICONGBRYAN.FANG"),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "ADHOC_ETL"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "PRODDB"),
    )
    if token:
        params["token"] = token
        params["authenticator"] = "PROGRAMMATIC_ACCESS_TOKEN"
    else:
        params["authenticator"] = "externalbrowser"
    return snowflake.connector.connect(**params)


def query_to_df(conn, sql: str) -> pd.DataFrame:
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [desc[0].lower() for desc in cur.description]
        rows = cur.fetchall()
        return pd.DataFrame(rows, columns=cols)
    finally:
        cur.close()


def fetch_orders(conn, consumer_ids: list[int], batch_size: int = 1000) -> pd.DataFrame:
    from datetime import datetime, timedelta

    start_date = (
        datetime.strptime(EVAL_DATE, "%Y-%m-%d") - timedelta(days=ORDER_LOOKBACK_DAYS)
    ).strftime("%Y-%m-%d")

    chunks: list[pd.DataFrame] = []
    total_batches = (len(consumer_ids) + batch_size - 1) // batch_size

    for i in range(0, len(consumer_ids), batch_size):
        batch = consumer_ids[i : i + batch_size]
        id_list = ", ".join(str(cid) for cid in batch)
        sql = f"""
        WITH base_order_items AS (
            SELECT
                a.creator_id                AS consumer_id,
                a.store_id,
                a.item_id,
                a.item_name,
                a.description,
                EXTRACT(HOUR FROM CONVERT_TIMEZONE(
                    'UTC', a.timezone, a.actual_delivery_time
                ))                           AS local_hour,
                DAYOFWEEKISO(CONVERT_TIMEZONE(
                    'UTC', a.timezone, a.actual_delivery_time
                ))                           AS day_of_week
            FROM public.dimension_order_item a
            WHERE a.created_at::DATE BETWEEN '{start_date}' AND '{EVAL_DATE}'
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
            CASE WHEN b.day_of_week <= 5 THEN 'weekday' ELSE 'weekend' END
                || '_' || dm.day_part_regroup  AS day_part,
            b.item_id,
            b.item_name,
            COALESCE(b.description, '')        AS description,
            ds.is_cng,
            dmu.cuisine_tags                   AS cuisine_tags_from_menu
        FROM base_order_items b
        INNER JOIN daypart_map dm              ON b.local_hour = dm.local_hour
        INNER JOIN edw.merchant.dimension_store ds ON b.store_id = ds.store_id
        LEFT  JOIN edw.merchant.dimension_menu dmu ON b.store_id = dmu.store_id
        WHERE ds.is_cng = 0
        """
        batch_num = i // batch_size + 1
        print(f"[fetch] Batch {batch_num}/{total_batches} ({len(batch)} consumers) ...")
        chunk = query_to_df(conn, sql)
        chunks.append(chunk)
        print(f"  -> {len(chunk):,} rows")

    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="10k eval CSV with CONSUMER_ID column")
    p.add_argument("--output", default="carousel_eval/10k_eval/10k_orders.csv")
    p.add_argument("--user", default=None, help="Snowflake username")
    p.add_argument("--token", default=None, help="Snowflake PAT token")
    args = p.parse_args()

    print(f"[load] Reading consumer IDs from {args.input} ...")
    df = pd.read_csv(args.input, usecols=["CONSUMER_ID"])
    consumer_ids = sorted(df["CONSUMER_ID"].unique().tolist())
    print(f"[load] {len(consumer_ids):,} unique consumers")

    print("[connect] Connecting to Snowflake (browser SSO) ...")
    conn = get_connection(user=args.user, token=args.token)
    print("[connect] Connected!")

    df_orders = fetch_orders(conn, consumer_ids)
    conn.close()

    print(f"\n[save] Total order rows: {len(df_orders):,}")
    df_orders.to_csv(args.output, index=False)
    print(f"[save] Saved to {args.output}")


if __name__ == "__main__":
    main()
