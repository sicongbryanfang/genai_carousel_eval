# Carousel Quality Evaluation — A Guide for Product Managers

## What Is This?

Every time DoorDash generates personalized food carousels for a consumer (e.g. "Korean fried chicken", "Late night ramen"), we run an automated quality check to answer two fundamental questions:

1. **Are the carousels actually relevant to this person?** Do they reflect what the consumer has ordered before?
2. **Are the carousels well-made?** Are they diverse, internally consistent, and formatted correctly?

This system scores every generated carousel set on a scale of 0–1 across 7 metrics, grouped into three dimensions: **Relevance**, **Diversity**, and **Content Quality**.

---

## How It Works (Simply Put)

Each consumer's order history (past 90 days, same meal period) is used as **ground truth** — a signal of what they actually like. The generated carousels are then compared against this ground truth using a language model to compute semantic (meaning-based) similarity.

Think of it like a teacher grading a student's answer against an answer key — except instead of exact word matching, we measure *meaning* similarity. "Korean fried chicken" and "crispy Korean wings" are treated as nearly identical concepts.

---

## The 7 Metrics

### Relevance — Do the carousels match what this person orders?

---

#### R1 · Mean Max Similarity (MMS)
> *"On average, how well is each of the consumer's food interests covered by at least one carousel?"*

For every item the consumer has ordered in the past 90 days during this meal period, we find the most similar carousel and record that similarity score. We then average across all items.

| Score | Meaning |
|---|---|
| 0.8 – 1.0 | Carousels closely reflect the consumer's actual order history |
| 0.5 – 0.8 | Partial match — some interests represented, some missed |
| < 0.5 | Carousels are largely unrelated to what this consumer orders |

**Example**: A consumer who mainly orders sushi, ramen, and Korean BBQ gets carousels for "Sushi rolls", "Japanese ramen", and "Korean fried chicken". MMS would be high. If instead they got carousels for "Italian pasta" and "Greek salad", MMS would be low.

---

#### R2 · Semantic Recall @ K (SR@K)
> *"What percentage of the consumer's food interests have at least one meaningful carousel match?"*

Similar to MMS, but binary: each ordered item either has a good-enough match in the top K carousels, or it doesn't. We report this at K = 3, 5, and 10.

| Score | Meaning |
|---|---|
| 1.0 | Every food interest the consumer has is represented by a carousel |
| 0.6 | 60% of their interests are covered; 40% are not |
| 0.0 | None of their ordered items have a matching carousel |

**Why report at different K values?** SR@3 tells us if the most prominent carousels are on target. SR@10 tells us if the full set covers all of the consumer's tastes. A gap between SR@3 and SR@10 suggests the best carousels are good but the rest are padding.

---

#### R3 · Cuisine Coverage Recall (CCR)
> *"Does the carousel set cover the cuisine families this consumer actually orders from?"*

This is the simplest and most interpretable relevance metric. It asks: if a consumer regularly orders Korean, Japanese, and Thai food, do any of the 10 carousels represent those cuisine families?

| Score | Meaning |
|---|---|
| 1.0 | Every cuisine family the consumer orders from has at least one carousel |
| 0.5 | Half their cuisine interests are represented |
| 0.0 | None of their cuisine interests are represented |

**Example**: Consumer orders from Korean, Japanese, Thai restaurants. Carousels are: "Mexican street tacos", "Italian pasta", "Greek gyros"… CCR = 0. Carousels are: "Korean fried chicken", "Sushi rolls", "Spicy Thai curry"… CCR = 1.0.

---

### Diversity — Do the 10 carousels cover different things?

---

#### D1 · Intra-List Diversity (ILD)
> *"How different are the 10 carousels from each other?"*

Having 10 nearly identical carousels (e.g., "Pepperoni pizza", "Cheese pizza", "Margherita pizza"…) wastes the opportunity to help consumers discover different foods. ILD measures how semantically distinct the carousels are from each other.

| Score | Meaning |
|---|---|
| 0.8 – 1.0 | Highly diverse — each carousel covers a meaningfully different food concept |
| 0.4 – 0.8 | Moderate diversity |
| < 0.3 | Low diversity — carousels are redundant variations of the same theme |

**Note**: This metric does not need order history. It only looks at the 10 generated carousels themselves.

---

#### D2 · Order History Coverage Diversity (OHCD)
> *"Are different carousels serving different parts of the consumer's tastes?"*

ILD measures diversity in isolation. OHCD measures diversity *relative to the consumer*. Even if 10 carousels are all different from each other, they might all be relevant to only one aspect of the consumer's tastes (e.g., all are Japanese food variations for someone who also loves Mexican and Indian food).

OHCD asks: across all the consumer's ordered items, how many of the 10 carousels are "doing useful work" by being the best match for at least one item?

| Score | Meaning |
|---|---|
| 1.0 | All 10 carousels serve a distinct portion of the consumer's taste profile |
| 0.5 | Only 5 of the 10 carousels are serving distinct interests; the rest overlap |
| 0.1 | Only 1 carousel is relevant; the rest are clustered around the same niche |

---

### Content Quality — Are individual carousels well-made?

---

#### Q1 · Title–Metadata Coherence (TMC)
> *"Does the carousel title match the food items behind it?"*

