# Statistical Significance: prompt4 vs no_think

- **Test**: Wilcoxon signed-rank (two-sided, non-parametric paired test)
- **Effect size**: Cohen's d (paired)
- **Correction**: Holm-Bonferroni for 12 metrics
- **Significance level**: 0.05
- **Common (consumer, daypart) pairs**: 42,949

| Metric | Mean prompt4 | Mean no_think | Mean Diff | Cohen's d | Effect | Wilcoxon p | Adj. p | Sig? | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MMS | 0.5013 | 0.5259 | -0.0246 | -0.3144 | small | 0.00e+00 | 0.00e+00 | Yes | 42,949 |
| SR@3 | 0.3797 | 0.3815 | -0.0018 | -0.0078 | negligible | 0.5454 | 0.5454 | No | 42,949 |
| SR@5 | 0.4714 | 0.4840 | -0.0126 | -0.0540 | negligible | 1.51e-23 | 4.53e-23 | Yes | 42,949 |
| SR@10 | 0.5797 | 0.6108 | -0.0312 | -0.1380 | negligible | 3.26e-191 | 2.28e-190 | Yes | 42,949 |
| CCR | 0.7758 | 0.7627 | +0.0131 | +0.1210 | negligible | 6.08e-122 | 3.65e-121 | Yes | 41,371 |
| ILD | 0.6468 | 0.6606 | -0.0138 | -0.2745 | small | 0.00e+00 | 0.00e+00 | Yes | 42,949 |
| TCD | 0.8780 | 0.8621 | +0.0159 | +0.1124 | negligible | 1.22e-115 | 6.09e-115 | Yes | 42,949 |
| Redundancy Rate | 0.0088 | 0.0132 | -0.0044 | -0.1969 | negligible | 0.00e+00 | 0.00e+00 | Yes | 42,949 |
| OHCD | 0.4373 | 0.4442 | -0.0069 | -0.0756 | negligible | 1.18e-49 | 4.71e-49 | Yes | 42,949 |
| TMC | 0.1665 | 0.1607 | +0.0058 | +0.2678 | small | 0.00e+00 | 0.00e+00 | Yes | 42,949 |
| FCS | 0.8326 | 0.8324 | +0.0002 | +0.0468 | negligible | 2.48e-22 | 4.95e-22 | Yes | 42,949 |
| **Composite** | 0.5768 | 0.5858 | -0.0090 | -0.1431 | negligible | 6.83e-205 | 5.46e-204 | **Yes** | 42,949 |

## Interpretation

Positive mean diff = prompt4 higher. Negative = no_think higher.
For Redundancy Rate, lower is better.

**prompt4 significantly better:**
- CCR (+0.0131, d=+0.1210)
- TCD (+0.0159, d=+0.1124)
- Redundancy Rate (-0.0044, d=-0.1969)
- TMC (+0.0058, d=+0.2678)
- FCS (+0.0002, d=+0.0468)

**no_think significantly better:**
- MMS (-0.0246, d=-0.3144)
- SR@5 (-0.0126, d=-0.0540)
- SR@10 (-0.0312, d=-0.1380)
- ILD (-0.0138, d=-0.2745)
- OHCD (-0.0069, d=-0.0756)
- Composite (-0.0090, d=-0.1431)

**No significant difference:** SR@3

## Notes

- With n~43k, nearly all differences are statistically significant. Focus on **Cohen's d** (effect size) for practical significance.
- |d| < 0.2 = negligible, 0.2-0.5 = small, 0.5-0.8 = medium, > 0.8 = large.
