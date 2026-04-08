# TMC Analysis: Why Retrieved Carousels Score Higher

**Title-Metadata Coherence (TMC)**: Average cosine similarity between each carousel's title embedding and its food_type embedding (comma-joined food_type tags). Higher TMC = title is more semantically aligned with the food_type list.

| Source    | TMC (mean) |
| --------- | ---------- |
| Prod/EBR  | 0.635      |
| Retrieved | 0.672      |
| Delta     | **+0.037** |


## Root Cause: Title Abstraction Level

The gap is driven by a fundamental **title generation style difference** between the two sources.


### Prod/EBR: Subjective Qualifier + Generic Category

Prod titles prioritize marketing appeal with editorial-style phrasing:

| Title                | food_type (from tags)                                            |
| -------------------- | ---------------------------------------------------------------- |
| Hearty sandwiches    | Philly cheesesteak, Italian sub, club sandwich, pulled pork sandwich |
| Comfort burgers      | classic cheeseburger, bacon burger, mushroom burger              |
| Mediterranean fare   | gyros, falafel wraps, stuffed grape leaves, couscous salad       |
| Savory skewers       | chicken skewers, beef skewers, vegetable skewers                 |
| Fresh bakery items   | croissant, blueberry muffin, cinnamon roll                       |


### Retrieved: Specific Food-Item Titles

Retrieved titles name the actual food, often echoing an entry from the food_type list:

| Title                         | food_type (from tags)                                          |
| ----------------------------- | -------------------------------------------------------------- |
| chicken biryani               | chicken biryani, vegetable biryani, dum biryani, spicy biryani |
| mapo tofu                     | mapo tofu, tofu stir fry, spicy tofu, braised tofu            |
| pad thai stir fried noodles   | pad thai, stir fried noodles, pad see ew, spicy pad thai       |
| cheesy pepperoni pizza        | cheesy pizza, pepperoni pizza, margherita pizza                 |
| coffee and lattes             | iced latte, caffe latte, oatmilk latte, cold brew              |


## Three Contributing Factors

### 1. Prod titles use subjective adjectives with no semantic counterpart in food_type (biggest factor)

Words like "Hearty", "Gourmet", "Savory", "Comfort", "Satisfying" are sentiment/quality descriptors. They push the title embedding toward an "appealing food" semantic space, while the food_type embedding is anchored in **specific dish names**.

The cosine similarity between "Hearty sandwiches" and "Philly cheesesteak, Italian sub, club sandwich" is lower than between "club sandwiches" and the same food_type list.

~31% of prod titles contain subjective qualifiers vs ~18% for retrieved.

### 2. Retrieved titles echo the food_type list directly

In ~34% of retrieved carousels, the title text is a substring of (or contains) one of the food_type entries, versus only ~21% for prod. When the title literally appears in the food_type string, the embeddings align closely because they share the same key noun phrases.

The retrieved system appears to derive its title from the food_type content (or vice versa), creating tighter semantic coupling.

### 3. Prod titles operate at a higher level of abstraction

Prod titles use category-level terms ("sandwiches", "burgers", "fare", "dishes") while the food_type lists contain specific instances ("Philly cheesesteak", "bacon burger"). This hypernym-hyponym gap creates an embedding distance — the embedding model (`all-MiniLM-L6-v2`) captures that "sandwiches" and "Philly cheesesteak" are related but not identical concepts.

Retrieved titles collapse this gap by naming the specific food.


## Quantitative Evidence

| Signal                                          | Prod   | Retrieved |
| ----------------------------------------------- | ------ | --------- |
| Title uses subjective qualifier                 | **31%** | 18%      |
| Title is/contains a food_type item              | 21%    | **34%**   |
| Title matches first food_type item              | 19%    | **31%**   |
| Title word recall in food_type string           | 0.446  | **0.533** |
| All title words found in food_type              | 15%    | **24%**   |
| Uses generic category nouns (fare, dishes, etc) | **29%** | 25%      |
| Retrieved TMC > Prod TMC (per-consumer pairs)   | —      | **72%**   |


## Daypart Variation

TMC delta is largest for dinner/lunch dayparts (+0.05) and smallest for breakfast/late_night (+0.02). This aligns with dinner/lunch having more diverse food vocabulary where the abstraction gap matters more.

| Daypart            | Prod TMC | Retrieved TMC | Delta   |
| ------------------ | -------- | ------------- | ------- |
| weekday_breakfast  | 0.691    | 0.709         | +0.017  |
| weekday_dinner     | 0.617    | 0.671         | +0.054  |
| weekday_late_night | 0.643    | 0.672         | +0.029  |
| weekday_lunch      | 0.638    | 0.674         | +0.037  |
| weekend_breakfast  | 0.678    | 0.699         | +0.021  |
| weekend_dinner     | 0.602    | 0.652         | +0.050  |
| weekend_late_night | 0.639    | 0.657         | +0.018  |
| weekend_lunch      | 0.621    | 0.656         | +0.035  |


## Interpretation

This is **not necessarily a quality deficiency** in prod. It reflects a deliberate design choice:

- **Prod/EBR** optimizes for **consumer-facing appeal** — creative, editorial-style titles that sound engaging ("Hearty sandwiches" vs "club sandwiches")
- **Retrieved** optimizes for **food-type specificity** — titles that precisely describe the carousel content

If TMC alignment is desirable, the prod title generation prompt could be tuned to include at least one specific food item from the food_type list while retaining the editorial tone (e.g., "Hearty Philly cheesesteaks" instead of "Hearty sandwiches").
