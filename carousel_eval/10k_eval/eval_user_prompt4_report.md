# 10k Eval Carousel Evaluation Report

- **Order history**: 90-day lookback ending 2026-04-16 (495,551 rows)
- **Embedding mode**: title_metadata (all-MiniLM-L6-v2)

## Variant Glossary

The five compared variants:

- **`prompt_v1`** — Baseline prompt (version 1). Default thinking-token budget; rationale field present in output.
- **`prompt_v4`** — Prompt version 4. Default thinking-token budget; rationale field present in output.
- **`prompt_v4_thinking_1024`** — `prompt_v4` with thinking-token budget capped at 1024; rationale field still produced.
- **`prompt_v4_no_rationale_thinking_1024`** — `prompt_v4` with thinking-token budget capped at 1024 and the rationale field removed from output.
- **`prompt_v4_no_thinking_no_rationale`** — `prompt_v4` with thinking tokens disabled and the rationale field removed from output.
- **`genai_v2_thinking_1024`** — GenAI v2 model (v319 batch) with thinking-token budget capped at 1024.

## Composite Score Formula

TCD and Redundancy Rate are diagnostic only.

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

Five variants are compared. The two `_thinking_1024` variants are runs of the `prompt_v4` family with the LLM's thinking budget capped at 1024 tokens.

| Metric                         | prompt_v1  | prompt_v4  | prompt_v4_no_thinking_no_rationale | prompt_v4_thinking_1024 | prompt_v4_no_rationale_thinking_1024 | genai_v2_thinking_1024 |
| ------------------------------ | ---------- | ---------- | ---------------------------------- | ----------------------- | ------------------------------------ | ---------------------- |
| **Composite Quality Score**    | **0.5750** | **0.5767** | **0.5858**                         | **0.5804**              | **0.5816**                           | **0.5804**             |
| MMS (mean max similarity)      | 0.4962     | 0.5013     | 0.5260                             | 0.5138                  | 0.5165                               | 0.5122                 |
| SR@3                           | 0.3716     | 0.3794     | 0.3816                             | 0.3782                  | 0.3791                               | 0.3743                 |
| SR@5                           | 0.4623     | 0.4712     | 0.4840                             | 0.4762                  | 0.4794                               | 0.4734                 |
| SR@10                          | 0.5679     | 0.5795     | 0.6108                             | 0.5935                  | 0.6007                               | 0.5911                 |
| CCR (cuisine coverage recall)  | 0.7778     | 0.7757     | 0.7627                             | 0.7683                  | 0.7660                               | 0.7698                 |
| ILD (intra-list diversity)     | 0.6550     | 0.6468     | 0.6606                             | 0.6516                  | 0.6512                               | 0.6530                 |
| TCD (title cluster diversity)  | 0.8949     | 0.8781     | 0.8621                             | 0.8616                  | 0.8545                               | 0.8715                 |
| Redundancy Rate                | 0.0066     | 0.0088     | 0.0132                             | 0.0125                  | 0.0135                               | 0.0102                 |
| OHCD                           | 0.4353     | 0.4373     | 0.4442                             | 0.4400                  | 0.4417                               | 0.4423                 |
| FCS (format compliance)        | 0.8314     | 0.8326     | 0.8324                             | 0.8325                  | 0.8326                               | 0.8316                 |
| Consumers evaluated            | 9,444      | 9,461      | 9,372                              | 9,407                   | 9,312                                | 9,179                  |
| (consumer, daypart) groups     | 43,331     | 43,403     | 42,963                             | 43,145                  | 42,728                               | 42,280                 |

### Effect of capping the thinking budget at 1024 tokens (vs `prompt_v4` default)

| Metric    | prompt_v4  | prompt_v4_thinking_1024 | delta (thinking_1024 - v4) |
| --------- | ---------- | ----------------------- | -------------------------- |
| Composite | **0.5767** | **0.5804**              | **+0.0037**                |
| MMS       | 0.5013     | 0.5138                  | +0.0125                    |
| SR@5      | 0.4712     | 0.4762                  | +0.0050                    |
| SR@10     | 0.5795     | 0.5935                  | +0.0140                    |
| CCR       | 0.7757     | 0.7683                  | -0.0074                    |
| ILD       | 0.6468     | 0.6516                  | +0.0048                    |
| TCD       | 0.8781     | 0.8616                  | -0.0165                    |
| OHCD      | 0.4373     | 0.4400                  | +0.0027                    |

