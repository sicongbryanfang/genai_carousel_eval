"""
Comprehensive evaluation for sparse_cx prompt variants.

Computes ILD, MMS, SR@K, OHCD, CCR, and composite metrics using:
  - TITLE + CUISINE_FILTER from carousels
  - INFO_FORMATTED (order history) + SUMMARY (engagement) for item embeddings
  - SEARCH_QUERIES_FORMATTED for cuisine tags (CCR)

Usage:
    python carousel_eval/sparse_cx/eval_sparse_cx.py
"""

from __future__ import annotations

import json
import os
import re
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_THETA = 0.45
SR_K_VALUES = (3, 5, 10)

# Composite weights (excluding FCS and TMC — not computable for sparse data).
COMPOSITE_WEIGHTS: Dict[str, float] = {
    "mms": 0.20,
    "sr_at_5": 0.15,
    "ccr": 0.15,
    "ild": 0.10,
    "ohcd": 0.10,
}

SPARSE_DIR = os.path.dirname(__file__)
PROMPT_FILES = [f"Carousel_evals_prompt{i}.csv" for i in range(1, 5)]

METRIC_COLS = [
    "ild", "tcd", "redundancy_rate",
    "mms", "sr_at_3", "sr_at_5", "sr_at_10", "ohcd", "ccr",
    "composite_quality_score",
]

# ---------------------------------------------------------------------------
# Cuisine taxonomy (inlined from local_eval_test.py — fabricator not available)
# ---------------------------------------------------------------------------

