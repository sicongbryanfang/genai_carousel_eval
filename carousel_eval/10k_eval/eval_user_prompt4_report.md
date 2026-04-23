# 10k Eval Carousel Evaluation Report

- **Order history**: 90-day lookback ending 2026-04-16 (495,551 rows)
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
| **Composite Quality Score**    | **0.5750** | **0.5767** | **0.5858**       | **+0.0018**     | **+0.0091**           |
| MMS (mean max similarity)      | 0.4962     | 0.5013     | 0.5260           | +0.0051         | +0.0247               |
| SR@3                           | 0.3716     | 0.3794     | 0.3816           | +0.0078         | +0.0022               |
| SR@5                           | 0.4623     | 0.4712     | 0.4840           | +0.0089         | +0.0128               |
| SR@10                          | 0.5679     | 0.5795     | 0.6108           | +0.0116         | +0.0313               |
| CCR (cuisine coverage recall)  | 0.7778     | 0.7757     | 0.7627           | -0.0021         | -0.0130               |
| ILD (intra-list diversity)     | 0.6550     | 0.6468     | 0.6606           | -0.0082         | +0.0138               |
| TCD (title cluster diversity)  | 0.8949     | 0.8781     | 0.8621           | -0.0168         | -0.0160               |
| Redundancy Rate                | 0.0066     | 0.0088     | 0.0132           | +0.0022         | +0.0044               |
| OHCD                           | 0.4353     | 0.4373     | 0.4442           | +0.0020         | +0.0069               |
| TMC (title-metadata coherence) | 0.1694     | 0.1665     | 0.1607           | -0.0029         | -0.0058               |
| FCS (format compliance)        | 0.8314     | 0.8326     | 0.8324           | +0.0012         | -0.0002               |
| Consumers evaluated            | 9,444      | 9,461      | 9,372            |                 |                       |
| (consumer, daypart) groups     | 43,331     | 43,403     | 42,963           |                 |                       |


## prompt4_no_think_no_rationale — Overall Metrics

Prompt4 variant with LLM thinking tokens disabled and no rationale in the output.

| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.5260     | 0.1168     | 42,963     |
| SR@3                                    | 0.3816     | 0.3014     | 42,963     |
| SR@5                                    | 0.4840     | 0.3021     | 42,963     |
| SR@10                                   | 0.6108     | 0.2827     | 42,963     |
| CCR (cuisine coverage recall)           | 0.7627     | 0.3181     | 41,385     |
| ILD (intra-list diversity)              | 0.6606     | 0.0546     | 42,963     |
| TCD (title cluster diversity)           | 0.8621     | 0.1322     | 42,963     |
| Redundancy Rate                         | 0.0132     | 0.0217     | 42,963     |
| OHCD (order history coverage diversity) | 0.4442     | 0.2664     | 42,963     |
| TMC (title-metadata coherence)          | 0.1607     | 0.0220     | 42,963     |
| FCS (format compliance)                 | 0.8324     | 0.0040     | 42,963     |
| **Composite Quality Score**             | **0.5858** | **0.0954** | **42,963** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,564 | 0.5356 | 0.5222 | 0.8765 | 0.6431 | 0.6043    |
| weekday_dinner     | 7,601 | 0.5188 | 0.4608 | 0.6816 | 0.6669 | 0.5877    |
| weekday_late_night | 4,830 | 0.5315 | 0.4945 | 0.7743 | 0.6679 | 0.5848    |
| weekday_lunch      | 7,036 | 0.5167 | 0.4670 | 0.7350 | 0.6520 | 0.5897    |
| weekend_breakfast  | 3,673 | 0.5447 | 0.5438 | 0.8925 | 0.6434 | 0.6030    |
| weekend_dinner     | 6,084 | 0.5236 | 0.4650 | 0.7065 | 0.6733 | 0.5700    |
| weekend_late_night | 3,446 | 0.5375 | 0.5061 | 0.7998 | 0.6711 | 0.5768    |
| weekend_lunch      | 5,729 | 0.5181 | 0.4653 | 0.7595 | 0.6619 | 0.5760    |


## user_prompt4 — Overall Metrics


| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.5013     | 0.1109     | 43,403     |
| SR@3                                    | 0.3794     | 0.2961     | 43,403     |
| SR@5                                    | 0.4712     | 0.2971     | 43,403     |
| SR@10                                   | 0.5795     | 0.2854     | 43,403     |
| CCR (cuisine coverage recall)           | 0.7757     | 0.3115     | 41,808     |
| ILD (intra-list diversity)              | 0.6468     | 0.0524     | 43,403     |
| TCD (title cluster diversity)           | 0.8781     | 0.1253     | 43,403     |
| Redundancy Rate                         | 0.0088     | 0.0163     | 43,403     |
| OHCD (order history coverage diversity) | 0.4373     | 0.2638     | 43,403     |
| TMC (title-metadata coherence)          | 0.1665     | 0.0205     | 43,403     |
| FCS (format compliance)                 | 0.8326     | 0.0035     | 43,403     |
| **Composite Quality Score**             | **0.5767** | **0.0945** | **43,403** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,606 | 0.4964 | 0.4786 | 0.8894 | 0.6157 | 0.5844    |
| weekday_dinner     | 7,675 | 0.5017 | 0.4566 | 0.6983 | 0.6537 | 0.5827    |
| weekday_late_night | 4,876 | 0.5095 | 0.4887 | 0.7859 | 0.6542 | 0.5779    |
| weekday_lunch      | 7,108 | 0.4945 | 0.4581 | 0.7523 | 0.6407 | 0.5825    |
| weekend_breakfast  | 3,710 | 0.5071 | 0.5064 | 0.8995 | 0.6269 | 0.5852    |
| weekend_dinner     | 6,149 | 0.5030 | 0.4606 | 0.7196 | 0.6619 | 0.5637    |
| weekend_late_night | 3,487 | 0.5125 | 0.5001 | 0.8092 | 0.6600 | 0.5687    |
| weekend_lunch      | 5,792 | 0.4937 | 0.4573 | 0.7698 | 0.6526 | 0.5679    |


## user_prompt1 — Overall Metrics


| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.4962     | 0.1109     | 43,331     |
| SR@3                                    | 0.3716     | 0.2955     | 43,331     |
| SR@5                                    | 0.4623     | 0.2972     | 43,331     |
| SR@10                                   | 0.5679     | 0.2884     | 43,331     |
| CCR (cuisine coverage recall)           | 0.7778     | 0.3098     | 41,739     |
| ILD (intra-list diversity)              | 0.6550     | 0.0513     | 43,331     |
| TCD (title cluster diversity)           | 0.8949     | 0.1125     | 43,331     |
| Redundancy Rate                         | 0.0066     | 0.0129     | 43,331     |
| OHCD (order history coverage diversity) | 0.4353     | 0.2626     | 43,331     |
| TMC (title-metadata coherence)          | 0.1694     | 0.0199     | 43,331     |
| FCS (format compliance)                 | 0.8314     | 0.0061     | 43,331     |
| **Composite Quality Score**             | **0.5750** | **0.0944** | **43,331** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,600 | 0.4913 | 0.4754 | 0.8920 | 0.6253 | 0.5840    |
| weekday_dinner     | 7,660 | 0.4980 | 0.4472 | 0.7009 | 0.6613 | 0.5810    |
| weekday_late_night | 4,867 | 0.5018 | 0.4800 | 0.7851 | 0.6572 | 0.5744    |
| weekday_lunch      | 7,097 | 0.4908 | 0.4476 | 0.7555 | 0.6509 | 0.5812    |
| weekend_breakfast  | 3,705 | 0.4998 | 0.4984 | 0.8991 | 0.6373 | 0.5828    |
| weekend_dinner     | 6,134 | 0.4989 | 0.4518 | 0.7211 | 0.6721 | 0.5624    |
| weekend_late_night | 3,483 | 0.5041 | 0.4875 | 0.8118 | 0.6630 | 0.5652    |
| weekend_lunch      | 5,785 | 0.4899 | 0.4482 | 0.7737 | 0.6620 | 0.5668    |


## Statistical Significance: prompt4 vs no_think

We compared 42,949 matched (consumer, daypart) pairs using a Wilcoxon signed-rank test to determine whether the differences between prompt4 and no_think are real or just noise.

**How to read the table:**
- **Mean Diff**: negative means no_think scores higher; positive means prompt4 scores higher.
- **Cohen's d**: measures how big the difference actually is in practice (not just whether it's real). Think of it as "how many standard deviations apart are the two variants." A d of 0.12 means the gap is just 12% of one standard deviation — the variation across different consumers within the same variant is far larger than the difference between variants.
  - |d| < 0.2 = **negligible** — difference exists but too small to matter in practice
  - 0.2–0.5 = **small** — noticeable if you look for it, but minor
  - 0.5–0.8 = **medium** — clearly meaningful
  - \> 0.8 = **large** — obvious difference
