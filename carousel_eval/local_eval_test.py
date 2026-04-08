"""
Self-contained local carousel quality evaluation script.

Compares two carousel sources — EBR and Search-Title-Fallback — using
order-history as ground truth.  Produces per-daypart metric reports for
each source, restricted to consumer IDs present in both tables.

Dependencies (pip install):
    numpy pandas snowflake-connector-python sentence-transformers

Usage
-----
# 1. PREPARE: embed orders once + find common consumers across two carousel sources
python local_eval_test.py --prepare \
    --carousel_csv prod_carousels.csv \
    --carousel_csv_2 retrieved_carousel.csv \
    --order_history_csv orders.csv \
    --output_dir .
# Outputs: orders_embedded.pkl, common_consumers.csv

# 2. EVAL with pre-computed artifacts (sample 1000 consumers):
python local_eval_test.py --carousel_csv prod_carousels.csv \
    --orders_embedded_pkl ./orders_embedded.pkl \
    --common_consumers_csv ./common_consumers.csv \
    --source_name prod --sample_limit 1000 --output_dir .

python local_eval_test.py --carousel_csv retrieved_carousel.csv \
    --orders_embedded_pkl ./orders_embedded.pkl \
    --common_consumers_csv ./common_consumers.csv \
    --source_name retrieved --sample_limit 1000 --output_dir .

# 3. EVAL all consumers (omit --sample_limit):
python local_eval_test.py --carousel_csv prod_carousels.csv \
    --orders_embedded_pkl ./orders_embedded.pkl \
    --common_consumers_csv ./common_consumers.csv \
    --source_name prod --output_dir .

# Legacy: single CSV eval (embeds orders on the fly):
python local_eval_test.py --order_history_csv orders.csv --carousel_csv carousels.csv

# Legacy: dual-source Snowflake mode:
python local_eval_test.py --embed_mode title_only --sample_limit 100

Environment variables (for Snowflake queries):
    SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD,
    SNOWFLAKE_WAREHOUSE (default COMPUTE_WH), SNOWFLAKE_ROLE
"""

from __future__ import annotations

import argparse
import json
import os
import pickle
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# ============================================================================
# CUISINE TAXONOMY (inlined from constants.py — needed for CCR metric)
# ============================================================================

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

# ============================================================================
# METRIC CONSTANTS & HELPERS (inlined from metrics.py)
# ============================================================================

ADJECTIVE_BLOCKLIST = frozenset(
    {"fresh", "delicious", "tasty", "amazing", "great", "awesome", "yummy"}
)
ALCOHOL_TOKENS = frozenset(
    {"beer", "wine", "cocktail", "whiskey", "bourbon", "spirits", "vodka", "sake", "liquor", "cider"}
)
CUISINE_TOP_LEVEL: Dict[str, str] = {
    tag: path[0] for tag, path in CUISINE_TAXONOMY_DICT.items()
}

DEFAULT_THETA = 0.45
SR_K_VALUES = (3, 5, 10)

COMPOSITE_WEIGHTS: Dict[str, float] = {
    "mms": 0.20,
    "sr_at_5": 0.15,
    "ccr": 0.15,
    "ild": 0.10,
    "ohcd": 0.10,
    "tmc": 0.15,
    "fcs": 0.15,
}


def _top_level(tag: str) -> str:
    path = CUISINE_TAXONOMY_DICT.get(tag)
    return path[0] if path else tag


def _to_unit_array(arr: Optional[List[float]]) -> Optional[np.ndarray]:
    if arr is None:
        return None
    v = np.asarray(arr, dtype=np.float32)
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


# ============================================================================
# METRICS (inlined from metrics.py — pure NumPy, no Spark)
# ============================================================================


def format_compliance_score(
    title: Optional[str],
    food_type: Optional[List[str]],
    cuisine_type: Optional[List[str]],
) -> float:
    title = title or ""
    food_type = list(food_type or [])
    cuisine_type = list(cuisine_type or [])
    words = title.split()

    def sentence_case_ok() -> bool:
        if not words:
            return False
        if not words[0][0].isupper():
            return False
        return all(w.islower() for w in words[1:] if w.isalpha())

    checks = [
        len(words) <= 5,
        sentence_case_ok(),
        (words[0].lower() not in ADJECTIVE_BLOCKLIST) if words else True,
        not any(tok in ALCOHOL_TOKENS for tok in title.lower().split()),
        5 <= len(food_type) <= 15,
        all(2 <= len(tok.split()) <= 3 for tok in food_type),
        len(cuisine_type) <= 3,
    ]
    return sum(checks) / len(checks)


