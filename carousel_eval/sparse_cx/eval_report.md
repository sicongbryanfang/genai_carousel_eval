# Sparse CX Carousel Evaluation Report

Evaluation of 4 prompt candidates across 20 sparse consumers, 8 dayparts.
Carousels contain title + cuisine_filter only (no food_type metadata).

## Metrics Computed


| Metric    | Description                                                                                        |
| --------- | -------------------------------------------------------------------------------------------------- |
| ILD       | Intra-List Diversity (1 - mean pairwise cosine similarity of titles)                               |
| TCD       | Title Cluster Diversity (fraction of distinct topic clusters among titles, threshold=0.65)          |
| RR        | Redundancy Rate (fraction of title pairs that are near-duplicates, threshold=0.75; lower=better)   |
| MMS       | Mean Max Similarity (avg best match between order items and carousel titles)                       |
| SR@K      | Semantic Recall at K (fraction of order items covered by top-K carousels, threshold=0.45)          |
| OHCD      | Order History Coverage Diversity (fraction of carousels that best-match at least one order item)   |
| CCR       | Cuisine Coverage Recall (fraction of ordered cuisine families present in carousel cuisine filters) |
| Composite | Weighted average: MMS 20%, SR@5 15%, CCR 15%, ILD 10%, OHCD 10% (renormalized for missing)         |


## Data Coverage

- **Total consumers**: 20
- **Total (consumer, daypart) groups**: 160
- **Groups with order history** (for MMS, SR@K, OHCD, CCR): 82
- **Order history source**: Snowflake `public.dimension_order_item` — 2-year lookback (16 consumers with orders, 322 unique items)
- **CCR ground truth**: `CUISINE_TAGS_FROM_MENU` from order history (not search queries)

## Overall Comparison


| Metric    | Prompt 1              | Prompt 2              | Prompt 3              | Prompt 4              |
| --------- | --------------------- | --------------------- | --------------------- | --------------------- |
| ILD       | **0.6641 +/- 0.0521** | 0.6595 +/- 0.0523     | 0.6360 +/- 0.0607     | 0.6380 +/- 0.0601     |
| TCD       | **0.9200 +/- 0.1063** | 0.9181 +/- 0.0983     | 0.8769 +/- 0.1347     | 0.8787 +/- 0.1642     |
| RR        | 0.0038 +/- 0.0094     | **0.0017 +/- 0.0073** | 0.0076 +/- 0.0152     | 0.0083 +/- 0.0165     |
| MMS       | 0.4803 +/- 0.1465     | 0.4795 +/- 0.1444     | **0.4953 +/- 0.1466** | 0.4887 +/- 0.1472     |
| SR@3      | 0.3426 +/- 0.3193     | 0.3196 +/- 0.3181 | 0.3805 +/- 0.3304     | **0.3731 +/- 0.3258** |
| SR@5      | 0.4253 +/- 0.3224     | 0.3924 +/- 0.3161 | 0.4565 +/- 0.3321     | **0.4675 +/- 0.3336** |
| SR@10     | 0.4741 +/- 0.3312     | 0.4593 +/- 0.3231 | **0.5447 +/- 0.3279** | 0.5247 +/- 0.3341     |
| OHCD      | 0.3293 +/- 0.2076     | 0.3195 +/- 0.1934 | 0.3195 +/- 0.1959     | **0.3317 +/- 0.2137** |
| CCR       | **0.9545 +/- 0.1591** | 0.9416 +/- 0.1926 | 0.9188 +/- 0.2278     | 0.9481 +/- 0.1859     |
| Composite | **0.6187 +/- 0.1138** | 0.6078 +/- 0.1134 | 0.6048 +/- 0.1122     | 0.6050 +/- 0.1071     |


## Per-Daypart Breakdown

### Prompt 1


| Daypart            | n   | ILD    | TCD    | RR     | MMS    | SR@5   | CCR    | Composite |
| ------------------ | --- | ------ | ------ | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 20  | 0.6284 | 0.8150 | 0.0044 | 0.4224 | 0.3320 | 0.9375 | 0.5773    |
| weekday_dinner     | 20  | 0.6687 | 0.9300 | 0.0044 | 0.4878 | 0.4546 | 0.9306 | 0.6241    |
| weekday_late_night | 20  | 0.6680 | 0.9500 | 0.0033 | 0.5424 | 0.4480 | 0.9583 | 0.6277    |
| weekday_lunch      | 20  | 0.6493 | 0.8800 | 0.0022 | 0.4655 | 0.4352 | 1.0000 | 0.6090    |
| weekend_breakfast  | 20  | 0.6388 | 0.9250 | 0.0056 | 0.4481 | 0.2500 | 1.0000 | 0.5932    |
| weekend_dinner     | 20  | 0.7072 | 0.9800 | 0.0011 | 0.4504 | 0.3106 | 1.0000 | 0.6232    |
| weekend_late_night | 20  | 0.6807 | 0.9500 | 0.0033 | 0.5272 | 0.6759 | 0.9630 | 0.6780    |
| weekend_lunch      | 20  | 0.6721 | 0.9300 | 0.0056 | 0.4984 | 0.4918 | 0.8333 | 0.6171    |