### Effect of adding thinking back at 1024 (`prompt_v4_no_thinking_no_rationale` vs `prompt_v4_no_rationale_thinking_1024`)

| Metric    | prompt_v4_no_thinking_no_rationale | prompt_v4_no_rationale_thinking_1024 | delta       |
| --------- | ---------------------------------- | ------------------------------------ | ----------- |
| Composite | **0.5858**                         | **0.5816**                           | **-0.0042** |
| MMS       | 0.5260                             | 0.5165                               | -0.0095     |
| SR@5      | 0.4840                             | 0.4794                               | -0.0046     |
| SR@10     | 0.6108                             | 0.6007                               | -0.0101     |
| CCR       | 0.7627                             | 0.7660                               | +0.0033     |
| ILD       | 0.6606                             | 0.6512                               | -0.0094     |
| TCD       | 0.8621                             | 0.8545                               | -0.0076     |
| OHCD      | 0.4442                             | 0.4417                               | -0.0025     |


## `prompt_v4_thinking_1024` — Overall Metrics

`prompt_v4` with the LLM thinking budget capped at 1024 tokens (rationale field still produced).

| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.5138     | 0.1138     | 43,145     |
| SR@3                                    | 0.3782     | 0.2988     | 43,145     |
| SR@5                                    | 0.4762     | 0.2996     | 43,145     |
| SR@10                                   | 0.5935     | 0.2839     | 43,145     |
| CCR (cuisine coverage recall)           | 0.7683     | 0.3154     | 41,561     |
| ILD (intra-list diversity)              | 0.6516     | 0.0533     | 43,145     |
| TCD (title cluster diversity)           | 0.8616     | 0.1312     | 43,145     |
| Redundancy Rate                         | 0.0125     | 0.0203     | 43,145     |
| OHCD (order history coverage diversity) | 0.4400     | 0.2647     | 43,145     |
| FCS (format compliance)                 | 0.8325     | 0.0038     | 43,145     |
| **Composite Quality Score**             | **0.5804** | **0.0941** | **43,145** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,581 | 0.5069 | 0.4822 | 0.8829 | 0.6279 | 0.5873    |
| weekday_dinner     | 7,627 | 0.5114 | 0.4583 | 0.6868 | 0.6606 | 0.5848    |
| weekday_late_night | 4,853 | 0.5237 | 0.4943 | 0.7791 | 0.6605 | 0.5826    |
| weekday_lunch      | 7,064 | 0.5054 | 0.4620 | 0.7431 | 0.6430 | 0.5856    |
| weekend_breakfast  | 3,689 | 0.5236 | 0.5177 | 0.8962 | 0.6313 | 0.5914    |
| weekend_dinner     | 6,110 | 0.5144 | 0.4648 | 0.7109 | 0.6657 | 0.5667    |
| weekend_late_night | 3,467 | 0.5298 | 0.5120 | 0.8051 | 0.6637 | 0.5753    |
| weekend_lunch      | 5,754 | 0.5078 | 0.4614 | 0.7654 | 0.6526 | 0.5717    |


## `prompt_v4_no_rationale_thinking_1024` — Overall Metrics

`prompt_v4` with no rationale field in the output and the LLM thinking budget capped at 1024 tokens.

| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.5165     | 0.1142     | 42,728     |
| SR@3                                    | 0.3791     | 0.2996     | 42,728     |
| SR@5                                    | 0.4794     | 0.3001     | 42,728     |
| SR@10                                   | 0.6007     | 0.2835     | 42,728     |
| CCR (cuisine coverage recall)           | 0.7660     | 0.3164     | 41,166     |
| ILD (intra-list diversity)              | 0.6512     | 0.0554     | 42,728     |
| TCD (title cluster diversity)           | 0.8545     | 0.1361     | 42,728     |
| Redundancy Rate                         | 0.0135     | 0.0217     | 42,728     |
| OHCD (order history coverage diversity) | 0.4417     | 0.2654     | 42,728     |
| FCS (format compliance)                 | 0.8326     | 0.0037     | 42,728     |
| **Composite Quality Score**             | **0.5816** | **0.0944** | **42,728** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,536 | 0.5113 | 0.4896 | 0.8810 | 0.6262 | 0.5899    |
| weekday_dinner     | 7,553 | 0.5138 | 0.4605 | 0.6842 | 0.6590 | 0.5856    |
| weekday_late_night | 4,806 | 0.5253 | 0.4949 | 0.7777 | 0.6604 | 0.5825    |
| weekday_lunch      | 6,999 | 0.5076 | 0.4617 | 0.7398 | 0.6421 | 0.5854    |
| weekend_breakfast  | 3,649 | 0.5274 | 0.5251 | 0.8957 | 0.6315 | 0.5941    |
| weekend_dinner     | 6,052 | 0.5175 | 0.4691 | 0.7092 | 0.6662 | 0.5686    |
| weekend_late_night | 3,431 | 0.5323 | 0.5105 | 0.8011 | 0.6647 | 0.5754    |
| weekend_lunch      | 5,702 | 0.5100 | 0.4683 | 0.7632 | 0.6526 | 0.5735    |


