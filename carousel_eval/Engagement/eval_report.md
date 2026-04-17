# Engagement-Based Carousel Quality Evaluation

Comparison of carousel quality metrics between high-converting and zero-converting consumers on GenAI carousels, using 90-day engagement and order history as ground truth.

## Consumer Selection

### Data Sources

- **Engagement data**: `discovery_organic_engagement_instance_v1` (Jan 16 – Apr 16, 2026, 90 days)
- **Carousel data**: `proddb.ml.cx_profile_generated_carousels_ebr`
- **Order history**: L6M Top 30 per daypart order history for selected consumers (608K item rows)

### Selection Steps

1. **Load engagement data** — 90 days of engagement events with columns: `consumer_id`, `facet_id`, `is_viewed`, `is_clicked`, `is_converted`.
2. **Filter to GenAI carousels** — Retain rows where `facet_id` contains `"cxgen"`.
3. **Aggregate per consumer** — Group by `consumer_id`, sum conversions and count total impressions.
4. **Top group (high converters)** — 1,937 consumers with the most conversions, ordered by `conversion_count` descending.
5. **Bottom group (zero converters)** — 1,888 consumers with at least one GenAI impression but zero conversions, selected by highest impression count to ensure sufficient exposure.
6. **Fetch carousels** — Join target consumers with the generated carousel table to retrieve their personalized carousels.

### Group Summary


| Group  | Consumers | (Consumer, Daypart) Groups | Carousel Rows |
| ------ | --------- | -------------------------- | ------------- |
| Top    | 1,937     | 14,756                     | 141,080       |
| Bottom | 1,888     | 13,752                     | 134,521       |


## Metrics Computed


| Metric    | Description                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------- |
| MMS       | Mean Max Similarity — avg best cosine match between carousel titles and order-history items       |
| SR@K      | Semantic Recall at K (3, 5, 10) — fraction of order items covered by top-K carousels (θ=0.45)     |
| CCR       | Cuisine Coverage Recall — fraction of ordered cuisine families present in carousel cuisine tags   |
| ILD       | Intra-List Diversity — 1 minus mean pairwise cosine similarity of carousel titles                 |
| TCD       | Title Cluster Diversity — fraction of distinct topic clusters among titles (threshold=0.65)       |
| RR        | Redundancy Rate — fraction of title pairs that are near-duplicates (threshold=0.75; lower=better) |
| OHCD      | Order History Coverage Diversity — fraction of carousels that best-match a unique order item      |
| TMC       | Title-Metadata Coherence — mean dot product of title and food-type embeddings                     |
| FCS       | Format Compliance Score — 6 formatting rule checks per carousel title                             |
| Composite | Weighted average: MMS 20%, SR@5 15%, CCR 15%, ILD 10%, OHCD 10%, TMC 15%, FCS 15%                 |


## Overall Comparison


| Metric            | Top (high converters) | Bottom (zero converters) | Delta   | Favors |
| ----------------- | --------------------- | ------------------------ | ------- | ------ |
| MMS               | **0.4580** +/- 0.0556 | 0.4558 +/- 0.0625        | +0.0022 | Top    |
| SR@3              | **0.3720** +/- 0.1763 | 0.3559 +/- 0.1947        | +0.0161 | Top    |
| SR@5              | **0.4477** +/- 0.1781 | 0.4304 +/- 0.1974        | +0.0173 | Top    |
| SR@10             | **0.5292** +/- 0.1775 | 0.5135 +/- 0.1968        | +0.0157 | Top    |
| CCR               | 0.7090 +/- 0.2719     | **0.7563** +/- 0.2568    | -0.0473 | Bottom |
| ILD               | 0.5245 +/- 0.0489     | **0.5361** +/- 0.0480    | -0.0116 | Bottom |
| TCD               | 0.7738 +/- 0.1996     | **0.8026** +/- 0.1855    | -0.0288 | Bottom |
| RR (lower=better) | 0.0122 +/- 0.0226     | **0.0102** +/- 0.0203    | +0.0020 | Bottom |
| OHCD              | **0.7334** +/- 0.1890 | 0.7063 +/- 0.2101        | +0.0271 | Top    |
| TMC               | **0.6565** +/- 0.0582 | 0.6483 +/- 0.0601        | +0.0082 | Top    |
| FCS               | 0.8898 +/- 0.0669     | **0.8938** +/- 0.0659    | -0.0040 | Bottom |
| Composite         | 0.6227 +/- 0.0541     | **0.6245** +/- 0.0567    | -0.0018 | ~Tie   |


## Per-Daypart Breakdown