def avg_format_compliance(
    titles: List[Optional[str]],
    food_types: List[Optional[List[str]]],
    cuisine_types: List[Optional[List[str]]],
) -> Optional[float]:
    if not titles:
        return None
    scores = [
        format_compliance_score(t, ft, ct)
        for t, ft, ct in zip(titles, food_types, cuisine_types)
    ]
    return float(np.mean(scores))


def cuisine_coverage_recall(
    carousel_cuisines: List[Optional[List[str]]],
    order_cuisine_tags: List[Optional[str]],
) -> Optional[float]:
    gt_raw = [c for c in order_cuisine_tags if c]
    if not gt_raw:
        return None
    gt_families = {_top_level(c) for c in gt_raw}
    pred_raw = [c for row in carousel_cuisines for c in (row or [])]
    pred_families = {_top_level(c) for c in pred_raw}
    return float(len(gt_families & pred_families) / len(gt_families))


def intra_list_diversity(carousel_embs: np.ndarray) -> Optional[float]:
    k = len(carousel_embs)
    if k < 2:
        return None
    sim = carousel_embs @ carousel_embs.T
    i, j = np.triu_indices(k, k=1)
    return float(1.0 - sim[i, j].mean())


def similarity_matrix(
    item_embs: np.ndarray, carousel_embs: np.ndarray
) -> np.ndarray:
    return item_embs @ carousel_embs.T


def mean_max_similarity(sim: np.ndarray) -> float:
    return float(sim.max(axis=1).mean())


def semantic_recall_at_k(
    sim: np.ndarray, k: int, theta: float = DEFAULT_THETA
) -> float:
    k_actual = min(k, sim.shape[1])
    top_k_sim = sim[:, :k_actual]
    return float((top_k_sim.max(axis=1) >= theta).mean())


def order_history_coverage_diversity(sim: np.ndarray) -> float:
    assignment = sim.argmax(axis=1)
    return float(len(set(assignment.tolist())) / sim.shape[1])


def title_metadata_coherence(
    title_embs: np.ndarray, food_type_embs: np.ndarray
) -> Optional[float]:
    if len(title_embs) == 0 or title_embs.shape != food_type_embs.shape:
        return None
    per_carousel = (title_embs * food_type_embs).sum(axis=1)
    return float(per_carousel.mean())


def composite_score(metric_values: Dict[str, Optional[float]]) -> Optional[float]:
    available = {
        k: v
        for k, v in metric_values.items()
        if k in COMPOSITE_WEIGHTS and v is not None
    }
    if not available:
        return None
    total_weight = sum(COMPOSITE_WEIGHTS[k] for k in available)
    return float(
        sum(COMPOSITE_WEIGHTS[k] * available[k] for k in available) / total_weight
    )


def compute_all_metrics(
    carousel_ranks: List[int],
    titles: List[Optional[str]],
    food_types: List[Optional[List[str]]],
    cuisine_types: List[Optional[List[str]]],
    carousel_emb_list: List[Optional[List[float]]],
    title_emb_list: List[Optional[List[float]]],
    food_type_emb_list: List[Optional[List[float]]],
    item_emb_list: List[Optional[List[float]]],
    item_cuisine_tag_list: List[Optional[List[str]]],
    theta: float = DEFAULT_THETA,
) -> Dict[str, Optional[float]]:
    results: Dict[str, Optional[float]] = {}

    order = sorted(range(len(carousel_ranks)), key=lambda i: carousel_ranks[i])
    titles_ord = [titles[i] for i in order]
    food_types_ord = [food_types[i] for i in order]
    cuisine_types_ord = [cuisine_types[i] for i in order]
    carousel_embs_ord = [carousel_emb_list[i] for i in order]
    title_embs_ord = [title_emb_list[i] for i in order]
    food_type_embs_ord = [food_type_emb_list[i] for i in order]

    # Q2: FCS
    results["fcs"] = avg_format_compliance(titles_ord, food_types_ord, cuisine_types_ord)

    # R3: CCR
    order_cuisines_flat = [c for tags in item_cuisine_tag_list for c in (tags or [])]
    results["ccr"] = cuisine_coverage_recall(cuisine_types_ord, order_cuisines_flat)

    # Build carousel embedding matrix
    carousel_emb_arrays = [_to_unit_array(e) for e in carousel_embs_ord]
    valid_carousel_mask = [a is not None for a in carousel_emb_arrays]
    valid_carousel_embs = [a for a in carousel_emb_arrays if a is not None]

    if len(valid_carousel_embs) >= 2:
        c_embs = np.stack(valid_carousel_embs)

        results["ild"] = intra_list_diversity(c_embs)

        t_arrays = [
            _to_unit_array(e)
            for e, v in zip(title_embs_ord, valid_carousel_mask)
            if v
        ]
        ft_arrays = [
            _to_unit_array(e)
            for e, v in zip(food_type_embs_ord, valid_carousel_mask)
            if v
        ]
        if all(a is not None for a in t_arrays) and all(
            a is not None for a in ft_arrays
        ):
            results["tmc"] = title_metadata_coherence(
                np.stack(t_arrays), np.stack(ft_arrays)
            )

        item_emb_arrays = [_to_unit_array(e) for e in item_emb_list if e is not None]
        if item_emb_arrays:
            i_embs = np.stack(item_emb_arrays)
            sim = similarity_matrix(i_embs, c_embs)
            results["mms"] = mean_max_similarity(sim)
            for k in SR_K_VALUES:
                results[f"sr_at_{k}"] = semantic_recall_at_k(sim, k, theta)
            results["ohcd"] = order_history_coverage_diversity(sim)

    results["composite_quality_score"] = composite_score(results)
    return results


