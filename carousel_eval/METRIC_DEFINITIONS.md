# Carousel Quality Evaluation — Metric Definitions

## Overview

Every time a personalized food carousel set is generated for a consumer (e.g. "Korean fried chicken", "Late night ramen"), the evaluation system answers two questions:

1. **Are the carousels relevant to this person?** Do they reflect what the consumer has ordered before?
2. **Are the carousels well-made?** Are they diverse, internally consistent, and formatted correctly?

The system scores every generated carousel set on a scale of 0–1 across 9 metrics, grouped into three dimensions: **Relevance**, **Diversity**, and **Content Quality**.

---

## How It Works

Each consumer's order history (past 90 days, same meal period) is used as **ground truth** — a signal of what they actually like. The generated carousels are compared against this ground truth using a sentence-transformer model (`all-MiniLM-L6-v2`) to compute semantic (meaning-based) similarity.

Instead of exact word matching, the system measures *meaning* similarity. "Korean fried chicken" and "crispy Korean wings" are treated as nearly identical concepts.

---

## The 9 Metrics

### Relevance — Do the carousels match what this person orders?

---

#### R1 · Mean Max Similarity (MMS)
> *"On average, how well is each of the consumer's food interests covered by at least one carousel?"*

For every item the consumer has ordered in the past 90 days during this meal period, we find the most similar carousel and record that similarity score. We then average across all items.

| Score | Interpretation |
|---|---|
| 0.8 – 1.0 | Carousels closely reflect the consumer's actual order history |
| 0.5 – 0.8 | Partial match — some interests represented, some missed |
| < 0.5 | Carousels are largely unrelated to what this consumer orders |

**Example**: A consumer who mainly orders sushi, ramen, and Korean BBQ gets carousels for "Sushi rolls", "Japanese ramen", and "Korean fried chicken". MMS would be high. If instead they got carousels for "Italian pasta" and "Greek salad", MMS would be low.

**Implementation**: `mean_max_similarity(sim)` — takes the row-wise max of the `(N_items, K_carousels)` cosine similarity matrix, then averages.

---

#### R2 · Semantic Recall @ K (SR@K)
> *"What percentage of the consumer's food interests have at least one meaningful carousel match?"*

Similar to MMS, but binary: each ordered item either has a good-enough match (cosine similarity ≥ `theta`) in the top K carousels, or it doesn't. Reported at K = 3, 5, and 10.

| Score | Interpretation |
|---|---|
| 1.0 | Every food interest the consumer has is represented by a carousel |
| 0.6 | 60% of their interests are covered; 40% are not |
| 0.0 | None of their ordered items have a matching carousel |

**Why report at different K values?** SR@3 tells us if the most prominent carousels are on target. SR@10 tells us if the full set covers all of the consumer's tastes. A gap between SR@3 and SR@10 suggests the best carousels are good but the rest are padding.

**Implementation**: `semantic_recall_at_k(sim, k, theta=0.45)` — checks whether `sim[:, :k].max(axis=1) >= theta` for each item, then takes the mean.

---

#### R3 · Cuisine Coverage Recall (CCR)
> *"Does the carousel set cover the cuisine families this consumer actually orders from?"*

The simplest and most interpretable relevance metric. Each cuisine tag is mapped to its top-level family via the ~270-entry cuisine taxonomy. CCR is the fraction of the consumer's historically ordered cuisine families that appear in at least one carousel's `cuisine_type` list.

| Score | Interpretation |
|---|---|
| 1.0 | Every cuisine family the consumer orders from has at least one carousel |
| 0.5 | Half their cuisine interests are represented |
| 0.0 | None of their cuisine interests are represented |

**Example**: Consumer orders from Korean, Japanese, Thai restaurants. Carousels are: "Mexican street tacos", "Italian pasta", "Greek gyros" — CCR = 0. Carousels are: "Korean fried chicken", "Sushi rolls", "Spicy Thai curry" — CCR = 1.0.

**Implementation**: `cuisine_coverage_recall(carousel_cuisines, order_cuisine_tags)` — taxonomy-based, no embeddings needed.

---

### Diversity — Do the carousels cover different things?

---

#### D1 · Intra-List Diversity (ILD)
> *"How different are the carousels from each other?"*

Having nearly identical carousels (e.g., "Pepperoni pizza", "Cheese pizza", "Margherita pizza") wastes the opportunity to surface different foods. ILD = 1 minus the mean pairwise cosine similarity across all carousel pairs.

| Score | Interpretation |
|---|---|
| 0.8 – 1.0 | Highly diverse — each carousel covers a meaningfully different food concept |
| 0.4 – 0.8 | Moderate diversity |
| < 0.3 | Low diversity — carousels are redundant variations of the same theme |

**Note**: This metric does not use order history. It only looks at the generated carousels themselves.

