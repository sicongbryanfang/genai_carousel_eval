# Statistical Significance: prompt4 vs no_think

- **Test**: Wilcoxon signed-rank (two-sided, non-parametric paired test)
- **Effect size**: Cohen's d (paired)
- **Correction**: Holm-Bonferroni for 12 metrics
- **Significance level**: 0.05
- **Common (consumer, daypart) pairs**: 42,991

| Metric | Mean prompt4 | Mean no_think | Mean Diff | Cohen's d | Effect | Wilcoxon p | Adj. p | Sig? | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MMS | 0.5039 | 0.5283 | -0.0243 | -0.3108 | small | 0.00e+00 | 0.00e+00 | Yes | 42,991 |
| SR@3 | 0.3875 | 0.3919 | -0.0044 | -0.0190 | negligible | 0.1186 | 0.1186 | No | 42,991 |
| SR@5 | 0.4793 | 0.4916 | -0.0123 | -0.0530 | negligible | 3.03e-20 | 9.08e-20 | Yes | 42,991 |
| SR@10 | 0.5836 | 0.6132 | -0.0296 | -0.1316 | negligible | 7.95e-168 | 6.36e-167 | Yes | 42,991 |
| CCR | 0.7722 | 0.7606 | +0.0117 | +0.1079 | negligible | 1.99e-98 | 9.94e-98 | Yes | 41,407 |
| ILD | 0.6457 | 0.6596 | -0.0139 | -0.2771 | small | 0.00e+00 | 0.00e+00 | Yes | 42,991 |
| TCD | 0.8765 | 0.8606 | +0.0159 | +0.1116 | negligible | 5.03e-115 | 3.02e-114 | Yes | 42,991 |
| Redundancy Rate | 0.0090 | 0.0135 | -0.0044 | -0.1959 | negligible | 0.00e+00 | 0.00e+00 | Yes | 42,991 |
| OHCD | 0.4276 | 0.4338 | -0.0062 | -0.0676 | negligible | 2.15e-38 | 8.60e-38 | Yes | 42,991 |
| TMC | 0.1665 | 0.1607 | +0.0058 | +0.2688 | small | 0.00e+00 | 0.00e+00 | Yes | 42,991 |
| FCS | 0.8326 | 0.8325 | +0.0002 | +0.0436 | negligible | 4.53e-20 | 9.08e-20 | Yes | 42,991 |
| **Composite** | 0.5439 | 0.5500 | -0.0062 | -0.1237 | negligible | 1.09e-148 | 7.63e-148 | **Yes** | 42,991 |

## Interpretation

Positive mean diff = prompt4 higher. Negative = no_think higher.
For Redundancy Rate, lower is better.

**prompt4 significantly better:**
- CCR (+0.0117, d=+0.1079)
- TCD (+0.0159, d=+0.1116)
- Redundancy Rate (-0.0044, d=-0.1959)
- TMC (+0.0058, d=+0.2688)
- FCS (+0.0002, d=+0.0436)

**no_think significantly better:**
- MMS (-0.0243, d=-0.3108)
- SR@5 (-0.0123, d=-0.0530)
- SR@10 (-0.0296, d=-0.1316)
- ILD (-0.0139, d=-0.2771)
- OHCD (-0.0062, d=-0.0676)
- Composite (-0.0062, d=-0.1237)

**No significant difference:** SR@3

## Notes

- With n~43k, nearly all differences are statistically significant. Focus on **Cohen's d** (effect size) for practical significance.
- |d| < 0.2 = negligible, 0.2-0.5 = small, 0.5-0.8 = medium, > 0.8 = large.
