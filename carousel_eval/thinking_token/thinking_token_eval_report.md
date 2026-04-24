# Thinking Token Budget Evaluation Report

**Date**: 2026-04-24
**Eval window**: 90-day order history ending 2026-03-19
**Embed mode**: title_only (`all-MiniLM-L6-v2`)
**Consumers**: 33 common (36 in source; 3 excluded — 1 scientific-notation ID, 2 with no orders in window)
**Candidates**: 3 thinking-token budgets (512, 1024, 8192)

> budget=8192 returned `null` for 2 consumers (1141863705, 633566040), so its eval covers 31 consumers / 144 groups vs 33 / 151 for the other two.

## Overall Results

| Metric | budget=512 | budget=1024 | budget=8192 | Direction |
|--------|-----------|------------|------------|-----------|
| **Composite** | **0.6058** | **0.6151** | **0.6020** | higher = better |
| MMS | 0.5605 | 0.5576 | 0.5283 | higher = better |
| SR@3 | 0.3376 | 0.3642 | 0.3380 | higher = better |
| SR@5 | 0.4265 | 0.4658 | 0.4254 | higher = better |
| SR@10 | 0.5930 | 0.5924 | 0.5489 | higher = better |
| CCR | 0.9003 | 0.9195 | 0.9087 | higher = better |
| ILD | 0.6738 | 0.6725 | 0.6857 | higher = better |
| TCD | 0.8616 | 0.8689 | 0.9056 | higher = better |
| RR | 0.0091 | 0.0094 | 0.0040 | lower = better |
| OHCD | 0.4636 | 0.4583 | 0.4646 | higher = better |
| FCS | 0.8308 | 0.8306 | 0.8302 | higher = better |

**Composite weights**: MMS 20%, SR@5 20%, CCR 15%, ILD 15%, OHCD 20%, FCS 10%.
TMC, TCD, and RR are diagnostic only (excluded from composite).

## Breakdown by Daypart

### budget=512 (33 consumers, 151 groups)

| Daypart | n | MMS | SR@5 | CCR | ILD | Composite |
|---------|---|-----|------|-----|-----|-----------|
| weekday_breakfast | 18 | 0.6129 | 0.5638 | 0.9412 | 0.6550 | 0.6385 |
| weekday_dinner | 30 | 0.5482 | 0.4032 | 0.9268 | 0.6803 | 0.6066 |
| weekday_late_night | 15 | 0.5379 | 0.4311 | 0.9778 | 0.6699 | 0.5870 |
| weekday_lunch | 33 | 0.5592 | 0.4644 | 0.8444 | 0.6604 | 0.6607 |
| weekend_breakfast | 10 | 0.6054 | 0.5464 | 1.0000 | 0.6586 | 0.6155 |
| weekend_dinner | 21 | 0.5429 | 0.4195 | 0.8947 | 0.6963 | 0.5803 |
| weekend_late_night | 6 | 0.5133 | 0.1993 | 0.9167 | 0.6844 | 0.5291 |
| weekend_lunch | 18 | 0.5614 | 0.2717 | 0.7979 | 0.6880 | 0.5366 |

### budget=1024 (33 consumers, 151 groups)

| Daypart | n | MMS | SR@5 | CCR | ILD | Composite |
|---------|---|-----|------|-----|-----|-----------|
| weekday_breakfast | 18 | 0.5640 | 0.4958 | 1.0000 | 0.6571 | 0.6218 |
| weekday_dinner | 30 | 0.5502 | 0.5082 | 0.9131 | 0.6805 | 0.6254 |
| weekday_late_night | 15 | 0.5641 | 0.5288 | 0.9778 | 0.6774 | 0.6128 |
| weekday_lunch | 33 | 0.5513 | 0.4587 | 0.8697 | 0.6596 | 0.6569 |
| weekend_breakfast | 10 | 0.6062 | 0.4929 | 0.9444 | 0.6583 | 0.5973 |
| weekend_dinner | 21 | 0.5691 | 0.4805 | 0.9254 | 0.6900 | 0.6098 |
| weekend_late_night | 6 | 0.5000 | 0.3659 | 0.9167 | 0.6514 | 0.5576 |
| weekend_lunch | 18 | 0.5487 | 0.3269 | 0.8729 | 0.6884 | 0.5519 |