CUISINE_TAXONOMY_DICT: Dict[str, List[str]] = {
    "Afghan": ["Asian", "South Asian", "Afghan"],
    "African": ["African"],
    "Afro-Caribbean": ["Latin American", "Central American", "Panamanian", "Afro-Caribbean"],
    "Albanian": ["European", "Eastern European", "Albanian"],
    "Algerian": ["African", "North African", "Algerian"],
    "Amazon Basin": ["Latin American", "Amazon Basin"],
    "American": ["North American", "American"],
    "Anatolia": ["Middle East", "Anatolia"],
    "Andean": ["Latin American", "Andean"],
    "Andorran": ["European", "Western European", "Andorran"],
    "Angolan": ["African", "Central African", "Angolan"],
    "Arabian Peninsula": ["Middle East", "Arabian Peninsula"],
    "Argentinian": ["Latin American", "Platine & Southern", "Argentinian"],
    "Armenian": ["Middle East", "Caucasus", "Armenian"],
    "Asian": ["Asian"],
    "Australian": ["Oceanic", "Australian & New Zealand", "Australian"],
    "Australian & New Zealand": ["Oceanic", "Australian & New Zealand"],
    "Austrian": ["European", "Central European", "Austrian"],
    "Azerbaijani": ["Middle East", "Caucasus", "Azerbaijani"],
    "Bahamas": ["North American", "Caribbean", "Bahamas"],
    "Bahraini": ["Middle East", "Arabian Peninsula", "Bahraini"],
    "Bangladeshi": ["Asian", "South Asian", "Bangladeshi"],
    "Barbados": ["North American", "Caribbean", "Barbados"],
    "Basque": ["European", "Mediterranean", "Spanish", "Basque"],
    "Beijing": ["Asian", "East Asian", "Chinese", "Beijing"],
    "Belarusian": ["European", "Eastern European", "Belarusian"],
    "Belgian": ["European", "Western European", "Belgian"],
    "Belizean": ["Latin American", "Central American", "Belizean"],
    "Bhutanese": ["Asian", "South Asian", "Bhutanese"],
    "Bolivian": ["Latin American", "Andean", "Bolivian"],
    "Brazilian": ["Latin American", "Amazon Basin", "Brazilian"],
    "British": ["European", "Northern European", "British"],
    "Brunei-Malay": ["Asian", "SouthEast Asian", "Bruneian", "Brunei-Malay"],
    "Bruneian": ["Asian", "SouthEast Asian", "Bruneian"],
    "Bulgarian": ["European", "Eastern European", "Bulgarian"],
    "Burmese": ["Asian", "SouthEast Asian", "Burmese"],
    "Cajun": ["North American", "American", "Cajun"],
    "Cambodian": ["Asian", "SouthEast Asian", "Cambodian"],
    "Cameroonian": ["African", "Central African", "Cameroonian"],
    "Canada": ["North American", "Canada"],
    "Canadian": ["North American", "Canadian"],
    "Canadian Fusion": ["North American", "Canadian", "Canadian Fusion"],
    "Cantonese": ["Asian", "East Asian", "Chinese", "Cantonese"],
    "Cape-Malay": ["African", "South African", "Cape-Malay"],
    "Caribbean": ["Latin American", "Caribbean"],
    "Caucasus": ["Middle East", "Caucasus"],
    "Central African": ["African", "Central African"],
    "Central America": ["Latin American", "Central America"],
    "Central American": ["Latin American", "Central American"],
    "Central Asian": ["Asian", "Central Asian"],
    "Central European": ["European", "Central European"],
    "Chilean": ["Latin American", "Andean", "Chilean"],
    "Chinese": ["Asian", "East Asian", "Chinese"],
    "Colombian": ["Latin American", "Andean", "Colombian"],
    "Costa Rican": ["Latin American", "Central American", "Costa Rican"],
    "Creole": ["Latin American", "Central American", "Belizean", "Creole"],
    "Cuban": ["North American", "Caribbean", "Cuban"],
    "Czech": ["European", "Central European", "Czech"],
    "Danish": ["European", "Northern European", "Danish"],
    "Diasporan": ["Global", "Diasporan"],
    "Dominican": ["North American", "Caribbean", "Dominican"],
    "Dutch": ["European", "Western European", "Dutch"],
    "Dutch Caribbean": ["North American", "Caribbean", "Dutch Caribbean"],
    "East African": ["African", "East African"],
    "East Asian": ["Asian", "East Asian"],
    "Eastern European": ["European", "Eastern European"],
    "Ecuadorian": ["Latin American", "Andean", "Ecuadorian"],
    "Egyptian": ["African", "North African", "Egyptian"],
    "El Salvadoran": ["Latin American", "Central American", "El Salvadoran"],
    "Emirati (UAE)": ["Middle East", "Arabian Peninsula", "Emirati (UAE)"],
    "Eritrean": ["African", "East African", "Eritrean"],
    "Estonian": ["European", "Eastern European", "Estonian"],
    "Ethiopian": ["African", "East African", "Ethiopian"],
    "European": ["European"],
    "Filipino": ["Asian", "SouthEast Asian", "Filipino"],
    "Finnish": ["European", "Northern European", "Finnish"],
    "French": ["European", "Mediterranean", "French"],
    "French Caribbean": ["North American", "Caribbean", "French Caribbean"],
    "French Guianese": ["Latin American", "Guianas", "French Guianese"],
    "Georgian": ["Middle East", "Caucasus", "Georgian"],
    "German": ["European", "Central European", "German"],
    "Ghanaian": ["African", "West African", "Ghanaian"],
    "Global": ["Global"],
    "Greek": ["European", "Mediterranean", "Greek"],
    "Guatemalan": ["Latin American", "Central America", "Guatemalan"],
    "Guianas": ["Latin American", "Guianas"],
    "Guyanese": ["Latin American", "Guianas", "Guyanese"],
    "Haitian": ["North American", "Caribbean", "Haitian"],
    "Hakka": ["Asian", "East Asian", "Taiwanese", "Hakka"],
    "Hawaiian": ["North American", "American", "Hawaiian"],
    "Honduran": ["Latin American", "Central American", "Honduran"],
    "Hong Kongese": ["Asian", "East Asian", "Chinese", "Hong Kongese"],
    "Hungarian": ["European", "Central European", "Hungarian"],
    "Icelandic": ["European", "Northern European", "Icelandic"],
    "Indian": ["Asian", "South Asian", "Indian"],
    "Indonesian": ["Asian", "SouthEast Asian", "Indonesian"],
    "Iranian": ["Middle East", "Persian Gulf", "Iranian"],
    "Iraqi": ["Middle East", "Persian Gulf", "Iraqi"],
    "Irish": ["European", "Northern European", "Irish"],
    "Israeli": ["Middle East", "Levant", "Israeli"],
    "Italian": ["European", "Mediterranean", "Italian"],
    "Jain": ["Asian", "South Asian", "Indian", "Jain"],
    "Jamaican": ["North American", "Caribbean", "Jamaican"],
    "Japanese": ["Asian", "East Asian", "Japanese"],
    "Jewish": ["Global", "Diasporan", "Jewish"],
    "Jordanian": ["Middle East", "Levant", "Jordanian"],
    "Kenyan": ["African", "East African", "Kenyan"],
    "Korean": ["Asian", "East Asian", "Korean"],
    "Kuwaiti": ["Middle East", "Arabian Peninsula", "Kuwaiti"],
    "Laotian": ["Asian", "SouthEast Asian", "Laotian"],
    "Latin American": ["Latin American"],
    "Latvian": ["European", "Eastern European", "Latvian"],
    "Lebanese": ["Middle East", "Levant", "Lebanese"],
    "Levant": ["Middle East", "Levant"],
    "Libyan": ["African", "North African", "Libyan"],
    "Lithuanian": ["European", "Eastern European", "Lithuanian"],
    "Malaysian": ["Asian", "SouthEast Asian", "Malaysian"],
    "Maldivian": ["Asian", "South Asian", "Maldivian"],
    "Mediterranean": ["European", "Mediterranean"],
    "Melanesian Islands": ["Oceanic", "Oceanic Islands", "Melanesian Islands"],
    "Mexican": ["Latin American", "North American", "Mexican"],
    "Micronesian Islands": ["Oceanic", "Oceanic Islands", "Micronesian Islands"],
    "Middle East": ["Middle East"],
    "Moldovan": ["European", "Eastern European", "Moldovan"],
    "Monacan": ["European", "Western European", "Monacan"],
    "Mongolian": ["Asian", "East Asian", "Mongolian"],
    "Moroccan": ["African", "North African", "Moroccan"],
    "Mozambican": ["African", "East African", "Mozambican"],
    "Mughlai": ["Asian", "South Asian", "Pakistani", "Mughlai"],
    "Namibian": ["African", "Southern African", "Namibian"],
    "Native American": ["North American", "Native American"],
    "Neapolitan": ["European", "Mediterranean", "Italian", "Neapolitan"],
    "Nepalese": ["Asian", "South Asian", "Nepalese"],
    "New American": ["North American", "American", "New American"],
    "New Zealand": ["Oceanic", "Australian & New Zealand", "New Zealand"],
    "Nicaraguan": ["Latin American", "Central American", "Nicaraguan"],
    "Nigerian": ["African", "West African", "Nigerian"],
    "North African": ["African", "North African"],
    "North American": ["Latin American", "North American"],
    "North Indian": ["Asian", "South Asian", "Indian", "North Indian"],
    "Northern European": ["European", "Northern European"],
    "Norwegian": ["European", "Northern European", "Norwegian"],
    "Oceanic": ["Oceanic"],
    "Oceanic Islands": ["Oceanic", "Oceanic Islands"],
    "Omani": ["Middle East", "Arabian Peninsula", "Omani"],
    "Pakistani": ["Asian", "South Asian", "Pakistani"],
    "Panamanian": ["Latin American", "Central American", "Panamanian"],
    "Paraguayan": ["Latin American", "Platine & Southern", "Paraguayan"],
    "Persian": ["Middle East", "Persian Gulf", "Persian"],
    "Persian Gulf": ["Middle East", "Persian Gulf"],
    "Peruvian": ["Latin American", "Andean", "Peruvian"],
    "Platine & Southern": ["Latin American", "Platine & Southern"],
    "Polish": ["European", "Central European", "Polish"],
    "Polynesian Islands": ["Oceanic", "Oceanic Islands", "Polynesian Islands"],
    "Portuguese": ["European", "Mediterranean", "Portuguese"],
    "Puerto Rican": ["North American", "Caribbean", "Puerto Rican"],
    "Qatari": ["Middle East", "Arabian Peninsula", "Qatari"],
    "Québécois": ["North American", "Canadian", "Québécois"],
    "Romanian": ["European", "Eastern European", "Romanian"],
    "Russian": ["European", "Eastern European", "Russian"],
    "Rwandan": ["African", "East African", "Rwandan"],
    "Saudi Arabian": ["Middle East", "Arabian Peninsula", "Saudi Arabian"],
    "Scotish": ["European", "Northern European", "British", "Scotish"],
    "Senegalese": ["African", "West African", "Senegalese"],
    "Serbian": ["European", "Eastern European", "Serbian"],
    "Shanghainese": ["Asian", "East Asian", "Chinese", "Shanghainese"],
    "Sichuan": ["Asian", "East Asian", "Chinese", "Sichuan"],
    "Sicilian": ["European", "Mediterranean", "Italian", "Sicilian"],
    "Singaporean": ["Asian", "SouthEast Asian", "Singaporean"],
    "Slovak": ["European", "Central European", "Slovak"],
    "Slovenian": ["European", "Central European", "Slovenian"],
    "Somali": ["African", "East African", "Somali"],
    "Soul Food": ["North American", "American", "Soul Food"],
    "South African": ["African", "South African"],
    "South Asian": ["Asian", "South Asian"],
    "South Indian": ["Asian", "South Asian", "Indian", "South Indian"],
    "SouthEast Asian": ["Asian", "SouthEast Asian"],
    "Southern African": ["African", "Southern African"],
    "Southern American": ["North American", "American", "Southern American"],
    "Southwestern": ["North American", "American", "Southwestern"],
    "Spanish": ["European", "Mediterranean", "Spanish"],
    "Sri Lankan": ["Asian", "South Asian", "Sri Lankan"],
    "Sudanese": ["African", "North African", "Sudanese"],
    "Surinamese": ["Latin American", "Guianas", "Surinamese"],
    "Swedish": ["European", "Northern European", "Swedish"],
    "Swiss": ["European", "Central European", "Swiss"],
    "Syrian": ["Middle East", "Levant", "Syrian"],
    "Taiwanese": ["Asian", "East Asian", "Taiwanese"],
    "Tex-Mex": ["North American", "American", "Tex-Mex"],
    "Thai": ["Asian", "SouthEast Asian", "Thai"],
    "Tibetan": ["Asian", "Central Asian", "Tibetan"],
    "Trindadian": ["North American", "Caribbean", "Trindadian"],
    "Tunisian": ["African", "North African", "Tunisian"],
    "Turkish": ["Middle East", "Anatolia", "Turkish"],
    "Ugandan": ["African", "East African", "Ugandan"],
    "Ukrainian": ["European", "Eastern European", "Ukrainian"],
    "Uruguayan": ["Latin American", "Platine & Southern", "Uruguayan"],
    "Uyghur": ["Asian", "Central Asian", "Uyghur"],
    "Uzbek": ["Asian", "Central Asian", "Uzbek"],
    "Venezuelan": ["Latin American", "Caribbean", "Venezuelan"],
    "Vietnamese": ["Asian", "SouthEast Asian", "Vietnamese"],
    "West African": ["African", "West African"],
    "Western European": ["European", "Western European"],
    "Yemeni": ["Middle East", "Arabian Peninsula", "Yemeni"],
    "Zambian": ["African", "East African", "Zambian"],
}