## `prompt_v4_no_thinking_no_rationale` — Overall Metrics

`prompt_v4` variant with LLM thinking tokens disabled and no rationale in the output.

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


## `prompt_v4` — Overall Metrics


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


## `prompt_v1` — Overall Metrics


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


## `genai_v2_thinking_1024` — Overall Metrics

GenAI v2 model (v319 batch) with the LLM thinking budget capped at 1024 tokens.

| Metric                                  | Mean       | Std        | n          |
| --------------------------------------- | ---------- | ---------- | ---------- |
| MMS (mean max similarity)               | 0.5122     | 0.1143     | 42,279     |
| SR@3                                    | 0.3743     | 0.2987     | 42,279     |
| SR@5                                    | 0.4734     | 0.2998     | 42,279     |
| SR@10                                   | 0.5911     | 0.2859     | 42,279     |
| CCR (cuisine coverage recall)           | 0.7698     | 0.3142     | 40,740     |
| ILD (intra-list diversity)              | 0.6530     | 0.0547     | 42,279     |
| TCD (title cluster diversity)           | 0.8715     | 0.1268     | 42,279     |
| Redundancy Rate                         | 0.0102     | 0.0174     | 42,279     |
| OHCD (order history coverage diversity) | 0.4423     | 0.2669     | 42,279     |
| FCS (format compliance)                 | 0.8316     | 0.0057     | 42,280     |
| **Composite Quality Score**             | **0.5804** | **0.0955** | **42,280** |


### Breakdown by Daypart


| Daypart            | Count | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ----- | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 4,499 | 0.5101 | 0.4952 | 0.8863 | 0.6272 | 0.5927    |
| weekday_dinner     | 7,465 | 0.5096 | 0.4509 | 0.6883 | 0.6615 | 0.5837    |
| weekday_late_night | 4,761 | 0.5206 | 0.4927 | 0.7797 | 0.6565 | 0.5813    |
| weekday_lunch      | 6,906 | 0.5034 | 0.4556 | 0.7478 | 0.6460 | 0.5852    |
| weekend_breakfast  | 3,636 | 0.5219 | 0.5203 | 0.8930 | 0.6295 | 0.5913    |
| weekend_dinner     | 5,984 | 0.5139 | 0.4602 | 0.7115 | 0.6717 | 0.5668    |
| weekend_late_night | 3,390 | 0.5264 | 0.5019 | 0.8059 | 0.6626 | 0.5728    |
| weekend_lunch      | 5,639 | 0.5045 | 0.4581 | 0.7659 | 0.6574 | 0.5714    |


## Statistical Significance: `prompt_v4` vs `prompt_v4_no_thinking_no_rationale`

We compared 42,949 matched (consumer, daypart) pairs using a Wilcoxon signed-rank test to determine whether the differences between `prompt_v4` and `prompt_v4_no_thinking_no_rationale` are real or just noise.

**How to read the table:**
- **Mean Diff**: negative means `prompt_v4_no_thinking_no_rationale` scores higher; positive means `prompt_v4` scores higher.
- **Cohen's d**: measures how big the difference actually is in practice (not just whether it's real). Think of it as "how many standard deviations apart are the two variants." A d of 0.12 means the gap is just 12% of one standard deviation — the variation across different consumers within the same variant is far larger than the difference between variants.
  - |d| < 0.2 = **negligible** — difference exists but too small to matter in practice
  - 0.2–0.5 = **small** — noticeable if you look for it, but minor
  - 0.5–0.8 = **medium** — clearly meaningful
  - \> 0.8 = **large** — obvious difference
- **Adj. p**: probability the difference is due to random chance (after correcting for testing 12 metrics at once). Values < 0.05 mean the difference is real, not random.

| Metric | Mean prompt_v4 | Mean prompt_v4_no_thinking_no_rationale | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
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
| FCS | 0.8326 | 0.8324 | +0.0002 | +0.05 | negligible | <0.001 | Yes |
| **Composite** | **0.5768** | **0.5858** | **-0.0090** | **-0.14** | **negligible** | **<0.001** | **Yes** |