### budget=8192 (31 consumers, 144 groups)

| Daypart | n | MMS | SR@5 | CCR | ILD | Composite |
|---------|---|-----|------|-----|-----|-----------|
| weekday_breakfast | 18 | 0.5160 | 0.4364 | 0.9118 | 0.6757 | 0.5904 |
| weekday_dinner | 29 | 0.5185 | 0.4226 | 0.9191 | 0.6925 | 0.6094 |
| weekday_late_night | 14 | 0.5783 | 0.5458 | 1.0000 | 0.6811 | 0.6302 |
| weekday_lunch | 31 | 0.5248 | 0.4503 | 0.8629 | 0.6764 | 0.6465 |
| weekend_breakfast | 10 | 0.5125 | 0.3821 | 1.0000 | 0.6663 | 0.5629 |
| weekend_dinner | 21 | 0.5391 | 0.4627 | 0.9079 | 0.6994 | 0.5995 |
| weekend_late_night | 5 | 0.5508 | 0.3212 | 0.9000 | 0.6963 | 0.5685 |
| weekend_lunch | 16 | 0.5112 | 0.2747 | 0.8405 | 0.6977 | 0.5284 |

## Business / Branded Item Leakage

Carousel titles should be generic food categories, not reference specific businesses or trademarked menu items. We scanned all unique titles per candidate against known chain names and branded items.

| | budget=512 | budget=1024 | budget=8192 |
|--|-----------|------------|------------|
| Unique titles | 1,177 | 1,170 | 1,014 |
| Flagged titles | 9 (0.8%) | 6 (0.5%) | 6 (0.6%) |
| Business names | 3 | 1 | 0 |
| Branded items | 7 | 6 | 6 |

### Business / chain name references

| Title | 512 | 1024 | 8192 |
|-------|-----|------|------|
| Chick-fil-A chicken sandwiches | x | | |
| Chicken chipotle sandwiches* | x | | |
| Cinnabon delights | x | x | |

\* Likely false positive — "chipotle" as a pepper/flavor, not the restaurant chain.

### Branded / trademarked item names

| Title | 512 | 1024 | 8192 |
|-------|-----|------|------|
| Big Mac burgers | x | x | |
| McChicken sandwiches | x | | |
| Crunchwrap / Crunchwrap Supreme | x | x | x |
| Bean crunchwraps | | x | x |
| Beef crunchwraps | | x | |
| Black bean crunchwraps | x | x | |
| Bean chalupas | x | | x |
| Black bean chalupas | x | x | x |
| Cinnabon delights | x | x | |

**Summary**: budget=8192 is cleanest on business names (zero), but all three candidates leak Taco Bell trademarks (`Crunchwrap`, `chalupa`). budget=512 has the most leakage including explicit brand references (`Chick-fil-A`, `Big Mac`, `McChicken`). budget=1024 is in between.

## Key Takeaways

1. **budget=1024 has the highest composite score (0.6151)**, driven by the best SR@5 (0.4658) and CCR (0.9195). It offers the best balance of relevance and cuisine coverage.

2. **budget=8192 leads on diversity** — highest ILD (0.6857), highest TCD (0.9056), and lowest redundancy (RR 0.0040) — but trails on relevance metrics (MMS, SR@5, SR@10). It also failed to produce carousels for 2 consumers.

3. **budget=512 is competitive** with a composite of 0.6058, highest MMS (0.5605), but slightly behind budget=1024 on SR@5 and CCR.

4. **All three candidates show similar patterns across dayparts**: breakfast and late_night tend to have higher relevance, while weekend_lunch and weekend_late_night are weakest.

## Data Notes

- Source file: `thinking_budget_comparison___2.csv` (36 consumers x 8 dayparts x 10 ranks x 3 budgets)
- 1 consumer ID (`1.1259E+15`) was stored in scientific notation — excluded due to precision loss
- 2 consumers (1102136904, 1876395311) had no orders in the 90-day window — excluded
- 2 consumers (1141863705, 633566040) returned `null` for all entries in budget=8192 only
- TMC is reported but not meaningful (no food_type metadata in source data)