**Implementation**: `intra_list_diversity(carousel_embs)` — computes the upper triangle of the `(K, K)` similarity matrix and returns `1 - mean`.

---

#### D1b · Title Cluster Diversity (TCD)
> *"How many distinct topic clusters do the carousel titles form?"*

ILD averages all pairwise similarities, which can mask a few near-duplicate pairs hidden among otherwise diverse titles. TCD takes a structural view: it builds a graph where titles are connected if their cosine similarity exceeds a threshold (`0.65`), then counts the number of connected components.

TCD = n_components / n_titles.

| Score | Interpretation |
|---|---|
| 1.0 | Every title is its own distinct cluster — maximally diverse |
| 0.7 – 0.9 | Most titles are distinct; a few share a topic cluster |
| < 0.5 | Titles are collapsing into very few topic groups |

**Example**: Carousels ["Korean fried chicken", "Spicy Korean wings", "Sushi rolls", "Pad Thai", "Butter chicken"] — "Korean fried chicken" and "Spicy Korean wings" form one cluster, the rest are separate. TCD = 4/5 = 0.8.

**Note**: Diagnostic metric — not included in the composite score. Higher is better.

**Implementation**: `title_cluster_diversity(carousel_embs, threshold=0.65)` — BFS-based connected component counting on the similarity graph.

---

#### D1c · Redundancy Rate (RR)
> *"What fraction of carousel pairs are near-duplicates?"*

While ILD measures average diversity and TCD measures structural clustering, RR specifically targets the worst-case: pairs of titles so similar they are effectively duplicates. A carousel set can have good ILD (many pairs are diverse) but still contain 1–2 near-duplicate pairs that waste slots.

RR = n_redundant_pairs / total_pairs, where a pair is "redundant" if cosine similarity ≥ `0.75`.

| Score | Interpretation |
|---|---|
| 0.0 | No near-duplicate pairs — every title is sufficiently distinct |
| 0.01 – 0.05 | 1–2 redundant pairs out of 45 (for 10 carousels) |
| > 0.10 | Significant redundancy — multiple title pairs are near-duplicates |

**Note**: Diagnostic metric — not included in the composite score. **Lower is better** (unlike all other metrics where higher = better).

**Implementation**: `redundancy_rate(carousel_embs, threshold=0.75)` — counts pairs exceeding the similarity threshold in the upper triangle.

---

#### D2 · Order History Coverage Diversity (OHCD)
> *"Are different carousels serving different parts of the consumer's tastes?"*

ILD measures diversity in isolation. OHCD measures diversity *relative to the consumer*. Even if carousels are all different from each other, they might all be relevant to only one aspect of the consumer's tastes (e.g., all Japanese food variations for someone who also loves Mexican and Indian food).

OHCD = fraction of carousels that are the best match for at least one ordered item.

| Score | Interpretation |
|---|---|
| 1.0 | All carousels serve a distinct portion of the consumer's taste profile |
| 0.5 | Only half the carousels are serving distinct interests; the rest overlap |
| 0.1 | Only 1 carousel is relevant; the rest are clustered around the same niche |

**Implementation**: `order_history_coverage_diversity(sim)` — assigns each item to its best-matching carousel via `argmax`, then counts unique assignments / total carousels.

---

### Content Quality — Are individual carousels well-made?

---

#### Q1 · Title–Metadata Coherence (TMC)
> *"Does the carousel title match the food items behind it?"*

Each carousel has a visible **title** (e.g., "Korean fried chicken") and a list of **food type tags** that drive which stores and items appear when a consumer taps the carousel (e.g., "fried chicken", "korean chicken", "crispy wings"). If the title says one thing but the food tags say another, the carousel will show irrelevant results.

TMC = average cosine similarity between each carousel's title embedding and its food-type-string embedding.

| Score | Interpretation |
|---|---|
| 0.8 – 1.0 | Title and food tags are well-aligned — what users see matches what they get |
| 0.5 – 0.8 | Partial alignment — some mismatch between title and content |
| < 0.5 | Strong mismatch — the carousel title is misleading relative to its content |

**Example of a bad carousel**: Title = "Late night comfort food" but food tags = ["sushi roll", "salmon nigiri", "tuna sashimi"]. TMC would be low because the title implies broad comfort food but the tags are sushi-specific.

**Implementation**: `title_metadata_coherence(title_embs, food_type_embs)` — row-wise dot product of unit-normalised embeddings, averaged.

---

#### Q2 · Format Compliance Score (FCS)
> *"Does the carousel follow the formatting rules defined in the generation prompt?"*

FCS checks whether 7 formatting rules were followed, using binary checks:

