# EDA Group-by Summary by Loan Status — wildcat_loans_clean.csv

Output of `scripts/eda_groupby_loan_status.py` run against `02_Data/Raw/wildcat_loans_clean.csv`. Sorted by count, descending.

| loan_status | Count | Mean loan_amount | Mean interest_rate | Mean credit_score | Mean debt_to_income_ratio |
|---|---|---|---|---|---|
| Current | 1454 | $70,770.63 | 11.3484% | 684.7 | 0.3148 |
| Paid Off | 532 | $67,404.88 | 12.2143% | 670.3 | 0.3124 |
| Delinquent | 248 | $57,476.85 | 13.3605% | 645.6 | 0.3208 |
| Default | 106 | $66,399.23 | 14.2347% | 617.1 | 0.3282 |

## Interpretation

Mean `credit_score` drops steadily as loan health worsens — 684.7 (Current) → 670.3 (Paid Off) → 645.6 (Delinquent) → 617.1 (Default) — a roughly 68-point gap between the best- and worst-performing groups. `mean_interest_rate` moves in the opposite direction, rising from 11.35% to 14.23% across the same groups, echoing the box plot findings: riskier (lower-credit-score) borrowers are priced at higher rates and are more likely to end up delinquent or in default.

`mean_debt_to_income_ratio` is fairly flat across groups (0.3124–0.3282), so it doesn't separate the groups nearly as clearly as credit score or interest rate do. `mean_loan_amount` also doesn't move in a clean progression — Delinquent loans actually have the lowest average amount ($57,476.85) of the four groups, so loan size on its own isn't a strong indicator of loan health here.