Each carousel has a visible **title** (e.g., "Korean fried chicken") and a hidden list of **food type tags** that drive which stores and items appear when a consumer taps the carousel (e.g., "fried chicken", "korean chicken", "crispy wings"…). If the title says one thing but the food tags say another, the carousel will show irrelevant results.

| Score | Meaning |
|---|---|
| 0.8 – 1.0 | Title and food tags are well-aligned — what users see matches what they get |
| 0.5 – 0.8 | Partial alignment — some mismatch between title and content |
| < 0.5 | Strong mismatch — the carousel title is misleading relative to its content |

**Example of a bad carousel**: Title = "Late night comfort food" but food tags = ["sushi roll", "salmon nigiri", "tuna sashimi"]. TMC would be low because the title implies broad comfort food but the tags are sushi-specific.

---

#### Q2 · Format Compliance Score (FCS)
> *"Does the carousel follow all the formatting rules we set in the prompt?"*

The AI is given explicit rules about how to format carousels. FCS checks whether those rules were followed, using 7 binary checks:

| Check | Rule | Example failure |
|---|---|---|
| Title length | ≤ 5 words | "Fresh and delicious late night bites" (7 words) |
| Sentence case | First word capitalized, rest lowercase | "korean Fried Chicken" |
| No filler adjectives | Can't start with "Fresh", "Delicious", "Amazing"… | "Delicious ramen bowls" |
| No alcohol | Title can't reference alcohol | "Wine and cheese pairings" |
| Food tag count | food_type list must have 5–15 items | Only 3 food tags listed |
| Food tag format | Each tag must be 2–3 words | Single-word tags like "pizza" or 4-word tags |
| Cuisine tag count | cuisine_type list must have ≤ 3 items | 5 cuisine tags listed |

**Score = fraction of checks passed**, averaged across all 10 carousels.

---

## The Composite Score

All 7 metrics are combined into a single **composite quality score** between 0 and 1:

| Metric | Weight | Why this weight? |
|---|---|---|
| MMS (R1) | 20% | Core relevance signal — most predictive of user satisfaction |
| SR@5 (R2) | 15% | Coverage completeness for the top 5 carousels |
| CCR (R3) | 15% | Cuisine-level alignment — interpretable for debugging |
| ILD (D1) | 10% | Structural diversity of the carousel set |
| OHCD (D2) | 10% | Grounded diversity against user taste breadth |
| TMC (Q1) | 15% | Internal consistency — affects actual retrieval quality |
| FCS (Q2) | 15% | Rule compliance — catches systematic LLM failures |

> Weights are configurable. These starting values reflect our current best guess; we will tune them as we gather data on which metrics best predict downstream click-through and order rates.

---

## How to Read the Results

### Good carousel set (composite ≈ 0.8)
```
Consumer 12345, weekday_lunch

MMS:    0.82   ✓  Ordered items are well-covered by carousels
SR@5:   0.90   ✓  90% of items have a match in the top 5 carousels
CCR:    1.00   ✓  All cuisine families represented
ILD:    0.55   ✓  Healthy diversity across carousels
OHCD:   0.80   ✓  8 of 10 carousels serve distinct interests
TMC:    0.88   ✓  Titles and food tags are aligned
FCS:    0.96   ✓  Format rules mostly followed

Composite: 0.86 ✓
```

### Problematic carousel set (composite ≈ 0.35)
```
Consumer 99999, weekday_dinner

MMS:    0.31   ✗  Carousels don't match what consumer orders
SR@5:   0.20   ✗  Only 20% of items have a match
CCR:    0.17   ✗  Only 1 of 6 cuisine families covered
ILD:    0.22   ✗  Carousels are very similar to each other
OHCD:   0.20   ✗  Only 2 of 10 carousels serve distinct interests
TMC:    0.61   ~  Acceptable title-tag alignment
FCS:    0.89   ✓  Format is fine

Composite: 0.35 ✗  → Investigate profile quality or prompt behavior
```

---

## What Can Go Wrong (And What Each Metric Catches)

| Problem | Caught By |
|---|---|
| LLM generates carousels for a cuisine the consumer never orders | MMS, SR@K, CCR |
| All 10 carousels are slight variations of the same food (e.g., all Italian) | ILD, OHCD, CCR |
| Title says "Late night snacks" but food tags are all breakfast items | TMC |
| LLM ignores the 5-word title limit or uses "Fresh" / "Delicious" | FCS |
| Consumer has diverse tastes but all carousels cluster on one interest | OHCD |
| Consumer's secondary cuisine interests are never represented | SR@10 vs SR@3 gap |

---

## Key Facts for Stakeholders

- **Scale**: Runs on up to 100,000 consumer/meal-period combinations per evaluation job.
- **Deterministic**: The same input always produces the same scores — no randomness. Safe to rerun for debugging.
- **No API cost**: Uses a lightweight open-source embedding model (`all-MiniLM-L6-v2`). Does not call OpenAI/Vertex/Claude for evaluation.
- **Fast**: Full evaluation on 100k consumer/daypart pairs completes in ~15–20 minutes on a standard Databricks cluster.
- **Ground truth**: Based on actual order history (past 90 days, same meal period). Not LLM-as-judge.
- **Extensible**: The same metrics can be computed against other data sources in the future (e.g., store engagement, search queries, saved stores) without changing the metric logic.