# ============================================================================
# CONFIGURATION
# ============================================================================

EBR_TABLE = "proddb.ml.cx_profile_generated_carousels_ebr"
FALLBACK_TABLE = (
    "proddb.graceluo.search_title_fallback_retrieved_titles_2026_03_16_v2"
)
EVAL_DATE = "2026-02-03"
ORDER_LOOKBACK_DAYS = 90
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

METRIC_COLS = [
    "mms",
    "sr_at_3",
    "sr_at_5",
    "sr_at_10",
    "ccr",
    "ild",
    "ohcd",
    "tmc",
    "fcs",
    "composite_quality_score",
]


# ============================================================================
# CLI
# ============================================================================


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Local carousel quality evaluation")
    p.add_argument(
        "--embed_mode",
        choices=["title_only", "title_metadata"],
        default="title_metadata",
        help="Embedding strategy for carousel text",
    )
    p.add_argument(
        "--order_history_csv",
        default=None,
        help=(
            "Path to a pre-downloaded CSV with columns: consumer_id, day_part, "
            "item_id, item_name, description, cuisine_tags_from_menu. "
            "If omitted, order history is pulled from Snowflake."
        ),
    )
    p.add_argument(
        "--carousel_csv",
        default=None,
        help="Path to a carousel CSV (same schema as fallback table). Evaluates this single source only.",
    )
    p.add_argument(
        "--carousel_csv_2",
        default=None,
        help="Second carousel CSV (used with --prepare to find common consumers across both sources).",
    )
    p.add_argument(
        "--source_name",
        default="carousel",
        help="Label for the carousel source when using --carousel_csv",
    )
    p.add_argument(
        "--sample_limit",
        type=int,
        default=0,
        help="Limit number of common consumers (0 = all)",
    )
    p.add_argument(
        "--prepare",
        action="store_true",
        help=(
            "Preparation mode: read both carousel CSVs + orders CSV, find common "
            "consumers, embed orders once, and save orders_embedded.pkl + "
            "common_consumers.csv to --output_dir.  Then exit."
        ),
    )
    p.add_argument(
        "--orders_embedded_pkl",
        default=None,
        help="Path to pre-embedded orders pickle (output of --prepare). Skips re-embedding.",
    )
    p.add_argument(
        "--common_consumers_csv",
        default=None,
        help="Path to pre-computed common consumer IDs CSV (output of --prepare).",
    )
    p.add_argument("--sr_theta", type=float, default=DEFAULT_THETA)
    p.add_argument("--output_dir", default=".", help="Directory for output CSVs")
    return p.parse_args()


# ============================================================================
# Snowflake helpers
# ============================================================================


def get_snowflake_connection():
    """Return a snowflake.connector connection using env vars or defaults."""
    import snowflake.connector

    params = dict(
        account=os.environ.get("SNOWFLAKE_ACCOUNT", "doordash"),
        user=os.environ.get("SNOWFLAKE_USER", "SICONGBRYANFANG"),
        password=os.environ.get("SNOWFLAKE_PASSWORD", ""),
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "ADHOC"),
        database=os.environ.get("SNOWFLAKE_DATABASE", "PRODDB"),
    )
    host = os.environ.get("SNOWFLAKE_HOST")
    if host:
        params["host"] = host
    role = os.environ.get("SNOWFLAKE_ROLE")
    if role:
        params["role"] = role
    return snowflake.connector.connect(**params)