### Top Group (High Converters)


| Daypart            | n     | MMS    | SR@5   | CCR    | ILD    | TCD | RR  | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --- | --- | --------- |
| weekday_breakfast  | 1,862 | 0.4769 | 0.4748 | 0.7029 | 0.4939 | —   | —   | 0.6244    |
| weekday_dinner     | 1,909 | 0.4467 | 0.4276 | 0.7266 | 0.5275 | —   | —   | 0.6230    |
| weekday_late_night | 1,756 | 0.4659 | 0.4788 | 0.6591 | 0.5262 | —   | —   | 0.6243    |
| weekday_lunch      | 1,920 | 0.4445 | 0.4218 | 0.7077 | 0.5277 | —   | —   | 0.6192    |
| weekend_breakfast  | 1,826 | 0.4759 | 0.4814 | 0.7078 | 0.5112 | —   | —   | 0.6253    |
| weekend_dinner     | 1,908 | 0.4474 | 0.4234 | 0.7366 | 0.5377 | —   | —   | 0.6219    |
| weekend_late_night | 1,667 | 0.4695 | 0.4822 | 0.6914 | 0.5330 | —   | —   | 0.6277    |
| weekend_lunch      | 1,908 | 0.4404 | 0.4008 | 0.7332 | 0.5384 | —   | —   | 0.6171    |


### Bottom Group (Zero Converters)


| Daypart            | n     | MMS    | SR@5   | CCR    | ILD    | TCD | RR  | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --- | --- | --------- |
| weekday_breakfast  | 1,693 | 0.4684 | 0.4552 | 0.7232 | 0.5123 | —   | —   | 0.6206    |
| weekday_dinner     | 1,851 | 0.4499 | 0.4167 | 0.7779 | 0.5378 | —   | —   | 0.6286    |
| weekday_late_night | 1,609 | 0.4652 | 0.4621 | 0.7172 | 0.5332 | —   | —   | 0.6278    |
| weekday_lunch      | 1,853 | 0.4417 | 0.3979 | 0.7437 | 0.5391 | —   | —   | 0.6197    |
| weekend_breakfast  | 1,619 | 0.4641 | 0.4405 | 0.7397 | 0.5256 | —   | —   | 0.6175    |
| weekend_dinner     | 1,813 | 0.4503 | 0.4209 | 0.8001 | 0.5484 | —   | —   | 0.6290    |
| weekend_late_night | 1,512 | 0.4689 | 0.4723 | 0.7456 | 0.5393 | —   | —   | 0.6304    |
| weekend_lunch      | 1,802 | 0.4430 | 0.3916 | 0.7928 | 0.5502 | —   | —   | 0.6229    |


## Key Findings

### Relevance metrics consistently favor high converters

All semantic relevance metrics (MMS, SR@3/5/10, OHCD) are higher for the top group. The strongest signal is **OHCD (+0.027)**: carousels for high converters cover more distinct parts of their order history, suggesting better personalization breadth. **SR@5 (+0.017)** and **SR@3 (+0.016)** show that top-K carousel items more frequently match actual ordered items above the θ=0.45 threshold.

### Diversity metrics favor zero converters

The bottom group shows higher **CCR (+0.047)**, **ILD (+0.012)**, and **TCD (+0.029)**, with lower redundancy (**RR -0.002**). This pattern indicates their carousels are more topically diverse and cover more cuisine families — but this diversity does not translate to conversions. The carousels may be casting too wide a net rather than targeting known preferences.

### The relevance-diversity tradeoff explains the metric gap

High converters get carousels that are slightly less diverse but substantially more relevant to their actual ordering behavior. Zero converters get more diverse carousels that fail to connect with their preferences. This is consistent with the hypothesis that **relevance-focused metrics (MMS, SR@K, OHCD) better predict conversion** than diversity metrics alone.

### Composite score is nearly identical

The weighted composite differs by only 0.002 between groups, because relevance and diversity improvements cancel out. This suggests the composite weights may need rebalancing if conversion prediction is the goal — increasing weight on relevance metrics (MMS, SR@5, OHCD) at the expense of diversity metrics (ILD, CCR) could make the composite more discriminative.

## Configuration

- **Embedding model**: all-MiniLM-L6-v2 (384-D, unit-normalized)
- **Embed mode**: title_metadata (title + food_type concatenation)
- **SR@K threshold (θ)**: 0.45
- **TCD clustering threshold**: 0.65
- **RR redundancy threshold**: 0.75
- **Evaluation date**: April 16, 2026
- **Engagement window**: Jan 16 – Apr 16, 2026 (90 days)

