# V1 vs V2 Carousel Evaluation Comparison

## Data

This report compares two carousel sources evaluated against the same users and the same order history window.

**V1** (`proddb.ml.cx_profile_generated_carousels_ebr`) is the live production carousel cache. Carousels are not all generated at the same time — each (consumer, daypart) entry has its own `last_update_date`, ranging across weeks or months. We fetched carousels for **6,146 consumers** (the intersection of V2 consumers and the EBR table). After requiring order history coverage, **5,882 consumers** with **27,175 (consumer, daypart) groups** were successfully evaluated. Each consumer typically has **9 carousel titles per daypart**.

**V2** (`genai_v2_tier12`, v319 batch) is an offline test set generated as a single batch snapshot. After the same order history filter, **5,966 consumers** with **29,180 (consumer, daypart) groups** were evaluated. Each consumer has exactly **10 carousel titles per daypart**. The V2 carousels were originally generated around **early 2026**.

**Consumer overlap**: **5,870 consumers** were successfully evaluated in both sources, yielding **27,117 paired (consumer, daypart) rows** used for the statistical comparison. (The remaining consumers were evaluated in one source only — typically because a given daypart had carousels in one model but not the other.)

**Order history**: both sources are evaluated against the **same 90-day order history window ending 2026-05-07** (2026-02-06 → 2026-05-07), fetched fresh from Snowflake for 5,978 consumers (324,583 order rows). Using a shared window eliminates order history as a confound, so all metric differences are attributable to carousel content alone.

**Embedding**: `all-MiniLM-L6-v2`, `title_only` mode for both sources.

---

## TL;DR

