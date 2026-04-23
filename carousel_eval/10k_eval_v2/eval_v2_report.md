# V2 Carousel Evaluation Report (Common Consumers Only)

- **Carousel source**: V2 (genai_v2_tier12, v319 batch)
- **Order history**: 90-day lookback ending 2026-03-21 (V2) / 2026-04-16 (P4/P1)
- **Embedding mode**: title_metadata (all-MiniLM-L6-v2)
- **Composite weights**: MMS 20%, SR@5 20%, OHCD 20%, CCR 15%, ILD 15%, FCS 10% (TMC excluded)
- **Common consumers**: 6,534 (present in V2, Prompt 4, and Prompt 1)
- **V2 groups**: 30,818 | **P4 groups**: 30,637 | **P1 groups**: 30,637

## V2 vs Prompt 4 vs Prompt 1 (Common Consumers)


| Metric                                  | V2         | Prompt 4   | Prompt 1   | Δ (V2 - P4) |
| --------------------------------------- | ---------- | ---------- | ---------- | ----------- |
| MMS (mean max similarity)               | 0.4921     | 0.5014     | 0.4967     | -0.0093     |
| SR@3                                    | 0.3681     | 0.3781     | 0.3712     | -0.0100     |
| SR@5                                    | 0.4574     | 0.4693     | 0.4625     | -0.0119     |
| SR@10                                   | 0.5593     | 0.5794     | 0.5686     | -0.0202     |
| CCR (cuisine coverage recall)           | 0.7719     | 0.7719     | 0.7742     | +0.0001     |
| ILD (intra-list diversity)              | 0.6514     | 0.6472     | 0.6556     | +0.0041     |
| TCD (title cluster diversity)           | 0.8915     | 0.8779     | 0.8949     | +0.0135     |
| Redundancy Rate                         | 0.0066     | 0.0088     | 0.0066     | -0.0022     |
| OHCD (order history coverage diversity) | 0.4353     | 0.4397     | 0.4375     | -0.0043     |
| TMC (title-metadata coherence)          | 0.1729     | 0.1663     | 0.1692     | +0.0066     |
| FCS (format compliance)                 | 0.8308     | 0.8326     | 0.8314     | -0.0019     |
| **Composite Quality Score**             | **0.5717** | **0.5764** | **0.5751** | **-0.0047** |
| Consumers                               | 6,534      | 6,534      | 6,534      |             |
| (consumer, daypart) groups              | 30,818     | 30,637     | 30,637     |             |


## V2 — Overall Metrics (Common Consumers)


| Metric                                  | Mean   | Std    | n      |
| --------------------------------------- | ------ | ------ | ------ |
| MMS (mean max similarity)               | 0.4921 | 0.1088 | 30,818 |
| SR@3                                    | 0.3681 | 0.2941 | 30,818 |
| SR@5                                    | 0.4574 | 0.2955 | 30,818 |
| SR@10                                   | 0.5593 | 0.2887 | 30,818 |
| CCR (cuisine coverage recall)           | 0.7719 | 0.3110 | 29,697 |
| ILD (intra-list diversity)              | 0.6514 | 0.0519 | 30,818 |
| TCD (title cluster diversity)           | 0.8915 | 0.1142 | 30,818 |
| Redundancy Rate                         | 0.0066 | 0.0129 | 30,818 |
| OHCD (order history coverage diversity) | 0.4353 | 0.2619 | 30,818 |
| TMC (title-metadata coherence)          | 0.1729 | 0.0196 | 30,818 |
| FCS (format compliance)                 | 0.8308 | 0.0072 | 30,818 |
| **Composite Quality Score**             | 0.5717 | 0.0950 | 30,818 |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 3,333 | 0.4870 | 0.4733 | 0.8797 | 0.6163 | 0.5795    |
| weekday_dinner     | 5,450 | 0.4952 | 0.4467 | 0.6945 | 0.6586 | 0.5796    |
| weekday_late_night | 3,386 | 0.5009 | 0.4808 | 0.7762 | 0.6543 | 0.5714    |
| weekday_lunch      | 5,102 | 0.4886 | 0.4465 | 0.7487 | 0.6479 | 0.5806    |
| weekend_breakfast  | 2,611 | 0.4903 | 0.4886 | 0.8960 | 0.6321 | 0.5765    |
| weekend_dinner     | 4,388 | 0.4930 | 0.4442 | 0.7140 | 0.6702 | 0.5588    |
| weekend_late_night | 2,405 | 0.4980 | 0.4706 | 0.8102 | 0.6595 | 0.5575    |
| weekend_lunch      | 4,143 | 0.4863 | 0.4395 | 0.7751 | 0.6593 | 0.5632    |


## Statistical Significance (V2 vs Prompt 4)

Wilcoxon signed-rank test (two-sided, non-parametric paired test) on 28,326 common (consumer, daypart) pairs. Holm-Bonferroni corrected for 12 metrics.


