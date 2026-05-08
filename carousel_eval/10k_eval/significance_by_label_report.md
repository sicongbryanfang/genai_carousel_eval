# Significance Report: no_rationale_think_1024 vs genai_v2_think_1024

- **Test**: Wilcoxon signed-rank (two-sided), Holm-Bonferroni correction, α=0.05
- **Effect size**: Cohen's d (paired). |d|<0.2=negligible, 0.2–0.5=small, 0.5–0.8=medium, >0.8=large
- **Positive mean diff** = no_rationale_think_1024 higher; **negative** = genai_v2_think_1024 higher
- **Label source**: `PRODDB.ANDYPARK.cx_carousel_v3_prompt_test_enriched`

## Metrics

| Metric | Full name | Description |
| --- | --- | --- |
| MMS | Mean Max Similarity | Mean of each order item's max cosine similarity to any carousel title. Higher = carousels better match order history. |
| SR@3/5/10 | Semantic Recall @K | Fraction of order items with max carousel similarity ≥ 0.45, evaluated against top-K carousels. Higher = better coverage. |
| CCR | Cuisine Coverage Recall | Fraction of cuisine families in order history covered by carousel cuisine tags. Higher = broader cuisine match. |
| ILD | Intra-List Diversity | Mean pairwise dissimilarity between carousel title embeddings. Higher = more diverse carousel set. |
| TCD | Title Cluster Diversity | Fraction of distinct topic clusters among carousel titles (sim threshold 0.65). Higher = less redundancy at topic level. |
| Redundancy Rate | Redundancy Rate | Fraction of title pairs with similarity ≥ 0.75 (near-duplicates). Lower = better. |
| OHCD | Order History Coverage Diversity | Fraction of carousel slots assigned at least one matching order item. Higher = better personalization coverage. |
| Composite | Composite Quality Score | Weighted average: MMS 20%, SR@5 20%, OHCD 20%, CCR 15%, ILD 15%, FCS 10% (weights renormalized if a metric is missing). |

> TMC and FCS are excluded from this report: both depend on `food_type` tags, which are absent in this carousel format.

## Overall

### All consumers  (n=41,621 pairs)

| Metric | Mean no_rationale_think_1024 | Mean genai_v2_think_1024 | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| MMS | 0.5165 | 0.5122 | +0.0043 | +0.0619 | negligible | 1.61e-30 | Yes |
| SR@3 | 0.3791 | 0.3745 | +0.0047 | +0.0211 | negligible | 1.54e-05 | Yes |
| SR@5 | 0.4795 | 0.4734 | +0.0060 | +0.0277 | negligible | 9.84e-07 | Yes |
| SR@10 | 0.6009 | 0.5911 | +0.0098 | +0.0457 | negligible | 1.96e-14 | Yes |
| CCR | 0.7661 | 0.7701 | -0.0040 | -0.0357 | negligible | 7.77e-11 | Yes |
| ILD | 0.6511 | 0.6529 | -0.0018 | -0.0347 | negligible | 1.03e-11 | Yes |
| TCD | 0.8542 | 0.8715 | -0.0173 | -0.1209 | negligible | 6.21e-121 | Yes |
| Redundancy Rate | 0.0135 | 0.0102 | +0.0034 | +0.1503 | negligible | 4.51e-196 | Yes |
| OHCD | 0.4426 | 0.4424 | +0.0002 | +0.0017 | negligible | 0.6132 | No |
| **Composite** | 0.5818 | 0.5804 | +0.0014 | +0.0235 | negligible | 5.28e-04 | **Yes** |

**no_rationale_think_1024 better:** MMS (d=+0.062), SR@3 (d=+0.021), SR@5 (d=+0.028), SR@10 (d=+0.046), Composite (d=+0.023)
**genai_v2_think_1024 better:** CCR (d=-0.036), ILD (d=-0.035), TCD (d=-0.121), Redundancy Rate (d=+0.150)
**No significant difference:** OHCD

## Breakdown by IS_SPARSE_ORDER

### IS_SPARSE_ORDER = True  (991 consumers)  (n=1,262 pairs)

| Metric | Mean no_rationale_think_1024 | Mean genai_v2_think_1024 | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| MMS | 0.5523 | 0.5357 | +0.0166 | +0.1848 | negligible | 8.45e-10 | Yes |
| SR@3 | 0.5123 | 0.4713 | +0.0410 | +0.1396 | negligible | 5.63e-06 | Yes |
| SR@5 | 0.5960 | 0.5624 | +0.0336 | +0.1109 | negligible | 2.54e-04 | Yes |
| SR@10 | 0.6932 | 0.6453 | +0.0479 | +0.1655 | negligible | 6.37e-08 | Yes |
| CCR | 0.7705 | 0.7670 | +0.0035 | +0.0357 | negligible | 0.2209 | No |
| ILD | 0.6351 | 0.6493 | -0.0142 | -0.2602 | small | 4.02e-18 | Yes |
| TCD | 0.8240 | 0.8742 | -0.0502 | -0.3173 | small | 3.55e-25 | Yes |
| Redundancy Rate | 0.0164 | 0.0084 | +0.0080 | +0.3284 | small | 4.37e-29 | Yes |
| OHCD | 0.2084 | 0.2051 | +0.0033 | +0.0631 | negligible | 0.0809 | No |
| **Composite** | 0.5616 | 0.5522 | +0.0094 | +0.1228 | negligible | 0.0648 | **No** |

**no_rationale_think_1024 better:** MMS (d=+0.185), SR@3 (d=+0.140), SR@5 (d=+0.111), SR@10 (d=+0.166)
**genai_v2_think_1024 better:** ILD (d=-0.260), TCD (d=-0.317), Redundancy Rate (d=+0.328)
**No significant difference:** CCR, OHCD, Composite

