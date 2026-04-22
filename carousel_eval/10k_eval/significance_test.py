"""
Statistical significance testing between two carousel eval CSVs.

Uses Wilcoxon signed-rank test (non-parametric paired test) with Cohen's d
for effect size and Holm-Bonferroni correction for multiple comparisons.

Usage:
    python carousel_eval/10k_eval/significance_test.py \
        --csv_a carousel_eval/10k_eval/eval_user_prompt4.csv \
        --csv_b carousel_eval/10k_eval/eval_user_prompt4_no_think_no_rationale.csv \
        --label_a prompt4 --label_b no_think \
        --output carousel_eval/10k_eval/significance_report.md
"""

from __future__ import annotations

import argparse
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


METRIC_COLS = [
    "mms", "sr_at_3", "sr_at_5", "sr_at_10",
    "ccr", "ild", "tcd", "redundancy_rate",
    "ohcd", "tmc", "fcs", "composite_quality_score",
]

METRIC_DISPLAY = {
    "mms": "MMS",
    "sr_at_3": "SR@3",
    "sr_at_5": "SR@5",
    "sr_at_10": "SR@10",
    "ccr": "CCR",
    "ild": "ILD",
    "tcd": "TCD",
    "redundancy_rate": "Redundancy Rate",
    "ohcd": "OHCD",
    "tmc": "TMC",
    "fcs": "FCS",
    "composite_quality_score": "Composite",
}

# For interpretation: higher is better for all except redundancy_rate
LOWER_IS_BETTER = {"redundancy_rate"}


def load_and_merge(csv_a: str, csv_b: str) -> pd.DataFrame:
    """Inner join two eval CSVs on (consumer_id, day_part)."""
    df_a = pd.read_csv(csv_a)
    df_b = pd.read_csv(csv_b)
    merged = df_a.merge(
        df_b,
        on=["consumer_id", "day_part"],
        suffixes=("_a", "_b"),
    )
    return merged


def cohens_d(diffs: np.ndarray) -> float:
    """Cohen's d for paired differences."""
    std = diffs.std(ddof=1)
    if std == 0:
        return 0.0
    return float(diffs.mean() / std)


def d_label(d: float) -> str:
    """Human-readable effect size label."""
    ad = abs(d)
    if ad < 0.2:
        return "negligible"
    if ad < 0.5:
        return "small"
    if ad < 0.8:
        return "medium"
    return "large"


def holm_bonferroni(p_values: Dict[str, float]) -> Dict[str, float]:
    """Holm-Bonferroni correction for multiple comparisons."""
    items = sorted(p_values.items(), key=lambda x: x[1])
    m = len(items)
    adjusted = {}
    max_so_far = 0.0
    for i, (name, p) in enumerate(items):
        adj_p = min(p * (m - i), 1.0)
        adj_p = max(adj_p, max_so_far)
        max_so_far = adj_p
        adjusted[name] = adj_p
    return adjusted


def run_test(
    merged: pd.DataFrame,
    metric: str,
    alpha: float = 0.05,
) -> Optional[dict]:
    """Run Wilcoxon signed-rank test for a single metric."""
    col_a = f"{metric}_a"
    col_b = f"{metric}_b"

    if col_a not in merged.columns or col_b not in merged.columns:
        return None

    valid = merged[[col_a, col_b]].dropna()
    if len(valid) < 10:
        return None

    vals_a = valid[col_a].values
    vals_b = valid[col_b].values
    diffs = vals_a - vals_b

    # Handle all-zero differences
    if np.all(diffs == 0):
        return {
            "metric": metric,
            "n": len(diffs),
            "mean_a": float(vals_a.mean()),
            "mean_b": float(vals_b.mean()),
            "mean_diff": 0.0,
            "median_diff": 0.0,
            "cohens_d": 0.0,
            "d_label": "negligible",
            "wilcoxon_p": 1.0,
        }

    stat, p = wilcoxon(diffs, alternative="two-sided")

    d = cohens_d(diffs)

    return {
        "metric": metric,
        "n": len(diffs),
        "mean_a": float(vals_a.mean()),
        "mean_b": float(vals_b.mean()),
        "mean_diff": float(diffs.mean()),
        "median_diff": float(np.median(diffs)),
        "cohens_d": d,
        "d_label": d_label(d),
        "wilcoxon_p": float(p),
    }


