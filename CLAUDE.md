# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Carousel quality evaluation system that scores generated food carousels on relevance, diversity, and content quality. Computes 7 deterministic metrics across 3 dimensions using semantic embeddings (`all-MiniLM-L6-v2`) and 90-day order history as ground truth.

## Commands

There is no build system, package manager config, or requirements.txt. Dependencies must be installed manually.

### Local Evaluation (no Spark required)

```bash
# Stage 1: Prepare — find common consumers across two carousel sources, embed orders
python carousel_eval/local_eval_test.py --prepare \
  --carousel_csv prod_carousels.csv \
  --carousel_csv_2 retrieved_carousel.csv \
  --order_history_csv orders.csv \
  --output_dir .

# Stage 2: Evaluate a carousel source
python carousel_eval/local_eval_test.py --carousel_csv prod_carousels.csv \
  --orders_embedded_pkl ./orders_embedded.pkl \
  --common_consumers_csv ./common_consumers.csv \
  --source_name prod --output_dir .
```

### Production Job (Databricks + Spark)

```bash
python carousel_eval/eval_job.py \
  --carousel_table proddb.ml.cx_profile_generated_carousels_ebr \
  --output_table proddb.ml.cx_carousel_quality_eval \
  --order_history_lookback_days 90
```

### Tests

Unit tests and smoke tests live in the Jupyter notebook `carousel_eval/eval_sample_test.ipynb`:
- **Stage 1**: Pure NumPy unit tests for each metric (no external deps beyond numpy)
- **Stage 2**: Embedding smoke test (requires `sentence-transformers`)
- **Stage 3**: End-to-end mini run (requires Databricks + Snowflake)

## Architecture

### Three-Layer Design

1. **Metric Layer** (`carousel_eval/metrics.py`) — Pure Python/NumPy metric functions. No Spark dependency. All functions are deterministic, side-effect-free, and return values in [0, 1] or None.

2. **Data Processing Layer** (`carousel_eval/eval_job.py`) — Spark-based production job. Loads carousels + order history from Snowflake, embeds both, unions into a combined DataFrame, then runs a single `applyInPandas` pass grouped by (consumer_id, day_part) to compute all metrics together.

3. **Local Evaluation Layer** (`carousel_eval/local_eval_test.py`) — Standalone script for CSV-based evaluation without production infrastructure. Supports a two-stage workflow: prepare (embed orders once, save pickle) then evaluate (load pickle, compute metrics).

### Data Flow (Production)

Snowflake carousels + order history → embed both → union into single DataFrame → `groupBy(consumer_id, day_part).applyInPandas(_compute_group)` → calls `compute_all_metrics()` from metrics.py → write results to Snowflake.

The combined-DataFrame + single-applyInPandas pattern lets all metrics share embedding lookups without redundant computation.

### The 7 Metrics

**Relevance**: MMS (mean max similarity), SR@K (semantic recall at K=3,5,10), CCR (cuisine coverage recall via inlined taxonomy)
**Diversity**: ILD (intra-list diversity), OHCD (order history coverage diversity)
**Quality**: TMC (title-metadata coherence), FCS (format compliance — 7 rule checks)
**Composite**: Weighted average with renormalization for missing metrics.

### Key Constants (in `metrics.py`)

- `DEFAULT_THETA = 0.45` — similarity threshold for SR@K
- `SR_K_VALUES = (3, 5, 10)`
- `COMPOSITE_WEIGHTS` — MMS: 20%, SR@5: 15%, CCR: 15%, ILD: 10%, OHCD: 10%, TMC: 15%, FCS: 15%
- Cuisine taxonomy: ~270 cuisines with hierarchical paths, mapped to top-level families for CCR

### Dependencies

**Core**: `numpy`, `pandas`, `sentence-transformers`
**Production only**: `pyspark`, `fabricator_core`, internal DoorDash libraries
**Optional**: `snowflake.connector` (for direct Snowflake queries in local script)

### Design Principles

- Metrics are pure functions fully testable in isolation — no metrics code imports Spark
- All computation is deterministic (same input → same output)
- Missing data handled via None propagation throughout
- Embedding model cached per executor process in production to avoid reloads
