# Similarity Threshold Calibration

Empirical reference for the two cosine-similarity thresholds used in the
diversity metrics:

- **RR (Redundancy Rate)** flags title pairs with cosine sim ≥ **0.75** as "near-duplicates"
- **TCD (Title Cluster Diversity)** groups titles into the same cluster when cosine sim ≥ **0.65**

All numbers below are real `all-MiniLM-L6-v2` cosine similarities on titles
drawn from `low_diversity_examples.md`.

---

## RR threshold (0.75) — what gets flagged as a near-duplicate

### Pairs that ARE flagged (sim ≥ 0.75)

| Title A | Title B | cos sim |
| --- | --- | ---: |
| Spicy chicken sandwiches | Spicy chicken sandwich meals | **0.927** |
| Chicken nugget meals | Chicken nugget happy meals | **0.898** |
| Meat lover burritos | Meat lover's breakfast burritos | **0.877** |
| Chicken sandwiches | BBQ chicken sandwiches | **0.867** |
| Chicken nuggets | Chicken nugget meals | **0.863** |
| Chicken sandwiches | Chicken sandwich meals | **0.860** |
| Sausage breakfast burritos | Bacon breakfast burritos | **0.851** |
| Chicken sandwiches | Spicy chicken sandwiches | **0.831** |
| Chicken nuggets | Chicken nugget happy meals | **0.829** |
| Beef burgers | Triple meat burgers | **0.818** |
| Sausage breakfast burritos | Sausage breakfast sandwiches | **0.816** |
| Big Mac burgers | Big Mac meals | **0.800** |
| Steak and egg burritos | Chorizo and egg burritos | **0.790** |
| Sausage breakfast burritos | Sausage breakfast crunchwraps | **0.775** |
| Bacon breakfast burritos | Bacon breakfast quesadillas | **0.761** |

### Pairs that are NOT flagged (sim < 0.75)

| Title A | Title B | cos sim |
| --- | --- | ---: |
| Chicken sandwiches | Chicken wings | 0.710 |
| Chicken nuggets | Chicken wings | 0.630 |
| Chicken nuggets | Chicken strips | 0.608 |
| Chicken nuggets | Chicken tenders | 0.588 |
| Orange chicken | Chicken stir-fry | 0.583 |
| Pad thai | Pad see ew | 0.460 |
| Sausage breakfast burritos | Onion rings | 0.346 |
| Chicken nuggets | Cheese pizza | 0.339 |
| Chicken wings | French toast sticks | 0.279 |
| Pad thai | Big Mac meals | 0.275 |

### What 0.75 captures

- **Same base noun, different modifier** (Big Mac burgers / Big Mac meals → 0.800): caught.
- **Same protein + format with tiny word variation** (Chicken nugget meals / Chicken nugget happy meals → 0.898): caught.
- **Different format, same protein-and-occasion** (Sausage breakfast burritos / Sausage breakfast sandwiches → 0.816): caught — these are arguably distinct dishes, so 0.75 is on the strict side here.
- **Different protein, same format/occasion** (Sausage breakfast burritos / Bacon breakfast burritos → 0.851): caught — model can't always tell sausage from bacon in this context.
- **Same protein, different format** (Chicken nuggets / Chicken wings → 0.630): NOT caught — these are treated as legitimately different.
- **Different cuisine, same protein** (Orange chicken / Chicken stir-fry → 0.583): NOT caught.

### Calibration takeaway

0.75 is a reasonable knee in the distribution:
- Pairs ≥ 0.75 are mostly recognizable as "the same item with a different word."
- Pairs in 0.60–0.75 are "related but different items" (nuggets vs wings, strips vs tenders).
- Pairs below 0.60 are unambiguously different foods.

A stricter 0.80 cutoff would miss the "burritos / crunchwraps" type pairs which read as duplicates to a human; a looser 0.70 cutoff would start flagging "Chicken wings / Chicken sandwiches" as duplicates which they aren't.

---

## TCD threshold (0.65) — what counts as "one cluster"

Primary worked example: consumer `42259697` / weekday_late_night / `no_rationale_think_1024`. This carousel set scores **TCD = 0.700** in the report (7 clusters for 10 titles) — a typical "moderate diversity" case where the cluster boundaries map cleanly onto food categories. Reproduces exactly with the algorithm.

