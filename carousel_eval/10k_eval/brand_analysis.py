"""
Compare brand-name title prevalence across prompt4-family input CSVs.

Reuses the same keyword set as the existing report so the numbers line up.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd


BRAND_KEYWORDS = [
    "big mac",
    "mcnugget",
    "whopper",
    "mcgriddle",
    "mcmuffin",
    "chipotle",
    "happy meal",
    "mcchicken",
    "chick-fil-a",
    "kfc",
]


def iter_titles(json_str: str):
    try:
        carousel_list = json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return
    for dp_obj in carousel_list:
        for _, dp_data in dp_obj.items():
            if not isinstance(dp_data, dict):
                continue
            for c in dp_data.get("carousels", []) or []:
                title = (c.get("title") or "").strip()
                if title:
                    yield title


def analyze(path: Path) -> dict:
    print(f"[load] {path.name}", flush=True)
    df = pd.read_csv(path, usecols=["NORMALIZED_CAROUSELS"])
    total_titles = 0
    brand_title_count = 0
    keyword_counts = Counter()
    title_counter = Counter()
    distinct_brand_titles = set()

    for js in df["NORMALIZED_CAROUSELS"]:
        for title in iter_titles(js):
            total_titles += 1
            lower = title.lower()
            title_counter[lower] += 1
            hit = False
            for kw in BRAND_KEYWORDS:
                if kw in lower:
                    keyword_counts[kw] += 1
                    hit = True
            if hit:
                brand_title_count += 1
                distinct_brand_titles.add(lower)

    return {
        "total": total_titles,
        "brand": brand_title_count,
        "brand_pct": brand_title_count / total_titles * 100 if total_titles else 0.0,
        "distinct_brand_titles": len(distinct_brand_titles),
        "keyword_counts": dict(keyword_counts),
        "title_counter": title_counter,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", required=True,
                    help="Pairs of label=path, e.g. prompt4=10k_user_promp4.csv")
    args = ap.parse_args()

    results = {}
    for spec in args.inputs:
        if "=" not in spec:
            print(f"bad --inputs entry: {spec}", file=sys.stderr)
            sys.exit(1)
        label, path = spec.split("=", 1)
        results[label] = analyze(Path(path))

    labels = list(results.keys())

    print("\n## Volume / brand share")
    print("| Variant | Total titles | Brand-title rows | Brand share | Distinct brand titles |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for label in labels:
        r = results[label]
        print(f"| {label} | {r['total']:,} | {r['brand']:,} | "
              f"{r['brand_pct']:.2f}% | {r['distinct_brand_titles']:,} |")

    print("\n## Brand keyword frequency")
    header = "| Brand keyword | " + " | ".join(labels) + " |"
    sep = "| --- | " + " | ".join("---:" for _ in labels) + " |"
    print(header)
    print(sep)
    for kw in BRAND_KEYWORDS:
        cells = [f"{results[l]['keyword_counts'].get(kw, 0):,}" for l in labels]
        print(f"| {kw} | " + " | ".join(cells) + " |")

    print("\n## Top brand-name title clusters (counts)")
    cluster_keys = [
        ("chicken mcnuggets / mcnuggets", ["chicken mcnuggets", "mcnuggets"]),
        ("big mac burgers", ["big mac burgers"]),
        ("big mac meals", ["big mac meals"]),
        ("sausage egg mcgriddles", ["sausage egg mcgriddles"]),
        ("whopper burgers / meals", ["whopper burgers", "whopper meals"]),
        ("happy meal variants", ["happy meal", "happy meals"]),
        ("sausage egg mcmuffins", ["sausage egg mcmuffins"]),
    ]
    print("| Title cluster | " + " | ".join(labels) + " |")
    print("| --- | " + " | ".join("---:" for _ in labels) + " |")
    for name, needles in cluster_keys:
        cells = []
        for l in labels:
            tc = results[l]["title_counter"]
            total = sum(c for t, c in tc.items() if any(n in t for n in needles))
            cells.append(f"{total:,}")
        print(f"| {name} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
