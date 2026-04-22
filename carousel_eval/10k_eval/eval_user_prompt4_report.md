# 10k Eval Carousel Evaluation Report

- **Order history**: 90-day lookback from Snowflake (463,996 rows)
- **Embedding mode**: title_metadata (all-MiniLM-L6-v2)

## Prompt Comparison


| Metric                         | prompt1    | prompt4    | prompt4_no_think | delta (p4 - p1) | delta (no_think - p4) |
| ------------------------------ | ---------- | ---------- | ---------------- | --------------- | --------------------- |
| **Composite Quality Score**    | **0.5427** | **0.5439** | **0.5501**       | **+0.0012**     | **+0.0062**           |
| MMS (mean max similarity)      | 0.4988     | 0.5039     | 0.5283           | +0.0051         | +0.0244               |
| SR@3                           | 0.3803     | 0.3874     | 0.3919           | +0.0071         | +0.0045               |
| SR@5                           | 0.4698     | 0.4793     | 0.4916           | +0.0095         | +0.0123               |
| SR@10                          | 0.5715     | 0.5836     | 0.6133           | +0.0121         | +0.0297               |
| CCR (cuisine coverage recall)  | 0.7744     | 0.7721     | 0.7606           | -0.0023         | -0.0115               |
| ILD (intra-list diversity)     | 0.6546     | 0.6458     | 0.6596           | -0.0088         | +0.0138               |
| TCD (title cluster diversity)  | 0.8941     | 0.8766     | 0.8606           | -0.0175         | -0.0160               |
| Redundancy Rate                | 0.0067     | 0.0090     | 0.0135           | +0.0023         | +0.0045               |
| OHCD                           | 0.4254     | 0.4278     | 0.4338           | +0.0024         | +0.0060               |
| TMC (title-metadata coherence) | 0.1695     | 0.1665     | 0.1607           | -0.0030         | -0.0058               |
| FCS (format compliance)        | 0.8314     | 0.8326     | 0.8325           | +0.0012         | -0.0001               |
| Consumers evaluated            | 9,630      | 9,647      | 9,560            |                 |                       |
| (consumer, daypart) groups     | 43,363     | 43,432     | 43,006           |                 |                       |


## prompt4_no_think_no_rationale — Overall Metrics

Prompt4 variant with LLM thinking tokens disabled and no rationale in the output.

| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.5283     | 0.1179     | 43,006     |
| SR@3                                    | 0.3919     | 0.3058     | 43,006     |
| SR@5                                    | 0.4916     | 0.3039     | 43,006     |
| SR@10                                   | 0.6133     | 0.2851     | 43,006     |
| CCR (cuisine coverage recall)           | 0.7606     | 0.3219     | 41,422     |
| ILD (intra-list diversity)              | 0.6596     | 0.0549     | 43,006     |
| TCD (title cluster diversity)           | 0.8606     | 0.1331     | 43,006     |
| Redundancy Rate                         | 0.0135     | 0.0219     | 43,006     |
| OHCD (order history coverage diversity) | 0.4338     | 0.2596     | 43,006     |
| TMC (title-metadata coherence)          | 0.1607     | 0.0219     | 43,006     |
| FCS (format compliance)                 | 0.8325     | 0.0041     | 43,006     |
| **Composite Quality Score**             | **0.5501** | **0.0798** | **43,006** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,668 | 0.5369 | 0.5284 | 0.8770 | 0.6421 | 0.5685    |
| weekday_dinner     | 7,646 | 0.5207 | 0.4668 | 0.6793 | 0.6660 | 0.5435    |
| weekday_late_night | 4,667 | 0.5341 | 0.5008 | 0.7785 | 0.6674 | 0.5527    |
| weekday_lunch      | 7,234 | 0.5202 | 0.4751 | 0.7313 | 0.6513 | 0.5474    |
| weekend_breakfast  | 3,618 | 0.5438 | 0.5390 | 0.8924 | 0.6425 | 0.5687    |
| weekend_dinner     | 6,069 | 0.5277 | 0.4808 | 0.7005 | 0.6727 | 0.5393    |
| weekend_late_night | 3,316 | 0.5379 | 0.5122 | 0.8027 | 0.6693 | 0.5513    |
| weekend_lunch      | 5,788 | 0.5220 | 0.4782 | 0.7549 | 0.6610 | 0.5438    |


## user_prompt4 — Overall Metrics


| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.5039     | 0.1116     | 43,432     |
| SR@3                                    | 0.3874     | 0.2992     | 43,432     |
| SR@5                                    | 0.4793     | 0.2992     | 43,432     |
| SR@10                                   | 0.5836     | 0.2881     | 43,432     |
| CCR (cuisine coverage recall)           | 0.7721     | 0.3156     | 41,837     |
| ILD (intra-list diversity)              | 0.6458     | 0.0528     | 43,432     |
| TCD (title cluster diversity)           | 0.8766     | 0.1264     | 43,432     |
| Redundancy Rate                         | 0.0090     | 0.0166     | 43,432     |
| OHCD (order history coverage diversity) | 0.4278     | 0.2569     | 43,432     |
| TMC (title-metadata coherence)          | 0.1665     | 0.0205     | 43,432     |
| FCS (format compliance)                 | 0.8326     | 0.0036     | 43,432     |
| **Composite Quality Score**             | **0.5439** | **0.0781** | **43,432** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,706 | 0.5006 | 0.4911 | 0.8862 | 0.6137 | 0.5540    |
| weekday_dinner     | 7,717 | 0.5039 | 0.4656 | 0.6941 | 0.6530 | 0.5413    |
| weekday_late_night | 4,714 | 0.5118 | 0.4964 | 0.7895 | 0.6537 | 0.5483    |
| weekday_lunch      | 7,308 | 0.4981 | 0.4676 | 0.7452 | 0.6402 | 0.5434    |
| weekend_breakfast  | 3,652 | 0.5068 | 0.5040 | 0.8985 | 0.6254 | 0.5553    |
| weekend_dinner     | 6,133 | 0.5068 | 0.4724 | 0.7103 | 0.6618 | 0.5344    |
| weekend_late_night | 3,355 | 0.5132 | 0.5061 | 0.8134 | 0.6579 | 0.5460    |
| weekend_lunch      | 5,847 | 0.4970 | 0.4650 | 0.7669 | 0.6516 | 0.5378    |


## user_prompt1 — Overall Metrics


| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.4988     | 0.1110     | 43,363     |
| SR@3                                    | 0.3803     | 0.2980     | 43,363     |
| SR@5                                    | 0.4698     | 0.2985     | 43,363     |
| SR@10                                   | 0.5715     | 0.2898     | 43,363     |
| CCR (cuisine coverage recall)           | 0.7744     | 0.3142     | 41,771     |
| ILD (intra-list diversity)              | 0.6546     | 0.0516     | 43,363     |
| TCD (title cluster diversity)           | 0.8941     | 0.1129     | 43,363     |
| Redundancy Rate                         | 0.0067     | 0.0130     | 43,363     |
| OHCD (order history coverage diversity) | 0.4254     | 0.2559     | 43,363     |
| TMC (title-metadata coherence)          | 0.1695     | 0.0199     | 43,363     |
| FCS (format compliance)                 | 0.8314     | 0.0063     | 43,363     |
| **Composite Quality Score**             | **0.5427** | **0.0780** | **43,363** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,697 | 0.4955 | 0.4834 | 0.8894 | 0.6250 | 0.5539    |
| weekday_dinner     | 7,705 | 0.4999 | 0.4570 | 0.6969 | 0.6610 | 0.5402    |
| weekday_late_night | 4,705 | 0.5045 | 0.4885 | 0.7908 | 0.6570 | 0.5462    |
| weekday_lunch      | 7,298 | 0.4948 | 0.4578 | 0.7481 | 0.6512 | 0.5428    |
| weekend_breakfast  | 3,648 | 0.5006 | 0.4964 | 0.8982 | 0.6364 | 0.5538    |
| weekend_dinner     | 6,118 | 0.5009 | 0.4607 | 0.7115 | 0.6728 | 0.5328    |
| weekend_late_night | 3,352 | 0.5049 | 0.4884 | 0.8157 | 0.6609 | 0.5424    |
| weekend_lunch      | 5,840 | 0.4937 | 0.4577 | 0.7706 | 0.6608 | 0.5375    |


## Data Volume Comparison (prompt4 vs no_think_no_rationale)


| Metric                   | prompt4   | no_think_no_rationale | delta    |
| ------------------------ | --------- | --------------------- | -------- |
| Consumers                | 10,170    | 10,170                | 0        |
| Total daypart groups     | 81,336    | 80,614                | -722     |
| Empty groups             | 0         | 25                    | +25      |
| Total carousels          | 813,360   | 805,753               | -7,607   |
| Distinct carousel titles | 39,718    | 64,083                | +24,365  |
| Avg carousels/consumer   | 80.0      | 79.2                  | -0.8     |
| Brand-specific titles    | 0.64%     | 1.99%                 | +1.35pp  |

- Same 10,170 consumers in both files.
- No-think is missing 722 daypart groups and 7,607 carousels — the model occasionally fails to produce complete output without thinking tokens (25 fully empty groups, plus some partial groups).
- Despite fewer total carousels, no-think produces 61% more distinct titles (64,083 vs 39,718). Without thinking, the model generates more varied, specific item-level names (e.g. "Chicken McNuggets Happy Meals", "Sausage egg mcgriddles") rather than reusing generic category titles across consumers.
- No-think has 3x more brand-specific titles (1.99% vs 0.64%), producing names that match order history items more closely via embedding similarity. This likely explains the higher MMS/SR@K scores despite no thinking tokens.


## Notes

- TMC is low (~0.17) because the carousel format lacks `food_type` tags; title-metadata coherence cannot be properly computed.
- CCR uses `cuisine_filter` from carousels mapped to the taxonomy, and `cuisine_tags_from_menu` from Snowflake order history.
- TCD and Redundancy Rate are diagnostic metrics not included in the composite score.

