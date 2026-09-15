# EDA Default Rate by Loan Purpose — wildcat_loans_clean.csv

Output of `scripts/eda_default_rate_by_purpose.py` run against `02_Data/Raw/wildcat_loans_clean.csv`. Sorted by default percentage, descending.

| loan_purpose | Count | Default count | Default % |
|---|---|---|---|
| Home Improvement | 724 | 47 | 6.49% |
| Personal | 475 | 23 | 4.84% |
| Business | 328 | 11 | 3.35% |
| Auto | 603 | 20 | 3.32% |
| Education | 210 | 5 | 2.38% |

## Interpretation

Home Improvement loans have the highest default rate (6.49%) — nearly triple Education's (2.38%), the lowest of the five purposes. Home Improvement is also the largest single group by volume (724 loans, ~31% of the portfolio), so it's contributing a disproportionate share of total defaults, not just a high rate on a small sample. Personal loans are a distant second at 4.84%. Business and Auto sit close together in the middle (3.35% and 3.32%), and Education loans default least often of any purpose.