def query_to_df(conn, sql: str) -> pd.DataFrame:
    """Execute *sql* and return a Pandas DataFrame."""
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [desc[0].lower() for desc in cur.description]
        rows = cur.fetchall()
        return pd.DataFrame(rows, columns=cols)
    finally:
        cur.close()


# ============================================================================
# Data loading
# ============================================================================


def load_ebr_carousels(conn, consumer_ids: List[int]) -> pd.DataFrame:
    """Load EBR carousels only for the given consumer_ids."""
    chunks: List[pd.DataFrame] = []
    batch_size = 1000
    total_batches = (len(consumer_ids) + batch_size - 1) // batch_size
    for i in range(0, len(consumer_ids), batch_size):
        batch = consumer_ids[i : i + batch_size]
        id_list = ", ".join(str(cid) for cid in batch)
        sql = f"""
            SELECT consumer_id, day_part, carousel_rank, title, tags
            FROM {EBR_TABLE}
            WHERE consumer_id IN ({id_list})
        """
        print(f"[load] EBR batch {i // batch_size + 1}/{total_batches} ...")
        chunks.append(query_to_df(conn, sql))

    print(f"[load] Queried EBR carousels from {EBR_TABLE} for {len(consumer_ids):,} consumers")
    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()


def load_fallback_carousels(conn) -> pd.DataFrame:
    sql = f"""
        SELECT
            CONSUMER_ID,
            TARGET_DAY_PART,
            RANK,
            TITLE,
            CUISINE_TYPE,
            TAGS,
            FOOD_TAG_ENTRY
        FROM {FALLBACK_TABLE}
    """
    print(f"[load] Querying fallback carousels from {FALLBACK_TABLE} ...")
    return query_to_df(conn, sql)


def load_order_history_from_snowflake(
    conn, consumer_ids: List[int]
) -> pd.DataFrame:
    """
    Load order history for *consumer_ids* over the 90-day lookback window.

    Adapted from purchased_items_for_profiles_base_instance.py — simplified
    to the columns needed for evaluation (no item extras / options).
    """
    end_date = EVAL_DATE
    start_date = (
        datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=ORDER_LOOKBACK_DAYS)
    ).strftime("%Y-%m-%d")

    chunks: List[pd.DataFrame] = []
    batch_size = 1000
    total_batches = (len(consumer_ids) + batch_size - 1) // batch_size
    for i in range(0, len(consumer_ids), batch_size):
        batch = consumer_ids[i : i + batch_size]
        id_list = ", ".join(str(cid) for cid in batch)
        sql = f"""
        WITH base_order_items AS (
            SELECT
                a.creator_id                AS consumer_id,
                a.store_id,
                a.item_id,
                a.item_name,
                a.description,
                a.is_group_order,
                EXTRACT(HOUR FROM CONVERT_TIMEZONE(
                    'UTC', a.timezone, a.actual_delivery_time
                ))                           AS local_hour,
                DAYOFWEEKISO(CONVERT_TIMEZONE(
                    'UTC', a.timezone, a.actual_delivery_time
                ))                           AS day_of_week
            FROM public.dimension_order_item a
            WHERE a.created_at::DATE BETWEEN '{start_date}' AND '{end_date}'
              AND a.order_cart_id IS NOT NULL
              AND a.is_filtered_core = TRUE
              AND a.removed_at IS NULL
              AND a.is_group_order = 0
              AND a.creator_id IN ({id_list})
        ),
        daypart_map AS (
            SELECT DISTINCT local_hour, day_part_regroup
            FROM static.hour_to_daypart_mapping
        )
        SELECT DISTINCT
            b.consumer_id,
            CASE WHEN b.day_of_week <= 5 THEN 'weekday' ELSE 'weekend' END
                || '_' || dm.day_part_regroup  AS day_part,
            b.item_id,
            b.item_name,
            COALESCE(b.description, '')        AS description,
            ds.is_cng,
            dmu.cuisine_tags                   AS cuisine_tags_from_menu
        FROM base_order_items b
        INNER JOIN daypart_map dm       ON b.local_hour = dm.local_hour
        INNER JOIN edw.merchant.dimension_store ds ON b.store_id = ds.store_id
        LEFT  JOIN edw.merchant.dimension_menu dmu ON b.store_id = dmu.store_id
        WHERE ds.is_cng = 0
        """
        print(f"[load] Order history batch {i // batch_size + 1}/{total_batches} ...")
        chunks.append(query_to_df(conn, sql))

    return pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame()