| Metric          | V2         | P4         | Diff        | Cohen's d   | Effect         | Adj. p       | Sig?    |
| --------------- | ---------- | ---------- | ----------- | ----------- | -------------- | ------------ | ------- |
| MMS             | 0.4907     | 0.4997     | -0.0090     | -0.1140     | negligible     | 2.81e-97     | Yes     |
| SR@3            | 0.3628     | 0.3711     | -0.0083     | -0.0337     | negligible     | 1.91e-06     | Yes     |
| SR@5            | 0.4522     | 0.4630     | -0.0108     | -0.0437     | negligible     | 5.16e-10     | Yes     |
| SR@10           | 0.5561     | 0.5749     | -0.0189     | -0.0796     | negligible     | 1.69e-39     | Yes     |
| CCR             | 0.7697     | 0.7689     | +0.0007     | +0.0039     | negligible     | 0.5250       | No      |
| ILD             | 0.6513     | 0.6472     | +0.0041     | +0.0823     | negligible     | 1.39e-32     | Yes     |
| TCD             | 0.8913     | 0.8779     | +0.0134     | +0.0977     | negligible     | 5.45e-54     | Yes     |
| Redundancy Rate | 0.0066     | 0.0088     | -0.0022     | -0.1242     | negligible     | 4.27e-92     | Yes     |
| OHCD            | 0.4542     | 0.4574     | -0.0033     | -0.0211     | negligible     | 3.12e-04     | Yes     |
| TMC             | 0.1728     | 0.1663     | +0.0066     | +0.3339     | small          | 0.00e+00     | Yes     |
| FCS             | 0.8307     | 0.8326     | -0.0019     | -0.2607     | small          | 0.00e+00     | Yes     |
| **Composite**   | **0.5739** | **0.5781** | **-0.0041** | **-0.0569** | **negligible** | **1.37e-17** | **Yes** |


- **V2 significantly better**: ILD, TCD, Redundancy Rate, TMC
- **P4 significantly better**: MMS, SR@3, SR@5, SR@10, FCS, OHCD, Composite
- **No significant difference**: CCR
- **Important**: With the updated composite weights (TMC excluded), the composite gap has flipped — P4 now scores slightly higher than V2 (d=-0.06, negligible). The old composite included TMC (15% weight) where V2 had an edge, inflating V2's composite. With TMC removed, P4's advantages on relevance metrics (MMS, SR@K, OHCD) outweigh V2's diversity advantages (ILD, TCD). Individual metric differences remain negligible (|d| < 0.13) except for TMC and FCS which are format-related, not order-dependent.

## Order Distribution by Consumer (Common Consumers)


|                        | V2 (ending 3/21) | P4 (ending 4/16) |
| ---------------------- | ---------------- | ---------------- |
| Consumers with orders  | 6,534            | 6,534            |
| Total order rows       | 321,614          | 328,324          |
| Mean orders/consumer   | 49.2             | 50.2             |
| Median orders/consumer | 27.0             | 27.0             |
| Std                    | 151.7            | 166.7            |
| Min                    | 1                | 1                |
| Max                    | 8,114            | 8,433            |


### Percentiles


| Percentile | V2  | P4  |
| ---------- | --- | --- |
| P10        | 5   | 4   |
| P25        | 11  | 11  |
| P50        | 27  | 27  |
| P75        | 57  | 59  |
| P90        | 102 | 105 |
| P95        | 143 | 143 |
| P99        | 274 | 284 |


### Order Count Buckets


| Bucket  | V2 Consumers | %     | P4 Consumers | %     |
| ------- | ------------ | ----- | ------------ | ----- |
| 1-5     | 765          | 11.7% | 815          | 12.5% |
| 6-10    | 752          | 11.5% | 724          | 11.1% |
| 11-20   | 1,169        | 17.9% | 1,183        | 18.1% |
| 21-50   | 1,936        | 29.6% | 1,882        | 28.8% |
| 51-100  | 1,234        | 18.9% | 1,225        | 18.7% |
| 101-200 | 538          | 8.2%  | 557          | 8.5%  |
| 201+    | 140          | 2.1%  | 148          | 2.3%  |


### Orders by Daypart


| Daypart            | V2 Rows | %     | P4 Rows | %     |
| ------------------ | ------- | ----- | ------- | ----- |
| weekday_breakfast  | 32,069  | 10.0% | 32,004  | 9.7%  |
| weekday_dinner     | 82,415  | 25.6% | 84,176  | 25.6% |
| weekday_late_night | 28,750  | 8.9%  | 30,815  | 9.4%  |
| weekday_lunch      | 73,408  | 22.8% | 74,293  | 22.6% |
| weekend_breakfast  | 18,012  | 5.6%  | 18,564  | 5.7%  |
| weekend_dinner     | 36,761  | 11.4% | 36,796  | 11.2% |
| weekend_late_night | 12,808  | 4.0%  | 13,666  | 4.2%  |
| weekend_lunch      | 37,391  | 11.6% | 38,010  | 11.6% |


Order distributions are well-matched across the two windows. P4 has ~2% more order rows due to the later evaluation date, but bucket distributions and daypart splits are nearly identical.

## Notes

- Only consumers present in all three versions (V2, Prompt 4, Prompt 1) are included.
- TMC is excluded from the composite score (low signal due to missing `food_type` tags).
- TCD and Redundancy Rate are diagnostic metrics not included in the composite score.
- Order history windows differ: V2 uses 2025-12-22 to 2026-03-21; P4/P1 use 2026-01-17 to 2026-04-16.
- With the updated composite weights (TMC excluded), P4/P1 now score slightly higher than V2 on composite. The old weights gave V2 a composite advantage because TMC (15% weight) favored V2; removing TMC and redistributing weight to relevance metrics (MMS, SR@5, OHCD) tips the composite in P4's favor.