# Map cuisine_filter underscore tags to taxonomy keys.
CUISINE_FILTER_TO_TAXONOMY: Dict[str, str] = {
    "american": "American",
    "arabian_peninsula": "Arabian Peninsula",
    "australian_new_zealand": "Australian & New Zealand",
    "canadian": "Canadian",
    "caribbean": "Caribbean",
    "caucasus": "Caucasus",
    "central_american": "Central American",
    "central_asian": "Central Asian",
    "central_european": "Central European",
    "east_asian": "East Asian",
    "eastern_european": "Eastern European",
    "levant": "Levant",
    "mediterranean": "Mediterranean",
    "mexican": "Mexican",
    "north_african": "North African",
    "northern_european": "Northern European",
    "oceanic_islands": "Oceanic Islands",
    "persian_gulf": "Persian Gulf",
    "south_american": "Latin American",
    "south_asian": "South Asian",
    "southeast_asian": "SouthEast Asian",
    "southern_american": "Southern American",
    "turkish": "Turkish",
    "western_european": "Western European",
    "western_ european": "Western European",  # typo in data
}


def _top_level(tag: str) -> str:
    """Return the top-level cuisine family for *tag*, or *tag* itself."""
    path = CUISINE_TAXONOMY_DICT.get(tag)
    return path[0] if path else tag