### What this means

Almost all differences are **statistically real** (p < 0.001) — but with 43k data points, even tiny differences show up as "significant." The more important question is: **are the differences big enough to matter?**

**The answer is: not really.** Every metric has a small or negligible effect size (|d| < 0.5). The largest effect is MMS at d=-0.31 (small) — even that would be hard to notice in practice.

**`prompt_v4_no_thinking_no_rationale` edges ahead on relevance:** MMS (small effect), ILD (small effect), SR@10, SR@5, OHCD, and the Composite — but all with negligible-to-small effect sizes.

**`prompt_v4` edges ahead on structure:** TCD, CCR, Redundancy Rate, FCS — again all negligible-to-small.

**No difference at all:** SR@3 (p=0.55, not even statistically significant).

**In plain terms:** If you picked a random consumer and looked at their carousels from both variants side by side, you'd have a very hard time telling which one came from which prompt. The two variants perform essentially the same.


## Data Volume Comparison (`prompt_v4` vs `prompt_v4_no_thinking_no_rationale`)


| Metric                   | prompt_v4 | prompt_v4_no_thinking_no_rationale | delta    |
| ------------------------ | --------- | ---------------------------------- | -------- |
| Consumers                | 10,170    | 10,170                             | 0        |
| Total daypart groups     | 81,336    | 80,614                             | -722     |
| Empty groups             | 0         | 25                                 | +25      |
| Total carousels          | 813,360   | 805,753                            | -7,607   |
| Distinct carousel titles | 39,718    | 64,083                             | +24,365  |
| Avg carousels/consumer   | 80.0      | 79.2                               | -0.8     |
| Brand-specific titles    | 0.66%     | 2.18%                              | +1.52pp  |

- Same 10,170 consumers in both files.
- `prompt_v4_no_thinking_no_rationale` is missing 722 daypart groups and 7,607 carousels — the model occasionally fails to produce complete output without thinking tokens (25 fully empty groups, plus some partial groups).
- Despite fewer total carousels, `prompt_v4_no_thinking_no_rationale` produces 61% more distinct titles (64,083 vs 39,718). Without thinking, the model generates more varied, specific item-level names (e.g. "Chicken McNuggets Happy Meals", "Sausage egg mcgriddles") rather than reusing generic category titles across consumers.
- `prompt_v4_no_thinking_no_rationale` has 3.3x more brand-specific titles (2.18% vs 0.66%), producing names that match order history items more closely via embedding similarity. This likely explains the higher MMS/SR@K scores despite no thinking tokens. The 1024-token variants sit in between (1.51%).


## Brand-Name Title Analysis

The same brand keyword set was applied to all four `prompt_v4`-family variants. The two `_thinking_1024` variants sit roughly halfway between `prompt_v4` (default thinking) and `prompt_v4_no_thinking_no_rationale` — confirming that brand repetition scales monotonically with how much the model is allowed to skip deliberation.

### Brand share

| Variant                                | Total titles | Brand-title rows | Brand share | Distinct brand titles |
| -------------------------------------- | -----------: | ---------------: | ----------: | --------------------: |
| prompt_v4                              |      813,360 |            5,367 |       0.66% |                   279 |
| genai_v2_thinking_1024                 |      784,317 |            8,406 |       1.07% |                   319 |
| prompt_v4_thinking_1024                |      808,609 |           12,235 |       1.51% |                   433 |
| prompt_v4_no_rationale_thinking_1024   |      800,344 |           12,111 |       1.51% |                   417 |
| prompt_v4_no_thinking_no_rationale     |      805,748 |           17,531 |       2.18% |                   564 |

### Brand keyword frequency

| Brand keyword | prompt_v4 | genai_v2_thinking_1024 | prompt_v4_thinking_1024 | prompt_v4_no_rationale_thinking_1024 | prompt_v4_no_thinking_no_rationale |
| ------------- | --------: | ---------------------: | ----------------------: | -----------------------------------: | ---------------------------------: |
| big mac       |     1,622 |                  2,650 |                   3,425 |                                3,389 |                              4,315 |
| mcnugget      |       837 |                  1,342 |                   2,425 |                                2,125 |                              3,526 |
| whopper       |       768 |                  1,203 |                   1,923 |                                1,849 |                              2,507 |
| mcgriddle     |       676 |                  1,188 |                   1,538 |                                1,574 |                              2,306 |
| mcmuffin      |       472 |                    947 |                   1,176 |                                1,204 |                              1,921 |
| chipotle      |       838 |                    377 |                     867 |                                  931 |                              1,135 |
| happy meal    |        79 |                    582 |                     501 |                                  672 |                              1,039 |
| mcchicken     |        49 |                    108 |                     248 |                                  254 |                                509 |
| chick-fil-a   |        12 |                     31 |                      62 |                                   26 |                                177 |
| kfc           |        15 |                     20 |                      96 |                                  100 |                                163 |

