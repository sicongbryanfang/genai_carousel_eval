# Carousel Quality Evaluation

Scores generated food carousels on **relevance**, **diversity**, and **content quality** using 7 deterministic metrics grounded in 90-day order history. Uses semantic embeddings (`all-MiniLM-L6-v2`) — no LLM-as-judge, no API cost.

## Metrics

| ID | Metric | Dimension | What it measures | Weight |
|----|--------|-----------|-----------------|--------|
| R1 | **MMS** — Mean Max Similarity | Relevance | How well each ordered item is covered by its best-matching carousel | 20% |
| R2 | **SR@K** — Semantic Recall @ K | Relevance | Fraction of ordered items with a good match in the top K carousels (K=3,5,10) | 15% (SR@5) |
| R3 | **CCR** — Cuisine Coverage Recall | Relevance | Fraction of ordered cuisine families represented in the carousel set | 15% |
| D1 | **ILD** — Intra-List Diversity | Diversity | How semantically different the carousels are from each other | 10% |
| D2 | **OHCD** — Order History Coverage Diversity | Diversity | Fraction of carousels that are the best match for at least one ordered item | 10% |
| Q1 | **TMC** — Title–Metadata Coherence | Quality | Cosine similarity between each carousel's title and its food-type tags | 15% |
| Q2 | **FCS** — Format Compliance Score | Quality | Fraction of 7 formatting rules passed (title length, casing, etc.) | 15% |

All metrics return values in [0, 1]. A **composite score** is the weighted average of available metrics, with renormalization when any metric is missing.

## Architecture

```
metrics.py                 Pure Python/NumPy metric functions (no Spark)
  ├── eval_job.py           Spark production job (Databricks + Snowflake)
  └── local_eval_test.py    Standalone CSV-based evaluation (no Spark required)
```

**Three layers:**

1. **Metric layer** (`carousel_eval/metrics.py`) — Pure functions, deterministic, side-effect-free. Testable in isolation.
2. **Production layer** (`carousel_eval/eval_job.py`) — Spark job that loads carousels + order history from Snowflake, embeds both, unions into a single DataFrame, and runs `applyInPandas` grouped by `(consumer_id, day_part)`.
3. **Local layer** (`carousel_eval/local_eval_test.py`) — Two-stage CSV workflow: prepare (embed orders once, save pickle) then evaluate (load pickle, compute metrics).

## Prerequisites

**Core** (always required):
```
numpy pandas sentence-transformers
```

**Production only:**
```
pyspark fabricator_core
```

**Optional** (for Snowflake queries in local script):
```
snowflake-connector-python
```

No `requirements.txt` — install dependencies manually with `pip install`.

## Usage

### Local evaluation (no Spark)

**Stage 1 — Prepare** (embed orders once, find common consumers across two carousel sources):

```bash
python carousel_eval/local_eval_test.py --prepare \
  --carousel_csv prod_carousels.csv \
  --carousel_csv_2 retrieved_carousel.csv \
  --order_history_csv orders.csv \
  --output_dir .
```

Outputs: `orders_embedded.pkl`, `common_consumers.csv`

**Stage 2 — Evaluate** a carousel source against pre-computed artifacts:

```bash
python carousel_eval/local_eval_test.py \
  --carousel_csv prod_carousels.csv \
  --orders_embedded_pkl ./orders_embedded.pkl \
  --common_consumers_csv ./common_consumers.csv \
  --source_name prod \
  --output_dir .
```

Add `--sample_limit 1000` to evaluate a random subset of consumers.

### Production job (Databricks)

```bash
python carousel_eval/eval_job.py \
  --carousel_table proddb.ml.cx_profile_generated_carousels_ebr \
  --output_table proddb.ml.cx_carousel_quality_eval \
  --order_history_lookback_days 90
```

### Tests

Unit tests and smoke tests live in `carousel_eval/eval_sample_test.ipynb`:
- **Stage 1**: Pure NumPy unit tests for each metric
- **Stage 2**: Embedding smoke test (requires `sentence-transformers`)
- **Stage 3**: End-to-end mini run (requires Databricks + Snowflake)

## Configuration

### Key constants (`metrics.py`)

| Constant | Default | Description |
|----------|---------|-------------|
| `DEFAULT_THETA` | 0.45 | Cosine similarity threshold for SR@K |
| `SR_K_VALUES` | (3, 5, 10) | K values for Semantic Recall |
| `COMPOSITE_WEIGHTS` | See table above | Per-metric weights summing to 1.0 |

### CLI flags (`eval_job.py`)

| Flag | Default | Description |
|------|---------|-------------|
| `--carousel_table` | `proddb.ml.cx_profile_generated_carousels_ebr` | Source carousel table |
| `--output_table` | `proddb.ml.cx_carousel_quality_eval` | Destination results table |
| `--order_history_lookback_days` | 90 | Days of order history to use |
| `--embedding_model` | `all-MiniLM-L6-v2` | Sentence-transformer model name |
| `--embed_batch_size` | 512 | Embedding batch size per executor |
| `--sr_theta` | 0.45 | SR@K similarity threshold |

### CLI flags (`local_eval_test.py`)

| Flag | Description |
|------|-------------|
| `--prepare` | Run prepare stage (embed orders, find common consumers) |
| `--carousel_csv` | Path to carousel CSV |
| `--carousel_csv_2` | Second carousel CSV (for common-consumer intersection) |
| `--order_history_csv` | Path to order history CSV |
| `--orders_embedded_pkl` | Pre-computed order embeddings pickle |
| `--common_consumers_csv` | Pre-computed common consumer IDs |
| `--source_name` | Label for the carousel source in output files |
| `--sample_limit` | Max consumers to evaluate (omit for all) |
| `--output_dir` | Directory for output files |

## Output schema

Each result row represents one `(consumer_id, day_part)` group:

| Column | Type | Description |
|--------|------|-------------|
| `consumer_id` | long | Consumer identifier |
| `day_part` | string | Meal period (e.g. `weekday_lunch`) |
| `mms` | float | Mean Max Similarity |
| `sr_at_3` | float | Semantic Recall @ 3 |
| `sr_at_5` | float | Semantic Recall @ 5 |
| `sr_at_10` | float | Semantic Recall @ 10 |
| `ccr` | float | Cuisine Coverage Recall |
| `ild` | float | Intra-List Diversity |
| `ohcd` | float | Order History Coverage Diversity |
| `tmc` | float | Title–Metadata Coherence |
| `fcs` | float | Format Compliance Score |
| `composite_quality_score` | float | Weighted composite of above metrics |
| `active_date` | string | Evaluation date (production only) |
| `embedding_model` | string | Model used for embeddings (production only) |