def _cuisine_filter_to_top_level(tag: str) -> Optional[str]:
    """Map a cuisine_filter value (e.g. 'east_asian') to its top-level family."""
    if tag == "unknown":
        return None
    taxonomy_key = CUISINE_FILTER_TO_TAXONOMY.get(tag)
    if taxonomy_key is None:
        return None
    return _top_level(taxonomy_key)


# ---------------------------------------------------------------------------
# Metric functions (inlined from metrics.py — fabricator import not available)
# ---------------------------------------------------------------------------

def intra_list_diversity(carousel_embs: np.ndarray) -> Optional[float]:
    k = len(carousel_embs)
    if k < 2:
        return None
    sim = carousel_embs @ carousel_embs.T
    i, j = np.triu_indices(k, k=1)
    return float(1.0 - sim[i, j].mean())


DEFAULT_TCD_THRESHOLD = 0.65
DEFAULT_RR_THRESHOLD = 0.75


def title_cluster_diversity(
    carousel_embs: np.ndarray,
    threshold: float = DEFAULT_TCD_THRESHOLD,
) -> Optional[float]:
    """TCD = n_connected_components / n_titles (higher = more diverse)."""
    k = len(carousel_embs)
    if k < 2:
        return None
    sim = carousel_embs @ carousel_embs.T
    adj: Dict[int, List[int]] = {i: [] for i in range(k)}
    rows, cols = np.triu_indices(k, k=1)
    for r, c in zip(rows, cols):
        if sim[r, c] >= threshold:
            adj[r].append(c)
            adj[c].append(r)
    visited = [False] * k
    n_components = 0
    for start in range(k):
        if visited[start]:
            continue
        n_components += 1
        queue = [start]
        visited[start] = True
        while queue:
            node = queue.pop(0)
            for nb in adj[node]:
                if not visited[nb]:
                    visited[nb] = True
                    queue.append(nb)
    return float(n_components / k)


def redundancy_rate(
    carousel_embs: np.ndarray,
    threshold: float = DEFAULT_RR_THRESHOLD,
) -> Optional[float]:
    """RR = n_redundant_pairs / total_pairs (lower = better, 0 = no redundancy)."""
    k = len(carousel_embs)
    if k < 2:
        return None
    sim = carousel_embs @ carousel_embs.T
    i, j = np.triu_indices(k, k=1)
    total_pairs = len(i)
    n_redundant = int((sim[i, j] >= threshold).sum())
    return float(n_redundant / total_pairs)


def similarity_matrix(item_embs: np.ndarray, carousel_embs: np.ndarray) -> np.ndarray:
    return item_embs @ carousel_embs.T


