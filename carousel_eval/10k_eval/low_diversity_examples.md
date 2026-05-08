# Low-Diversity Carousel Examples

Consumer+daypart pairs where **both** variants score in the bottom 5% of ILD
(< 0.54). Shown side-by-side to illustrate where each model repeats itself.

- **ILD** (Intra-List Diversity) — mean pairwise title dissimilarity; lower = more repetitive
- **RR** (Redundancy Rate) — fraction of title pairs with similarity ≥ 0.75; higher = more near-duplicates
- **TCD** (Title Cluster Diversity) — fraction of distinct topic clusters; lower = more clustered

---

## consumer `1398034370` — weekend_lunch

| | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| ILD | 0.496 | **0.386** ← worse |
| RR | 0.067 | 0.089 |
| TCD | 0.500 | **0.200** ← worse |

| # | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| 1 | Chicken strips | Chicken nugget meals |
| 2 | Chicken nuggets | Chicken sandwich meals |
| 3 | Chicken sandwiches | Chicken strip meals |
| 4 | Barbeque chicken sandwiches | Orange chicken |
| 5 | Orange chicken | Chicken tenders |
| 6 | Spicy chicken sandwiches | Chicken nuggets |
| 7 | Cheese pizza | Spicy chicken sandwiches |
| 8 | Chicken wings | BBQ chicken sandwiches |
| 9 | Chinese noodles | Fried chicken |
| 10 | Sub sandwiches | Chicken burgers |

**Observation**: Both variants are heavily chicken-focused for this consumer. v2 is worse — 9 of 10 titles contain "chicken", and all 10 use the same "[protein] + [format]" pattern. no_rationale at least breaks out with "Cheese pizza", "Chinese noodles", and "Sub sandwiches".

---

## consumer `34420201` — weekday_breakfast

| | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| ILD | 0.538 | **0.422** ← worse |
| RR | 0.022 | **0.200** ← worse |
| TCD | 0.800 | **0.400** ← worse |

| # | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| 1 | Meat lover burritos | Meat lover's breakfast burritos |
| 2 | Sausage egg croissan'wich | Sausage breakfast sandwiches |
| 3 | Ranch chicken sandwiches | Steak and egg muffins |
| 4 | Meat lover's omelettes | Bacon breakfast sandwiches |
| 5 | Steak egg muffins | Chicken breakfast biscuits |
| 6 | Sausage egg biscuits | Loaded breakfast sandwiches |
| 7 | Chicken breakfast burritos | Meat lover's omelettes |
| 8 | Loaded breakfast sandwiches | Sausage breakfast biscuits |
| 9 | Bacon steak sandwiches | Sausage scramble burritos |
| 10 | Chicken egg biscuits | Steak breakfast sandwiches |

**Observation**: v2 clusters tightly around "breakfast [format]" titles — 8 of 10 follow that exact template. no_rationale has more variation in phrasing ("croissan'wich", "omelettes", "ranch chicken").

---

## consumer `395521458` — weekday_breakfast

| | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| ILD | 0.488 | **0.430** ← worse |
| RR | 0.178 | 0.178 |
| TCD | 0.400 | **0.200** ← worse |

| # | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| 1 | Sausage breakfast crunchwraps | Sausage breakfast crunchwraps |
| 2 | Sausage breakfast burritos | Sausage breakfast burritos |
| 3 | Sausage breakfast sandwiches | Sausage breakfast sandwiches |
| 4 | Bacon breakfast burritos | Bacon breakfast burritos |
| 5 | Bacon breakfast quesadillas | Steak and egg burritos |
| 6 | Steak breakfast burritos | Bacon breakfast quesadillas |
| 7 | Bacon breakfast specials | Sausage and egg bagels |
| 8 | Bacon cheeseburger combos | Bacon egg and cheese bagels |
| 9 | Big Jack's skillet | Breakfast burger |
| 10 | Onion rings | French toast sticks |

