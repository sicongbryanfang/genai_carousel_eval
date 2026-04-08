"""Generate results.md from eval CSVs.

Usage:
    python carousel_eval/generate_report.py <results_dir>

Example:
    python carousel_eval/generate_report.py carousel_eval/results_all_cx_title_only
"""

import sys
import pandas as pd
import os

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <results_dir>")
    sys.exit(1)

RESULTS_DIR = sys.argv[1]

prod = pd.read_csv(os.path.join(RESULTS_DIR, "eval_prod.csv"))
ret = pd.read_csv(os.path.join(RESULTS_DIR, "eval_retrieved.csv"))

METRICS = ["mms", "sr_at_3", "sr_at_5", "sr_at_10", "ccr", "ild", "ohcd", "tmc", "fcs", "composite_quality_score"]
DISPLAY = ["MMS", "SR@3", "SR@5", "SR@10", "CCR", "ILD", "OHCD", "TMC", "FCS", "Composite"]
DAYPART_ORDER = [
    "weekday_breakfast", "weekday_lunch", "weekday_dinner", "weekday_late_night",
    "weekend_breakfast", "weekend_lunch", "weekend_dinner", "weekend_late_night",
]
KEY_METRICS = ["mms", "sr_at_5", "ccr", "ild", "composite_quality_score"]
KEY_DISPLAY = ["MMS", "SR@5", "CCR", "ILD", "Composite"]

lines = []
lines.append("# Carousel Evaluation Results — All Consumers, Title Only\n")
lines.append(f"- **Embed mode**: title_only")
lines.append(f"- **Common consumers**: {prod['consumer_id'].nunique():,}")
lines.append("- **Model**: all-MiniLM-L6-v2\n")

# --- Overall Results ---
lines.append("## Overall Results\n")
lines.append("| Metric | Prod | Retrieved | Delta |")
lines.append("|--------|------|-----------|-------|")
for m, d in zip(METRICS, DISPLAY):
    p = prod[m].mean()
    r = ret[m].mean()
    delta = r - p
    bold_p = f"**{p:.4f}**" if p > r else f"{p:.4f}"
    bold_r = f"**{r:.4f}**" if r > p else f"{r:.4f}"
    d_str = f"**{d}**" if m == "composite_quality_score" else d
    delta_str = f"**{delta:+.4f}**" if m == "composite_quality_score" else f"{delta:+.4f}"
    lines.append(f"| {d_str} | {bold_p} | {bold_r} | {delta_str} |")

# --- Overall % Change ---
lines.append("\n## Overall Results — Percentage Change\n")
lines.append("| Metric | Prod | Retrieved | % Change |")
lines.append("|--------|------|-----------|----------|")
for m, d in zip(METRICS, DISPLAY):
    p = prod[m].mean()
    r = ret[m].mean()
    pct = (r - p) / p * 100
    d_str = f"**{d}**" if m == "composite_quality_score" else d
    pct_str = f"**{pct:+.1f}%**" if m == "composite_quality_score" else f"{pct:+.1f}%"
    lines.append(f"| {d_str} | {p:.4f} | {r:.4f} | {pct_str} |")

# --- Per-Daypart Composite % Change ---
prod_dp = prod.groupby("day_part")["composite_quality_score"].mean()
ret_dp = ret.groupby("day_part")["composite_quality_score"].mean()

lines.append("\n## Per-Daypart — Composite % Change (Retrieved vs Prod)\n")
lines.append("| Daypart | Prod | Retrieved | % Change |")
lines.append("|---------|------|-----------|----------|")
for dp in DAYPART_ORDER:
    p = prod_dp[dp]
    r = ret_dp[dp]
    pct = (r - p) / p * 100
    lines.append(f"| {dp} | {p:.4f} | {r:.4f} | {pct:+.1f}% |")

# --- Per-Daypart Prod ---
lines.append("\n## Per-Daypart Results — Prod\n")
header = "| Daypart | Count | " + " | ".join(KEY_DISPLAY) + " |"
sep = "|---------|-------|" + "|".join(["------"] * len(KEY_DISPLAY)) + "|"
lines.append(header)
lines.append(sep)
for dp in DAYPART_ORDER:
    grp = prod[prod["day_part"] == dp]
    vals = " | ".join(f"{grp[m].mean():.4f}" for m in KEY_METRICS)
    lines.append(f"| {dp} | {len(grp):,} | {vals} |")

# --- Per-Daypart Retrieved ---
lines.append("\n## Per-Daypart Results — Retrieved\n")
lines.append(header)
lines.append(sep)
for dp in DAYPART_ORDER:
    grp = ret[ret["day_part"] == dp]
    vals = " | ".join(f"{grp[m].mean():.4f}" for m in KEY_METRICS)
    lines.append(f"| {dp} | {len(grp):,} | {vals} |")

output = "\n".join(lines) + "\n"
out_path = os.path.join(RESULTS_DIR, "results.md")
with open(out_path, "w") as f:
    f.write(output)

print(f"Written {out_path}")
