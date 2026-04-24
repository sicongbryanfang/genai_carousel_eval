"""
Parse thinking_budget_comparison___2.csv into 3 separate carousel CSVs,
one per thinking-token budget (512, 1024, 8192).

Each cell in the source CSV is formatted as:
    Title
    [cuisine1, cuisine2, ...]

Output CSVs have columns:
    CONSUMER_ID, DAY_PART, CAROUSEL_RANK, TITLE, TAGS
matching the format expected by local_eval_test.py.
"""

import csv
import json
import re

INPUT = "thinking_budget_comparison___2.csv"
BUDGETS = ["budget=512", "budget=1024", "budget=8192"]

# Source uses snake_case; taxonomy uses title-case with spaces.
# Fix edge cases that .replace("_"," ").title() gets wrong.
CUISINE_FIXUPS = {
    "Australian New Zealand": "Australian & New Zealand",
    "Southeast Asian": "SouthEast Asian",
}


def _normalise_cuisine(raw: str) -> str:
    # Collapse whitespace (handles typos like "eastern_ european")
    name = re.sub(r"\s+", " ", raw.replace("_", " ")).strip().title()
    return CUISINE_FIXUPS.get(name, name)


def parse_cell(cell_text: str):
    """Extract title and cuisine list from a cell."""
    lines = cell_text.strip().split("\n")
    title = lines[0].strip()
    cuisines = []
    if len(lines) >= 2:
        bracket_line = lines[1].strip()
        m = re.match(r"\[(.+)\]", bracket_line)
        if m:
            cuisines = [
                _normalise_cuisine(c) for c in m.group(1).split(",")
            ]
    return title, cuisines


def main():
    with open(INPUT, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for budget in BUDGETS:
        out_name = f"carousel_{budget.replace('=', '_')}.csv"
        with open(out_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["CONSUMER_ID", "DAY_PART", "CAROUSEL_RANK", "TITLE", "TAGS"])
            for row in rows:
                cid = row["consumer_id"]
                daypart = row["daypart"]
                rank = row["rank"]
                cell = row[budget]
                if not cell or not cell.strip() or cell.strip().lower() == "null":
                    continue
                title, cuisines = parse_cell(cell)
                tags = json.dumps({"cuisine_type": cuisines, "food_type": []})
                writer.writerow([cid, daypart, rank, title, tags])
        print(f"Wrote {out_name}")


if __name__ == "__main__":
    main()
