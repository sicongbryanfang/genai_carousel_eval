# Side-by-Side Carousel Comparison: Prod vs Retrieved

One representative consumer per metric (selected near 95th percentile of gap).

**Source data:** `eval_prod.csv`, `eval_retrieved.csv`, `prod_carousels.csv`, `retrieved_carousel.csv`, `orders_embedded.pkl`

---

## MMS — consumer 19334643, weekend_dinner

**mms:** prod=0.4642 → retrieved=0.6543 (delta=+0.1900)

### Order History (5 items)


| #   | Item                                                    | Cuisine          |
| --- | ------------------------------------------------------- | ---------------- |
| 1   | Juicy Pork Bao (6Pcs)                                   | Asian            |
| 2   | Pork Dumpling with Sesame Sauce and Red Chili Oil(8Pcs) | Asian            |
| 3   | Dry Cooked Green Beans                                  | Asian            |
| 4   | Pork and Vegetable Pot Stickers(5Pcs)                   | Asian            |
| 5   | Kung Pao Tofu 宮保豆腐                                      | Sichuan, Chinese |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title               | Prod Food Types                                                                           | Retr Title                  | Retr Food Types                                                                                  |
| ---- | ------------------------ | ----------------------------------------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------ |
| 1    | Himalayan comfort fare   | tofu curry, momos, himalayan veggie chili, fried momo, steamed rice                       | dumplings with bold flavors | vegetable dumplings, spicy tofu dumplings, paneer dumplings, Momo, chili dumplings               |
| 1    | Thai noodle dishes       | pad thai, spicy noodle stir-fry, green curry, red curry with tofu, khao soi               | kung pao dishes             | kung pao chicken, kung pao tofu, kung pao shrimp, kung pao beef                                  |
| 2    | Japanese sushi rolls     | specialty sushi roll, dragon roll, salmon nigiri, tempura roll, spicy tuna roll           | baked bbq pork bao          | bbq pork buns, steamed pork buns, pork bao, baked pork buns, char siu bao                        |
| 3    | Burmese samosas          | samosas, burmese samusas, veggie samosa, pork samosa                                      | garlic string beans         | garlic string beans, stir-fried green beans, sautéed string beans, spicy garlic green beans      |
| 4    | Signature curries        | massaman curry, panang curry, green curry, red curry, butter chicken                      | pan-fried potstickers       | beef potstickers, pork potstickers, chicken potstickers, vegetable potstickers, duck potstickers |
| 5    | Customizable pizzas      | veggie pizza, tofu topping pizza, spicy pepperoni pizza, mushroom pizza, margherita pizza | indulgent asian dumplings   | pork dumplings, chicken dumplings, shrimp dumplings, vegetable dumplings, pan-fried dumplings    |
| 6    | Gourmet pizza            | wood-fired margherita, quattro formaggi, truffle mushroom, spicy pepperoni                | japanese special rolls      | dynamite roll, spicy lobster roll, ninja roll, summer roll, assorted sushi                       |
| 7    | Spicy Indian street food | vada pav, samosas, bhel puri, pani puri, pakoras                                          | tofu dishes                 | sesame tofu stir-fry, tofu curry, tofu salad, spicy tofu tacos, tofu and vegetable stir-fry      |
| 8    | Thai curry dishes        | green curry, red curry, yellow curry, massaman curry                                      | classic samosas             | vegetable samosa, chicken samosa, lamb samosa, potato samosa, spiced paneer samosa               |
| 9    | Fusion Asian dishes      | korean tacos, sushi burritos, ramen burger, boba tea, pork belly bao                      | pepperoni pizza slices      | pepperoni pizza, cheese pizza, vegetable pizza, meat lovers pizza, BBQ chicken pizza             |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4642 | 0.6543    | +0.1900 **←** |
| sr_at_3                 | 0.2000 | 0.6000    | +0.4000       |
| sr_at_5                 | 0.4000 | 1.0000    | +0.6000       |
| sr_at_10                | 0.6000 | 1.0000    | +0.4000       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.5678 | 0.5958    | +0.0280       |
| ohcd                    | 0.4000 | 0.5000    | +0.1000       |
| tmc                     | 0.5228 | 0.6875    | +0.1648       |
| fcs                     | 0.8714 | 0.7857    | -0.0857       |
| composite_quality_score | 0.6088 | 0.7614    | +0.1527       |


---

## SR_AT_5 — consumer 17913910, weekend_lunch

**sr_at_5:** prod=0.2500 → retrieved=1.0000 (delta=+0.7500)

### Order History (4 items)


| #   | Item                        | Cuisine           |
| --- | --------------------------- | ----------------- |
| 1   | Brioche French Toast        |                   |
| 2   | Bacon                       |                   |
| 3   | 3Pc Signature Chicken Combo | Southern American |
| 4   | Midtown Scramble            |                   |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                 | Prod Food Types                                                                                        | Retr Title                  | Retr Food Types                                                                                                  |
| ---- | -------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1    | Family-style fried chicken | fried chicken, chicken tenders, southern fried chicken, buttermilk fried chicken, crispy chicken combo | signature chicken combos    | signature chicken combo, fried chicken bowl, 2 piece signature chicken dinner, 3 piece signature chicken combo   |
| 1    | BBQ family feast           | BBQ ribs, smoked brisket, pulled pork, BBQ chicken, Texas-style BBQ                                    | bacon meals                 | bacon egg cheese sandwich, bacon biscuit meal, bacon cheeseburger, bacon-wrapped fries, bacon pancakes           |
| 2    | BBQ and ribs feast         | St. Louis style spareribs, burnt ends, BBQ ribs, 3 meat combo BBQ                                      | brioche french toast        | French toast, stuffed French toast, cinnamon French toast, banana bread French toast                             |
| 3    | New Orleans favorites      | catfish fries, who Dat chicken, bayou bucket                                                           | grilled steak combos        | tri-tip steak combo, steak and shrimp, steak and lobster, steak fajitas, steak and chicken                       |
| 4    | St. Louis style ribs       | St. Louis style ribs, bbq ribs, burnt ends, 3 meat combo, bbq sampler                                  | fried chicken strips        | chicken tenders, crispy chicken, fried chicken, chicken fingers                                                  |
| 5    | Hearty pizza slices        | pepperoni pizza, vegetarian pizza, meat lovers pizza, BBQ chicken pizza, four cheese pizza             | classic chicken combo       | chicken combo meals, chicken tenders meals, crispy chicken meals, classic fried chicken meals, bbq chicken meals |
| 6    | Savory signature combos    | chicken combo meals, ribs combo, meat combo platter, petite combo packs                                | classic american desserts   | cheesecake, chocolate cake, apple pie, brownies, milkshake                                                       |
| 7    | Tender family meals        | 12-piece tenders family meal                                                                           | st. louis style ribs        | full rack of ribs, rib tips, smoked baby back ribs, BBQ steak                                                    |
| 8    | Delightful desserts        | triple chocolate chunk brownie, budtinis assortment, custard bar donuts                                | chicken tenders and fries   | chicken tenders, French fries, crispy chicken strips, spicy chicken tenders, jalapeño poppers                    |
| 9    | Wholesome salad options    | caesar salad, cobb salad, southwest chicken salad, mixed greens salad                                  | family-style italian dishes | lasagna, spaghetti and meatballs, chicken Parmesan, fettuccine Alfredo, stuffed shells                           |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4063 | 0.6588    | +0.2524       |
| sr_at_3                 | 0.2500 | 1.0000    | +0.7500       |
| sr_at_5                 | 0.2500 | 1.0000    | +0.7500 **←** |
| sr_at_10                | 0.2500 | 1.0000    | +0.7500       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.5749 | 0.5832    | +0.0083       |
| ohcd                    | 0.4000 | 0.3000    | -0.1000       |
| tmc                     | 0.5795 | 0.6407    | +0.0613       |
| fcs                     | 0.8286 | 0.7000    | -0.1286       |
| composite_quality_score | 0.5775 | 0.7212    | +0.1437       |


---

## CCR — consumer 12301816, weekend_lunch

**ccr:** prod=0.5000 → retrieved=1.0000 (delta=+0.5000)

### Order History (4 items)