### Prompt 2


| Daypart            | n   | ILD    | TCD    | RR     | MMS    | SR@5   | CCR    | Composite |
| ------------------ | --- | ------ | ------ | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 20  | 0.6262 | 0.8250 | 0.0067 | 0.4065 | 0.2487 | 0.8125 | 0.5505    |
| weekday_dinner     | 20  | 0.6580 | 0.9300 | 0.0000 | 0.4927 | 0.4435 | 0.9306 | 0.6167    |
| weekday_late_night | 20  | 0.6622 | 0.9450 | 0.0011 | 0.5092 | 0.4807 | 0.9583 | 0.6220    |
| weekday_lunch      | 20  | 0.6458 | 0.8950 | 0.0022 | 0.4699 | 0.3485 | 0.9722 | 0.5898    |
| weekend_breakfast  | 20  | 0.6303 | 0.9000 | 0.0022 | 0.4630 | 0.3333 | 1.0000 | 0.5982    |
| weekend_dinner     | 20  | 0.7048 | 0.9700 | 0.0000 | 0.4479 | 0.2708 | 1.0000 | 0.6029    |
| weekend_late_night | 20  | 0.6768 | 0.9500 | 0.0000 | 0.5503 | 0.6852 | 1.0000 | 0.6800    |
| weekend_lunch      | 20  | 0.6717 | 0.9300 | 0.0011 | 0.4984 | 0.3541 | 0.8333 | 0.6022    |


### Prompt 3


| Daypart            | n   | ILD    | TCD    | RR     | MMS    | SR@5   | CCR    | Composite |
| ------------------ | --- | ------ | ------ | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 20  | 0.5806 | 0.7750 | 0.0200 | 0.4796 | 0.3294 | 0.9375 | 0.5513    |
| weekday_dinner     | 20  | 0.6374 | 0.8700 | 0.0044 | 0.4937 | 0.4343 | 0.9028 | 0.6089    |
| weekday_late_night | 20  | 0.6553 | 0.9300 | 0.0022 | 0.5174 | 0.5059 | 0.9583 | 0.6231    |
| weekday_lunch      | 20  | 0.6188 | 0.8350 | 0.0078 | 0.4759 | 0.3708 | 0.9722 | 0.5882    |
| weekend_breakfast  | 20  | 0.6151 | 0.8750 | 0.0122 | 0.4188 | 0.2292 | 1.0000 | 0.5721    |
| weekend_dinner     | 20  | 0.6605 | 0.9050 | 0.0056 | 0.4788 | 0.4653 | 1.0000 | 0.6170    |
| weekend_late_night | 20  | 0.6712 | 0.9400 | 0.0011 | 0.5726 | 0.7037 | 0.8519 | 0.6713    |
| weekend_lunch      | 20  | 0.6490 | 0.8850 | 0.0078 | 0.5241 | 0.5995 | 0.7130 | 0.6069    |


### Prompt 4


| Daypart            | n   | ILD    | TCD    | RR     | MMS    | SR@5   | CCR    | Composite |
| ------------------ | --- | ------ | ------ | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 20  | 0.6016 | 0.8250 | 0.0178 | 0.4435 | 0.3386 | 0.9375 | 0.5638    |
| weekday_dinner     | 20  | 0.6386 | 0.8750 | 0.0067 | 0.4651 | 0.3676 | 0.9722 | 0.5966    |
| weekday_late_night | 20  | 0.6590 | 0.9050 | 0.0056 | 0.5068 | 0.5109 | 0.9583 | 0.6191    |
| weekday_lunch      | 20  | 0.6324 | 0.8600 | 0.0067 | 0.4744 | 0.4282 | 1.0000 | 0.6016    |
| weekend_breakfast  | 20  | 0.6016 | 0.8350 | 0.0133 | 0.4644 | 0.3542 | 1.0000 | 0.5755    |
| weekend_dinner     | 20  | 0.6698 | 0.9300 | 0.0033 | 0.4849 | 0.5014 | 1.0000 | 0.6251    |
| weekend_late_night | 20  | 0.6571 | 0.9200 | 0.0067 | 0.5609 | 0.6812 | 0.8519 | 0.6577    |
| weekend_lunch      | 20  | 0.6435 | 0.8800 | 0.0067 | 0.5161 | 0.5649 | 0.8333 | 0.6010    |


## Notes

- FCS (Format Compliance) and TMC (Title-Metadata Coherence) were skipped — carousels lack food_type metadata.
- MMS, SR@K, OHCD use item names from 2-year Snowflake order history (`ITEM_NAME` from `public.dimension_order_item`) as ground truth.
- CCR uses `CUISINE_TAGS_FROM_MENU` from order history as ground truth, mapped to the same taxonomy as carousel `CUISINE_FILTER`.
- Composite renormalizes weights across available metrics per group.
- TCD and RR are diagnostic diversity metrics (not included in composite). TCD uses a 0.65 similarity threshold for clustering; RR uses 0.75 for redundancy detection.
- Embedding model: all-MiniLM-L6-v2 (384-D).
- 4 consumers (out of 20) had no order history in the 2-year window; their groups contribute only ILD/TCD/RR to the composite.