def load_order_history_from_csv(path: str) -> pd.DataFrame:
    """
    Read a pre-downloaded order history CSV.

    Expected columns:
        consumer_id, day_part, item_id, item_name, description,
        cuisine_tags_from_menu
    """
    print(f"[load] Reading order history from {path} ...")
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


# ============================================================================
# Normalisation
# ============================================================================


def _parse_json(val) -> dict:
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return {}
    return {}


def normalize_ebr(df: pd.DataFrame) -> pd.DataFrame:
    """Parse EBR tags column -> food_type & cuisine_type lists."""
    df = df.copy()
    parsed = df["tags"].apply(_parse_json)
    df["food_type"] = parsed.apply(lambda t: t.get("food_type", []) or [])
    df["cuisine_type"] = parsed.apply(lambda t: t.get("cuisine_type", []) or [])
    df["food_type"] = df["food_type"].apply(
        lambda x: x if isinstance(x, list) else []
    )
    df["cuisine_type"] = df["cuisine_type"].apply(
        lambda x: x if isinstance(x, list) else []
    )
    return df[
        ["consumer_id", "day_part", "carousel_rank", "title", "food_type", "cuisine_type"]
    ]


def normalize_fallback(df: pd.DataFrame) -> pd.DataFrame:
    """Rename fallback columns and parse tags/cuisine into lists."""
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(
        columns={"target_day_part": "day_part", "rank": "carousel_rank"}
    )

    def _extract_food_type(row):
        tags = _parse_json(row.get("tags"))
        ft = tags.get("food_type", [])
        if ft and isinstance(ft, list):
            return ft
        return []

    def _extract_cuisine_type(row):
        tags = _parse_json(row.get("tags"))
        ct = tags.get("cuisine_type", [])
        if ct and isinstance(ct, list):
            return ct
        raw = row.get("_cuisine_type_raw")
        if pd.notna(raw) and raw:
            return [str(raw)]
        return []

    if "cuisine_type" in df.columns:
        df = df.rename(columns={"cuisine_type": "_cuisine_type_raw"})

    df["food_type"] = df.apply(_extract_food_type, axis=1)
    df["cuisine_type"] = df.apply(_extract_cuisine_type, axis=1)

    return df[
        ["consumer_id", "day_part", "carousel_rank", "title", "food_type", "cuisine_type"]
    ]


def normalize_order_history(df: pd.DataFrame) -> pd.DataFrame:
    """Split cuisine tags, deduplicate per (consumer, daypart, item)."""
    df = df.copy()
    df["description"] = df["description"].fillna("")
    df["cuisine_tags_from_menu"] = df["cuisine_tags_from_menu"].fillna("")
    df["item_cuisine_tags"] = df["cuisine_tags_from_menu"].apply(
        lambda s: [t.strip() for t in str(s).split(",") if t.strip()] if s else []
    )
    df = df.drop_duplicates(subset=["consumer_id", "day_part", "item_id"])
    return df


# ============================================================================
# Embedding
# ============================================================================