| #   | Item                                | Cuisine           |
| --- | ----------------------------------- | ----------------- |
| 1   | Cinnamon Bread Bites                | American, Italian |
| 2   | Ranch Dipping Cup                   | American, Italian |
| 3   | Spicy Buffalo 5-Cheese Mac & Cheese | American, Italian |
| 4   | Ultimate Pepperoni                  | American, Italian |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title             | Prod Food Types                                                                                                            | Retr Title                 | Retr Food Types                                                                                                                   |
| ---- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Breakfast burritos     | breakfast burritos, bacon breakfast burrito, chorizo breakfast burritos, veggie breakfast burritos, egg and cheese burrito | hearty american breakfasts | breakfast plates, pancakes and eggs, bacon and eggs, breakfast sandwiches, omelettes                                              |
| 1    | Hearty tacos           | bacon tacos, beef tacos, chicken tacos, breakfast tacos, pork tacos                                                        | ultimate pepperoni pizza   | pepperoni pizza, loaded pizza, cheese pizza, bacon pizza, stuffed crust pepperoni pizza                                           |
| 2    | Savory chilaquiles     | red sauce chilaquiles, green sauce chilaquiles, beef chilaquiles, chicken chilaquiles, chilaquiles with eggs               | brunch burritos            | bacon breakfast burrito, chicken breakfast burrito, vegetarian breakfast burrito, California breakfast burrito, breakfast burrito |
| 3    | Loaded nachos          | beef nachos, bacon nachos, chicken nachos, loaded vegetarian nachos, spicy nachos                                          | brunch-style french toast  | French toast, Kids French toast, Stuffed French toast, Banana bread French toast, Cinnamon French toast                           |
| 4    | Gourmet sandwiches     | bacon grilled cheese, beef brisket sandwich, turkey club sandwich, pulled pork sandwich, fried chicken sandwich            | pretzel bites              | pretzel nuggets, filled pretzels, sweet pretzel bites, soft pretzels with cheese, pretzel sticks                                  |
| 5    | Flavorful quesadillas  | beef quesadilla, chicken quesadilla, bacon quesadilla, cheese quesadilla, vegetable quesadilla                             | mac and cheese             | four cheese mac and cheese, baked mac and cheese, lobster mac and cheese, spicy jalapeno mac, buffalo chicken mac                 |
| 6    | Spicy nachos           | beef nachos, chicken nachos, loaded nachos, vegetarian nachos                                                              | sweet lemonades            | citrus lemonade, strawberry lemonade, lavender lemonade, mango lemonade, passion fruit lemonade                                   |
| 7    | Bacon and cheese fries | loaded bacon fries, cheese fries, beef chili fries, Tex-Mex fries, spicy chicken fries                                     | pollo tacos                | pollo taco, chicken taco, taco al pastor, fish taco, chicken burrito                                                              |
| 8    | Burrito bowls          | beef burrito bowl, chicken burrito bowl, veggie burrito bowl, pulled pork burrito bowl, taco salad                         | bacon meals                | bacon egg cheese sandwich, bacon biscuit meal, bacon cheeseburger, bacon-wrapped fries, bacon pancakes                            |
| 9    | Spicy wings            | buffalo wings, barbecue wings, honey garlic wings, teriyaki wings, nashville hot wings                                     | hand-crafted burgers       | classic cheeseburger, bacon cheeseburger, barbecue burger, mushroom Swiss burger, chicken burger                                  |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4173 | 0.5694    | +0.1521       |
| sr_at_3                 | 0.5000 | 0.2500    | -0.2500       |
| sr_at_5                 | 0.5000 | 0.2500    | -0.2500       |
| sr_at_10                | 0.5000 | 0.7500    | +0.2500       |
| ccr                     | 0.5000 | 1.0000    | +0.5000 **←** |
| ild                     | 0.4890 | 0.5895    | +0.1005       |
| ohcd                    | 0.4000 | 0.4000    | +0.0000       |
| tmc                     | 0.6576 | 0.6206    | -0.0370       |
| fcs                     | 0.9571 | 0.7714    | -0.1857       |
| composite_quality_score | 0.5646 | 0.6091    | +0.0446       |


---

## ILD — consumer 1467142, weekday_breakfast

**ild:** prod=0.4526 → retrieved=0.5762 (delta=+0.1237)

### Order History (12 items)


| #   | Item                         | Cuisine  |
| --- | ---------------------------- | -------- |
| 1   | Big Breakfast® with Hotcakes | American |
| 2   | Hash Browns                  | American |
| 3   | Jr. Grand Slam®              | American |
| 4   | Hotcakes                     | American |
| 5   | Soft Drinks                  | American |
| 6   | Stack of Pancakes            | American |
| 7   | Build Your Own Grand Slam®   | American |
| 8   | Soft Drinks                  | American |
| 9   | Sausage McMuffin® with Egg   | American |
| 10  | Build Your Own Grand Slam®   | American |
| 11  | Double Cheeseburger          | American |
| 12  | Hotcakes and Sausage         | American |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                   | Prod Food Types                                                                                     | Retr Title               | Retr Food Types                                                                                                  |
| ---- | ---------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| 1    | Build your own breakfast     | bacon and eggs, pancakes, breakfast burrito, omelette, egg and cheese sandwich                      | all-american breakfast   | pancake breakfast, breakfast platter, omelette with toast, breakfast hash, classic breakfast                     |
| 1    | Classic breakfast combos     | big breakfast, breakfast sandwich, cheesy hash browns, breakfast platter, full breakfast            | customizable meal combos | build your own meal, custom chicken meal, breakfast combo platter, chicken and waffles, fries and sandwich combo |
| 2    | Hearty breakfast wraps       | bacon egg wrap, breakfast burrito, sausage egg wrap, chicken breakfast burrito, hash brown wrap     | cheeseburgers            | bacon cheeseburgers, double cheeseburgers, classic cheeseburgers, quarter pounders, cheeseburger sliders         |
| 3    | Savory breakfast sandwiches  | bacon egg cheese bagel, sausage muffin, breakfast croissant, breakfast biscuit, egg muffin sandwich | hotcakes and sausages    | hotcakes, sausage breakfast platter, sausage and pancakes, hotcakes and bacon, buttermilk pancakes               |
| 4    | Pancakes and syrup           | buttermilk pancakes, chocolate chip pancakes, blueberry pancakes, banana pancakes, waffles          | mexican hotcakes         | Mexican hotcakes, sweet corn pancakes, cinnamon pancakes, vanilla pancakes                                       |
| 5    | Traditional breakfast items  | scrambled eggs, bacon strips, french toast, home fries, grits                                       | coffee frappes           | coffee frappes, caramel frappes, mocha frappes, vanilla frappes                                                  |
| 6    | Diners' breakfast favorites  | eggs benedict, hash browns, omelets, French toast                                                   | coffee and soda drinks   | black coffee, latte, cappuccino, fountain drinks, iced coffee                                                    |
| 7    | Customizable breakfast bowls | quinoa breakfast bowl, egg breakfast bowl, grain bowl, yogurt and granola, fruit bowl               | american pancake stacks  | buttermilk pancakes, blueberry pancakes, chocolate chip pancakes, banana pancakes, pancake platter               |
| 8    | Smoothie bowls               | fruit smoothie bowls, yogurt smoothie bowls, acai smoothie bowls                                    | sausage egg muffins      | sausage egg muffin, spicy sausage muffin, cheese egg muffin                                                      |
| 9    | Sweet bakery items           | donuts, muffins, croissants, pastries, cinnamon rolls                                               | classic breakfast eggs   | fried eggs, poached eggs, scrambled eggs, omelette, baked eggs                                                   |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4515 | 0.5357    | +0.0841       |
| sr_at_3                 | 0.4167 | 0.4167    | +0.0000       |
| sr_at_5                 | 0.5833 | 0.5833    | +0.0000       |
| sr_at_10                | 0.5833 | 0.7500    | +0.1667       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.4526 | 0.5762    | +0.1237 **←** |
| ohcd                    | 0.6000 | 0.6000    | +0.0000       |
| tmc                     | 0.6313 | 0.7269    | +0.0955       |
| fcs                     | 0.8857 | 0.7571    | -0.1286       |
| composite_quality_score | 0.6606 | 0.6849    | +0.0242       |


---

## OHCD — consumer 9419142, weekend_lunch

**ohcd:** prod=0.7000 → retrieved=1.0000 (delta=+0.3000)

### Order History (12+6 more items)