def mean_max_similarity(sim: np.ndarray) -> float:
    return float(sim.max(axis=1).mean())


def semantic_recall_at_k(sim: np.ndarray, k: int, theta: float = DEFAULT_THETA) -> float:
    k_actual = min(k, sim.shape[1])
    top_k_sim = sim[:, :k_actual]
    return float((top_k_sim.max(axis=1) >= theta).mean())


def order_history_coverage_diversity(sim: np.ndarray) -> float:
    assignment = sim.argmax(axis=1)
    return float(len(set(assignment.tolist())) / sim.shape[1])


def cuisine_coverage_recall(
    carousel_cuisines: List[Optional[List[str]]],
    order_cuisine_tags: List[str],
) -> Optional[float]:
    gt_raw = [c for c in order_cuisine_tags if c]
    if not gt_raw:
        return None
    gt_families = {_top_level(c) for c in gt_raw}
    pred_raw = [c for row in carousel_cuisines for c in (row or [])]
    pred_families = {_top_level(c) for c in pred_raw}
    return float(len(gt_families & pred_families) / len(gt_families))


def composite_score(metric_values: Dict[str, Optional[float]]) -> Optional[float]:
    available = {
        k: v for k, v in metric_values.items()
        if k in COMPOSITE_WEIGHTS and v is not None
    }
    if not available:
        return None
    total_weight = sum(COMPOSITE_WEIGHTS[k] for k in available)
    return float(sum(COMPOSITE_WEIGHTS[k] * available[k] for k in available) / total_weight)


# ---------------------------------------------------------------------------
# Parsers for text-format consumer data
# ---------------------------------------------------------------------------

_ORDER_LINE_RE = re.compile(
    r"\[([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^\]]+?)\]"
    r"(?:\s*\{[^}]*\})?"       # optional customizations
    r"\s*\((\d+)\)"            # count
)

_DAYPART_HEADER_RE = re.compile(r"^(weekday_\w+|weekend_\w+):")

_SUMMARY_ITEM_RE = re.compile(r"^\s*(.+?)\s*\|\s*(.+)\s+\((\d+)\)\s*$")

_SEARCH_FREQ_RE = re.compile(r"^(.+)\((\d+)\)\s*$")


def _info_daypart_to_csv(header: str) -> str:
    """Convert 'breakfast (weekday)' → 'weekday_breakfast'."""
    m = re.match(r"(\w+(?:_\w+)?)\s*\((\w+)\)", header.strip())
    if m:
        meal, day = m.group(1), m.group(2)
        return f"{day}_{meal}"
    return header.strip()


def parse_info_formatted(text: str) -> Dict[str, List[str]]:
    """Parse INFO_FORMATTED → {daypart: [item_name, ...]}."""
    if not text or text == "nan" or pd.isna(text):
        return {}
    sections = re.split(r"\n(?=\w+(?:_\w+)?\s*\([^)]+\)\s*:)", str(text).strip())
    result: Dict[str, List[str]] = {}
    for section in sections:
        lines = section.strip().split("\n")
        header = lines[0].strip().rstrip(":")
        daypart = _info_daypart_to_csv(header)
        items = _ORDER_LINE_RE.findall(section)
        item_names = []
        for _, item_name, _, _ in items:
            name = item_name.strip()
            if name:
                item_names.append(name)
        if item_names:
            result[daypart] = list(dict.fromkeys(item_names))  # deduplicate, keep order
    return result


def parse_summary(text: str) -> Dict[str, List[str]]:
    """Parse SUMMARY → {daypart: [item_name, ...]}."""
    if not text or text == "nan" or pd.isna(text):
        return {}
    result: Dict[str, List[str]] = {}
    current_daypart = None
    for line in str(text).split("\n"):
        stripped = line.rstrip()
        if not stripped:
            continue
        lower = stripped.lower()
        if "add-to-cart" in lower or "page-visit" in lower or "item_detail_views" in lower:
            continue
        dp_match = _DAYPART_HEADER_RE.match(stripped)
        if dp_match:
            current_daypart = dp_match.group(1)
            rest = stripped[dp_match.end():].strip()
            m = _SUMMARY_ITEM_RE.match(rest)
            if m:
                item = m.group(2).strip()
                if item:
                    result.setdefault(current_daypart, []).append(item)
        else:
            m = _SUMMARY_ITEM_RE.match(stripped)
            if m and current_daypart:
                item = m.group(2).strip()
                if item:
                    result.setdefault(current_daypart, []).append(item)
    # Deduplicate per daypart
    return {dp: list(dict.fromkeys(items)) for dp, items in result.items()}


