"""
Carousel Generation Quality Evaluation Job.

Computes 7 deterministic quality metrics for generated carousels using
order-history as ground truth and all-MiniLM-L6-v2 as the embedding model.
Designed to run *before* the production 768-D embedding pipeline is complete.

Metrics
-------
R1  mms          Mean Max Similarity (relevance, continuous)
R2  sr_at_{3,5,10} Semantic Recall @ K (relevance, binary coverage)
R3  ccr          Cuisine Coverage Recall (relevance, taxonomy-based)
D1  ild          Intra-List Diversity (diversity, carousel-only)
D2  ohcd         Order History Coverage Diversity (diversity, grounded)
Q1  tmc          Title–Metadata Coherence (quality, carousel-only)
Q2  fcs          Format Compliance Score (quality, rule-based)

Output
------
One row per (consumer_id, day_part, active_date) written to OUTPUT_TABLE.
"""

import argparse
import datetime
from typing import List, Optional

import numpy as np
import pandas as pd
from fabricator_core.connectors.context_io import load_from_context
from fabricator_core.connectors.snowflake import load_data_spark
from fabricator_core.core.contexts.dataset_context import DatasetContext
from fabricator_core.core.etl.dataset import DatasetUpload
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T

from fabricator.repository.features.cx_discovery.store_consumer_profiles.cx_profile.carousel_eval.metrics import (
    DEFAULT_THETA,
    SR_K_VALUES,
    compute_all_metrics,
)

# ---------------------------------------------------------------------------
# CLI args
# ---------------------------------------------------------------------------


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--carousel_table", default="proddb.ml.cx_profile_generated_carousels_ebr")
    parser.add_argument("--output_table", default="proddb.ml.cx_carousel_quality_eval")
    parser.add_argument("--order_history_lookback_days", type=int, default=90)
    parser.add_argument("--embedding_model", default="all-MiniLM-L6-v2")
    parser.add_argument("--embed_batch_size", type=int, default=512)
    parser.add_argument("--sr_theta", type=float, default=DEFAULT_THETA)
    known_args, _ = parser.parse_known_args()
    return known_args


TASK_PARAMS = parse_args()
CAROUSEL_TABLE = TASK_PARAMS.carousel_table
OUTPUT_TABLE = TASK_PARAMS.output_table
ORDER_HISTORY_LOOKBACK_DAYS = TASK_PARAMS.order_history_lookback_days
EMBEDDING_MODEL = TASK_PARAMS.embedding_model
EMBED_BATCH_SIZE = TASK_PARAMS.embed_batch_size
SR_THETA = TASK_PARAMS.sr_theta

# ---------------------------------------------------------------------------
# Embedding UDF
# Loads the sentence-transformer model once per executor process (cached via
# module-level dict).  Encodes texts in batches with L2-normalised output.
# ---------------------------------------------------------------------------

_MODEL_CACHE: dict = {}