| #   | Item                                       | Cuisine   |
| --- | ------------------------------------------ | --------- |
| 1   | K4. Fresh Mango Sago Dessert               | Asian     |
| 2   | Y1. Basil Popcorn Chicken                  | Asian     |
| 3   | Super Burrito                              | Mexican   |
| 4   | Y11. Fish Ball                             | Asian     |
| 5   | D5. Passion Green Tea                      | Asian     |
| 6   | Fresh Yellow Chicken Congee(Contain Bones) | Cantonese |
| 7   | Pork & Gold Preserved Egg Congee           | Cantonese |
| 8   | NO.1. Original Spam & Egg                  | Asian     |
| 9   | Corn Rice Noodle Roll                      | Cantonese |
| 10  | Y29 Crispy Short Rib Bao (2pcs)            | Asian     |
| 11  | Dough Stick                                | Cantonese |
| 12  | Home-Style Hot & Sour Soup (Vegan)         |           |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                | Prod Food Types                                                                                                     | Retr Title                | Retr Food Types                                                                                                           |
| ---- | ------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1    | Thai noodle dishes        | pad kee mao, drunken noodles, pad thai, yellow curry noodles, spicy basil noodles                                   | chinese congee            | preserved egg congee, pork blood congee, shrimp congee, chicken congee, vegetable congee                                  |
| 1    | Sichuan spicy rice dishes | spicy fried rice, mapo tofu rice, Sichuan chicken stir-fry, Sichuan mixed rice, spicy fried congee                  | special rice noodle rolls | beef rice noodle rolls, pork rice noodle rolls, shrimp rice noodle rolls, vegetable rice noodle rolls, steamed rice rolls |
| 2    | American summer salads    | Caesar salad, cobb salad, berry salad, grilled chicken salad, Mediterranean quinoa salad                            | premium burritos          | super burrito, chicken burrito, beef burrito, vegetarian burrito, breakfast burrito                                       |
| 3    | Japanese rice bowls       | chirashi sushi, unagi don, katsu don, gyudon, sushi rice bowl                                                       | diverse asian dishes      | teriyaki chicken bowl, pad Thai, crispy spring rolls, beef stir-fry, char siu rice                                        |
| 4    | Vietnamese rice plates    | broken rice plate, lemongrass chicken rice, grilled pork rice, vietnamese curry rice, seafood rice                  | fresh teas                | iced green tea, black tea, fruit iced tea, milk tea, bubble tea                                                           |
| 5    | Korean barbecue fare      | bulgogi, galbi, samgyeopsal, bibimbap, korean fried chicken                                                         | fresh rice rolls          | shrimp rice rolls, pork rice rolls, vegetable rice rolls, beef rice rolls, rice paper rolls                               |
| 6    | Seafood rice dishes       | seafood fried rice, shrimp rice bowl, clam rice, crab fried rice, seafood congee                                    | spicy hot soup            | hot and sour soup, spicy seafood soup, szechuan hot pot, kimchi stew, spicy wonton soup                                   |
| 7    | Gourmet fried chicken     | fried chicken sandwich, crispy chicken tenders, spicy chicken wings, korean fried chicken, buttermilk fried chicken | california burritos       | burrito, loaded burrito, breakfast burrito                                                                                |
| 8    | Savory seafood dishes     | blackened shrimp, grilled salmon, seafood paella, clam chowder, seafood pasta                                       | tasty bao                 | pork bao, chicken bao, veggie bao, bbq bao, steamed bao                                                                   |
| 9    | Vegan fresh salads        | kale salad, chickpea salad, grain salad, avocado salad, mediterranean salad                                         | mango pomelo sago         | mango sago dessert, pomelo dessert, mango dessert, mango pudding, tapioca dessert                                         |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4235 | 0.5415    | +0.1179       |
| sr_at_3                 | 0.3333 | 0.4444    | +0.1111       |
| sr_at_5                 | 0.3333 | 0.4444    | +0.1111       |
| sr_at_10                | 0.4444 | 0.6667    | +0.2222       |
| ccr                     | 0.5000 | 1.0000    | +0.5000       |
| ild                     | 0.5397 | 0.6114    | +0.0717       |
| ohcd                    | 0.7000 | 1.0000    | +0.3000 **←** |
| tmc                     | 0.6358 | 0.6556    | +0.0198       |
| fcs                     | 0.9714 | 0.7571    | -0.2143       |
| composite_quality_score | 0.5748 | 0.6980    | +0.1232       |


---

## TMC — consumer 14682040, weekend_dinner

**tmc:** prod=0.5264 → retrieved=0.6636 (delta=+0.1372)

### Order History (12+8 more items)


| #   | Item                            | Cuisine              |
| --- | ------------------------------- | -------------------- |
| 1   | Bufalina Pizza                  | Italian              |
| 2   | Kung Pao Chicken                | Chinese              |
| 3   | Fettuccine Short Ribs           | Italian              |
| 4   | Philly Cheesesteak Spring Rolls | American             |
| 5   | Super Bowl                      | American             |
| 6   | Cheeseburger                    | American Traditional |
| 7   | Won Ton Soup                    | Chinese              |
| 8   | Town Filet Burgers              | American             |
| 9   | Little Gem Salad                | Italian              |
| 10  | Fried Calzone                   | Italian              |
| 11  | Pot Stickers (6)                | Chinese              |
| 12  | Jalapeño Pizza                  | Italian              |


### Carousels (prod=9, retrieved=10)


| Rank | Prod Title            | Prod Food Types                                                                                   | Retr Title                | Retr Food Types                                                                                                |
| ---- | --------------------- | ------------------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 1    | Gourmet burgers       | cheeseburger, jalapeño cheddar burger, super burger, mini burger, classic burger                  | hearty american entrees   | cheeseburger, fried chicken sandwich, meatloaf, pork chops, steak dinner                                       |
| 1    | Spicy chicken dinners | chicken tikka masala, jalapeño chicken, spicy fried chicken, grilled spicy chicken, chicken curry | italian pastas and pizzas | margherita pizza, spaghetti carbonara, fettuccine alfredo, pesto pasta, pepperoni pizza                        |
| 2    | Sushi rolls           | rainbow roll, nigiri, sashimi, tempura roll, vegetable roll                                       | classic caesar salad      | grilled chicken Caesar, shrimp Caesar, veggie Caesar, steak Caesar                                             |
| 3    | Spicy burritos        | chicken burrito, beef burrito, vegetarian burrito, burrito bowl, spicy pork burrito               | vegetarian spring rolls   | fried vegetable rolls, fresh vegetable rolls, tofu spring rolls, crispy vegetable rolls, spicy vegetable rolls |
| 4    | Artisanal pizzas      | pepperoni pizza, margherita pizza, bbq chicken pizza, vegetable pizza, gourmet cheese pizza       | margherita pizzas         | margherita pizza, buffalo mozzarella pizza, classic Italian pizza, toppings pizza, vegetable pizza             |
| 5    | Hearty pasta dishes   | fettuccine alfredo, spaghetti and meatballs, pesto pasta, baked ziti, pasta primavera             | wonton soups              | wonton soup, pork wontons, veggie wontons, chicken wontons, shrimp wontons                                     |
| 6    | Korean barbecue       | bulgogi, galbi, spicy pork belly, korean fried chicken, bbq beef short ribs                       | thai curry meals          | green curry, red curry, massaman curry, yellow curry, panang curry                                             |
| 7    | Malaysian flavors     | nasi lemak, char kway teow, laksa, roti canai, satay skewers                                      | meatball marinara         | meatball sub, meatball sandwich, meatball hoagie                                                               |
| 8    | Middle Eastern fare   | shawarma, falafel, hummus platter, kebabs, tabbouleh                                              | hearty chow mein          | chicken chow mein, beef chow mein, mixed vegetable chow mein, shrimp chow mein                                 |
| 10   | —                     | —                                                                                                 | savory cheesesteaks       | steak cheesesteaks, chicken cheesesteaks, vegetable cheesesteaks, Philly cheesesteaks                          |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4915 | 0.5694    | +0.0780       |
| sr_at_3                 | 0.4000 | 0.6000    | +0.2000       |
| sr_at_5                 | 0.6500 | 0.6500    | +0.0000       |
| sr_at_10                | 0.7500 | 0.8000    | +0.0500       |
| ccr                     | 0.7500 | 0.7500    | +0.0000       |
| ild                     | 0.5949 | 0.6059    | +0.0110       |
| ohcd                    | 0.7778 | 1.0000    | +0.2222       |
| tmc                     | 0.5264 | 0.6636    | +0.1372 **←** |
| fcs                     | 0.9048 | 0.7714    | -0.1333       |
| composite_quality_score | 0.6602 | 0.6997    | +0.0395       |


---

## FCS — consumer 12028416, weekday_lunch

**fcs:** prod=0.9714 → retrieved=0.7571 (delta=-0.2143)

### Order History (12+57 more items)