def parse_search_cuisines(text: str) -> Dict[str, List[str]]:
    """Parse SEARCH_QUERIES_FORMATTED → {daypart: [cuisine_tag, ...]}."""
    if not text or text == "nan" or pd.isna(text):
        return {}
    result: Dict[str, List[str]] = {}
    current_daypart = None
    for line in str(text).split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        dp_match = _DAYPART_HEADER_RE.match(stripped)
        if dp_match:
            current_daypart = dp_match.group(1)
            continue
        if current_daypart is None:
            continue
        freq_match = _SEARCH_FREQ_RE.match(stripped)
        if not freq_match:
            continue
        content = freq_match.group(1).strip()
        parts = [p.strip() for p in content.split("|")]
        if len(parts) >= 4:
            cuisine_str = parts[-1]
            cuisines = [c.strip() for c in cuisine_str.split(",") if c.strip()]
            result.setdefault(current_daypart, []).extend(cuisines)
    # Deduplicate per daypart
    return {dp: list(dict.fromkeys(tags)) for dp, tags in result.items()}


# ---------------------------------------------------------------------------
# Data loading & embedding
# ---------------------------------------------------------------------------

def _explode_carousels_json(df: pd.DataFrame) -> pd.DataFrame:
    """Explode CAROUSELS JSON column into one row per (consumer, daypart, rank)."""
    rows = []
    for _, row in df.iterrows():
        try:
            carousels = json.loads(row["carousels"])
        except (json.JSONDecodeError, TypeError):
            continue
        for daypart, items in carousels.items():
            if isinstance(items, dict) and "carousels" in items:
                items = items["carousels"]
            if not isinstance(items, list):
                continue
            for rank, item in enumerate(items, 1):
                if not isinstance(item, dict):
                    continue
                new_row = {
                    "consumer_id": row["consumer_id"],
                    "day_part": daypart,
                    "carousel_rank": rank,
                    "title": item.get("title"),
                    "cuisine_filter": json.dumps(item.get("cuisine_filter", [])),
                }
                # Carry over shared columns
                for col in ("info_formatted", "search_queries_formatted",
                            "sparsity", "summary"):
                    if col in row.index:
                        new_row[col] = row[col]
                rows.append(new_row)
    return pd.DataFrame(rows)


def load_and_normalize(path: str) -> pd.DataFrame:
    """Load sparse_cx CSV, normalize columns, parse CUISINE_FILTER.

    Handles two formats:
      - Pre-exploded (has DAYPART, RANK, TITLE, CUISINE_FILTER columns)
      - Raw JSON (only CAROUSELS column, needs exploding)
    """
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    if "daypart" not in df.columns and "day_part" not in df.columns:
        # Raw JSON format — explode CAROUSELS
        df = _explode_carousels_json(df)
    else:
        df = df.rename(columns={"daypart": "day_part", "rank": "carousel_rank"})

    def _parse_cuisine_filter(raw):
        if pd.isna(raw):
            return []
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return parsed
            return []
        except (json.JSONDecodeError, TypeError):
            return []

    df["cuisine_filter_list"] = df["cuisine_filter"].apply(_parse_cuisine_filter)
    return df


def build_order_data(df: pd.DataFrame) -> Tuple[
    Dict[int, Dict[str, List[str]]],  # items: consumer → daypart → [item_names]
    Dict[int, Dict[str, List[str]]],  # cuisines: consumer → daypart → [cuisine_tags]
]:
    """Parse all consumer data sources into structured dicts (shared across prompts)."""
    item_data: Dict[int, Dict[str, List[str]]] = {}
    cuisine_data: Dict[int, Dict[str, List[str]]] = {}

    for cid in df["consumer_id"].unique():
        row = df[df["consumer_id"] == cid].iloc[0]

        # Combine INFO_FORMATTED + SUMMARY for item names
        info_items = parse_info_formatted(row.get("info_formatted"))
        summary_items = parse_summary(row.get("summary"))

        merged: Dict[str, List[str]] = {}
        all_dayparts = set(info_items.keys()) | set(summary_items.keys())
        for dp in all_dayparts:
            names = list(dict.fromkeys(
                info_items.get(dp, []) + summary_items.get(dp, [])
            ))
            if names:
                merged[dp] = names

        if merged:
            item_data[cid] = merged

        # Cuisine tags from SEARCH_QUERIES_FORMATTED
        search_cuisines = parse_search_cuisines(row.get("search_queries_formatted"))
        if search_cuisines:
            cuisine_data[cid] = search_cuisines

    return item_data, cuisine_data


