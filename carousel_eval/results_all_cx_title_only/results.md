# Carousel Evaluation Results — All Consumers, Title Only

- **Embed mode**: title_only
- **Common consumers**: 15,639
- **Model**: all-MiniLM-L6-v2

## Overall Results


| Metric        | Prod       | Retrieved  | Delta       |
| ------------- | ---------- | ---------- | ----------- |
| MMS           | 0.4262     | **0.5408** | +0.1146     |
| SR@3          | 0.2272     | **0.4346** | +0.2073     |
| SR@5          | 0.2937     | **0.5301** | +0.2363     |
| SR@10         | 0.3818     | **0.6284** | +0.2466     |
| CCR           | 0.8376     | **0.9057** | +0.0681     |
| ILD           | 0.6560     | **0.6763** | +0.0204     |
| OHCD          | 0.4464     | **0.4891** | +0.0426     |
| TMC           | 0.6399     | **0.6713** | +0.0314     |
| FCS           | **0.9067** | 0.7731     | -0.1336     |
| **Composite** | 0.5952     | **0.6545** | **+0.0593** |


## Overall Results — Percentage Change


| Metric        | Prod   | Retrieved | % Change   |
| ------------- | ------ | --------- | ---------- |
| MMS           | 0.4262 | 0.5408    | +26.9%     |
| SR@3          | 0.2272 | 0.4346    | +91.2%     |
| SR@5          | 0.2937 | 0.5301    | +80.5%     |
| SR@10         | 0.3818 | 0.6284    | +64.6%     |
| CCR           | 0.8376 | 0.9057    | +8.1%      |
| ILD           | 0.6560 | 0.6763    | +3.1%      |
| OHCD          | 0.4464 | 0.4891    | +9.6%      |
| TMC           | 0.6399 | 0.6713    | +4.9%      |
| FCS           | 0.9067 | 0.7731    | -14.7%     |
| **Composite** | 0.5952 | 0.6545    | **+10.0%** |


## Per-Daypart — Composite % Change (Retrieved vs Prod)


| Daypart            | Prod   | Retrieved | % Change |
| ------------------ | ------ | --------- | -------- |
| weekday_breakfast  | 0.5933 | 0.6659    | +12.2%   |
| weekday_lunch      | 0.6075 | 0.6590    | +8.5%    |
| weekday_dinner     | 0.6027 | 0.6593    | +9.4%    |
| weekday_late_night | 0.5944 | 0.6546    | +10.1%   |
| weekend_breakfast  | 0.5861 | 0.6534    | +11.5%   |
| weekend_lunch      | 0.5861 | 0.6505    | +11.0%   |
| weekend_dinner     | 0.5881 | 0.6513    | +10.7%   |
| weekend_late_night | 0.5889 | 0.6296    | +6.9%    |


## Per-Daypart Results — Prod


| Daypart            | Count  | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ------ | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 7,497  | 0.4453 | 0.3447 | 0.8041 | 0.5826 | 0.5933    |
| weekday_lunch      | 13,297 | 0.4275 | 0.2997 | 0.8339 | 0.6634 | 0.6075    |
| weekday_dinner     | 13,114 | 0.4227 | 0.2854 | 0.8309 | 0.6719 | 0.6027    |
| weekday_late_night | 7,385  | 0.4362 | 0.3181 | 0.8134 | 0.6605 | 0.5944    |
| weekend_breakfast  | 5,337  | 0.4346 | 0.3173 | 0.8328 | 0.5946 | 0.5861    |
| weekend_lunch      | 9,415  | 0.4117 | 0.2564 | 0.8656 | 0.6772 | 0.5861    |
| weekend_dinner     | 10,375 | 0.4140 | 0.2569 | 0.8685 | 0.6825 | 0.5881    |
| weekend_late_night | 5,007  | 0.4322 | 0.3084 | 0.8386 | 0.6682 | 0.5889    |


## Per-Daypart Results — Retrieved


| Daypart            | Count  | MMS    | SR@5   | CCR    | ILD    | Composite |
| ------------------ | ------ | ------ | ------ | ------ | ------ | --------- |
| weekday_breakfast  | 7,779  | 0.5703 | 0.5947 | 0.9147 | 0.6603 | 0.6659    |
| weekday_lunch      | 13,406 | 0.5359 | 0.4962 | 0.8828 | 0.6850 | 0.6590    |
| weekday_dinner     | 13,226 | 0.5354 | 0.4944 | 0.8868 | 0.6855 | 0.6593    |
| weekday_late_night | 7,598  | 0.5461 | 0.5604 | 0.9203 | 0.6594 | 0.6546    |
| weekend_breakfast  | 5,650  | 0.5527 | 0.5842 | 0.9299 | 0.6488 | 0.6534    |
| weekend_lunch      | 9,670  | 0.5410 | 0.5347 | 0.9123 | 0.6928 | 0.6505    |
| weekend_dinner     | 10,564 | 0.5376 | 0.5242 | 0.9115 | 0.6893 | 0.6513    |
| weekend_late_night | 5,307  | 0.5092 | 0.5119 | 0.9301 | 0.6529 | 0.6296    |


