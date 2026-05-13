"""
Reverse eval: rank all consumers by MMS / SR@5 metric score, then check what
fraction of each tier comes from the high-engagement vs zero-engagement group.

Usage:
    python carousel_eval/Engagement/reverse_eval.py
    python carousel_eval/Engagement/reverse_eval.py --by-daypart
"""
import argparse
import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

EVAL_TOP = os.path.join(os.path.dirname(__file__), "results", "eval_top.csv")
EVAL_BOTTOM = os.path.join(os.path.dirname(__file__), "results", "eval_bottom.csv")

METRICS = [
    ("mms",    "MMS"),
    ("sr_at_5", "SR@5"),
    ("sr_at_10", "SR@10"),
]


def load_data() -> pd.DataFrame:
    top = pd.read_csv(EVAL_TOP)
    bottom = pd.read_csv(EVAL_BOTTOM)
    top["group"] = "top"
    bottom["group"] = "bottom"
    return pd.concat([top, bottom], ignore_index=True)


def aggregate_per_consumer(df: pd.DataFrame) -> pd.DataFrame:
    agg = (
        df.groupby("consumer_id")
        .agg(
            group=("group", "first"),
            mms=("mms", "mean"),
            sr_at_5=("sr_at_5", "mean"),
            sr_at_10=("sr_at_10", "mean"),
        )
        .reset_index()
    )
    return agg


def tier_label(series: pd.Series) -> pd.Series:
    p25 = series.quantile(0.25)
    p75 = series.quantile(0.75)
    labels = pd.Series("middle", index=series.index)
    labels[series >= p75] = "top_quartile"
    labels[series <= p25] = "bottom_quartile"
    return labels, p25, p75


def cross_tab_section(consumers: pd.DataFrame, col: str, label: str) -> str:
    tiers, p25, p75 = tier_label(consumers[col])
    consumers = consumers.copy()
    consumers["tier"] = tiers

    lines = [
        f"## {label} — Quartile Tiers",
        "",
        f"- p25 threshold: {p25:.4f}",
        f"- p75 threshold: {p75:.4f}",
        "",
    ]

    # Cross-tabulate tier x group (only top/bottom quartile rows)
    subset = consumers[consumers["tier"].isin(["top_quartile", "bottom_quartile"])].copy()
    ct = pd.crosstab(subset["tier"], subset["group"])

    # Ensure both columns exist
    for g in ["top", "bottom"]:
        if g not in ct.columns:
            ct[g] = 0

    ct = ct[["top", "bottom"]]
    ct["total"] = ct["top"] + ct["bottom"]
    ct["top_%"] = (ct["top"] / ct["total"] * 100).round(1)
    ct["bottom_%"] = (ct["bottom"] / ct["total"] * 100).round(1)

    # Markdown table
    lines.append(
        f"| Metric Tier       | top-engagement | %     | zero-engagement | %     | total |"
    )
    lines.append(
        f"| ----------------- | -------------- | ----- | --------------- | ----- | ----- |"
    )

    tier_order = [("top_quartile", "Top Q (≥ p75)"), ("bottom_quartile", "Bottom Q (≤ p25)")]
    for tier_key, tier_display in tier_order:
        if tier_key in ct.index:
            row = ct.loc[tier_key]
            lines.append(
                f"| {tier_display:<17} | {int(row['top']):>14} | {row['top_%']:>5}% "
                f"| {int(row['bottom']):>15} | {row['bottom_%']:>5}% | {int(row['total']):>5} |"
            )

    # Chi-square test
    if len(ct) == 2:
        contingency = ct[["top", "bottom"]].values
        chi2, p_val, dof, _ = chi2_contingency(contingency)
        lines.append("")
        lines.append(
            f"Chi-square test of independence: χ²={chi2:.3f}, p={p_val:.4f}, dof={dof}"
        )
        if p_val < 0.05:
            lines.append("→ Distribution is **statistically significant** (p < 0.05)")
        else:
            lines.append("→ Distribution is **not statistically significant** (p ≥ 0.05)")

    # Median split summary
    median = consumers[col].median()
    above = consumers[consumers[col] >= median]
    below = consumers[consumers[col] < median]

    lines.append("")
    lines.append(f"### Median Split (median = {median:.4f})")
    lines.append("")
    lines.append(
        "| Half              | top-engagement | %     | zero-engagement | %     | total |"
    )
    lines.append(
        "| ----------------- | -------------- | ----- | --------------- | ----- | ----- |"
    )
    for half, half_df, half_label in [
        ("above", above, f"Above median"),
        ("below", below, f"Below median"),
    ]:
        n_top = (half_df["group"] == "top").sum()
        n_bot = (half_df["group"] == "bottom").sum()
        n_total = n_top + n_bot
        pct_top = n_top / n_total * 100 if n_total else 0
        pct_bot = n_bot / n_total * 100 if n_total else 0
        lines.append(
            f"| {half_label:<17} | {n_top:>14} | {pct_top:>5.1f}% "
            f"| {n_bot:>15} | {pct_bot:>5.1f}% | {n_total:>5} |"
        )

    lines.append("")
    return "\n".join(lines)