def build_order_data_from_csv(orders_csv: str) -> Tuple[
    Dict[int, Dict[str, List[str]]],  # items: consumer → daypart → [item_names]
    Dict[int, Dict[str, List[str]]],  # cuisines: consumer → daypart → [cuisine_tags]
]:
    """Build order data from a Snowflake-exported orders CSV (sparse_orders.csv).

    Uses ITEM_NAME for item embeddings and CUISINE_TAGS_FROM_MENU for CCR.
    """
    df = pd.read_csv(orders_csv)
    df.columns = [c.strip().lower() for c in df.columns]

    item_data: Dict[int, Dict[str, List[str]]] = {}
    cuisine_data: Dict[int, Dict[str, List[str]]] = {}

    for (cid, dp), grp in df.groupby(["consumer_id", "day_part"]):
        # Item names (drop nulls and non-food items flagged as CNG)
        items = grp[grp["is_cng"] == 0]["item_name"].dropna().unique().tolist()
        if items:
            item_data.setdefault(cid, {})[dp] = items

        # Cuisine tags from menu (comma-separated, e.g. "Asian, Chinese")
        raw_tags = grp[grp["is_cng"] == 0]["cuisine_tags_from_menu"].dropna().tolist()
        tags: List[str] = []
        for t in raw_tags:
            for c in str(t).split(","):
                c = c.strip()
                if c:
                    tags.append(c)
        if tags:
            cuisine_data.setdefault(cid, {})[dp] = list(dict.fromkeys(tags))

    return item_data, cuisine_data


def embed_texts(model, texts: List[str]) -> np.ndarray:
    """Encode texts with the sentence-transformer model, unit-normalised."""
    return model.encode(
        texts, batch_size=512, normalize_embeddings=True, show_progress_bar=True,
    )


# ---------------------------------------------------------------------------
# Per-group metric computation
# ---------------------------------------------------------------------------

