# 10k Eval Carousel Evaluation Report

- **Order history**: 90-day lookback from Snowflake (463,996 rows)
- **Embedding mode**: title_metadata (all-MiniLM-L6-v2)

## Composite Score Formula

TMC is excluded from the composite because the carousel format lacks `food_type` tags, making title-metadata coherence unreliable. TCD and Redundancy Rate are diagnostic only.

```
Composite = 0.20 * MMS + 0.20 * SR@5 + 0.20 * OHCD + 0.15 * CCR + 0.15 * ILD + 0.10 * FCS
```

When a metric is missing (e.g. CCR with no cuisine data), weights are renormalized over available metrics.

| Component | Weight |
| --------- | ------ |
| MMS       | 20%    |
| SR@5      | 20%    |
| OHCD      | 20%    |
| CCR       | 15%    |
| ILD       | 15%    |
| FCS       | 10%    |


## Prompt Comparison


| Metric                         | prompt1    | prompt4    | prompt4_no_think | delta (p4 - p1) | delta (no_think - p4) |
| ------------------------------ | ---------- | ---------- | ---------------- | --------------- | --------------------- |
| **Composite Quality Score**    | **0.5745** | **0.5763** | **0.5853**       | **+0.0018**     | **+0.0090**           |
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
| **Composite Quality Score**             | **0.5853** | **0.0952** | **43,006** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,668 | 0.5369 | 0.5284 | 0.8770 | 0.6421 | 0.6049    |
| weekday_dinner     | 7,646 | 0.5207 | 0.4668 | 0.6793 | 0.6660 | 0.5865    |
| weekday_late_night | 4,667 | 0.5341 | 0.5008 | 0.7785 | 0.6674 | 0.5836    |
| weekday_lunch      | 7,234 | 0.5202 | 0.4751 | 0.7313 | 0.6513 | 0.5891    |
| weekend_breakfast  | 3,618 | 0.5438 | 0.5390 | 0.8924 | 0.6425 | 0.5995    |
| weekend_dinner     | 6,069 | 0.5277 | 0.4808 | 0.7005 | 0.6727 | 0.5716    |
| weekend_late_night | 3,316 | 0.5379 | 0.5122 | 0.8027 | 0.6693 | 0.5747    |
| weekend_lunch      | 5,788 | 0.5220 | 0.4782 | 0.7549 | 0.6610 | 0.5763    |


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
| **Composite Quality Score**             | **0.5763** | **0.0941** | **43,432** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,706 | 0.5006 | 0.4911 | 0.8862 | 0.6137 | 0.5860    |
| weekday_dinner     | 7,717 | 0.5039 | 0.4656 | 0.6941 | 0.6530 | 0.5820    |
| weekday_late_night | 4,714 | 0.5118 | 0.4964 | 0.7895 | 0.6537 | 0.5764    |
| weekday_lunch      | 7,308 | 0.4981 | 0.4676 | 0.7452 | 0.6402 | 0.5823    |
| weekend_breakfast  | 3,652 | 0.5068 | 0.5040 | 0.8985 | 0.6254 | 0.5824    |
| weekend_dinner     | 6,133 | 0.5068 | 0.4724 | 0.7103 | 0.6618 | 0.5645    |
| weekend_late_night | 3,355 | 0.5132 | 0.5061 | 0.8134 | 0.6579 | 0.5673    |
| weekend_lunch      | 5,847 | 0.4970 | 0.4650 | 0.7669 | 0.6516 | 0.5674    |


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
| **Composite Quality Score**             | **0.5745** | **0.0941** | **43,363** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,697 | 0.4955 | 0.4834 | 0.8894 | 0.6250 | 0.5854    |
| weekday_dinner     | 7,705 | 0.4999 | 0.4570 | 0.6969 | 0.6610 | 0.5803    |
| weekday_late_night | 4,705 | 0.5045 | 0.4885 | 0.7908 | 0.6570 | 0.5737    |
| weekday_lunch      | 7,298 | 0.4948 | 0.4578 | 0.7481 | 0.6512 | 0.5809    |
| weekend_breakfast  | 3,648 | 0.5006 | 0.4964 | 0.8982 | 0.6364 | 0.5800    |
| weekend_dinner     | 6,118 | 0.5009 | 0.4607 | 0.7115 | 0.6728 | 0.5625    |
| weekend_late_night | 3,352 | 0.5049 | 0.4884 | 0.8157 | 0.6609 | 0.5621    |
| weekend_lunch      | 5,840 | 0.4937 | 0.4577 | 0.7706 | 0.6608 | 0.5667    |


## Statistical Significance: prompt4 vs no_think

Wilcoxon signed-rank test (non-parametric paired test) with Holm-Bonferroni correction across 42,991 common (consumer, daypart) pairs.