### IS_SPARSE_ORDER = False  (8,044 consumers)  (n=40,359 pairs)

| Metric | Mean no_rationale_think_1024 | Mean genai_v2_think_1024 | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| MMS | 0.5154 | 0.5115 | +0.0039 | +0.0571 | negligible | 1.07e-25 | Yes |
| SR@3 | 0.3750 | 0.3714 | +0.0035 | +0.0162 | negligible | 8.95e-04 | Yes |
| SR@5 | 0.4758 | 0.4706 | +0.0052 | +0.0241 | negligible | 2.63e-05 | Yes |
| SR@10 | 0.5980 | 0.5894 | +0.0086 | +0.0407 | negligible | 5.36e-11 | Yes |
| CCR | 0.7660 | 0.7702 | -0.0042 | -0.0375 | negligible | 2.31e-11 | Yes |
| ILD | 0.6516 | 0.6530 | -0.0014 | -0.0271 | negligible | 1.58e-07 | Yes |
| TCD | 0.8552 | 0.8714 | -0.0163 | -0.1142 | negligible | 6.50e-105 | Yes |
| Redundancy Rate | 0.0135 | 0.0102 | +0.0032 | +0.1444 | negligible | 3.24e-175 | Yes |
| OHCD | 0.4499 | 0.4498 | +0.0001 | +0.0006 | negligible | 0.7850 | No |
| **Composite** | 0.5824 | 0.5813 | +0.0011 | +0.0194 | negligible | 0.0025 | **Yes** |

**no_rationale_think_1024 better:** MMS (d=+0.057), SR@3 (d=+0.016), SR@5 (d=+0.024), SR@10 (d=+0.041), Composite (d=+0.019)
**genai_v2_think_1024 better:** CCR (d=-0.038), ILD (d=-0.027), TCD (d=-0.114), Redundancy Rate (d=+0.144)
**No significant difference:** OHCD

## Breakdown by IS_SPARSE_BROWSE

### IS_SPARSE_BROWSE = True  (229 consumers)  (n=340 pairs)

| Metric | Mean no_rationale_think_1024 | Mean genai_v2_think_1024 | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| MMS | 0.5365 | 0.5302 | +0.0063 | +0.0751 | negligible | 0.4233 | No |
| SR@3 | 0.5072 | 0.4850 | +0.0223 | +0.0786 | negligible | 0.6013 | No |
| SR@5 | 0.5817 | 0.5621 | +0.0196 | +0.0683 | negligible | 0.6013 | No |
| SR@10 | 0.6514 | 0.6424 | +0.0090 | +0.0343 | negligible | 1.0000 | No |
| CCR | 0.7494 | 0.7593 | -0.0100 | -0.1397 | negligible | 0.1511 | No |
| ILD | 0.6315 | 0.6496 | -0.0181 | -0.2926 | small | 8.08e-06 | Yes |
| TCD | 0.8224 | 0.8703 | -0.0479 | -0.2947 | small | 1.48e-06 | Yes |
| Redundancy Rate | 0.0172 | 0.0085 | +0.0087 | +0.3319 | small | 1.92e-08 | Yes |
| OHCD | 0.3262 | 0.3179 | +0.0082 | +0.1461 | negligible | 0.1087 | No |
| **Composite** | 0.5768 | 0.5739 | +0.0029 | +0.0403 | negligible | 1.0000 | **No** |

**genai_v2_think_1024 better:** ILD (d=-0.293), TCD (d=-0.295), Redundancy Rate (d=+0.332)
**No significant difference:** MMS, SR@3, SR@5, SR@10, CCR, OHCD, Composite

### IS_SPARSE_BROWSE = False  (8,806 consumers)  (n=41,281 pairs)

| Metric | Mean no_rationale_think_1024 | Mean genai_v2_think_1024 | Mean Diff | Cohen's d | Effect | Adj. p | Sig? |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- |
| MMS | 0.5164 | 0.5121 | +0.0043 | +0.0618 | negligible | 5.99e-30 | Yes |
| SR@3 | 0.3781 | 0.3736 | +0.0045 | +0.0205 | negligible | 2.62e-05 | Yes |
| SR@5 | 0.4786 | 0.4727 | +0.0059 | +0.0272 | negligible | 1.76e-06 | Yes |
| SR@10 | 0.6004 | 0.5906 | +0.0098 | +0.0459 | negligible | 2.65e-14 | Yes |
| CCR | 0.7663 | 0.7702 | -0.0039 | -0.0351 | negligible | 1.87e-10 | Yes |
| ILD | 0.6513 | 0.6529 | -0.0016 | -0.0321 | negligible | 1.93e-10 | Yes |
| TCD | 0.8545 | 0.8715 | -0.0170 | -0.1193 | negligible | 9.66e-117 | Yes |
| Redundancy Rate | 0.0135 | 0.0102 | +0.0033 | +0.1486 | negligible | 4.93e-190 | Yes |
| OHCD | 0.4435 | 0.4434 | +0.0001 | +0.0009 | negligible | 0.7199 | No |
| **Composite** | 0.5818 | 0.5805 | +0.0014 | +0.0233 | negligible | 5.26e-04 | **Yes** |

**no_rationale_think_1024 better:** MMS (d=+0.062), SR@3 (d=+0.021), SR@5 (d=+0.027), SR@10 (d=+0.046), Composite (d=+0.023)
**genai_v2_think_1024 better:** CCR (d=-0.035), ILD (d=-0.032), TCD (d=-0.119), Redundancy Rate (d=+0.149)
**No significant difference:** OHCD