- **Adj. p**: probability the difference is due to random chance (after correcting for testing 12 metrics at once). Values < 0.05 mean the difference is real, not random.

| Metric | Mean prompt4 | Mean no_think | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MMS | 0.5013 | 0.5259 | -0.0246 | -0.31 | small | <0.001 | Yes |
| SR@3 | 0.3797 | 0.3815 | -0.0018 | -0.01 | negligible | 0.5454 | No |
| SR@5 | 0.4714 | 0.4840 | -0.0126 | -0.05 | negligible | <0.001 | Yes |
| SR@10 | 0.5797 | 0.6108 | -0.0312 | -0.14 | negligible | <0.001 | Yes |
| CCR | 0.7758 | 0.7627 | +0.0131 | +0.12 | negligible | <0.001 | Yes |
| ILD | 0.6468 | 0.6606 | -0.0138 | -0.27 | small | <0.001 | Yes |
| TCD | 0.8780 | 0.8621 | +0.0159 | +0.11 | negligible | <0.001 | Yes |
| Redundancy Rate | 0.0088 | 0.0132 | -0.0044 | -0.20 | negligible | <0.001 | Yes |
| OHCD | 0.4373 | 0.4442 | -0.0069 | -0.08 | negligible | <0.001 | Yes |
| TMC | 0.1665 | 0.1607 | +0.0058 | +0.27 | small | <0.001 | Yes |
| FCS | 0.8326 | 0.8324 | +0.0002 | +0.05 | negligible | <0.001 | Yes |
| **Composite** | **0.5768** | **0.5858** | **-0.0090** | **-0.14** | **negligible** | **<0.001** | **Yes** |

### What this means

Almost all differences are **statistically real** (p < 0.001) — but with 43k data points, even tiny differences show up as "significant." The more important question is: **are the differences big enough to matter?**

**The answer is: not really.** Every metric has a small or negligible effect size (|d| < 0.5). The largest effect is MMS at d=-0.31 (small) — even that would be hard to notice in practice.

**no_think edges ahead on relevance:** MMS (small effect), ILD (small effect), SR@10, SR@5, OHCD, and the Composite — but all with negligible-to-small effect sizes.

**prompt4 edges ahead on structure:** TMC (small effect), TCD, CCR, Redundancy Rate, FCS — again all negligible-to-small.

**No difference at all:** SR@3 (p=0.55, not even statistically significant).

**In plain terms:** If you picked a random consumer and looked at their carousels from both variants side by side, you'd have a very hard time telling which one came from which prompt. The two variants perform essentially the same.


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

**The two variants produce nearly identical quality carousels.** The composite score differs by just 0.009 — for context, the spread across consumers within a single variant is ~0.095, so the between-variant gap is about 10x smaller than normal consumer-to-consumer variation. You would not be able to tell the carousels apart by looking at them.

**No_think scores slightly higher on relevance metrics** (MMS, SR@K, OHCD), but this is largely explained by the brand-name repetition pattern: it defaults to specific item names like "Chicken McNuggets" and "Big Mac meals" 3-13x more often than prompt4. These titles match order history item names almost exactly in embedding space, boosting similarity scores. Prompt4 uses more generic titles like "Chicken nuggets" that mean the same thing but score slightly lower. This is a measurement artifact, not a genuine recommendation quality difference.

**Prompt4 scores slightly higher on structure and diversity** (CCR, TCD, Redundancy Rate). With thinking tokens, the model produces better-organized carousels with broader cuisine coverage and fewer near-duplicate titles. These effects are also small.

**Prompt4 is more reliable.** It generates exactly 10 carousels per daypart group every time. No_think fails to produce complete output in some cases — 722 missing daypart groups, 7,607 missing carousels, and 25 completely empty groups.

**Bottom line:** The quality difference between the two variants is negligible. Prompt4 is the safer choice because it produces complete, well-structured output every time, and its slightly lower relevance scores are likely an artifact of using generic food names instead of repeating brand-specific item names.


## Notes

- TMC is excluded from the composite score because the carousel format lacks `food_type` tags; title-metadata coherence cannot be properly computed (~0.17 across all variants).
- CCR uses `cuisine_filter` from carousels mapped to the taxonomy, and `cuisine_tags_from_menu` from Snowflake order history.
- TCD and Redundancy Rate are diagnostic metrics not included in the composite score.