def daypart_section(df: pd.DataFrame, col: str, label: str) -> str:
    lines = [f"## {label} — Breakdown by Daypart", ""]

    for daypart, grp in df.groupby("day_part"):
        agg = (
            grp.groupby("consumer_id")
            .agg(group=("group", "first"), score=(col, "mean"))
            .reset_index()
        )
        if len(agg) < 10:
            continue
        p25 = agg["score"].quantile(0.25)
        p75 = agg["score"].quantile(0.75)
        top_q = agg[agg["score"] >= p75]
        bot_q = agg[agg["score"] <= p25]
        lines.append(f"### {daypart} (n={len(agg)})")
        for tier_label_str, tier_df in [("Top Q", top_q), ("Bottom Q", bot_q)]:
            n_top = (tier_df["group"] == "top").sum()
            n_bot = (tier_df["group"] == "bottom").sum()
            n = n_top + n_bot
            lines.append(
                f"  {tier_label_str}: top={n_top} ({n_top/n*100:.1f}%)  "
                f"zero={n_bot} ({n_bot/n*100:.1f}%)  total={n}"
            )
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--by-daypart", action="store_true")
    args = parser.parse_args()

    df = load_data()
    consumers = aggregate_per_consumer(df)

    n_top = (consumers["group"] == "top").sum()
    n_bot = (consumers["group"] == "bottom").sum()
    base_pct_top = n_top / len(consumers) * 100
    base_pct_bot = n_bot / len(consumers) * 100

    output = [
        "# Reverse Eval — Metric Tiers vs Engagement Groups",
        "",
        "Pool all consumers from both engagement groups, rank by carousel quality metric,",
        "cut into top/bottom quartiles, and check what fraction of each tier is from the",
        "high-engagement (top) vs zero-engagement (bottom) group.",
        "",
        "## Consumer Pool",
        "",
        f"| Group           | Consumers | Base % |",
        f"| --------------- | --------- | ------ |",
        f"| top-engagement  | {n_top:>9} | {base_pct_top:>5.1f}% |",
        f"| zero-engagement | {n_bot:>9} | {base_pct_bot:>5.1f}% |",
        f"| **total**       | {len(consumers):>9} |        |",
        "",
        "A random split would give these base rates in every tier.",
        "Deviation from base % indicates the metric predicts engagement.",
        "",
    ]

    for col, label in METRICS:
        output.append(cross_tab_section(consumers, col, label))
        output.append("")

    if args.by_daypart:
        for col, label in METRICS:
            output.append(daypart_section(df, col, label))
            output.append("")

    print("\n".join(output))


if __name__ == "__main__":
    main()