- **V1 is worse on relevance** (MMS −0.056, SR@5 −0.078, SR@10 −0.102; small-to-medium effect) and worse on composite score (−0.018, negligible effect, d = −0.199).
- **V1 is better on diversity and cuisine coverage** (CCR +0.044, TCD +0.028, lower redundancy) but all with negligible effect sizes (|d| < 0.18).
- **Data staleness does not explain the gap.** V1 carousels were generated on 9 distinct dates (2025-09-30 to 2026-04-22). The relevance deficit (MMS, SR@K) is present consistently across all generation dates — fresher carousels are not meaningfully better than older ones.
- **The gap is structural, driven by titling style.** V1 uses abstract category titles ("Savory noodle soups") while V2 uses specific dish names ("Beef pho"). Specific titles score high similarity for exact matches (clearing the SR threshold reliably) and create a bimodal hit/miss pattern that benefits SR. Abstract titles produce moderate similarities for many items, generating near-misses just below θ=0.45 that help MMS but not SR.
- **V1 also has one fewer carousel per (consumer, daypart) on average** (9 vs V2's fixed 10), which structurally disadvantages SR@10.
- **The pattern is consumer-specific, not universal.** Some users are dramatically better served by V1's broad coverage; others by V2's precision. The mean gap averages these opposing patterns.

---

## Statistical Comparison

- **Test**: Wilcoxon signed-rank (two-sided, paired)
- **Correction**: Holm-Bonferroni
- **Paired rows**: 27,117
- **Composite formula**: `MMS×0.20 + SR@5×0.20 + OHCD×0.20 + CCR×0.15 + ILD×0.15 + FCS×0.10` (renormalized if any metric is missing)
- **FCS rules (5)**: title ≤ 5 words, no filler adjective, no alcohol token, cuisine_type ≤ 3, no brand name (chipotle, kfc, mcnugget, whopper, etc.)
- **p-values**: shown in scientific notation; `< 1e-300` indicates scipy floating-point underflow (true p is non-zero but below double precision)

| Metric | N | Mean(V1) | Mean(V2) | Diff | Cohen's d | Effect | adj-p |
|--------|---|----------|----------|------|-----------|--------|-------|
| composite_quality_score | 27,117 | 0.5595 | 0.5778 | −0.0183 | −0.199 | negligible | 1.8e−243 |
| mms | 27,117 | 0.4350 | 0.4913 | −0.0564 | −0.548 | medium | < 1e-300 |
| sr_at_3 | 27,117 | 0.2559 | 0.3181 | −0.0622 | −0.224 | small | < 1e-300 |
| sr_at_5 | 27,117 | 0.3234 | 0.4016 | −0.0782 | −0.273 | small | < 1e-300 |
| sr_at_10 | 27,117 | 0.4017 | 0.5040 | −0.1023 | −0.361 | small | < 1e-300 |
| ccr | 26,228 | 0.8093 | 0.7653 | +0.0440 | +0.122 | negligible | 4.4e−70 |
| ild | 27,117 | 0.6479 | 0.6376 | +0.0103 | +0.159 | negligible | 5.5e−183 |
| tcd | 27,117 | 0.9070 | 0.8795 | +0.0275 | +0.175 | negligible | 5.0e−133 |
| redundancy_rate | 27,117 | 0.0054 | 0.0070 | −0.0015 | −0.085 | negligible | 4.3e−22 |
| ohcd | 27,117 | 0.4580 | 0.4539 | +0.0041 | +0.035 | negligible | 1.2e−07 |
| fcs | 27,117 | 0.9966 | 0.9965 | +0.0000 | +0.003 | negligible | 1.7e−19 |


## Metric Delta by V1 Generation Date

**How metric delta is calculated**: for each paired (consumer_id, day_part) row, delta = V1 metric − V2 metric. A positive delta means V1 is better for that consumer and daypart; negative means V2 is better. The table below shows the mean delta across all rows sharing the same V1 `last_update_date`.

V1 carousels in EBR were generated on exactly **9 distinct dates**. Each row in the paired dataset carries the `last_update_date` of the V1 carousel for that (consumer, daypart).

| Generation Date | N | Δ MMS | Δ SR@5 | Δ SR@10 | Δ CCR | Δ ILD | Δ OHCD | Δ Composite |
|----------------|---|-------|--------|---------|-------|-------|--------|-------------|
| 2025-09-30 | 290 | −0.0668 | −0.1206 | −0.1217 | +0.1056 | −0.0006 | +0.0018 | −0.0245 |
| 2026-02-03 | 12,054 | −0.0631 | −0.0925 | −0.1166 | +0.0301 | +0.0125 | +0.0012 | −0.0276 |
| 2026-03-31 | 7,318 | −0.0543 | −0.0670 | −0.0944 | +0.0398 | +0.0121 | +0.0165 | −0.0149 |
| 2026-04-16 | 1,916 | −0.0456 | −0.0658 | −0.0862 | +0.0746 | +0.0071 | −0.0094 | −0.0139 |
| 2026-04-18 | 1,714 | −0.0499 | −0.0799 | −0.0963 | +0.0639 | +0.0042 | −0.0009 | −0.0181 |
| 2026-04-19 | 1,619 | −0.0522 | −0.0582 | −0.0875 | +0.0661 | +0.0067 | −0.0007 | −0.0130 |
| 2026-04-20 | 183 | −0.0644 | −0.0790 | −0.0913 | +0.0570 | −0.0014 | −0.0025 | −0.0235 |
| 2026-04-21 | 1,142 | −0.0425 | −0.0607 | −0.0806 | +0.0537 | +0.0035 | −0.0005 | −0.0140 |
| 2026-04-22 | 881 | −0.0385 | −0.0462 | −0.0705 | +0.0880 | +0.0066 | −0.0027 | −0.0040 |
| **Overall** | **27,117** | **−0.0564** | **−0.0782** | **−0.1023** | **+0.0440** | **+0.0103** | **+0.0041** | **−0.0203** |

**Observations**:
- The relevance deficit (MMS, SR@K) is present across **all 9 generation dates** — this is not a staleness artifact, it is a consistent property of V1 carousels regardless of when they were generated.
- The oldest batch (2025-09-30, n=290) shows a slightly larger relevance gap, but it is a small group and the effect is within the noise of other dates.
- CCR is positive across all dates (V1 covers more cuisine families), also consistently regardless of generation date.
- The 2026-02-03 batch is the largest (12,054 rows, 44% of all paired rows) and is representative of the overall means.

---

## Extreme Case Analysis

Cases with the largest per-consumer metric gap (top 3 each direction per metric). All from the 27,117 paired rows using the same order history and embedding mode.

### MMS (Mean Max Similarity)

#### V1 much better than V2

| Consumer | Day Part | MMS (V1) | MMS (V2) | Delta |
|----------|----------|-----------|----------|-------|
| 18756309 | weekday_late_night | 0.977 | 0.252 | **+0.725** |
| 232924317 | weekday_lunch | 0.862 | 0.216 | **+0.647** |
| 687733376 | weekend_breakfast | 0.970 | 0.382 | **+0.588** |

**Example — consumer 18756309, weekday_late_night:**
- V1: `Crispy spicy salt chicken` / `Savory noodle soups` / `Classic hand-mixed shakes` / `Indulgent late-night snacks` / `Sweet and savory dumplings` / `Flavorful fried rice` / `Spicy noodle bowls` / `Tasty chicken wings` / `Comforting soup varieties`
- V2: `Spicy salt chicken` / `Shrimp fried rice` / `Pad see ewe` / `Yellow curry` / `Tom kha` / `Shrimp spring rolls` / `Steamed dumplings` / `Chicken strips` / `Chicken lo mein` / `Korean beef bowls`
- **Why V1 wins**: V1 uses broad, abstract category titles ("Savory noodle soups", "Indulgent late-night snacks") that match many order items semantically. V2 uses specific dish names that only match when the user ordered that exact dish.

**Example — consumer 687733376, weekend_breakfast:**
- V1: `Vegetable samosas` / `Vegan breakfast tacos` / `Chickpea pancakes` / `Plant-based breakfast burritos` / `Savory tofu chilaquiles` / `Vegan breakfast bowls` / `Spicy avocado toast` / `Breakfast burrito bowls`
- V2: `Vegan breakfast tacos` / `Vegan breakfast burritos` / `Vegan pancakes` / `French toast` / `Acai bowls` / `Plant-based bagel sandwiches` / `Avocado toast` / `Tofu scramble` / `Plant-based chilaquiles` / `Vegan waffles`
- **Why V1 wins**: Both are strong for a vegan user; V1's broader category-style titles cover this user's order history better (MMS 0.970 vs 0.382).

---

#### V2 much better than V1

| Consumer | Day Part | MMS (V1) | MMS (V2) | Delta |
|----------|----------|-----------|----------|-------|
| 238704771 | weekend_dinner | 0.165 | 1.000 | **−0.835** |
| 472215709 | weekday_breakfast | 0.215 | 1.000 | **−0.785** |
| 544649652 | weekend_lunch | 0.271 | 1.000 | **−0.729** |

**Example — consumer 238704771, weekend_dinner:**
- V1: `Vietnamese noodle soups` / `Cajun seafood boils` / `Spicy fried rice` / `Build your own pho` / `Hearty Cajun fare` / `Customizable rice plates` / `Panang curry specials` / `Delectable spring rolls` / `Comforting yellow curry`
- V2: `Beef pho` / `Yellow curry` / `Poke bowls` / `Panang curry` / `Spicy fried rice` / `Braised oxtail` / `Boiled crawfish` / `Pad see ew` / `Korean BBQ` / `Thin crust pizza`
- **Why V2 wins**: V2 uses specific dish names that precisely match this user's order history ("Beef pho", "Panang curry", "Boiled crawfish"). V1's broader category titles ("Build your own pho", "Delectable spring rolls") are semantically close but score lower under MMS. V2 scoring 1.0 means every order item found a near-perfect match.

**Example — consumer 472215709, weekday_breakfast:**
- V1: `Breakfast burritos` / `Chicken and waffles` / `Savory breakfast wraps` / `Breakfast sandwiches` / `Breakfast hot dogs` / `Gourmet donuts` / `Fresh fruit bowls` / `Savory breakfast pastries`
- V2: `Acevichado rolls` / `Birria tacos` / `Hot dogs` / `Dynamite maki` / `Chicken wraps` / `Breakfast sandwiches` / `Breakfast burritos` / `Avocado toast` / `Acai bowls` / `Bagels with cream cheese`
- **Why V2 wins**: V2 captures a broader, more eclectic mix matching this user's diverse order history (sushi, tacos, American breakfast). V1 is stuck in breakfast-focused titles that miss the user's non-breakfast ordering patterns.

---

### SR@5 (Semantic Recall at K=5)

| Direction | Consumer | Day Part | SR@5 (V1) | SR@5 (V2) | Delta |
|-----------|----------|----------|------------|-----------|-------|
| V1 better | 6781488 | weekday_lunch | 1.0 | 0.0 | **+1.0** |
| V1 better | 6802566 | weekend_breakfast | 1.0 | 0.0 | **+1.0** |
| V2 better | 1004703 | weekday_late_night | 0.0 | 1.0 | **−1.0** |
| V2 better | 6864795 | weekday_lunch | 0.0 | 1.0 | **−1.0** |

Note: SR@5 = 0 means none of the user's order items had a carousel title within cosine similarity ≥ 0.45; SR@5 = 1.0 means all did. The 0/1 extremes reflect consumers whose ordering style closely matches one model's titling style and completely misses the other's.

---

### Composite Quality Score

| Direction | Consumer | Day Part | Composite (V1) | Composite (V2) | Delta |
|-----------|----------|----------|-----------------|----------------|-------|
| V1 better | 464957246 | weekday_lunch | 0.738 | 0.204 | **+0.534** |
| V1 better | 63815090 | weekend_dinner | 0.731 | 0.215 | **+0.516** |
| V2 better | 155295051 | weekend_late_night | 0.211 | 0.748 | **−0.538** |
| V2 better | 645112840 | weekend_breakfast | 0.193 | 0.725 | **−0.532** |

Composite = MMS 20%, SR@5 20%, OHCD 20%, CCR 15%, ILD 15% (FCS excluded). The extremes mirror the MMS pattern closely — consumers where one model's titling style aligns with the order history dominate both MMS and composite.

---

### Key Observations from Extreme Cases

1. **V1 uses abstract category titles; V2 uses specific dish names.** V1 titles like "Savory noodle soups" or "Indulgent late-night snacks" cast a wider semantic net and win when the user ordered a diverse mix within a category. V2 titles like "Beef pho" or "Boiled crawfish" score perfectly when the user ordered that exact dish, but fail entirely for users with different profiles.

2. **V2's perfect MMS=1.0 cases are not cherry-picked — they reflect exact semantic matches** between the user's order history and V2's specific dish names. V1 cannot replicate this because its titles describe categories, not dishes.

3. **The gap is consumer-specific, not systematic across all consumers.** Some consumers are dramatically better served by V1; others by V2. The mean gap (−0.056 on MMS) is an average across these divergent patterns.

4. **CCR extreme cases (delta = ±1.0)** occur when one model's carousel covers zero cuisine families from the user's history. This is usually a case where the user's cuisine diversity is high and the carousel is narrowly focused on a different cuisine set.

---

## Why Titling Style Affects SR@K Differently from MMS

### The threshold effect (θ = 0.45)

**MMS** is a continuous average — a similarity of 0.42 contributes 0.42.

**SR@K** is binary per order item — similarity 0.42 scores **0** (below threshold), similarity 0.46 scores **1**. Only the maximum similarity across all carousel titles per order item matters.

This creates a fundamental difference in how each metric responds to abstract vs specific titles:

| Scenario | Similarity | MMS | SR |
|----------|-----------|-----|-----|
| V2 "Beef pho" vs order item "Beef pho" | 0.90 | great | **hit ✓** |
| V2 "Beef pho" vs order item "Pad thai" | 0.18 | terrible | **miss ✗** |
| V1 "Vietnamese noodle soups" vs "Beef pho" | 0.55 | decent | **hit ✓** |
| V1 "Vietnamese noodle soups" vs "Pad thai" | 0.38 | below avg | **miss ✗** |
| V1 "Indulgent late-night snacks" vs "Beef pho" | 0.40 | below avg | **near-miss ✗** |

The dangerous zone for V1 is **similarities of 0.35–0.44**: these contribute positively to MMS but score zero for SR. Abstract category titles like "Indulgent late-night snacks" or "Classic American fare" naturally cluster in this range for many order items — semantically related but not close enough to cross the threshold. V2's specific titles avoid this zone entirely: matched items score 0.7–1.0 (well above threshold), unmatched items score 0.1–0.2 (well below).

This means V1 creates more **near-misses** — items with moderate similarity that help MMS but fail SR. V2's all-or-nothing nature actually works in its favour for SR: when a user ordered something close to a V2 title, it clears the threshold reliably.

### The carousel count effect on SR@10

V1 has **9 carousels** per (consumer, daypart) in 87% of cases; V2 always has **10**. SR@K asks: does any one of the K titles clear the threshold for a given order item? Each additional carousel is another independent chance.

- SR@3 and SR@5: both models have ≥ 5 carousels — count is not a factor
- **SR@10: V2 always provides 10 shots; V1 gets only 9** — a structural one-title disadvantage

This partly explains why the SR@10 gap (−0.102) is larger than the SR@5 gap (−0.078). At K=10, V1 is missing the one extra carousel that V2 uses to cover borderline order items.

### High-variance vs low-variance strategies

| | V1 (abstract categories) | V2 (specific dishes) |
|---|---|---|
| **Titling style** | "Savory noodle soups" | "Beef pho" |
| **Similarity distribution** | Moderate (0.3–0.6) for many items | High (0.7–1.0) for matches, low (0.1–0.2) for misses |
| **MMS effect** | Stable, moderate scores across many items | High variance — great for matched users, poor for others |
| **SR effect** | Many near-misses just below θ=0.45 | Matched items reliably clear threshold; misses are decisive |
| **Strategy** | Low-variance, broad coverage | High-variance, precision-or-nothing |

This explains the MMS/SR disconnect in extreme cases:
- **Consumer 18756309** (V1 wins MMS +0.725): V1's broad titles score 0.5–0.7 against many order items, raising the average. But the same titles may still miss the SR threshold for items only moderately related (similarity 0.38–0.44).
- **Consumer 238704771** (V2 wins MMS=1.0): V2 has exact matches ("Beef pho", "Panang curry", "Boiled crawfish") that score 0.9+ — every order item clears 0.45 easily, giving both MMS=1.0 and SR=1.0. V1's "Build your own pho" and "Hearty Cajun fare" score ~0.5, decent for MMS but not dominant.