| Check | Rule | Example failure |
|---|---|---|
| Title length | ≤ 5 words | "Fresh and delicious late night bites" (7 words) |
| Sentence case | First word capitalized, rest lowercase | "korean Fried Chicken" |
| No filler adjectives | Can't start with "Fresh", "Delicious", "Amazing"... | "Delicious ramen bowls" |
| No alcohol | Title can't reference alcohol | "Wine and cheese pairings" |
| Food tag count | `food_type` list must have 5–15 items | Only 3 food tags listed |
| Food tag format | Each tag must be 2–3 words | Single-word tags like "pizza" or 4-word tags |
| Cuisine tag count | `cuisine_type` list must have ≤ 3 items | 5 cuisine tags listed |

**Score** = fraction of checks passed, averaged across all carousels.

**Implementation**: `format_compliance_score(title, food_type, cuisine_type)` — no embeddings needed. `avg_format_compliance()` averages across the carousel set.

---

## Composite Score

The 7 core metrics are combined into a single **composite quality score** between 0 and 1:

| Metric | Weight | Rationale |
|---|---|---|
| MMS (R1) | 20% | Core relevance signal — most predictive of user satisfaction |
| SR@5 (R2) | 15% | Coverage completeness for the top 5 carousels |
| CCR (R3) | 15% | Cuisine-level alignment — interpretable for debugging |
| ILD (D1) | 10% | Structural diversity of the carousel set |
| OHCD (D2) | 10% | Grounded diversity against user taste breadth |
| TMC (Q1) | 15% | Internal consistency — affects actual retrieval quality |
| FCS (Q2) | 15% | Rule compliance — catches systematic generation failures |

**TCD (D1b) and RR (D1c) are diagnostic metrics** — they are reported alongside the composite but are **not included in the composite weights**. They provide supplementary diversity signals that help identify specific failure modes (thematic clustering, near-duplicate pairs) that ILD's mean-based approach can miss.

Missing metrics (e.g. when embeddings are absent) are excluded and remaining weights are renormalized so the composite stays in [0, 1]. Weights are configurable in `COMPOSITE_WEIGHTS` and can be tuned as data on downstream click-through and order rates is gathered.

**Implementation**: `composite_score(metric_values)` in `metrics.py`.

---

## Interpreting Results

### Good carousel set (composite ~ 0.8)
```
Consumer 12345, weekday_lunch

MMS:    0.82   Ordered items are well-covered by carousels
SR@5:   0.90   90% of items have a match in the top 5 carousels
CCR:    1.00   All cuisine families represented
ILD:    0.55   Healthy diversity across carousels
TCD:    1.00   Every title is its own distinct cluster
RR:     0.00   No near-duplicate pairs
OHCD:   0.80   8 of 10 carousels serve distinct interests
TMC:    0.88   Titles and food tags are aligned
FCS:    0.96   Format rules mostly followed

Composite: 0.86
```

### Problematic carousel set (composite ~ 0.35)
```
Consumer 99999, weekday_dinner

MMS:    0.31   Carousels don't match what consumer orders
SR@5:   0.20   Only 20% of items have a match
CCR:    0.17   Only 1 of 6 cuisine families covered
ILD:    0.22   Carousels are very similar to each other
TCD:    0.30   Only 3 distinct clusters among 10 titles
RR:     0.13   6 out of 45 pairs are near-duplicates
OHCD:   0.20   Only 2 of 10 carousels serve distinct interests
TMC:    0.61   Acceptable title-tag alignment
FCS:    0.89   Format is fine

Composite: 0.35  → Investigate profile quality or prompt behavior
```

---

## Failure Modes

| Problem | Detected by |
|---|---|
| Carousels for cuisines the consumer never orders | MMS, SR@K, CCR |
| All carousels are slight variations of the same food (e.g., all Italian) | ILD, TCD, OHCD, CCR |
| A few carousel titles are near-duplicates (e.g., "Chicken tacos" and "Chicken taco plates") | RR, TCD |
| Titles orbit 2–3 themes but aren't exact duplicates (moderate ILD but low structural diversity) | TCD |
| Title says "Late night snacks" but food tags are all breakfast items | TMC |
| Generator ignores the 5-word title limit or uses filler adjectives | FCS |
| Consumer has diverse tastes but all carousels cluster on one interest | OHCD |
| Consumer's secondary cuisine interests are never represented | SR@10 vs SR@3 gap |

---

## Key Properties

- **Deterministic**: Same input always produces the same scores — no randomness. Safe to rerun for debugging.
- **No API cost**: Uses the open-source `all-MiniLM-L6-v2` embedding model. No external LLM calls for evaluation.
- **Ground truth**: Grounded in actual order history (past 90 days, same meal period). Not LLM-as-judge.
- **Scale**: Runs on up to 100,000 consumer/meal-period combinations per evaluation job.
- **Speed**: Full evaluation on 100k consumer/daypart pairs completes in ~15–20 minutes on a standard Databricks cluster.
- **Extensible**: Metrics can be computed against other data sources (e.g., store engagement, search queries, saved stores) without changing the metric logic.
