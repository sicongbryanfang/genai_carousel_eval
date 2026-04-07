"""
Pure-Python / NumPy metric implementations for carousel quality evaluation.

All functions in this module are side-effect-free and Spark-free so they can
be called inside a Pandas UDF or tested in isolation without a Spark session.

Dimensions
----------
R – Relevance   (do carousels reflect what the consumer actually orders?)
D – Diversity   (do carousels cover different parts of the interest space?)
Q – Quality     (are individual carousels internally well-formed?)
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np

from fabricator.repository.features.cx_discovery.store_consumer_profiles.cx_profile.constants import (
    CUISINE_TAXONOMY_DICT,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ADJECTIVE_BLOCKLIST = frozenset(
    {"fresh", "delicious", "tasty", "amazing", "great", "awesome", "yummy"}
)
ALCOHOL_TOKENS = frozenset(
    {"beer", "wine", "cocktail", "whiskey", "bourbon", "spirits", "vodka", "sake", "liquor", "cider"}
)

# Map each cuisine tag to its top-level family for diversity / CCR grouping.
CUISINE_TOP_LEVEL: Dict[str, str] = {
    tag: path[0] for tag, path in CUISINE_TAXONOMY_DICT.items()
}

# Default SR@K threshold, appropriate for all-MiniLM-L6-v2 similarity range.
DEFAULT_THETA = 0.45
SR_K_VALUES = (3, 5, 10)

# Composite weights — sum to 1.0.  Tune after gathering baseline distributions.
COMPOSITE_WEIGHTS: Dict[str, float] = {
    "mms": 0.20,
    "sr_at_5": 0.15,
    "ccr": 0.15,
    "ild": 0.10,
    "ohcd": 0.10,
    "tmc": 0.15,
    "fcs": 0.15,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _top_level(tag: str) -> str:
    """Return the top-level cuisine family for *tag*, or *tag* itself if unknown."""
    path = CUISINE_TAXONOMY_DICT.get(tag)
    return path[0] if path else tag


def _to_unit_array(arr: Optional[List[float]]) -> Optional[np.ndarray]:
    if arr is None:
        return None
    v = np.asarray(arr, dtype=np.float32)
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


# ---------------------------------------------------------------------------
# Q2 – Format Compliance Score (FCS)
# No embeddings needed.
# ---------------------------------------------------------------------------

def format_compliance_score(
    title: Optional[str],
    food_type: Optional[List[str]],
    cuisine_type: Optional[List[str]],
) -> float:
    """
    Return a [0, 1] compliance score for a single carousel based on the prompt rules:

    - Title ≤ 5 words
    - Sentence case  (first word capitalised, rest lowercase)
    - Title does not start with a known filler adjective
    - Title contains no alcohol tokens
    - food_type array has 5–15 items, each token 2–3 words
    - cuisine_type array has ≤ 3 items
    """
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
    """Average FCS across all carousels in the list."""
    if not titles:
        return None
    scores = [
        format_compliance_score(t, ft, ct)
        for t, ft, ct in zip(titles, food_types, cuisine_types)
    ]
    return float(np.mean(scores))


# ---------------------------------------------------------------------------
# R3 – Cuisine Coverage Recall (CCR)
# Taxonomy-based, no embeddings needed.
# ---------------------------------------------------------------------------

def cuisine_coverage_recall(
    carousel_cuisines: List[Optional[List[str]]],
    order_cuisine_tags: List[Optional[str]],
) -> Optional[float]:
    """
    Fraction of the consumer's historically ordered cuisine top-level families
    that appear in at least one carousel's cuisine_type list.

    Parameters
    ----------
    carousel_cuisines
        One entry per carousel; each entry is the carousel's cuisine_type array.
    order_cuisine_tags
        Flat list of raw cuisine tag strings from order history
        (e.g. ``["Italian", "Pizza", "Cantonese"]``).
    """
    gt_raw = [c for c in order_cuisine_tags if c]
    if not gt_raw:
        return None
    gt_families = {_top_level(c) for c in gt_raw}
    pred_raw = [c for row in carousel_cuisines for c in (row or [])]
    pred_families = {_top_level(c) for c in pred_raw}
    return float(len(gt_families & pred_families) / len(gt_families))


# ---------------------------------------------------------------------------
# D1 – Intra-List Diversity (ILD)
# Requires carousel embeddings only — no order history needed.
# ---------------------------------------------------------------------------

def intra_list_diversity(carousel_embs: np.ndarray) -> Optional[float]:
    """
    ILD = 1 − mean pairwise cosine similarity across the carousel set.

    Parameters
    ----------
    carousel_embs : (K, D) float32 array of *unit-normalised* embeddings.
    """
    k = len(carousel_embs)
    if k < 2:
        return None
    sim = carousel_embs @ carousel_embs.T  # (K, K), already unit-normed
    i, j = np.triu_indices(k, k=1)
    return float(1.0 - sim[i, j].mean())


# ---------------------------------------------------------------------------
# R1/R2/D2 – Similarity-matrix-based metrics
# Requires both item embeddings (ground truth) and carousel embeddings.
# ---------------------------------------------------------------------------

def similarity_matrix(
    item_embs: np.ndarray,
    carousel_embs: np.ndarray,
) -> np.ndarray:
    """
    Cosine similarity matrix of shape (N_items, K_carousels).
    Assumes both inputs are *unit-normalised* (dot product = cosine sim).
    """
    return item_embs @ carousel_embs.T


def mean_max_similarity(sim: np.ndarray) -> float:
    """R1 – For each item, take its best-matching carousel. Average across items."""
    return float(sim.max(axis=1).mean())


def semantic_recall_at_k(
    sim: np.ndarray,
    k: int,
    theta: float = DEFAULT_THETA,
) -> float:
    """
    R2 – Fraction of items covered by at least one of the top-K carousels
    (coverage = cosine similarity ≥ theta).

    The sim matrix columns are assumed to be in carousel rank order (rank 0 first).
    """
    k_actual = min(k, sim.shape[1])
    top_k_sim = sim[:, :k_actual]
    return float((top_k_sim.max(axis=1) >= theta).mean())


def order_history_coverage_diversity(sim: np.ndarray) -> float:
    """
    D2 – Fraction of carousels that are the best match for at least one ordered item.

    Measures whether different carousels serve different portions of the
    consumer's interest space (vs. all carousels clustering on the same items).
    """
    assignment = sim.argmax(axis=1)
    return float(len(set(assignment.tolist())) / sim.shape[1])


# ---------------------------------------------------------------------------
# Q1 – Title–Metadata Coherence (TMC)
# Requires embeddings of title and food_type string (no order history).
# ---------------------------------------------------------------------------

def title_metadata_coherence(
    title_embs: np.ndarray,
    food_type_embs: np.ndarray,
) -> Optional[float]:
    """
    Average cosine similarity between each carousel's title embedding and its
    food_type embedding across the carousel list.

    Parameters
    ----------
    title_embs     : (K, D) unit-normalised title embeddings
    food_type_embs : (K, D) unit-normalised food_type-string embeddings
    """
    if len(title_embs) == 0 or title_embs.shape != food_type_embs.shape:
        return None
    per_carousel = (title_embs * food_type_embs).sum(axis=1)  # dot product row-wise
    return float(per_carousel.mean())


# ---------------------------------------------------------------------------
# Composite score
# ---------------------------------------------------------------------------

def composite_score(metric_values: Dict[str, Optional[float]]) -> Optional[float]:
    """
    Weighted average of available metrics.  Missing (None) metrics are skipped
    and the remaining weights are renormalised so the result stays in [0, 1].
    """
    available = {k: v for k, v in metric_values.items() if k in COMPOSITE_WEIGHTS and v is not None}
    if not available:
        return None
    total_weight = sum(COMPOSITE_WEIGHTS[k] for k in available)
    return float(sum(COMPOSITE_WEIGHTS[k] * available[k] for k in available) / total_weight)


# ---------------------------------------------------------------------------
# Top-level per-group computation (called from Pandas UDF)
# ---------------------------------------------------------------------------

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
    """
    Compute all metrics for a single (consumer_id, day_part) group.

    Carousel inputs are parallel lists indexed by carousel position.
    Item inputs are parallel lists indexed by ordered item.

    Returns a dict with keys: mms, sr_at_3, sr_at_5, sr_at_10, ccr,
    ild, ohcd, tmc, fcs, composite_quality_score.
    """
    results: Dict[str, Optional[float]] = {}

    # Sort carousels by rank so SR@K respects ordering.
    order = sorted(range(len(carousel_ranks)), key=lambda i: carousel_ranks[i])
    titles_ord = [titles[i] for i in order]
    food_types_ord = [food_types[i] for i in order]
    cuisine_types_ord = [cuisine_types[i] for i in order]
    carousel_embs_ord = [carousel_emb_list[i] for i in order]
    title_embs_ord = [title_emb_list[i] for i in order]
    food_type_embs_ord = [food_type_emb_list[i] for i in order]

    # Q2: FCS — no embeddings
    results["fcs"] = avg_format_compliance(titles_ord, food_types_ord, cuisine_types_ord)

    # R3: CCR — taxonomy only
    order_cuisines_flat = [c for tags in item_cuisine_tag_list for c in (tags or [])]
    results["ccr"] = cuisine_coverage_recall(cuisine_types_ord, order_cuisines_flat)

    # Build carousel embedding matrix (skip carousels with missing embeddings)
    carousel_emb_arrays = [_to_unit_array(e) for e in carousel_embs_ord]
    valid_carousel_mask = [a is not None for a in carousel_emb_arrays]
    valid_carousel_embs = [a for a in carousel_emb_arrays if a is not None]

    if len(valid_carousel_embs) >= 2:
        c_embs = np.stack(valid_carousel_embs)  # (K, D)

        # D1: ILD
        results["ild"] = intra_list_diversity(c_embs)

        # Q1: TMC
        t_arrays = [_to_unit_array(e) for e, v in zip(title_embs_ord, valid_carousel_mask) if v]
        ft_arrays = [_to_unit_array(e) for e, v in zip(food_type_embs_ord, valid_carousel_mask) if v]
        if all(a is not None for a in t_arrays) and all(a is not None for a in ft_arrays):
            results["tmc"] = title_metadata_coherence(
                np.stack(t_arrays), np.stack(ft_arrays)
            )

        # Relevance & D2 — need item embeddings
        item_emb_arrays = [_to_unit_array(e) for e in item_emb_list if e is not None]
        if item_emb_arrays:
            i_embs = np.stack(item_emb_arrays)  # (N, D)
            sim = similarity_matrix(i_embs, c_embs)  # (N, K)
            results["mms"] = mean_max_similarity(sim)
            for k in SR_K_VALUES:
                results[f"sr_at_{k}"] = semantic_recall_at_k(sim, k, theta)
            results["ohcd"] = order_history_coverage_diversity(sim)

    results["composite_quality_score"] = composite_score(results)
    return results