**Observation**: The first 4 titles are identical between both variants — clear evidence of a sausage/bacon breakfast-heavy consumer. no_rationale diversifies later with "Big Jack's skillet" and "Onion rings"; v2 stays in breakfast-sandwich territory throughout.

---

## consumer `1452374422` — weekday_dinner

| | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| ILD | **0.443** ← worse | 0.536 |
| RR | **0.200** ← worse | 0.067 |
| TCD | **0.300** ← worse | 0.800 |

| # | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| 1 | Chicken nugget meals | Chicken nugget meals |
| 2 | Chicken nuggets | Chicken nuggets |
| 3 | Chicken nugget happy meals | Chicken nugget happy meals |
| 4 | Spicy chicken sandwich meals | Spicy chicken sandwiches |
| 5 | Chicken sandwiches | Chicken stir-fry |
| 6 | Spicy chicken sandwiches | Chicken chow mein |
| 7 | Chicken sandwich meals | Chicken parmesan |
| 8 | Chicken wings | Chicken fajitas |
| 9 | Burgers | Pad see ew |
| 10 | Pad thai | Chicken pasta |

**Observation**: A case where no_rationale is clearly worse — titles 1–3 are near-identical ("Chicken nugget meals / Chicken nuggets / Chicken nugget happy meals"), and titles 4/6/7 are near-duplicates of each other. v2 recognizes this consumer likes chicken but pivots to different cuisines (stir-fry, chow mein, parmesan, fajitas) after the first few, achieving much better TCD (0.800 vs 0.300).

---

## consumer `357310410` — weekday_breakfast

| | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| ILD | 0.456 | 0.447 |
| RR | 0.200 | 0.200 |
| TCD | 0.400 | 0.400 |

| # | no_rationale_think_1024 | genai_v2_think_1024 |
| --- | --- | --- |
| 1 | Sausage breakfast burritos | Sausage breakfast burritos |
| 2 | Meat lovers burritos | Fish sandwiches |
| 3 | Fish sandwiches | Meat lovers burritos |
| 4 | Triple meat burgers | Beef burgers |
| 5 | Steak and egg burritos | Steak and egg burritos |
| 6 | Chicken flautas | Chicken sandwiches |
| 7 | Chorizo and egg burritos | Chorizo and egg burritos |
| 8 | Bacon and egg burritos | Chicken flautas |
| 9 | Sausage breakfast platters | Sausage breakfast platters |
| 10 | Double meat burgers | Bacon and egg burritos |

**Observation**: Both variants are nearly identical in content (same titles, mostly reordered). The redundancy comes from heavy burrito repetition (sausage burritos, meat lover burritos, steak burritos, chorizo burritos, bacon burritos) — this is the consumer's actual order pattern, so the models are faithfully reflecting a low-variety history rather than generating poor carousels.

---

## Summary

| consumer | day_part | worse on ILD | worse on RR | worse on TCD | pattern |
| --- | --- | --- | --- | --- | --- |
| 1398034370 | weekend_lunch | genai_v2 | genai_v2 | genai_v2 | All-chicken loop in v2 |
| 34420201 | weekday_breakfast | genai_v2 | genai_v2 | genai_v2 | "[protein] breakfast [format]" template in v2 |
| 395521458 | weekday_breakfast | genai_v2 | tie | genai_v2 | Both bad; v2 stays in breakfast-sandwich mode |
| 1452374422 | weekday_dinner | no_rationale | no_rationale | no_rationale | Near-duplicate nugget titles in no_rationale |
| 357310410 | weekday_breakfast | tie | tie | tie | Consumer's own order history is low-variety |

4 of 5 examples show genai_v2 as worse on structure metrics. The exception
(`1452374422`) is the clearest failure mode for no_rationale — it generated
three near-identical "chicken nugget" titles in a row. The last example
(`357310410`) is a genuine low-variety consumer rather than a model failure.
