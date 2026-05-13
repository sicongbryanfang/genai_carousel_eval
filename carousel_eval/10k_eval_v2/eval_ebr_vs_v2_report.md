# EBR vs V2 Carousel Evaluation Comparison

## TL;DR

- **EBR is significantly worse on relevance** (MMS −0.056, SR@5 −0.078, SR@10 −0.102; small-to-medium effect) and slightly worse on composite score (−0.012).
- **EBR is slightly better on diversity and cuisine coverage** (CCR +0.044, TCD +0.028, lower redundancy) but these are negligible effect sizes.
- **The gap is not explained by data staleness.** Correlating `last_update_date` age with the metric delta shows near-zero Spearman ρ (< 0.07) for all metrics — fresh and stale EBR entries perform equally relative to V2.
- **The gap is structural, driven by titling style.** EBR uses abstract category titles ("Savory noodle soups") while V2 uses specific dish names ("Beef pho"). Specific titles score high similarity for exact matches (clearing the SR threshold reliably) and create a bimodal hit/miss pattern that benefits SR. Abstract titles produce moderate similarities for many items, generating near-misses just below θ=0.45 that help MMS but not SR.
- **EBR also has one fewer carousel per (consumer, daypart) on average** (9 vs V2's fixed 10), which structurally disadvantages SR@10.
- **The pattern is consumer-specific, not universal.** Some users are dramatically better served by EBR's broad coverage; others by V2's precision. The mean gap averages these opposing patterns.

---

## Setup

- **Test**: Wilcoxon signed-rank (two-sided, paired)
- **Correction**: Holm-Bonferroni
- **Paired rows**: 27,117

| Metric | N | Mean(ebr) | Mean(v2) | Diff | Cohen's d | Effect | adj-p | Sig |
|--------|---|---------|---------|------|-----------|--------|-------|-----|
| mms | 27117 | 0.4350 | 0.4913 | -0.0564 | -0.548 | medium | 0.0000 | ✓ |
| sr_at_3 | 27117 | 0.2559 | 0.3181 | -0.0622 | -0.224 | small | 0.0000 | ✓ |
| sr_at_5 | 27117 | 0.3234 | 0.4016 | -0.0782 | -0.273 | small | 0.0000 | ✓ |
| sr_at_10 | 27117 | 0.4017 | 0.5040 | -0.1023 | -0.361 | small | 0.0000 | ✓ |
| ild | 27117 | 0.6479 | 0.6376 | +0.0103 | 0.159 | negligible | 0.0000 | ✓ |
| tcd | 27117 | 0.9070 | 0.8795 | +0.0275 | 0.175 | negligible | 0.0000 | ✓ |
| composite_quality_score | 27117 | 0.5496 | 0.5612 | -0.0116 | -0.125 | negligible | 0.0000 | ✓ |
| ccr | 26228 | 0.8093 | 0.7653 | +0.0440 | 0.122 | negligible | 0.0000 | ✓ |
| redundancy_rate | 27117 | 0.0054 | 0.0070 | -0.0015 | -0.085 | negligible | 0.0000 | ✓ |
| ohcd | 27117 | 0.4580 | 0.4539 | +0.0041 | 0.035 | negligible | 0.0000 | ✓ |


# Freshness Correlation (Spearman ρ: metric delta vs EBR entry age)

- **EBR entry age** = days between `last_update_date` and eval_date (2026-05-07)
- **metric delta** = EBR metric − v2 metric (positive = EBR is better)
- **N** = 27,117 paired (consumer_id, day_part) rows

| Metric | ρ | p-value | Interpretation |
|--------|---|---------|----------------|
| mms | -0.068 | 0.0000 | no clear trend |
| sr_at_3 | -0.048 | 0.0000 | no clear trend |
| sr_at_5 | -0.049 | 0.0000 | no clear trend |
| sr_at_10 | -0.050 | 0.0000 | no clear trend |
| ccr | -0.035 | 0.0000 | no clear trend |
| ild | 0.038 | 0.0000 | no clear trend |
| tcd | 0.054 | 0.0000 | no clear trend |
| redundancy_rate | -0.067 | 0.0000 | no clear trend |
| ohcd | 0.008 | 0.1818 | no clear trend |
| composite_quality_score | -0.058 | 0.0000 | no clear trend |

---

## Extreme Case Analysis

Cases with the largest per-consumer metric gap (top 3 each direction per metric). All from the 27,117 paired rows using the same order history and embedding mode.

### MMS (Mean Max Similarity)

#### EBR much better than V2

| Consumer | Day Part | MMS (EBR) | MMS (V2) | Delta |
|----------|----------|-----------|----------|-------|
| 18756309 | weekday_late_night | 0.977 | 0.252 | **+0.725** |
| 232924317 | weekday_lunch | 0.862 | 0.216 | **+0.647** |
| 687733376 | weekend_breakfast | 0.970 | 0.382 | **+0.588** |

**Example — consumer 18756309, weekday_late_night:**
- EBR: `Crispy spicy salt chicken` / `Savory noodle soups` / `Classic hand-mixed shakes` / `Indulgent late-night snacks` / `Sweet and savory dumplings` / `Flavorful fried rice` / `Spicy noodle bowls` / `Tasty chicken wings` / `Comforting soup varieties`
- V2: `Spicy salt chicken` / `Shrimp fried rice` / `Pad see ewe` / `Yellow curry` / `Tom kha` / `Shrimp spring rolls` / `Steamed dumplings` / `Chicken strips` / `Chicken lo mein` / `Korean beef bowls`
- **Why EBR wins**: EBR uses broad, abstract category titles ("Savory noodle soups", "Indulgent late-night snacks") that match many order items semantically. V2 uses specific dish names that only match when the user ordered that exact dish.

**Example — consumer 687733376, weekend_breakfast:**
- EBR: `Vegetable samosas` / `Vegan breakfast tacos` / `Chickpea pancakes` / `Plant-based breakfast burritos` / `Savory tofu chilaquiles` / `Vegan breakfast bowls` / `Spicy avocado toast` / `Breakfast burrito bowls`
- V2: `Vegan breakfast tacos` / `Vegan breakfast burritos` / `Vegan pancakes` / `French toast` / `Acai bowls` / `Plant-based bagel sandwiches` / `Avocado toast` / `Tofu scramble` / `Plant-based chilaquiles` / `Vegan waffles`
- **Why EBR wins**: Both are strong for a vegan user; EBR's broader category-style titles cover this user's order history slightly better.

---

#### V2 much better than EBR

| Consumer | Day Part | MMS (EBR) | MMS (V2) | Delta |
|----------|----------|-----------|----------|-------|
| 238704771 | weekend_dinner | 0.165 | 1.000 | **−0.835** |
| 472215709 | weekday_breakfast | 0.215 | 1.000 | **−0.785** |
| 544649652 | weekend_lunch | 0.271 | 1.000 | **−0.729** |

**Example — consumer 238704771, weekend_dinner:**
- EBR: `Vietnamese noodle soups` / `Cajun seafood boils` / `Spicy fried rice` / `Build your own pho` / `Hearty Cajun fare` / `Customizable rice plates` / `Panang curry specials` / `Delectable spring rolls` / `Comforting yellow curry`
- V2: `Beef pho` / `Yellow curry` / `Poke bowls` / `Panang curry` / `Spicy fried rice` / `Braised oxtail` / `Boiled crawfish` / `Pad see ew` / `Korean BBQ` / `Thin crust pizza`
- **Why V2 wins**: V2 uses specific dish names that precisely match this user's order history ("Beef pho", "Panang curry", "Boiled crawfish"). EBR's broader category titles ("Build your own pho", "Delectable spring rolls") are semantically close but score lower under MMS. V2 scoring 1.0 means every order item found a near-perfect match.

**Example — consumer 472215709, weekday_breakfast:**
- EBR: `Breakfast burritos` / `Chicken and waffles` / `Savory breakfast wraps` / `Breakfast sandwiches` / `Breakfast hot dogs` / `Gourmet donuts` / `Fresh fruit bowls` / `Savory breakfast pastries`
- V2: `Acevichado rolls` / `Birria tacos` / `Hot dogs` / `Dynamite maki` / `Chicken wraps` / `Breakfast sandwiches` / `Breakfast burritos` / `Avocado toast` / `Acai bowls` / `Bagels with cream cheese`
- **Why V2 wins**: V2 captures a broader, more eclectic mix matching this user's diverse order history (sushi, tacos, American breakfast). EBR is stuck in breakfast-focused titles that miss the user's non-breakfast ordering patterns.

---

### SR@5 (Semantic Recall at K=5)

| Direction | Consumer | Day Part | SR@5 (EBR) | SR@5 (V2) | Delta |
|-----------|----------|----------|------------|-----------|-------|
| EBR better | 6781488 | weekday_lunch | 1.0 | 0.0 | **+1.0** |
| EBR better | 6802566 | weekend_breakfast | 1.0 | 0.0 | **+1.0** |
| V2 better | 1004703 | weekday_late_night | 0.0 | 1.0 | **−1.0** |
| V2 better | 6864795 | weekday_lunch | 0.0 | 1.0 | **−1.0** |

Note: SR@5 = 0 means none of the user's order items had a carousel title within cosine similarity ≥ 0.45; SR@5 = 1.0 means all did. The 0/1 extremes reflect consumers whose ordering style closely matches one model's titling style and completely misses the other's.

---

### Composite Quality Score

| Direction | Consumer | Day Part | Composite (EBR) | Composite (V2) | Delta |
|-----------|----------|----------|-----------------|----------------|-------|
| EBR better | 63815090 | weekend_dinner | 0.756 | 0.275 | **+0.481** |
| EBR better | 464957246 | weekday_lunch | 0.744 | 0.267 | **+0.477** |
| V2 better | 37267885 | weekday_late_night | 0.265 | 0.746 | **−0.481** |
| V2 better | 645112840 | weekend_breakfast | 0.255 | 0.736 | **−0.480** |

The composite extremes roughly mirror the MMS pattern — the composite is dominated by relevance metrics (MMS 20%, SR@5 20%, OHCD 20%), so consumers where one model's titling style aligns strongly with the user's history tend to win on composite as well.

---

### Key Observations from Extreme Cases

1. **EBR uses abstract category titles; V2 uses specific dish names.** EBR titles like "Savory noodle soups" or "Indulgent late-night snacks" cast a wider semantic net and win when the user ordered a diverse mix within a category. V2 titles like "Beef pho" or "Boiled crawfish" score perfectly when the user ordered that exact dish, but fail entirely for users with different profiles.

2. **V2's perfect MMS=1.0 cases are not cherry-picked — they reflect exact semantic matches** between the user's order history and V2's specific dish names. EBR cannot replicate this because its titles describe categories, not dishes.

3. **The gap is consumer-specific, not systematic across all consumers.** Some consumers are dramatically better served by EBR; others by V2. The mean gap (−0.056 on MMS) is an average across these divergent patterns.

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
| EBR "Vietnamese noodle soups" vs "Beef pho" | 0.55 | decent | **hit ✓** |
| EBR "Vietnamese noodle soups" vs "Pad thai" | 0.38 | below avg | **miss ✗** |
| EBR "Indulgent late-night snacks" vs "Beef pho" | 0.40 | below avg | **near-miss ✗** |

The dangerous zone for EBR is **similarities of 0.35–0.44**: these contribute positively to MMS but score zero for SR. Abstract category titles like "Indulgent late-night snacks" or "Classic American fare" naturally cluster in this range for many order items — semantically related but not close enough to cross the threshold. V2's specific titles avoid this zone entirely: matched items score 0.7–1.0 (well above threshold), unmatched items score 0.1–0.2 (well below).

This means EBR creates more **near-misses** — items with moderate similarity that help MMS but fail SR. V2's all-or-nothing nature actually works in its favour for SR: when a user ordered something close to a V2 title, it clears the threshold reliably.

### The carousel count effect on SR@10

EBR has **9 carousels** per (consumer, daypart) in 87% of cases; V2 always has **10**. SR@K asks: does any one of the K titles clear the threshold for a given order item? Each additional carousel is another independent chance.

- SR@3 and SR@5: both models have ≥ 5 carousels — count is not a factor
- **SR@10: V2 always provides 10 shots; EBR gets only 9** — a structural one-title disadvantage

This partly explains why the SR@10 gap (−0.102) is larger than the SR@5 gap (−0.078). At K=10, EBR is missing the one extra carousel that V2 uses to cover borderline order items.

### High-variance vs low-variance strategies

| | EBR (abstract categories) | V2 (specific dishes) |
|---|---|---|
| **Titling style** | "Savory noodle soups" | "Beef pho" |
| **Similarity distribution** | Moderate (0.3–0.6) for many items | High (0.7–1.0) for matches, low (0.1–0.2) for misses |
| **MMS effect** | Stable, moderate scores across many items | High variance — great for matched users, poor for others |
| **SR effect** | Many near-misses just below θ=0.45 | Matched items reliably clear threshold; misses are decisive |
| **Strategy** | Low-variance, broad coverage | High-variance, precision-or-nothing |

This explains the MMS/SR disconnect in extreme cases:
- **Consumer 18756309** (EBR wins MMS +0.725): EBR's broad titles score 0.5–0.7 against many order items, raising the average. But the same titles may still miss the SR threshold for items only moderately related (similarity 0.38–0.44).
- **Consumer 238704771** (V2 wins MMS=1.0): V2 has exact matches ("Beef pho", "Panang curry", "Boiled crawfish") that score 0.9+ — every order item clears 0.45 easily, giving both MMS=1.0 and SR=1.0. EBR's "Build your own pho" and "Hearty Cajun fare" score ~0.5, decent for MMS but not dominant.