def compute_group_metrics(
    title_embs: np.ndarray,
    carousel_ranks: List[int],
    cuisine_filter_lists: List[List[str]],
    item_embs: Optional[np.ndarray],
    order_cuisine_tags: Optional[List[str]],
    theta: float = DEFAULT_THETA,
) -> Dict[str, Optional[float]]:
    """Compute all metrics for one (consumer_id, day_part) group."""
    results: Dict[str, Optional[float]] = {}

    # Sort by rank
    order = sorted(range(len(carousel_ranks)), key=lambda i: carousel_ranks[i])
    t_embs = title_embs[order]
    cuisine_lists_ord = [cuisine_filter_lists[i] for i in order]

    # ILD
    results["ild"] = intra_list_diversity(t_embs)

    # TCD (Title Cluster Diversity)
    results["tcd"] = title_cluster_diversity(t_embs)

    # Redundancy Rate
    results["redundancy_rate"] = redundancy_rate(t_embs)

    # Map carousel cuisine_filter to taxonomy keys for CCR
    carousel_cuisine_mapped: List[Optional[List[str]]] = []
    for cf_list in cuisine_lists_ord:
        mapped = []
        for tag in cf_list:
            taxonomy_key = CUISINE_FILTER_TO_TAXONOMY.get(tag)
            if taxonomy_key:
                mapped.append(taxonomy_key)
        carousel_cuisine_mapped.append(mapped if mapped else None)

    # CCR
    if order_cuisine_tags:
        results["ccr"] = cuisine_coverage_recall(carousel_cuisine_mapped, order_cuisine_tags)
    else:
        results["ccr"] = None

    # Similarity-based metrics (MMS, SR@K, OHCD)
    if item_embs is not None and len(item_embs) > 0 and len(t_embs) >= 2:
        sim = similarity_matrix(item_embs, t_embs)
        results["mms"] = mean_max_similarity(sim)
        for k in SR_K_VALUES:
            results[f"sr_at_{k}"] = semantic_recall_at_k(sim, k, theta)
        results["ohcd"] = order_history_coverage_diversity(sim)
    else:
        results["mms"] = None
        for k in SR_K_VALUES:
            results[f"sr_at_{k}"] = None
        results["ohcd"] = None

    results["composite_quality_score"] = composite_score(results)
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    from sentence_transformers import SentenceTransformer

    print(f"[model] Loading {EMBEDDING_MODEL_NAME} ...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # --- Load order history from Snowflake-exported CSV ---
    orders_csv = os.path.join(SPARSE_DIR, "sparse_orders.csv")
    print(f"\n[data] Loading order history from: {orders_csv}")
    item_data, cuisine_data = build_order_data_from_csv(orders_csv)

    print(f"  Consumers with item data: {len(item_data)}")
    print(f"  Consumers with cuisine data: {len(cuisine_data)}")

    # Embed all unique order item names
    all_item_names: Set[str] = set()
    for consumer_items in item_data.values():
        for names in consumer_items.values():
            all_item_names.update(names)

    print(f"\n[embed] Encoding {len(all_item_names)} unique order item names ...")
    item_name_list = sorted(all_item_names)
    if item_name_list:
        item_embs_array = embed_texts(model, item_name_list)
        item_emb_map = dict(zip(item_name_list, item_embs_array))
    else:
        item_emb_map = {}

    # --- Evaluate each prompt ---
    all_summaries = []

    for fname in PROMPT_FILES:
        path = os.path.join(SPARSE_DIR, fname)
        prompt_name = fname.replace("Carousel_evals_", "").replace(".csv", "")
        print(f"\n{'='*60}")
        print(f"  {prompt_name}")
        print(f"{'='*60}")

        df = load_and_normalize(path)
        print(f"  Rows: {len(df):,}, Consumers: {df['consumer_id'].nunique()}, "
              f"Dayparts: {df['day_part'].nunique()}")

        # Embed unique titles for this prompt
        unique_titles = df["title"].dropna().unique().tolist()
        print(f"  [embed] Encoding {len(unique_titles)} unique titles ...")
        title_embs_array = embed_texts(model, unique_titles)
        title_emb_map = dict(zip(unique_titles, title_embs_array))

        # Compute metrics per (consumer_id, day_part) group
        results: List[dict] = []
        groups = df.groupby(["consumer_id", "day_part"])
        total = len(groups)

        for idx, ((cid, dp), grp) in enumerate(groups, 1):
            # Title embeddings
            titles = grp["title"].tolist()
            t_embs_list = []
            for t in titles:
                if pd.notna(t) and t in title_emb_map:
                    t_embs_list.append(title_emb_map[t])
            if len(t_embs_list) < 2:
                continue
            t_embs = np.stack(t_embs_list)

            # Item embeddings for this consumer+daypart
            consumer_items = item_data.get(cid, {})
            dp_items = consumer_items.get(dp, [])
            i_embs = None
            if dp_items:
                valid_embs = [item_emb_map[n] for n in dp_items if n in item_emb_map]
                if valid_embs:
                    i_embs = np.stack(valid_embs)

            # Cuisine tags for this consumer+daypart
            consumer_cuisines = cuisine_data.get(cid, {})
            dp_cuisines = consumer_cuisines.get(dp, [])

            metrics = compute_group_metrics(
                title_embs=t_embs,
                carousel_ranks=grp["carousel_rank"].tolist(),
                cuisine_filter_lists=grp["cuisine_filter_list"].tolist(),
                item_embs=i_embs,
                order_cuisine_tags=dp_cuisines if dp_cuisines else None,
                theta=DEFAULT_THETA,
            )

            sparsity = grp["sparsity"].iloc[0] if "sparsity" in grp.columns else ""
            row = {
                "consumer_id": cid,
                "day_part": dp,
                "sparsity": sparsity,
                "n_carousels": len(grp),
                "n_order_items": len(dp_items),
            }
            row.update(metrics)
            results.append(row)

            if idx % 500 == 0 or idx == total:
                print(f"  [{prompt_name}] {idx}/{total} groups processed")

        metrics_df = pd.DataFrame(results)

        # Report
        print(f"\n  Overall Metrics (mean +/- std):")
        for col in METRIC_COLS:
            if col in metrics_df.columns:
                vals = metrics_df[col].dropna()
                if len(vals) > 0:
                    print(f"    {col:<28s} {vals.mean():.4f} +/- {vals.std():.4f}  (n={len(vals)})")

        # Per-daypart breakdown
        summary_cols = ["ild", "mms", "sr_at_5", "ccr", "composite_quality_score"]
        header_line = f"  {'daypart':<24s} | {'count':>5s}"
        for c in summary_cols:
            header_line += f" | {c:>12s}"
        print(f"\n  Breakdown by Daypart:\n{header_line}")
        print("  " + "-" * (len(header_line) - 2))

        for dp in sorted(metrics_df["day_part"].unique()):
            grp = metrics_df[metrics_df["day_part"] == dp]
            line = f"  {dp:<24s} | {len(grp):>5d}"
            for c in summary_cols:
                if c in grp.columns:
                    vals = grp[c].dropna()
                    line += f" | {vals.mean():>12.4f}" if len(vals) > 0 else f" | {'N/A':>12s}"
                else:
                    line += f" | {'N/A':>12s}"
            print(line)

        # Save per-prompt results
        out_path = os.path.join(SPARSE_DIR, f"metrics_{prompt_name}.csv")
        metrics_df.to_csv(out_path, index=False)
        print(f"\n  Saved {out_path}")

        # Collect summary for comparison
        summary = {"prompt": prompt_name}
        summary["n_consumers"] = metrics_df["consumer_id"].nunique()
        summary["n_groups"] = len(metrics_df)
        summary["n_groups_with_orders"] = int(metrics_df["n_order_items"].gt(0).sum())
        for col in METRIC_COLS:
            if col in metrics_df.columns:
                vals = metrics_df[col].dropna()
                summary[f"{col}_mean"] = vals.mean() if len(vals) > 0 else None
                summary[f"{col}_std"] = vals.std() if len(vals) > 0 else None
        all_summaries.append(summary)

    # --- Comparison table ---
    summary_df = pd.DataFrame(all_summaries)
    print(f"\n{'='*60}")
    print("  Metrics Comparison Across Prompts")
    print(f"{'='*60}")
    print(summary_df.to_string(index=False))

    comparison_path = os.path.join(SPARSE_DIR, "metrics_comparison.csv")
    summary_df.to_csv(comparison_path, index=False)
    print(f"\n[done] Saved {comparison_path}")


if __name__ == "__main__":
    main()