| #   | Item                                                         | Cuisine           |
| --- | ------------------------------------------------------------ | ----------------- |
| 1   | Large Chips & Large Queso Blanco                             | Mexican           |
| 2   | Desserts                                                     | American          |
| 3   | Chicken Noodle                                               | American          |
| 4   | Angry Mac                                                    | American          |
| 5   | Maui Zaui™ with Ham (Medium 12")                             | American, Italian |
| 6   | Mac & Cheese                                                 | American          |
| 7   | Duracell Coppertop AAA Alkaline Batteries (16 ct) (3166675 ) |                   |
| 8   | Diet Coke®                                                   | American          |
| 9   | Strawberry Southern Lemonade                                 | American          |
| 10  | Chips                                                        | American          |
| 11  | McChicken®                                                   | American          |
| 12  | Chili Cheese Dog                                             | American          |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                    | Prod Food Types                                                                                                                     | Retr Title                | Retr Food Types                                                                                                               |
| ---- | ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 1    | Turkey and avocado sandwiches | turkey and avocado sandwiches, chicken avocado sandwiches, club sandwiches, smoked turkey sandwiches, vegetarian avocado sandwiches | american fast-food meals  | grilled chicken plates, chicken nuggets, big mac meals, combo meals, french fries                                             |
| 1    | Vietnamese rice bowls         | lemongrass chicken rice bowl, beef pho bowls, veggie rice bowls, pork rice bowls, crispy chicken rice bowl                          | milkshakes and sodas      | chocolate milkshake, strawberry milkshake, vanilla milkshake, root beer float, soda pop beverage                              |
| 2    | Savory burritos               | beef burritos, chicken burritos, vegetarian burritos, rice burritos, pulled pork burritos                                           | customizable pizza        | Margarita pizza, BBQ chicken pizza, Vegetarian pizza, Spicy pepperoni pizza, Buffalo chicken pizza                            |
| 3    | Gourmet sushi rolls           | spicy tuna rolls, salmon avocado rolls, veggie rolls, tempura rolls, rainbow rolls                                                  | chicken nuggets and meals | 10 pc. chicken nuggets, chicken nugget meal, spicy chicken nuggets, chicken tenders, chicken nugget combo                     |
| 4    | Chicken noodle bowls          | chicken ramen, pho chicken noodle, stir-fried chicken noodles, soba chicken bowls, chicken pad thai                                 | macaroni and cheese       | creamy macaroni and cheese, baked macaroni and cheese, mac and cheese with bacon, mac and cheese side, chicken mac and cheese |
| 5    | Spicy tacos                   | chicken tacos, beef tacos, fish tacos, vegetable tacos, pork tacos                                                                  | sushi rolls and combos    | spicy tuna rolls, California rolls, sashimi platter, tempura rolls                                                            |
| 6    | Pulled pork sandwiches        | classic pulled pork, pulled pork sliders, spicy pulled pork, bbq pulled pork, pulled chicken sandwich                               | turkey and avocado        | turkey avocado sandwich, turkey club, turkey sub, avocado turkey wrap, turkey and cheese sandwich                             |
| 7    | Sushi rolls                   | spicy tuna roll, California roll, dragon roll, salmon avocado roll, tempura roll                                                    | burritos de carne         | beef burrito, chicken burrito, pork burrito, vegetarian burrito, fajita burrito                                               |
| 8    | Tex-Mex bowls                 | chicken burrito bowl, beef taco bowl, vegetarian fajita bowl, bbq chicken bowl, quesadilla bowl                                     | chips with queso          | chips with queso, tortilla chips with cheese, chips and guacamole                                                             |
| 9    | Light salads                  | chicken ceasar salads, garden salads, avocado salads, mediterranean salads, quinoa salads                                           | refreshing limeades       | sweet limeades, cherry limeades, flavored limeades, carbonated lime drinks                                                    |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.3806 | 0.4808    | +0.1002       |
| sr_at_3                 | 0.1304 | 0.3043    | +0.1739       |
| sr_at_5                 | 0.1739 | 0.3478    | +0.1739       |
| sr_at_10                | 0.2754 | 0.5507    | +0.2754       |
| ccr                     | 0.7500 | 0.7500    | +0.0000       |
| ild                     | 0.5149 | 0.6179    | +0.1030       |
| ohcd                    | 0.9000 | 1.0000    | +0.1000       |
| tmc                     | 0.6460 | 0.6603    | +0.0143       |
| fcs                     | 0.9714 | 0.7571    | -0.2143 **←** |
| composite_quality_score | 0.5988 | 0.6352    | +0.0364       |


---

## COMPOSITE_QUALITY_SCORE — consumer 9662074, weekend_lunch

**composite_quality_score:** prod=0.5424 → retrieved=0.7159 (delta=+0.1735)

### Order History (6 items)


| #   | Item                       | Cuisine |
| --- | -------------------------- | ------- |
| 1   | Cantina Chicken Quesadilla | Mexican |
| 2   | Chicken Enchilada Burrito  | Mexican |
| 3   | Crunchy Taco               | Mexican |
| 4   | Beefy 5-Layer Burrito      | Mexican |
| 5   | Hot Sauce Packet           | Mexican |
| 6   | Beefy 5-Layer Burrito      | Mexican |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title             | Prod Food Types                                                                                        | Retr Title               | Retr Food Types                                                                                             |
| ---- | ---------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| 1    | Loaded nacho plates    | nacho plates, beef nachos, chicken nachos, veggie nachos, loaded nachos                                | chicken quesadilla       | chicken quesadilla, beef quesadilla, grilled chicken quesadilla, quesadilla with guacamole                  |
| 1    | Chicken enchiladas     | chicken enchiladas, beef enchiladas, cheese enchiladas                                                 | mexican burrito          | super burrito, grilled chicken burrito, steak burrito, vegetarian burrito, pork burrito                     |
| 2    | Pulled pork sandwiches | pulled pork sandwiches, BBQ pulled chicken, smoked brisket sandwiches                                  | crispy fried tacos       | crispy beef tacos, chicken tacos, fish tacos, shredded pork tacos, vegetarian tacos                         |
| 3    | Classic pizzas         | pepperoni pizza, vegetarian pizza, BBQ chicken pizza, cheese pizza                                     | grilled chicken burrito  | grilled chicken burrito, spicy chicken burrito, beef burrito, veggie burrito, baja burrito                  |
| 4    | Savory chicken wings   | BBQ chicken wings, spicy chicken wings, garlic parmesan wings, honey mustard wings, lemon pepper wings | premium chicken wings    | chicken wing combo, spicy wings, garlic parmesan wings, buffalo wings, honey BBQ wings                      |
| 5    | Savory tacos           | chicken tacos, beef tacos, fish tacos, vegetarian tacos                                                | build your own pizza     | custom pizza, veggie pizza, pepperoni pizza, BBQ chicken pizza, cheese pizza                                |
| 6    | Gourmet sandwiches     | chicken sandwiches, BLT sandwiches, veggie sandwiches, turkey club sandwiches                          | grilled beef tacos       | carne asada tacos, beef tacos, beef street tacos, chicken tacos, taco al pastor                             |
| 7    | Stuffed quesadillas    | chicken quesadillas, beef quesadillas, veggie quesadillas                                              | italian chicken plates   | chicken pasta plates, chicken Parmesan, chicken Alfredo, baked chicken with pasta, chicken caprese          |
| 8    | Southern-style chicken | fried chicken, chicken tenders, buttermilk chicken                                                     | garlic chicken pizza     | garlic chicken pizza, BBQ chicken pizza, buffalo chicken pizza, Mediterranean chicken pizza                 |
| 9    | Spicy ramen bowls      | ramen bowl, spicy tonkotsu ramen, chicken ramen, beef ramen, vegetable ramen                           | fried chicken sandwiches | fried chicken sandwich, spicy chicken sandwich, buttermilk fried chicken sandwich, classic chicken sandwich |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.5359 | 0.5959    | +0.0600       |
| sr_at_3                 | 0.6667 | 0.8333    | +0.1667       |
| sr_at_5                 | 0.6667 | 0.8333    | +0.1667       |
| sr_at_10                | 0.8333 | 0.8333    | +0.0000       |
| ccr                     | 0.0000 | 1.0000    | +1.0000       |
| ild                     | 0.5374 | 0.4487    | -0.0887       |
| ohcd                    | 0.4000 | 0.5000    | +0.1000       |
| tmc                     | 0.7099 | 0.7268    | +0.0169       |
| fcs                     | 0.9000 | 0.7857    | -0.1143       |
| composite_quality_score | 0.5424 | 0.7159    | +0.1735 **←** |


---

# Prod Outperforms Retrieved: Side-by-Side Examples

One representative consumer per metric where **prod beats retrieved** (selected near 5th percentile of gap).
For FCS (where prod generally wins), we show a case where **retrieved beats prod** instead.

---

## MMS (prod wins) — consumer 21782626, weekend_late_night

**mms:** prod=0.6164 → retrieved=0.5912 (delta=-0.0253)

### Order History (2 items)


| #   | Item         | Cuisine |
| --- | ------------ | ------- |
| 1   | Kao Gra Prow | Thai    |
| 2   | Crab Rangoon | Thai    |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                      | Prod Food Types                                                                                                             | Retr Title             | Retr Food Types                                                                                            |
| ---- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1    | Hearty rice plates              | kai gra prow rice plate, chicken teriyaki rice plate, beef stir fry rice, spicy basil chicken rice, fried rice with chicken | thai fried rice        | pad thai, spicy basil fried rice, fried rice with chicken                                                  |
| 1    | Hearty fried chicken sandwiches | fried chicken sandwich, buffalo chicken sandwich, chicken parm sandwich, spicy crispy chicken, chicken tender sandwich      | pad thai               | Pad Thai, Thai noodles, spicy Pad Thai, chicken Pad Thai, shrimp Pad Thai                                  |
| 2    | Flavorful pizza                 | customized pizza, pepperoni pizza, BBQ chicken pizza, vegetable pizza, four cheese pizza                                    | vegetable samosas      | vegetable samosas, spiced potato samosas, crispy vegetable pastries                                        |
| 3    | Savory Indian snacks            | vegetable samosas, chicken pakoras, pav bhaji, paneer tikka, chicken chaat                                                  | indian butter chicken  | butter chicken, chicken tikka masala, paneer butter masala, chicken korma, tandoori chicken                |
| 4    | Gourmet customizable pizzas     | bbq chicken pizza, pepperoni pizza, vegetable supreme pizza, meat lovers pizza, cheese pizza                                | american fried chicken | crispy fried chicken, spicy chicken wings, mild chicken wings, popcorn chicken, chicken tenders            |
| 5    | Spicy chicken wings             | buffalo chicken wings, lemon pepper wings, barbecue wings, honey garlic wings, teriyaki wings                               | classic combo meals    | burger combos, chicken sandwich combos, wing combo meals, taco combos, wrap combo meals                    |
| 6    | Savory Thai bites               | pad thai, chicken larb, crab rangoon, tom yum soup, spicy basil chicken                                                     | pasta primavera        | vegetable pasta, creamy pasta with chicken, spaghetti marinara, pasta with garlic and olive oil            |
| 7    | Delicious curries               | butter chicken, chicken tikka masala, vegetable curry, lamb curry, paneer tikka masala                                      | gourmet calzones       | chicken calzone, pepperoni calzone, four cheese calzone, vegetable calzone, spicy chicken calzone          |
| 8    | Flavorful Thai street food      | pad see ew, khao soi, som tam salad, moshi balls, grilled pork skewers                                                      | indulgent cheesecakes  | strawberry cheesecake, classic cheesecake, chocolate cheesecake, blueberry cheesecake, key lime cheesecake |
| 9    | Comfort food plates             | meatloaf plate, pot roast plate, chicken fried steak, country fried steak, shepherd's pie                                   | comforting milkshakes  | chocolate milkshakes, vanilla milkshakes, strawberry milkshakes                                            |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.6164 | 0.5912    | -0.0253 **←** |
| sr_at_3                 | 1.0000 | 1.0000    | +0.0000       |
| sr_at_5                 | 1.0000 | 1.0000    | +0.0000       |
| sr_at_10                | 1.0000 | 1.0000    | +0.0000       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.4887 | 0.5994    | +0.1107       |
| ohcd                    | 0.2000 | 0.2000    | +0.0000       |
| tmc                     | 0.6001 | 0.6835    | +0.0834       |
| fcs                     | 0.9286 | 0.7714    | -0.1571       |
| composite_quality_score | 0.7215 | 0.7164    | -0.0050       |


---

## SR_AT_5 (prod wins) — consumer 10713171, weekend_dinner

**sr_at_5:** prod=0.5556 → retrieved=0.3889 (delta=-0.1667)

### Order History (12+6 more items)


| #   | Item                            | Cuisine           |
| --- | ------------------------------- | ----------------- |
| 1   | Chili                           | American          |
| 2   | Chili Cheese Dog                | American          |
| 3   | Beef / Cheese Enchiladas        | Mexican           |
| 4   | Short Bridge                    | Italian           |
| 5   | Steamed Fresh Vegetables        | Japanese          |
| 6   | Onion Rings                     | American          |
| 7   | Agua Fresca                     | Mexican           |
| 8   | Chef's Choice 10 pcs of Sashimi | Japanese          |
| 9   | Mini Pecan Pie                  | Southern American |
| 10  | Dragon Roll                     | Japanese          |
| 11  | Plain Quesadilla                | Mexican           |
| 12  | A7. Crab Cheese Puff (8 Pcs.)   | Chinese           |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                   | Prod Food Types                                                                                               | Retr Title                | Retr Food Types                                                                                                |
| ---- | ---------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 1    | Southern BBQ classics        | pulled pork sandwiches, smoked brisket plates, BBQ chicken, ribs, fried chicken                               | hearty american entrees   | cheeseburger, fried chicken sandwich, meatloaf, pork chops, steak dinner                                       |
| 1    | Spicy General Tso's chicken  | General Tso's chicken, Kung Pao chicken, spicy sesame chicken, orange chicken, sweet and sour chicken         | baby back ribs            | pork ribs, barbecue ribs, spicy ribs, smoked ribs, rib platter                                                 |
| 2    | Authentic Mexican tacos      | carne asada tacos, al pastor tacos, fish tacos, barbacoa tacos, chicken tinga tacos                           | general tso chicken       | General Tso chicken, sesame chicken, orange chicken, chicken fried rice, beef broccoli                         |
| 3    | Hearty gourmet burgers       | classic cheeseburgers, bacon burgers, spicy jalapeno burgers, barbecue burgers, mushroom swiss burgers        | gourmet churros           | classic churros, spiced churros, churros with chocolate, churros with caramel, churros with strawberry sauce   |
| 4    | Sushi and rolls              | California rolls, spicy tuna rolls, tempura rolls, salmon sashimi, gyoza                                      | sausage pizzas            | spicy fennel sausage pizza, italian sausage pizza, pepperoni pizza, meatball pizza, cheese pizza               |
| 5    | Gourmet pizza options        | deep dish pizza, Margherita pizza, BBQ chicken pizza, vegetable pizza, pepperoni pizza                        | quesadillas with cheese   | cheese quesadillas, chicken quesadillas, beef quesadillas, vegetarian quesadillas, spicy quesadillas           |
| 6    | Flavorful Mediterranean fare | shawarma plates, falafel wraps, lamb gyros, hummus and pita, tabbouleh                                        | savory crab wontons       | crab cheese wontons, crab wontons, fried crab dumplings                                                        |
| 7    | Savory fried chicken         | spicy fried chicken, buttermilk fried chicken, chicken tenders, fried chicken sandwiches, fried chicken wings | savory mexican enchiladas | chicken enchiladas, beef enchiladas, vegetable enchiladas, cheese enchiladas                                   |
| 8    | Vibrant vegetarian dishes    | vegetable curry, stuffed bell peppers, chickpea stew, veggie sushi, vegetable stir fry                        | agua frescas              | agua frescas, fruit-based drinks, refreshing aguas, natural fruit juices                                       |
| 9    | Indulgent desserts           | chocolate cake, cheesecake, tiramisu, mousse, union churros                                                   | chicken fried chicken     | crispy fried chicken, buttermilk fried chicken, bbq chicken plates, fried chicken dinners, spicy fried chicken |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4923 | 0.5189    | +0.0265       |
| sr_at_3                 | 0.4444 | 0.2778    | -0.1667       |
| sr_at_5                 | 0.5556 | 0.3889    | -0.1667 **←** |
| sr_at_10                | 0.7222 | 0.6667    | -0.0556       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.5517 | 0.5847    | +0.0329       |
| ohcd                    | 0.9000 | 0.9000    | +0.0000       |
| tmc                     | 0.5863 | 0.6324    | +0.0461       |
| fcs                     | 0.8714 | 0.7714    | -0.1000       |
| composite_quality_score | 0.6956 | 0.6711    | -0.0245       |


---

## CCR (prod wins) — consumer 14678074, weekend_lunch

**ccr:** prod=1.0000 → retrieved=0.6667 (delta=-0.3333)

### Order History (12+2 more items)


| #   | Item                                           | Cuisine  |
| --- | ---------------------------------------------- | -------- |
| 1   | Grilled Chicken Street Taco                    | Mexican  |
| 2   | Chicken Teriyaki Bowl                          | Japanese |
| 3   | French Fries                                   | American |
| 4   | Del Scorcho - Medium                           | Mexican  |
| 5   | Del Inferno - Hot                              | Mexican  |
| 6   | Snack Taco                                     | Mexican  |
| 7   | Crab Rangoons                                  | Japanese |
| 8   | Picadillo                                      |          |
| 9   | Enchilada Plates                               |          |
| 10  | Tamales                                        |          |
| 11  | Double Cheeseburger                            | American |
| 12  | Epic Carne Asada Steak Fresh Guacamole Burrito | Mexican  |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title              | Prod Food Types                                                                                | Retr Title              | Retr Food Types                                                                                            |
| ---- | ----------------------- | ---------------------------------------------------------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1    | Mexican tamales         | steamed tamales, pork tamales, chicken tamales, vegetarian tamales, beef tamales               | tangy chicken dishes    | orange chicken, sweet and sour chicken, lemon chicken, honey sesame chicken, spicy garlic chicken          |
| 1    | Mediterranean gyros     | chicken gyros, beef gyros, lamb gyros, veggie gyros, gyros platter                             | savory enchilada plates | chicken enchiladas, beef enchiladas, vegetable enchiladas, cheese enchiladas, seafood enchiladas           |
| 2    | Barbecue plates         | brisket plate, pulled pork plate, ribs plate, chicken plate, bbq platter                       | teriyaki chicken bowls  | teriyaki chicken bowl, chicken donburi, beef teriyaki bowl, vegetable teriyaki, grilled chicken bowl       |
| 3    | Spicy noodle dishes     | pad Thai, spicy noodles, ramen, udon bowls, chili garlic noodles                               | chicken street tacos    | chicken street tacos, al pastor tacos, grilled steak tacos, vegetarian street tacos, carnitas street tacos |
| 4    | Baja fish tacos         | crispy fish tacos, battered fish tacos, grilled fish tacos, spicy fish tacos, cajun fish tacos | mexican tamales         | chicken tamales, pork tamales, cheese tamales, sweet tamales, vegetable tamales                            |
| 5    | Savory rice bowls       | chicken rice bowl, beef rice bowl, pork rice bowl, veggie rice bowl, spicy rice bowl           | grilled beef tacos      | carne asada tacos, beef tacos, beef street tacos, chicken tacos, taco al pastor                            |
| 6    | Middle Eastern shawarma | chicken shawarma, beef shawarma, lamb shawarma, shawarma wraps, shawarma platters              | mexican platillos       | asada platillos, camaron platillos, chicken platillos, pork platillos, vegetable platillos                 |
| 7    | Poke bowls              | salmon poke, tuna poke, spicy poke, vegetable poke, miso poke                                  | burritos de carne asada | burritos de carne asada, steak burrito, grilled steak burrito, carne asada bowl                            |
| 8    | Sizzling fajitas        | chicken fajitas, steak fajitas, shrimp fajitas, vegetarian fajitas, mixed fajitas              | crab rangoons           | fried crab rangoons, cream cheese rangoons, spicy crab rangoons                                            |
| 9    | Thai curry dishes       | green curry, red curry, yellow curry, massaman curry, panang curry                             | rice dishes             | fried rice, chicken fried rice, beef stir-fried rice, rice bowl, burrito rice bowl                         |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4925 | 0.5837    | +0.0913       |
| sr_at_3                 | 0.3571 | 0.2857    | -0.0714       |
| sr_at_5                 | 0.6429 | 0.4286    | -0.2143       |
| sr_at_10                | 0.7143 | 0.7857    | +0.0714       |
| ccr                     | 1.0000 | 0.6667    | -0.3333 **←** |
| ild                     | 0.5806 | 0.5239    | -0.0568       |
| ohcd                    | 0.7000 | 1.0000    | +0.3000       |
| tmc                     | 0.6470 | 0.6900    | +0.0431       |
| fcs                     | 0.9714 | 0.8000    | -0.1714       |
| composite_quality_score | 0.7157 | 0.6569    | -0.0588       |


---

## ILD (prod wins) — consumer 2042923, weekend_lunch

**ild:** prod=0.6098 → retrieved=0.5452 (delta=-0.0646)

### Order History (12+5 more items)


| #   | Item                                                       | Cuisine               |
| --- | ---------------------------------------------------------- | --------------------- |
| 1   | 椒鹽排 / Crispy Pork Chops with Peppery Salt /                | Chinese, Shanghainese |
| 2   | 乾煸四季豆 / Dry Sautéed String Beans /                         | Chinese, Shanghainese |
| 3   | N.1.2 Stewed Pork Ribs Noodle 红烧排骨面                        | Chinese               |
| 4   | 芥藍牛肉 / Sliced Beef with Broccoli /                         | Chinese, Shanghainese |
| 5   | 蟹粉小籠包 / Crab Meat with Pork Steamed Soup Buns (6 Pieces) / | Chinese, Shanghainese |
| 6   | Boneless Meal Deal For 2                                   | American              |
| 7   | 開洋白菜 / Chinese Cabbage with Dried Shrimps /                | Chinese, Shanghainese |
| 8   | 52 oz Simply Lemonade®                                     | American              |
| 9   | Spicy Beef Noodle Soup 川味牛腩汤面                              | Chinese               |
| 10  | Side of Flavor                                             | American              |
| 11  | apple 'n greens™                                           | American              |
| 12  | Bigger Plate                                               | Chinese               |


### Carousels (prod=9, retrieved=10)


| Rank | Prod Title             | Prod Food Types                                                                             | Retr Title                 | Retr Food Types                                                                                                          |
| ---- | ---------------------- | ------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 1    | Vegetarian dumplings   | pork dumplings, vegetable dumplings, steamed dumplings, pan-fried dumplings, soup dumplings | boneless chicken meals     | chickenjoy meals, fried chicken combo, chicken and rice combo, chicken bucket meals, chicken sandwich meals              |
| 1    | Japanese rice bowls    | chicken teriyaki bowl, sushi rice bowl, beef gyudon, salmon donburi, vegetable donburi      | traditional chinese dishes | beef noodle soup, sweet and sour pork, kung pao chicken, mapo tofu, fried rice                                           |
| 2    | Pulled pork sandwiches | pulled pork sliders, BBQ pork sandwiches, pork hoagies                                      | salt and pepper shrimp     | salt and pepper shrimp, szechuan shrimp, garlic shrimp                                                                   |
| 3    | Malaysian flavors      | nasi lemak, char kway teow, roti canai                                                      | rice plates with meat      | beef rice plate, chicken rice plate, pork rice plate, shrimp rice plate, mixed meat rice plate                           |
| 4    | Spicy ramen bowls      | tonkotsu ramen, spicy miso ramen, vegetarian ramen                                          | soup dumplings             | soup dumplings, pan-fried dumplings, steamed dumplings, pork dumplings, vegetable dumplings                              |
| 5    | Sichuan noodle dishes  | spicy wonton noodles, dan dan noodles, Sichuan cold noodles                                 | hunan stir-fry dishes      | Hunan style sautéed beef, spicy Hunan chicken, Hunan-style noodle stir-fry, ginger scallion rice, stir-fried green beans |
| 6    | Gourmet salads         | quinoa salad, Mediterranean salad, chicken caesar salad                                     | pork chop over rice        | pork chop over rice, pork belly rice, fried pork chop, grilled pork over rice, sweet and sour pork                       |
| 7    | Korean BBQ options     | bulgogi, galbi, Korean fried chicken                                                        | creative dumplings         | vegan dumplings, tofu potstickers, vegetable gyoza, Thai dumplings, mushroom dumplings                                   |
| 9    | Thai rice dishes       | pad thai, fried rice, green curry rice                                                      | braised beef noodles       | beef noodle soup, braised beef rice, beef stir-fried noodles, spicy braised beef noodles                                 |
| 10   | —                      | —                                                                                           | vegetarian indian fare     | saag paneer, paneer tikka masala, vegetarian curry, chana masala, dal makhani                                            |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4287 | 0.4995    | +0.0708       |
| sr_at_3                 | 0.2353 | 0.5294    | +0.2941       |
| sr_at_5                 | 0.2941 | 0.5882    | +0.2941       |
| sr_at_10                | 0.3529 | 0.6471    | +0.2941       |
| ccr                     | 1.0000 | 0.6667    | -0.3333       |
| ild                     | 0.6098 | 0.5452    | -0.0646 **←** |
| ohcd                    | 0.4444 | 0.8000    | +0.3556       |
| tmc                     | 0.6193 | 0.6876    | +0.0683       |
| fcs                     | 0.8571 | 0.7286    | -0.1286       |
| composite_quality_score | 0.6067 | 0.6351    | +0.0283       |


---

## OHCD (prod wins) — consumer 13555615, weekday_dinner

**ohcd:** prod=0.4000 → retrieved=0.3000 (delta=-0.1000)

### Order History (6 items)


| #   | Item                          | Cuisine          |
| --- | ----------------------------- | ---------------- |
| 1   | White Rice                    | Korean           |
| 2   | C2. Bbq Beef & Tofu Combo     | Korean           |
| 3   | Spicy                         | Japanese, Korean |
| 4   | T10. Beef & Octopus Tofu Soup | Korean           |
| 5   | Spicy Ramen / 라면              | Korean           |
| 6   | T8. Pork Tofu Soup            | Korean           |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                  | Prod Food Types                                                                                                      | Retr Title                   | Retr Food Types                                                                                                            |
| ---- | --------------------------- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1    | Korean comfort stews        | kimchi stew, beef bulgogi, spicy pork stew, seafood jjigae, chicken ginseng soup                                     | beef tofu soup               | beef tofu soup, spicy tofu soup, seafood tofu soup, vegetable tofu soup, chicken tofu soup                                 |
| 1    | Savory rice bowls           | beef rice bowl, chicken teriyaki bowl, korean bibimbap, pork katsu don, seafood poke bowl                            | beef ramen                   | tonkotsu ramen, shoyu ramen, spicy ramen, beef yakisoba, chicken ramen                                                     |
| 2    | Spicy Korean fried rice     | kimchi fried rice, spicy pork fried rice, seafood fried rice, beef fried rice, vegetable fried rice                  | korean fried rice            | kimchi fried rice, bulgogi fried rice, seafood fried rice, chicken fried rice, veggie fried rice                           |
| 3    | Delicious noodle dishes     | ramen, udon, jajangmyeon, pho, beef noodle soup                                                                      | classic american combo meals | burger combo, fried chicken meal, fish sandwich meal, chicken nuggets combo, fried shrimp platter                          |
| 4    | Hearty combo meals          | burrito bowl, chicken parmesan with pasta, german sausage platter, korean fried chicken with rice, beef and broccoli | burrito bowl                 | burrito bowl, chicken burrito bowl, beef burrito bowl, carnitas burrito bowl, vegetarian burrito bowl                      |
| 5    | Comforting ramen bowls      | shoyu ramen, miso ramen, tonkotsu ramen, spicy ramen, vegan ramen                                                    | vietnamese vermicelli        | grilled chicken vermicelli, pork vermicelli, crab vermicelli, bun bo hue, imperial rolls vermicelli                        |
| 6    | Savory tacos and burritos   | beef tacos, chicken burrito, pork carnitas taco, vegetarian burrito, fish tacos                                      | classic pepperoni pizzas     | classic pepperoni pizza, deep dish pizza, stuffed crust pizza, meat lovers pizza, supreme pizza                            |
| 7    | Flavorful curry dishes      | chicken curry, beef curry, vegetable curry, lamb curry, green curry                                                  | tasty desserts               | cinnamon twists, cookies, brownies, churros, cheesecake                                                                    |
| 8    | American-style comfort food | mac and cheese, chicken fried steak, meatloaf, pot roast, shepherd's pie                                             | chocolate shakes             | large chocolate shakes, frozen chocolate drinks, rich chocolate shakes, decadent chocolate shakes, smooth chocolate shakes |
| 9    | Rich and creamy pasta       | alfredo pasta, carbonara, fettuccine alfredo, pasta primavera, baked ziti                                            | milk tea                     | brown sugar milk tea, classic milk tea, fruit milk tea, milk tea with boba, winter melon milk tea                          |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.4709 | 0.5670    | +0.0961       |
| sr_at_3                 | 0.5000 | 1.0000    | +0.5000       |
| sr_at_5                 | 0.5000 | 1.0000    | +0.5000       |
| sr_at_10                | 0.5000 | 1.0000    | +0.5000       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.5452 | 0.6239    | +0.0787       |
| ohcd                    | 0.4000 | 0.3000    | -0.1000 **←** |
| tmc                     | 0.6119 | 0.6858    | +0.0739       |
| fcs                     | 0.9000 | 0.8143    | -0.0857       |
| composite_quality_score | 0.6405 | 0.7308    | +0.0903       |


---

## TMC (prod wins) — consumer 18256056, weekday_breakfast

**tmc:** prod=0.7435 → retrieved=0.6799 (delta=-0.0635)

### Order History (5 items)


| #   | Item                              | Cuisine  |
| --- | --------------------------------- | -------- |
| 1   | Hash Browns                       | American |
| 2   | Sausage, Egg & Cheese McGriddles® | American |
| 3   | Santa Barbara Char                | American |
| 4   | Grilled Cheese                    | American |
| 5   | Sausage McMuffin® with Egg        | American |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title                   | Prod Food Types                                                                                           | Retr Title                 | Retr Food Types                                                                                                                |
| ---- | ---------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1    | Breakfast egg sandwiches     | egg sandwich, sausage and egg sandwich, bacon egg sandwich, cheddar egg sandwich, turkey sausage sandwich | grilled cheese             | classic grilled cheese, bacon grilled cheese, cheddar grilled cheese, pepper jack grilled cheese, mozzarella grilled cheese    |
| 1    | Fresh bagels and shmear      | bagel with cream cheese, onion bagel, garlic bagel, everything bagel, plain bagel                         | sausage & egg muffins      | sausage & egg muffin, bacon & egg muffin, egg muffin, cheddar muffin, veggie muffin                                            |
| 2    | Breakfast platters           | breakfast platter, breakfast combo, mixed breakfast, eggs and sides, full breakfast                       | sausage and egg sandwiches | sausage egg sandwich, breakfast sausage muffin, sausage biscuit, egg and cheese croissant, sausage McGriddle                   |
| 3    | Savory hash browns           | hash browns, loaded hash browns, cheesy hash browns, baked hash browns                                    | charbroiled burgers        | double cheeseburger, bacon cheeseburger, guacamole bacon burger, western bacon cheeseburger                                    |
| 4    | Chicken breakfast combos     | chicken sandwich combo, chicken and waffles, fried chicken breakfast, breakfast chicken biscuit           | american-style breakfasts  | big breakfast with pancakes, breakfast sausage platter, bacon and eggs plate, stuffed French toast, classic breakfast sandwich |
| 5    | Pancakes and waffles         | pancakes, waffles, buttermilk pancakes, maple syrup pancakes                                              | bagels with cream cheese   | lox bagel, plain bagel with cream cheese, everything bagel, flavored cream cheese bagel, sesame bagel                          |
| 6    | Breakfast burritos           | breakfast burrito, sausage breakfast burrito, chicken breakfast burrito, veggie breakfast burrito         | savory soups               | cream of chicken soup, grilled chicken and corn chowder, tomato garden vegetable soup                                          |
| 7    | Customizable breakfast bowls | breakfast bowl, eggs and avocado bowl, protein breakfast bowl, grain breakfast bowl                       | nova lox sandwiches        | nova lox sandwiches, bagel sandwiches, cream cheese bagels, smoked salmon bagels, lox bagels                                   |
| 8    | Quick breakfast wraps        | breakfast wrap, egg and cheese wrap, chicken wrap, veggie wrap                                            | pho noodle soups           | rare steak pho, brisket pho, house special pho, veggie pho, chicken pho                                                        |
| 9    | Classic breakfast sandwiches | bacon egg and cheese, sausage egg and cheese, ham egg sandwich, breakfast biscuit                         | hearty chicken soups       | chicken soup, vegetable chicken soup, creamy chicken soup, spicy chicken soup, chicken noodle soup                             |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.5478 | 0.6034    | +0.0556       |
| sr_at_3                 | 0.4000 | 0.6000    | +0.2000       |
| sr_at_5                 | 0.6000 | 0.8000    | +0.2000       |
| sr_at_10                | 0.8000 | 0.8000    | +0.0000       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.4913 | 0.5802    | +0.0889       |
| ohcd                    | 0.4000 | 0.3000    | -0.1000       |
| tmc                     | 0.7435 | 0.6799    | -0.0635 **←** |
| fcs                     | 0.8000 | 0.7429    | -0.0571       |
| composite_quality_score | 0.6702 | 0.6921    | +0.0219       |


---

## FCS (prod wins) — consumer 8894279, weekday_late_night

**fcs:** prod=0.8286 → retrieved=0.8000 (delta=-0.0286)

### Order History (3 items)


| #   | Item                     | Cuisine  |
| --- | ------------------------ | -------- |
| 1   | Ají Amarillo sauce (2oz) | Peruvian |
| 2   | Quarter White            | Peruvian |
| 3   | Sprite                   | Peruvian |


### Carousels (prod=10, retrieved=10)


| Rank | Prod Title             | Prod Food Types                                                               | Retr Title                  | Retr Food Types                                                                                                              |
| ---- | ---------------------- | ----------------------------------------------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 1    | Gourmet burgers        | cheeseburgers, double burgers, bacon burgers, veggie burgers, chicken burgers | peruvian lomo saltado       | beef lomo saltado, chicken lomo saltado, vegetarian lomo saltado, seafood lomo saltado                                       |
| 1    | Loaded fries           | cheese fries, bacon cheese fries, chili fries, garlic fries, poutine          | american fried chicken      | fried chicken, chicken tenders, chicken wings                                                                                |
| 2    | Pulled pork sandwiches | barbecue pork sandwiches, BBQ chicken sandwiches, pulled chicken sandwiches   | rich cheesecakes            | peanut butter cup cheesecake, chocolate fudge cheesecake, ny style cheesecake, strawberry cheesecake, turtle cheesecake      |
| 3    | Gourmet sandwiches     | club sandwiches, turkey sandwiches, Italian sandwiches, cheese steaks         | dessert crepes              | chocolate crepes, strawberry crepes, banana Nutella crepes, lemon sugar crepes, sweet cream crepes                           |
| 4    | Chow mein              | chicken chow mein, beef chow mein, vegetable chow mein                        | steak and cheese sandwiches | cheesesteak sandwich, steak sandwich, chicken cheese sandwich, loaded meat sandwich, grilled chicken sandwich                |
| 5    | Szechuan chicken       | spicy chicken stir fry, chicken with peanuts, garlic Szechuan chicken         | poke bowls                  | build your poke bowl, spicy tuna poke, salmon poke bowl, ahi poke bowl, shrimp poke bowl                                     |
| 6    | Burgers and fries      | cheeseburgers, chicken sandwiches, fries                                      | classic grilled cheese      | grilled cheese sandwich, three-cheese grilled cheese, toasted grilled cheese, cheddar grilled cheese, gourmet grilled cheese |
| 7    | Savory pupusas         | cheese pupusas, bean pupusas, pork pupusas                                    | tacos de carne              | beef tacos, carnitas tacos, barbacoa tacos, chicken tacos, fish tacos                                                        |
| 8    | Spicy tacos            | chicken tacos, beef tacos, pork tacos                                         | cheeseburgers               | cheeseburger meal, double cheeseburger, bacon cheeseburger, cheeseburger combos, classic cheeseburger                        |
| 9    | Comfort food bowls     | fried rice, rice and chicken, chicken noodle soup, mac and cheese             | chicken pasta dishes        | chicken fettuccine alfredo, chicken pesto penne, chicken parmesan pasta, chicken spaghetti, chicken carbonara                |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.3426 | 0.3529    | +0.0103       |
| sr_at_3                 | 0.0000 | 0.3333    | +0.3333       |
| sr_at_5                 | 0.0000 | 0.3333    | +0.3333       |
| sr_at_10                | 0.3333 | 0.3333    | +0.0000       |
| ccr                     | 1.0000 | 1.0000    | +0.0000       |
| ild                     | 0.5424 | 0.6085    | +0.0661       |
| ohcd                    | 0.3000 | 0.3000    | +0.0000       |
| tmc                     | 0.6834 | 0.6487    | -0.0347       |
| fcs                     | 0.8286 | 0.8000    | -0.0286 **←** |
| composite_quality_score | 0.5295 | 0.5787    | +0.0492       |


---

## COMPOSITE_QUALITY_SCORE (prod wins) — consumer 16621859, weekend_breakfast

**composite_quality_score:** prod=0.4253 → retrieved=0.3747 (delta=-0.0507)

### Order History (2 items)


| #   | Item                              | Cuisine |
| --- | --------------------------------- | ------- |
| 1   | Bloom Haus™ Whimsical Bouquet - B |         |
| 2   | Dozen Red Rose Arrangement        |         |


### Carousels (prod=9, retrieved=10)


| Rank | Prod Title                | Prod Food Types                                                                                                        | Retr Title                     | Retr Food Types                                                                                                    |
| ---- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| 1    | Breakfast burritos        | ham egg cheese burrito, bacon egg cheese burrito, sausage egg cheese burrito, chorizo egg burrito, breakfast burrito   | sausage & egg muffins          | sausage muffins, egg & cheese muffins, breakfast ham muffins                                                       |
| 1    | Gourmet sandwiches        | bacon egg sandwich, egg and cheese sandwich, sausage egg sandwich, breakfast sandwich, turkey bacon sandwich           | classic breakfast burritos     | hash brown scramble burrito, breakfast burrito, bacon breakfast burrito, sausage breakfast burrito, veggie burrito |
| 2    | Hearty breakfast platters | breakfast platter, vegetable breakfast platter, meat breakfast platter, full breakfast, egg and meat platter           | bacon and egg wraps            | bacon egg wraps, breakfast sausage wraps, chicken and egg wraps                                                    |
| 3    | Pancakes and waffles      | buttermilk pancakes, blueberry pancakes, waffles with syrup, banana pancakes, chocolate chip pancakes                  | eggs and bacon dishes          | eggs benedict, scrambled eggs with bacon, bacon and egg hash, breakfast egg platters, bacon sunrise bowls          |
| 4    | French toast              | classic french toast, stuffed french toast, banana bread french toast, cinnamon roll french toast, churro french toast | fluffy waffles and pancakes    | buttermilk pancakes, Belgian waffles, banana pancakes, fruity waffles, chocolate chip pancakes                     |
| 6    | Classic bagels            | plain bagel with cream cheese, everything bagel, smoked salmon bagel, egg and cheese bagel, bacon egg bagel            | savory wings                   | buffalo wings, spicy garlic wings, parmesan wings, honey sriracha wings, teriyaki wings                            |
| 7    | French toast options      | classic french toast, stuffed french toast, cinnamon french toast, banana french toast, blueberry french toast         | sourdough breakfast sandwiches | sourdough jack sandwich, bacon egg sourdough sandwich, steak egg sourdough sandwich                                |
| 8    | Smoothie bowls            | tropical smoothie bowl, berry smoothie bowl, green smoothie bowl, peanut butter smoothie bowl, chocolate smoothie bowl | sweet brunch options           | banana bread, fruit salad, waffles with fruit, chocolate chip pancakes, coffee cake                                |
| 9    | Breakfast smoothies       | banana smoothie, berry smoothie, green smoothie, protein breakfast smoothie, yogurt parfait                            | savory hash brown plates       | hash browns, loaded hash browns, vegetable hash brown plates, meat and hash brown plates                           |
| 10   | —                         | —                                                                                                                      | southern breakfast plates      | shrimp and grits, country ham and eggs, biscuits and gravy, chicken and waffles, catfish and eggs                  |


### All Metrics


| Metric                  | Prod   | Retrieved | Delta         |
| ----------------------- | ------ | --------- | ------------- |
| mms                     | 0.2208 | 0.2175    | -0.0033       |
| sr_at_3                 | 0.0000 | 0.0000    | +0.0000       |
| sr_at_5                 | 0.0000 | 0.0000    | +0.0000       |
| sr_at_10                | 0.0000 | 0.0000    | +0.0000       |
| ccr                     | N/A    | N/A       | —             |
| ild                     | 0.5374 | 0.5290    | -0.0085       |
| ohcd                    | 0.2222 | 0.1000    | -0.1222       |
| tmc                     | 0.7046 | 0.7138    | +0.0092       |
| fcs                     | 0.9048 | 0.7000    | -0.2048       |
| composite_quality_score | 0.4253 | 0.3747    | -0.0507 **←** |