### Top brand-name title clusters

| Title cluster                 | prompt_v4 | genai_v2_thinking_1024 | prompt_v4_thinking_1024 | prompt_v4_no_rationale_thinking_1024 | prompt_v4_no_thinking_no_rationale |
| ----------------------------- | --------: | ---------------------: | ----------------------: | -----------------------------------: | ---------------------------------: |
| Chicken mcnuggets / McNuggets |       828 |                  1,322 |                   2,318 |                                2,065 |                              3,329 |
| Big mac burgers               |       778 |                    323 |                   1,120 |                                1,179 |                              1,352 |
| Big mac meals                 |       315 |                    669 |                   1,277 |                                1,293 |                              1,767 |
| Whopper burgers / meals       |       574 |                    737 |                   1,457 |                                1,424 |                              1,786 |
| Happy meal variants           |        79 |                    582 |                     501 |                                  672 |                              1,039 |
| Sausage egg mcgriddles        |       275 |                    120 |                     551 |                                  547 |                                715 |
| Sausage egg mcmuffins         |       156 |                     73 |                     329 |                                  356 |                                456 |

Cutting the thinking budget from default (~8192) to 1024 roughly **doubles** the brand-share for `prompt_v4` (0.66% → 1.51%), and removing thinking entirely roughly **triples** it (→ 2.18%). `prompt_v4_no_rationale_thinking_1024` is essentially indistinguishable from `prompt_v4_thinking_1024` on brand share — the rationale field's presence/absence has little effect once the budget is fixed, suggesting the brand-repetition effect is driven by reasoning depth, not output format.

`genai_v2_thinking_1024` sits between `prompt_v4` and the `prompt_v4_thinking_1024` variants at **1.07%**, despite also using a 1024-token thinking budget. The v2 model appears to resist brand-name repetition better than the v4 prompt at the same budget — its per-keyword counts are consistently 40–60% lower than `prompt_v4_thinking_1024` across most keywords, and notably lower on "chipotle" (377 vs 867). The same MMS/SR@K inflation noted for `prompt_v4_no_thinking_no_rationale` applies in muted form to the 1024-token variants, and `genai_v2_thinking_1024` is the least affected.


## Summary

**The two variants produce nearly identical quality carousels.** The composite score differs by just 0.009 — for context, the spread across consumers within a single variant is ~0.095, so the between-variant gap is about 10x smaller than normal consumer-to-consumer variation. You would not be able to tell the carousels apart by looking at them.

**`prompt_v4_no_thinking_no_rationale` scores slightly higher on relevance metrics** (MMS, SR@K, OHCD), but this is largely explained by the brand-name repetition pattern: it defaults to specific item names like "Chicken McNuggets" and "Big Mac meals" 3-13x more often than `prompt_v4`. These titles match order history item names almost exactly in embedding space, boosting similarity scores. `prompt_v4` uses more generic titles like "Chicken nuggets" that mean the same thing but score slightly lower. This is a measurement artifact, not a genuine recommendation quality difference.

**`prompt_v4` scores slightly higher on structure and diversity** (CCR, TCD, Redundancy Rate). With thinking tokens, the model produces better-organized carousels with broader cuisine coverage and fewer near-duplicate titles. These effects are also small.

**`prompt_v4` is more reliable.** It generates exactly 10 carousels per daypart group every time. `prompt_v4_no_thinking_no_rationale` fails to produce complete output in some cases — 722 missing daypart groups, 7,607 missing carousels, and 25 completely empty groups.

**Bottom line:** The quality difference between the two variants is negligible. `prompt_v4` is the safer choice because it produces complete, well-structured output every time, and its slightly lower relevance scores are likely an artifact of using generic food names instead of repeating brand-specific item names.


## Notes

- CCR uses `cuisine_filter` from carousels mapped to the taxonomy, and `cuisine_tags_from_menu` from Snowflake order history.
- TCD and Redundancy Rate are diagnostic metrics not included in the composite score.
