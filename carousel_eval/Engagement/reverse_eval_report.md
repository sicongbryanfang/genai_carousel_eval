# Reverse Eval — Metric Tiers vs Engagement Groups

## TL;DR

**Methodology:** Pool 3,825 consumers from two labeled engagement groups — 1,937 high-converters (clicked and converted on GenAI carousels) and 1,888 zero-converters (≥1 impression, zero conversions). For each carousel quality metric (MMS, SR@5, SR@10), compute each consumer's mean score across dayparts, then split into top and bottom quartiles. Check whether the top-metric quartile skews toward high-converters and the bottom-metric quartile skews toward zero-converters. A random metric would produce ~50/50 in every tier; deviation signals predictive power.

**Results:**
- **SR@5 and SR@10 predict engagement** — the top-SR quartile is 52–53% high-converters vs 43% in the bottom quartile, a ~10pp gap that is highly significant (χ² p < 0.0001). Users whose carousels cover more of their actual order history (above θ=0.45) are meaningfully more likely to be converters.
- **MMS does not discriminate** — top and bottom MMS quartiles are nearly identical (~48% vs 46% high-converters, p=0.44). Mean max similarity alone is not a reliable predictor of conversion.
- **Implication:** SR@K should carry more weight than MMS in the composite score if the goal is to optimize for engagement. The current composite (MMS 20%, SR@5 20%) treats them equally despite SR being the stronger signal.

---

Pool all consumers from both engagement groups, rank by carousel quality metric,
cut into top/bottom quartiles, and check what fraction of each tier is from the
high-engagement (top) vs zero-engagement (bottom) group.

## Consumer Pool

| Group           | Consumers | Base % |
| --------------- | --------- | ------ |
| top-engagement  |      1937 |  50.6% |
| zero-engagement |      1888 |  49.4% |
| **total**       |      3825 |        |

A random split would give these base rates in every tier.
Deviation from base % indicates the metric predicts engagement.

## MMS — Quartile Tiers

- p25 threshold: 0.4358
- p75 threshold: 0.4789

| Metric Tier       | top-engagement | %     | zero-engagement | %     | total |
| ----------------- | -------------- | ----- | --------------- | ----- | ----- |
| Top Q (≥ p75)     |            459 |  48.0% |             498 |  52.0% |   957 |
| Bottom Q (≤ p25)  |            441 |  46.1% |             516 |  53.9% |   957 |

Chi-square test of independence: χ²=0.606, p=0.4363, dof=1
→ Distribution is **not statistically significant** (p ≥ 0.05)

### Median Split (median = 0.4571)

| Half              | top-engagement | %     | zero-engagement | %     | total |
| ----------------- | -------------- | ----- | --------------- | ----- | ----- |
| Above median      |           1010 |  52.8% |             903 |  47.2% |  1913 |
| Below median      |            927 |  48.5% |             985 |  51.5% |  1912 |


## SR@5 — Quartile Tiers

- p25 threshold: 0.3694
- p75 threshold: 0.5074

| Metric Tier       | top-engagement | %     | zero-engagement | %     | total |
| ----------------- | -------------- | ----- | --------------- | ----- | ----- |
| Top Q (≥ p75)     |            502 |  52.5% |             455 |  47.5% |   957 |
| Bottom Q (≤ p25)  |            408 |  42.6% |             549 |  57.4% |   957 |

Chi-square test of independence: χ²=18.119, p=0.0000, dof=1
→ Distribution is **statistically significant** (p < 0.05)

### Median Split (median = 0.4370)

| Half              | top-engagement | %     | zero-engagement | %     | total |
| ----------------- | -------------- | ----- | --------------- | ----- | ----- |
| Above median      |           1030 |  53.8% |             883 |  46.2% |  1913 |
| Below median      |            907 |  47.4% |            1005 |  52.6% |  1912 |


## SR@10 — Quartile Tiers

- p25 threshold: 0.4528
- p75 threshold: 0.5923

| Metric Tier       | top-engagement | %     | zero-engagement | %     | total |
| ----------------- | -------------- | ----- | --------------- | ----- | ----- |
| Top Q (≥ p75)     |            504 |  52.7% |             453 |  47.3% |   957 |
| Bottom Q (≤ p25)  |            409 |  42.7% |             548 |  57.3% |   957 |

Chi-square test of independence: χ²=18.505, p=0.0000, dof=1
→ Distribution is **statistically significant** (p < 0.05)

### Median Split (median = 0.5251)

| Half              | top-engagement | %     | zero-engagement | %     | total |
| ----------------- | -------------- | ----- | --------------- | ----- | ----- |
| Above median      |           1026 |  53.6% |             887 |  46.4% |  1913 |
| Below median      |            911 |  47.6% |            1001 |  52.4% |  1912 |