@F.pandas_udf(T.ArrayType(T.FloatType()))
def embed_texts_udf(texts: pd.Series) -> pd.Series:
    global _MODEL_CACHE
    if EMBEDDING_MODEL not in _MODEL_CACHE:
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415

        _MODEL_CACHE[EMBEDDING_MODEL] = SentenceTransformer(EMBEDDING_MODEL)
    model = _MODEL_CACHE[EMBEDDING_MODEL]
    embs = model.encode(
        texts.tolist(),
        batch_size=EMBED_BATCH_SIZE,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return pd.Series(embs.tolist())


# ---------------------------------------------------------------------------
# applyInPandas schema and per-group function
# ---------------------------------------------------------------------------

_METRICS_SCHEMA = T.StructType(
    [
        T.StructField("consumer_id", T.LongType()),
        T.StructField("day_part", T.StringType()),
        T.StructField("mms", T.FloatType()),
        T.StructField("sr_at_3", T.FloatType()),
        T.StructField("sr_at_5", T.FloatType()),
        T.StructField("sr_at_10", T.FloatType()),
        T.StructField("ccr", T.FloatType()),
        T.StructField("ild", T.FloatType()),
        T.StructField("ohcd", T.FloatType()),
        T.StructField("tmc", T.FloatType()),
        T.StructField("fcs", T.FloatType()),
        T.StructField("composite_quality_score", T.FloatType()),
    ]
)


def _compute_group(pdf: pd.DataFrame) -> pd.DataFrame:
    """
    Called once per (consumer_id, day_part) group by applyInPandas.

    The combined DataFrame has two row_type values:
      - "carousel"  — one row per carousel (up to 10)
      - "item"      — one row per ordered item in this daypart

    Columns present in *all* rows: consumer_id, day_part, row_type.
    Carousel-only columns: carousel_rank, title, food_type, cuisine_type,
                           carousel_emb, title_emb, food_type_emb.
    Item-only columns:     item_emb, item_cuisine_tags.
    """
    consumer_id = int(pdf["consumer_id"].iloc[0])
    day_part = str(pdf["day_part"].iloc[0])

    carousel_pdf = pdf[pdf["row_type"] == "carousel"].copy()
    item_pdf = pdf[pdf["row_type"] == "item"].copy()

    metrics = compute_all_metrics(
        carousel_ranks=carousel_pdf["carousel_rank"].tolist(),
        titles=carousel_pdf["title"].tolist(),
        food_types=carousel_pdf["food_type"].tolist(),
        cuisine_types=carousel_pdf["cuisine_type"].tolist(),
        carousel_emb_list=carousel_pdf["carousel_emb"].tolist(),
        title_emb_list=carousel_pdf["title_emb"].tolist(),
        food_type_emb_list=carousel_pdf["food_type_emb"].tolist(),
        item_emb_list=item_pdf["item_emb"].tolist(),
        item_cuisine_tag_list=item_pdf["item_cuisine_tags"].tolist(),
        theta=SR_THETA,
    )

    # Initialise every schema column to None so applyInPandas never sees a
    # missing column, regardless of which code paths ran inside compute_all_metrics
    # (e.g. embedding-dependent metrics are skipped when embeddings are absent).
    row: dict = {
        "consumer_id": consumer_id,
        "day_part": day_part,
        "mms": None,
        "sr_at_3": None,
        "sr_at_5": None,
        "sr_at_10": None,
        "ccr": None,
        "ild": None,
        "ohcd": None,
        "tmc": None,
        "fcs": None,
        "composite_quality_score": None,
    }
    row.update(metrics)

    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# Main job class
# ---------------------------------------------------------------------------


class CarouselQualityEvalJob(DatasetUpload):
    def __init__(self, context: DatasetContext):
        self.context = context
        self.active_date = (context.time + datetime.timedelta(days=-1)).date().isoformat()
        self.start_date = (
            datetime.datetime.strptime(self.active_date, "%Y-%m-%d")
            - datetime.timedelta(days=ORDER_HISTORY_LOOKBACK_DAYS)
        ).date().isoformat()

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------

    def load_carousels(self) -> DataFrame:
        """Load generated carousels for the active date."""
        return load_data_spark(
            f"""
            SELECT
                consumer_id,
                day_part,
                carousel_rank,
                title,
                tags['food_type']    AS food_type,
                tags['cuisine_type'] AS cuisine_type
            FROM {CAROUSEL_TABLE}
            WHERE active_date = '{self.active_date}'
            """
        )

    def load_order_history(self) -> DataFrame:
        """
        Load restaurant order items from the lookback window.

        Only restaurant items are kept (is_cng = 0).  Group orders are excluded
        to avoid items that may not reflect the individual consumer's preference.
        cuisine_tags_from_menu is split into an array on ingestion.
        """
        df = load_from_context(
            DatasetContext.from_source("purchased_items_for_profiles_base_instance"),
            active_date_range=f"{self.start_date}...{self.active_date}",
            allowed_missing_dates=2,
        )
        return (
            df.filter(F.col("is_cng") == 0)
            .filter(F.col("is_group_order") == 0)
            .select(
                "consumer_id",
                F.col("daypart_breakdown").alias("day_part"),
                "item_id",
                "item_name",
                F.coalesce(F.col("description"), F.lit("")).alias("description"),
                F.split(
                    F.coalesce(F.col("cuisine_tags_from_menu"), F.lit("")), ", "
                ).alias("cuisine_tags"),
            )
            # One row per (consumer, daypart, item) — deduplicate repeated purchases
            # of the same item so the embedding lookup benefits from max deduplication.
            .dropDuplicates(["consumer_id", "day_part", "item_id"])
        )

    # ------------------------------------------------------------------
    # Embedding
    # ------------------------------------------------------------------

    def embed_carousels(self, df: DataFrame) -> DataFrame:
        """
        Add three embedding columns to the carousel DataFrame:
          - carousel_emb   : embed("{title}: {food_type joined}")  — for R1/R2/D1/D2
          - title_emb      : embed(title)                          — for Q1
          - food_type_emb  : embed(food_type joined)               — for Q1
        """
        return (
            df.withColumn("food_type_str", F.concat_ws(", ", F.col("food_type")))
            .withColumn(
                "carousel_text",
                F.concat(F.col("title"), F.lit(": "), F.col("food_type_str")),
            )
            .withColumn("carousel_emb", embed_texts_udf(F.col("carousel_text")))
            .withColumn("title_emb", embed_texts_udf(F.col("title")))
            .withColumn("food_type_emb", embed_texts_udf(F.col("food_type_str")))
        )

    def embed_items(self, df: DataFrame) -> DataFrame:
        """
        Add item_emb column to the order-history DataFrame.
        Embeds "{item_name}. {description}" (or just item_name if description is empty).
        """
        return df.withColumn(
            "item_text",
            F.when(
                F.col("description") != "",
                F.concat(F.col("item_name"), F.lit(". "), F.col("description")),
            ).otherwise(F.col("item_name")),
        ).withColumn("item_emb", embed_texts_udf(F.col("item_text")))

    # ------------------------------------------------------------------
    # Dataset construction
    # ------------------------------------------------------------------

    def construct_dataset(self):
        df_carousels = self.load_carousels()
        df_items = self.load_order_history()

        df_carousels = self.embed_carousels(df_carousels)
        df_items = self.embed_items(df_items)

        # Build a single combined DataFrame with two row types so that a single
        # applyInPandas pass can access both carousel and item data per group.
        _null_float_array = F.lit(None).cast(T.ArrayType(T.FloatType()))
        _null_str_array = F.lit(None).cast(T.ArrayType(T.StringType()))
        _null_str = F.lit(None).cast(T.StringType())
        _null_int = F.lit(None).cast(T.IntegerType())

        df_carousel_rows = df_carousels.select(
            "consumer_id",
            "day_part",
            F.lit("carousel").alias("row_type"),
            F.col("carousel_rank").cast(T.IntegerType()),
            "title",
            "food_type",
            "cuisine_type",
            "carousel_emb",
            "title_emb",
            "food_type_emb",
            _null_float_array.alias("item_emb"),
            _null_str_array.alias("item_cuisine_tags"),
        )

        df_item_rows = df_items.select(
            "consumer_id",
            "day_part",
            F.lit("item").alias("row_type"),
            _null_int.alias("carousel_rank"),
            _null_str.alias("title"),
            _null_str_array.alias("food_type"),
            _null_str_array.alias("cuisine_type"),
            _null_float_array.alias("carousel_emb"),
            _null_float_array.alias("title_emb"),
            _null_float_array.alias("food_type_emb"),
            "item_emb",
            F.col("cuisine_tags").alias("item_cuisine_tags"),
        )

        df_combined = df_carousel_rows.unionByName(df_item_rows)

        self.df = (
            df_combined.groupBy("consumer_id", "day_part")
            .applyInPandas(_compute_group, schema=_METRICS_SCHEMA)
            .withColumn("active_date", F.lit(self.active_date))
            .withColumn("embedding_model", F.lit(EMBEDDING_MODEL))
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

context = DatasetContext.init()
job = CarouselQualityEvalJob(context)
job.run()