### The 10 titles

| # | Title |
| --- | --- |
| 1 | Carnitas burrito bowls |
| 2 | Carnitas burritos |
| 3 | Carnitas quesadillas |
| 4 | Grilled fish feasts |
| 5 | Hibachi steak |
| 6 | Sunset strip rolls |
| 7 | Greek salads |
| 8 | Cookie packs |
| 9 | Pepperoni pizza |
| 10 | Margherita pizza |

### Pairwise cosine matrix (upper triangle, * = edge above 0.65)

```
          1     2     3     4     5     6     7     8     9    10
  1:      . 0.86* 0.62  0.34  0.26  0.13  0.30  0.21  0.33  0.32
  2:      .     . 0.73* 0.37  0.31  0.09  0.26  0.26  0.39  0.38
  3:      .     .     . 0.29  0.27  0.13  0.25  0.19  0.27  0.39
  4:      .     .     .     . 0.35  0.20  0.25  0.23  0.26  0.26
  5:      .     .     .     .     . 0.12  0.26  0.06  0.32  0.37
  6:      .     .     .     .     .     . 0.24  0.31  0.28  0.28
  7:      .     .     .     .     .     .     . 0.19  0.28  0.36
  8:      .     .     .     .     .     .     .     . 0.25  0.20
  9:      .     .     .     .     .     .     .     .     . 0.67*
 10:      .     .     .     .     .     .     .     .     .
```

### Resulting clusters (7 components)

| Cluster | Members | Bridging edges (≥ 0.65) |
| --- | --- | --- |
| **1 — Carnitas trio** | Carnitas burrito bowls, Carnitas burritos, Carnitas quesadillas | bowls↔burritos 0.857, burritos↔quesadillas 0.726 |
| **2 — Pizza pair** | Pepperoni pizza, Margherita pizza | pepperoni↔margherita 0.670 (just over threshold) |
| 3 (singleton) | Grilled fish feasts | — |
| 4 (singleton) | Hibachi steak | — |
| 5 (singleton) | Sunset strip rolls | — |
| 6 (singleton) | Greek salads | — |
| 7 (singleton) | Cookie packs | — |

TCD = 7 / 10 = **0.700**, matching the reported value.

### What "one cluster" means in practice

- **Variations of the same dish merge.** "Carnitas burrito bowls" / "Carnitas burritos" / "Carnitas quesadillas" → 1 cluster. All three share "carnitas" as the protein and feel like the same recommendation slot from a user perspective.
- **Same dish category across styles also merges.** "Pepperoni pizza" vs "Margherita pizza" sits right at 0.67 — different toppings but still recognizably the same dish slot. 0.65 catches this; a stricter 0.75 would not.
- **Items from genuinely different food categories stay separate**, even when both contain protein words like "chicken" or "steak" — the singletons here span Greek, Japanese hibachi, sushi-style rolls, fish feasts, and cookies.

### Contrast — extreme low diversity (TCD = 0.300)

For comparison, consumer `1452374422` / weekday_dinner produces TCD = 0.300 because 8 of 10 chicken-based titles transitively merge into a single cluster:

> Chicken nugget meals · Chicken nuggets · Chicken nugget happy meals · Spicy chicken sandwich meals · Chicken sandwiches · Spicy chicken sandwiches · Chicken sandwich meals · Chicken wings

The bridging edge that brings Chicken wings into the chicken cluster is its similarity to "Chicken sandwiches" (0.710) — without that edge, wings would be a singleton and TCD would rise to 0.400. This is why TCD can drop sharply when a consumer's history is narrow: a few near-duplicate titles cascade through transitive linkage.

### Calibration takeaway

- **0.65 catches "same dish, different presentation"** (carnitas variants, pizza styles) without fusing genuinely different foods.
- A **stricter 0.75 threshold** would leave Pepperoni/Margherita as 2 singletons (sim 0.67) and split the carnitas trio (burritos↔quesadillas sits at 0.726), which would overstate diversity for repetitive carousels.
- A **looser 0.55 threshold** would start fusing items like Carnitas burrito bowls + Carnitas quesadillas with anything containing "burrito" or "Mexican" — understating diversity.

---

## Reproducing

Script: `/tmp/threshold_calibration.py` (uses `all-MiniLM-L6-v2`, same model as the eval pipeline).