| Metric | Mean prompt4 | Mean no_think | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MMS | 0.5039 | 0.5283 | -0.0243 | -0.31 | small | <0.001 | Yes |
| SR@3 | 0.3875 | 0.3919 | -0.0044 | -0.02 | negligible | 0.1186 | No |
| SR@5 | 0.4793 | 0.4916 | -0.0123 | -0.05 | negligible | <0.001 | Yes |
| SR@10 | 0.5836 | 0.6132 | -0.0296 | -0.13 | negligible | <0.001 | Yes |
| CCR | 0.7722 | 0.7606 | +0.0117 | +0.11 | negligible | <0.001 | Yes |
| ILD | 0.6457 | 0.6596 | -0.0139 | -0.28 | small | <0.001 | Yes |
| TCD | 0.8765 | 0.8606 | +0.0159 | +0.11 | negligible | <0.001 | Yes |
| Redundancy Rate | 0.0090 | 0.0135 | -0.0044 | -0.20 | negligible | <0.001 | Yes |
| OHCD | 0.4276 | 0.4338 | -0.0062 | -0.07 | negligible | <0.001 | Yes |
| TMC | 0.1665 | 0.1607 | +0.0058 | +0.27 | small | <0.001 | Yes |
| FCS | 0.8326 | 0.8325 | +0.0002 | +0.04 | negligible | <0.001 | Yes |
| **Composite** | **0.5439** | **0.5500** | **-0.0062** | **-0.12** | **negligible** | **<0.001** | **Yes** |

Positive diff = prompt4 higher. Negative = no_think higher. For Redundancy Rate, lower is better.

**no_think significantly better:** MMS (d=-0.31, small), ILD (d=-0.28, small), SR@10, SR@5, OHCD, Composite

**prompt4 significantly better:** TMC (d=+0.27, small), TCD, CCR, Redundancy Rate, FCS

**No significant difference:** SR@3

All effect sizes are small or negligible (|d| < 0.5). With n=43k, statistical significance is easily achieved — practical significance (Cohen's d) matters more here.


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


## Brand-Name Title Analysis

No_think produces 3.3x more brand-name titles (18,149 vs 5,445), but the increase is driven by **repetition of the same items across consumers**, not broader brand diversity. Distinct brand titles only grow 2.3x (854 vs 366).

### Top brand-name titles

| Title | prompt4 | no_think | ratio |
| --- | --- | --- | --- |
| Chicken mcnuggets / McNuggets | 756 | 2,875 | 3.8x |
| Big mac burgers / Big Mac burgers | 778 | 1,351 | 1.7x |
| Sausage egg mcgriddles | 275 | 1,120 | 4.1x |
| Whopper burgers / meals | 433 | 1,226 | 2.8x |
| Happy meal variants | 79 | 1,039 | 13.2x |
| Sausage egg mcmuffins | 146 | 807 | 5.5x |
| Big mac meals / Big Mac meals | 315 | 1,767 | 5.6x |

### Brand keyword frequency

| Brand keyword | prompt4 | no_think | ratio |
| --- | --- | --- | --- |
| big mac | 1,622 | 4,315 | 2.7x |
| mcnugget | 837 | 3,526 | 4.2x |
| whopper | 768 | 2,507 | 3.3x |
| mcgriddle | 676 | 2,306 | 3.4x |
| mcmuffin | 472 | 1,921 | 4.1x |
| chipotle | 838 | 1,135 | 1.4x |
| happy meal | 79 | 1,039 | 13.1x |
| mcchicken | 49 | 509 | 10.4x |
| chick-fil-a | 12 | 177 | 14.8x |
| kfc | 15 | 163 | 10.9x |

The no_think model heavily defaults to McDonald's and Burger King item names across many consumers. These brand-specific titles (e.g., "Chicken McNuggets") closely match exact item names in order history, inflating MMS/SR@K scores compared to prompt4's more generic titles (e.g., "Chicken nuggets") which are semantically similar but not as close an embedding match. This suggests the no_think relevance gains are partly an artifact of title specificity rather than better personalization.


## Summary

Disabling thinking tokens produces carousels that score higher on the composite metric (+0.0062), but the effect size is negligible (Cohen's d = -0.12). All 12 metric differences have small or negligible effect sizes (|d| < 0.5), meaning the two variants perform similarly in practice.

**Where no_think wins (relevance):** It generates more specific, brand-level titles (3x more brand-specific, 61% more distinct titles overall) that match order history item names more closely in embedding space. This boosts MMS (d=-0.31, the largest effect) and SR@K metrics. However, this may reflect title-to-item-name similarity rather than genuinely better recommendations.

**Where prompt4 wins (structure):** Thinking tokens help produce better-organized carousels — higher cuisine coverage (CCR), more diverse topic clusters (TCD), lower redundancy, and slightly better format compliance. These are small effects but consistent.

**Where they're equal:** SR@3 shows no significant difference (p=0.12). FCS is virtually identical (diff=0.0002).

**Completeness trade-off:** No-think loses 722 daypart groups and 7,607 carousels (25 fully empty groups), showing the model occasionally produces incomplete structured output without thinking tokens. Prompt4 generates exactly 10 carousels per group every time.

**Bottom line:** The differences are statistically significant (n=43k makes this easy) but practically small. The choice between variants depends on whether you prioritize relevance-to-order-history (no_think) or structural quality and reliability (prompt4).


## Notes

- TMC is excluded from the composite score because the carousel format lacks `food_type` tags; title-metadata coherence cannot be properly computed (~0.17 across all variants).
- CCR uses `cuisine_filter` from carousels mapped to the taxonomy, and `cuisine_tags_from_menu` from Snowflake order history.
- TCD and Redundancy Rate are diagnostic metrics not included in the composite score.