def get_embedding_model():
    from sentence_transformers import SentenceTransformer

    print(f"[embed] Loading model {EMBEDDING_MODEL_NAME} ...")
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_carousels(
    model, df: pd.DataFrame, embed_mode: str
) -> pd.DataFrame:
    """
    Add carousel_emb, title_emb, food_type_emb columns.

    embed_mode controls carousel_emb text:
      - title_metadata: "{title}: {food_type joined}"
      - title_only:     "{title}"
    """
    df = df.copy()
    food_type_strs = df["food_type"].apply(
        lambda ft: ", ".join(ft) if ft else ""
    )

    if embed_mode == "title_metadata":
        carousel_texts = (df["title"].fillna("") + ": " + food_type_strs).tolist()
    else:
        carousel_texts = df["title"].fillna("").tolist()

    print(f"[embed] Encoding {len(carousel_texts)} carousel texts ({embed_mode}) ...")
    carousel_embs = model.encode(
        carousel_texts,
        batch_size=512,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    df["carousel_emb"] = list(carousel_embs)

    print(f"[embed] Encoding {len(df)} carousel titles ...")
    title_embs = model.encode(
        df["title"].fillna("").tolist(),
        batch_size=512,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    df["title_emb"] = list(title_embs)

    print(f"[embed] Encoding {len(df)} food-type strings ...")
    food_type_embs = model.encode(
        food_type_strs.tolist(),
        batch_size=512,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    df["food_type_emb"] = list(food_type_embs)

    return df


def embed_items(model, df: pd.DataFrame, embed_mode: str) -> pd.DataFrame:
    """Add item_emb column. embed_mode controls the text used:
      - title_only:     item_name
      - title_metadata: '{item_name}. {description}'
    """
    df = df.copy()
    if embed_mode == "title_metadata":
        texts = df.apply(
            lambda r: f"{r['item_name']}. {r['description']}"
            if r.get("description")
            else str(r["item_name"]),
            axis=1,
        ).tolist()
    else:
        texts = df["item_name"].fillna("").astype(str).tolist()

    print(f"[embed] Encoding {len(texts)} order-item texts ...")
    embs = model.encode(
        texts,
        batch_size=512,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    df["item_emb"] = list(embs)
    return df


# ============================================================================
# Evaluation
# ============================================================================


def run_evaluation(
    carousel_df: pd.DataFrame,
    order_df: pd.DataFrame,
    source_name: str,
    theta: float = DEFAULT_THETA,
) -> pd.DataFrame:
    """
    Iterate over (consumer_id, day_part) groups and compute all metrics.
    Returns a DataFrame with one row per group.
    """
    results: List[dict] = []
    groups = carousel_df.groupby(["consumer_id", "day_part"])
    total = len(groups)

    for idx, ((cid, dp), c_grp) in enumerate(groups, 1):
        i_grp = order_df[
            (order_df["consumer_id"] == cid) & (order_df["day_part"] == dp)
        ]
        if i_grp.empty:
            continue

        metrics = compute_all_metrics(
            carousel_ranks=c_grp["carousel_rank"].tolist(),
            titles=c_grp["title"].tolist(),
            food_types=c_grp["food_type"].tolist(),
            cuisine_types=c_grp["cuisine_type"].tolist(),
            carousel_emb_list=c_grp["carousel_emb"].tolist(),
            title_emb_list=c_grp["title_emb"].tolist(),
            food_type_emb_list=c_grp["food_type_emb"].tolist(),
            item_emb_list=i_grp["item_emb"].tolist(),
            item_cuisine_tag_list=i_grp["item_cuisine_tags"].tolist(),
            theta=theta,
        )

        row = {"consumer_id": cid, "day_part": dp, "source": source_name}
        row.update(metrics)
        results.append(row)

        if idx % 500 == 0 or idx == total:
            print(f"[eval][{source_name}] {idx}/{total} groups processed")

    return pd.DataFrame(results)


# ============================================================================
# Report
# ============================================================================


def generate_report(metrics_df: pd.DataFrame, source_name: str) -> None:
    """Print an overall and per-daypart summary to stdout."""
    if metrics_df.empty:
        print(f"\n[report] {source_name}: no evaluation results.")
        return

    print(f"\n{'=' * 55}")
    print(f"  {source_name} Carousel Evaluation Report")
    print(f"{'=' * 55}")
    print(f"  Total consumers evaluated : {metrics_df['consumer_id'].nunique():,}")
    print(f"  Total (consumer, daypart) : {len(metrics_df):,}")

    print("\n  Overall Metrics (mean +/- std):")
    for col in METRIC_COLS:
        if col in metrics_df.columns:
            vals = metrics_df[col].dropna()
            if len(vals) > 0:
                print(
                    f"    {col:<28s} {vals.mean():.4f} +/- {vals.std():.4f}  (n={len(vals)})"
                )

    # Per-daypart breakdown
    summary_cols = ["mms", "sr_at_5", "ccr", "ild", "composite_quality_score"]
    header = f"  {'daypart':<24s} | {'count':>5s}"
    for c in summary_cols:
        header += f" | {c:>12s}"
    print(f"\n  Breakdown by Daypart:\n{header}")
    print("  " + "-" * (len(header) - 2))

    for dp in sorted(metrics_df["day_part"].unique()):
        grp = metrics_df[metrics_df["day_part"] == dp]
        line = f"  {dp:<24s} | {len(grp):>5d}"
        for c in summary_cols:
            if c in grp.columns:
                vals = grp[c].dropna()
                line += (
                    f" | {vals.mean():>12.4f}"
                    if len(vals) > 0
                    else f" | {'N/A':>12s}"
                )
            else:
                line += f" | {'N/A':>12s}"
        print(line)

    print()


# ============================================================================
# Main
# ============================================================================


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # ---- Prepare mode: embed orders + find common consumers, then exit ----
    if args.prepare:
        if not args.carousel_csv or not args.carousel_csv_2 or not args.order_history_csv:
            print("[ERROR] --prepare requires --carousel_csv, --carousel_csv_2, and --order_history_csv")
            return

        print(f"[prepare] Reading carousel 1 from {args.carousel_csv} ...")
        df_c1 = pd.read_csv(args.carousel_csv)
        df_c1.columns = [c.strip().lower() for c in df_c1.columns]

        print(f"[prepare] Reading carousel 2 from {args.carousel_csv_2} ...")
        df_c2 = pd.read_csv(args.carousel_csv_2)
        df_c2.columns = [c.strip().lower() for c in df_c2.columns]

        print(f"[prepare] Reading order history from {args.order_history_csv} ...")
        df_orders_raw = load_order_history_from_csv(args.order_history_csv)

        c1_consumers = set(df_c1["consumer_id"].unique())
        c2_consumers = set(df_c2["consumer_id"].unique())
        order_consumers = set(df_orders_raw["consumer_id"].unique())
        common = sorted(c1_consumers & c2_consumers & order_consumers)

        print(f"[prepare] Carousel-1 consumers: {len(c1_consumers):,}, "
              f"Carousel-2 consumers: {len(c2_consumers):,}, "
              f"Order consumers: {len(order_consumers):,}, "
              f"Common (all 3): {len(common):,}")

        if not common:
            print("[ERROR] No common consumers found across all three sources.")
            return

        # Save common consumers
        common_path = os.path.join(args.output_dir, "common_consumers.csv")
        pd.DataFrame({"consumer_id": common}).to_csv(common_path, index=False)
        print(f"[prepare] Saved {common_path} ({len(common):,} consumers)")

        # Normalise and embed orders for common consumers only
        df_orders_raw = df_orders_raw[df_orders_raw["consumer_id"].isin(common)]
        df_orders = normalize_order_history(df_orders_raw)
        print(f"[prepare] Order rows after filtering: {len(df_orders):,}")

        model = get_embedding_model()
        df_orders = embed_items(model, df_orders, args.embed_mode)

        pkl_path = os.path.join(args.output_dir, f"orders_embedded_{args.embed_mode}.pkl")
        df_orders.to_pickle(pkl_path)
        print(f"[prepare] Saved {pkl_path} ({len(df_orders):,} rows)")
        print("[prepare] Done. You can now run eval with --orders_embedded_pkl and --common_consumers_csv.")
        return

    # ---- Single-source CSV mode ----
    if args.carousel_csv and (args.order_history_csv or args.orders_embedded_pkl):
        print(f"[load] Reading carousel data from {args.carousel_csv} ...")
        df_carousel_raw = pd.read_csv(args.carousel_csv)
        df_carousel_raw.columns = [c.strip().lower() for c in df_carousel_raw.columns]

        # Load orders: pre-embedded pickle or raw CSV
        if args.orders_embedded_pkl:
            print(f"[load] Loading pre-embedded orders from {args.orders_embedded_pkl} ...")
            df_orders = pd.read_pickle(args.orders_embedded_pkl)
            orders_pre_embedded = True
        else:
            df_orders_raw = load_order_history_from_csv(args.order_history_csv)
            orders_pre_embedded = False

        # Determine common consumers
        if args.common_consumers_csv:
            print(f"[load] Loading common consumers from {args.common_consumers_csv} ...")
            common_consumers = sorted(
                pd.read_csv(args.common_consumers_csv)["consumer_id"].tolist()
            )
            if args.sample_limit > 0:
                common_consumers = common_consumers[: args.sample_limit]
            print(f"[load] Using {len(common_consumers):,} common consumers"
                  f"{f' (sampled {args.sample_limit})' if args.sample_limit > 0 else ''}")
        else:
            carousel_consumers = set(df_carousel_raw["consumer_id"].unique())
            if orders_pre_embedded:
                order_consumers = set(df_orders["consumer_id"].unique())
            else:
                order_consumers = set(df_orders_raw["consumer_id"].unique())
            common_consumers = sorted(carousel_consumers & order_consumers)
            if args.sample_limit > 0:
                common_consumers = common_consumers[: args.sample_limit]
            print(f"[load] Carousel consumers: {len(carousel_consumers):,}, "
                  f"Order consumers: {len(order_consumers):,}, "
                  f"Common: {len(common_consumers):,}")

        if not common_consumers:
            print("[ERROR] No common consumers found.")
            return

        common_set = set(common_consumers)
        df_carousel_raw = df_carousel_raw[
            df_carousel_raw["consumer_id"].isin(common_set)
        ]

        if orders_pre_embedded:
            df_orders = df_orders[df_orders["consumer_id"].isin(common_set)]
        else:
            df_orders_raw = df_orders_raw[
                df_orders_raw["consumer_id"].isin(common_set)
            ]

        print(f"[load] Carousel rows: {len(df_carousel_raw):,}, "
              f"Order rows: {len(df_orders if orders_pre_embedded else df_orders_raw):,}")

        # Normalise
        df_carousel = normalize_fallback(df_carousel_raw)
        if not orders_pre_embedded:
            df_orders = normalize_order_history(df_orders_raw)
        print(f"[norm] Carousel: {len(df_carousel):,}, Orders: {len(df_orders):,}")

        # Embed
        model = get_embedding_model()
        df_carousel = embed_carousels(model, df_carousel, args.embed_mode)
        if not orders_pre_embedded:
            df_orders = embed_items(model, df_orders, args.embed_mode)

        # Evaluate
        source = args.source_name
        print(f"\n[eval] Running {source} evaluation ...")
        metrics = run_evaluation(df_carousel, df_orders, source, args.sr_theta)

        # Report & save
        generate_report(metrics, source)
        out_path = os.path.join(args.output_dir, f"eval_{source}.csv")
        metrics.to_csv(out_path, index=False)
        print(f"\n[done] Saved {out_path} ({len(metrics):,} rows)")
        return

    # ---- Dual-source Snowflake mode (original) ----
    conn = get_snowflake_connection()
    df_fallback_raw = load_fallback_carousels(conn)
    fallback_consumers = sorted(df_fallback_raw["consumer_id"].unique().tolist())
    print(f"[load] Fallback rows: {len(df_fallback_raw):,}, unique consumers: {len(fallback_consumers):,}")

    if args.sample_limit > 0:
        fallback_consumers = fallback_consumers[: args.sample_limit]
        df_fallback_raw = df_fallback_raw[
            df_fallback_raw["consumer_id"].isin(fallback_consumers)
        ]

    df_ebr_raw = load_ebr_carousels(conn, fallback_consumers)
    print(f"[load] EBR rows: {len(df_ebr_raw):,}")

    ebr_consumers = set(df_ebr_raw["consumer_id"].unique())
    common_consumers = sorted(set(fallback_consumers) & ebr_consumers)
    print(f"[load] Common consumers: {len(common_consumers):,}")

    if not common_consumers:
        print("[ERROR] No common consumers found between EBR and Fallback tables.")
        conn.close()
        return

    df_ebr_raw = df_ebr_raw[df_ebr_raw["consumer_id"].isin(common_consumers)]
    df_fallback_raw = df_fallback_raw[
        df_fallback_raw["consumer_id"].isin(common_consumers)
    ]

    if args.order_history_csv:
        df_orders_raw = load_order_history_from_csv(args.order_history_csv)
    else:
        df_orders_raw = load_order_history_from_snowflake(conn, common_consumers)

    conn.close()

    df_orders_raw = df_orders_raw[
        df_orders_raw["consumer_id"].isin(common_consumers)
    ]
    print(f"[load] Order history rows (filtered): {len(df_orders_raw):,}")

    df_ebr = normalize_ebr(df_ebr_raw)
    df_fallback = normalize_fallback(df_fallback_raw)
    df_orders = normalize_order_history(df_orders_raw)

    print(
        f"[norm] EBR: {len(df_ebr):,} rows, "
        f"Fallback: {len(df_fallback):,} rows, "
        f"Orders: {len(df_orders):,} rows"
    )

    model = get_embedding_model()
    df_ebr = embed_carousels(model, df_ebr, args.embed_mode)
    df_fallback = embed_carousels(model, df_fallback, args.embed_mode)
    df_orders = embed_items(model, df_orders, args.embed_mode)

    print("\n[eval] Running EBR evaluation ...")
    metrics_ebr = run_evaluation(df_ebr, df_orders, "ebr", args.sr_theta)

    print("[eval] Running Fallback evaluation ...")
    metrics_fallback = run_evaluation(
        df_fallback, df_orders, "fallback", args.sr_theta
    )

    generate_report(metrics_ebr, "EBR")
    generate_report(metrics_fallback, "Search-Title-Fallback")

    ebr_path = os.path.join(args.output_dir, "eval_ebr.csv")
    fb_path = os.path.join(args.output_dir, "eval_fallback.csv")
    metrics_ebr.to_csv(ebr_path, index=False)
    metrics_fallback.to_csv(fb_path, index=False)
    print(f"\n[done] Saved {ebr_path} ({len(metrics_ebr):,} rows)")
    print(f"[done] Saved {fb_path} ({len(metrics_fallback):,} rows)")


if __name__ == "__main__":
    main()