def format_report(
    results: List[dict],
    label_a: str,
    label_b: str,
    total_pairs: int,
    alpha: float,
) -> str:
    """Format results as markdown report."""
    lines = []
    lines.append(f"# Statistical Significance: {label_a} vs {label_b}")
    lines.append("")
    lines.append(f"- **Test**: Wilcoxon signed-rank (two-sided, non-parametric paired test)")
    lines.append(f"- **Effect size**: Cohen's d (paired)")
    lines.append(f"- **Correction**: Holm-Bonferroni for {len(results)} metrics")
    lines.append(f"- **Significance level**: {alpha}")
    lines.append(f"- **Common (consumer, daypart) pairs**: {total_pairs:,}")
    lines.append("")

    # Table header
    lines.append(
        f"| Metric | Mean {label_a} | Mean {label_b} | Mean Diff | Cohen's d | Effect | Wilcoxon p | Adj. p | Sig? | n |"
    )
    lines.append(
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    )

    for r in results:
        display = METRIC_DISPLAY.get(r["metric"], r["metric"])
        sig = "Yes" if r["adj_p"] < alpha else "No"
        # Bold composite row
        if r["metric"] == "composite_quality_score":
            display = f"**{display}**"
            sig = f"**{sig}**"

        def fmt_p(p):
            if p < 0.001:
                return f"{p:.2e}"
            return f"{p:.4f}"

        sign = "+" if r["mean_diff"] > 0 else ""
        lines.append(
            f"| {display} "
            f"| {r['mean_a']:.4f} "
            f"| {r['mean_b']:.4f} "
            f"| {sign}{r['mean_diff']:.4f} "
            f"| {r['cohens_d']:+.4f} "
            f"| {r['d_label']} "
            f"| {fmt_p(r['wilcoxon_p'])} "
            f"| {fmt_p(r['adj_p'])} "
            f"| {sig} "
            f"| {r['n']:,} |"
        )

    # Interpretation
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(f"Positive mean diff = {label_a} higher. Negative = {label_b} higher.")
    lines.append(f"For Redundancy Rate, lower is better.")
    lines.append("")

    sig_a_better = []
    sig_b_better = []
    not_sig = []

    for r in results:
        display = METRIC_DISPLAY.get(r["metric"], r["metric"])
        if r["adj_p"] >= alpha:
            not_sig.append(display)
            continue
        metric = r["metric"]
        # Determine which direction is "better"
        if metric in LOWER_IS_BETTER:
            if r["mean_diff"] < 0:
                sig_a_better.append(f"{display} ({r['mean_diff']:+.4f}, d={r['cohens_d']:+.4f})")
            else:
                sig_b_better.append(f"{display} ({r['mean_diff']:+.4f}, d={r['cohens_d']:+.4f})")
        else:
            if r["mean_diff"] > 0:
                sig_a_better.append(f"{display} ({r['mean_diff']:+.4f}, d={r['cohens_d']:+.4f})")
            else:
                sig_b_better.append(f"{display} ({r['mean_diff']:+.4f}, d={r['cohens_d']:+.4f})")

    if sig_a_better:
        lines.append(f"**{label_a} significantly better:**")
        for item in sig_a_better:
            lines.append(f"- {item}")
        lines.append("")

    if sig_b_better:
        lines.append(f"**{label_b} significantly better:**")
        for item in sig_b_better:
            lines.append(f"- {item}")
        lines.append("")

    if not_sig:
        lines.append(f"**No significant difference:** {', '.join(not_sig)}")
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- With n~43k, nearly all differences are statistically significant. "
                 "Focus on **Cohen's d** (effect size) for practical significance.")
    lines.append("- |d| < 0.2 = negligible, 0.2-0.5 = small, 0.5-0.8 = medium, > 0.8 = large.")
    lines.append("")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Statistical significance test between two eval CSVs")
    p.add_argument("--csv_a", required=True, help="First eval CSV (baseline)")
    p.add_argument("--csv_b", required=True, help="Second eval CSV (variant)")
    p.add_argument("--label_a", default="A", help="Label for first CSV")
    p.add_argument("--label_b", default="B", help="Label for second CSV")
    p.add_argument("--output", default=None, help="Output markdown file path")
    p.add_argument("--alpha", type=float, default=0.05, help="Significance level")
    args = p.parse_args()

    print(f"[load] Merging {args.csv_a} and {args.csv_b} ...")
    merged = load_and_merge(args.csv_a, args.csv_b)
    total_pairs = len(merged)
    print(f"[load] Common pairs: {total_pairs:,}")

    # Run tests
    results = []
    for metric in METRIC_COLS:
        r = run_test(merged, metric, args.alpha)
        if r is not None:
            results.append(r)
            print(f"[test] {metric:30s}  diff={r['mean_diff']:+.4f}  d={r['cohens_d']:+.4f}  p={r['wilcoxon_p']:.2e}")

    # Holm-Bonferroni correction
    raw_p = {r["metric"]: r["wilcoxon_p"] for r in results}
    adj_p = holm_bonferroni(raw_p)
    for r in results:
        r["adj_p"] = adj_p[r["metric"]]

    # Format and output
    report = format_report(results, args.label_a, args.label_b, total_pairs, args.alpha)
    print("\n" + report)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\n[done] Saved {args.output}")


if __name__ == "__main__":
    main()
