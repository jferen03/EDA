# EDA Missingness Analysis — wildcat_loans_clean.csv

Output of `scripts/eda_missingness_analysis.py` run against `02_Data/Raw/wildcat_loans_clean.csv`.

## Missing values per column

| Column | Missing count | Missing % |
|---|---|---|
| loan_id | 0 | 0.00% |
| origination_date | 0 | 0.00% |
| borrower_id | 0 | 0.00% |
| loan_amount | 0 | 0.00% |
| interest_rate | 0 | 0.00% |
| loan_term_months | 0 | 0.00% |
| credit_score | 47 | 2.01% |
| debt_to_income_ratio | 0 | 0.00% |
| loan_purpose | 0 | 0.00% |
| loan_status | 0 | 0.00% |
| annual_income | 0 | 0.00% |
| state | 0 | 0.00% |

`credit_score` is the only column with missing values: 47 rows (2.01% of the dataset).

## loan_status: full dataset vs. credit_score-missing rows

| loan_status | Full dataset % | credit_score-missing % |
|---|---|---|
| Current | 62.14% | 36.17% |
| Paid Off | 22.74% | 29.79% |
| Delinquent | 10.60% | 23.40% |
| Default | 4.53% | 10.64% |

## loan_purpose: full dataset vs. credit_score-missing rows

| loan_purpose | Full dataset % | credit_score-missing % |
|---|---|---|
| Home Improvement | 30.94% | 27.66% |
| Auto | 25.77% | 29.79% |
| Personal | 20.30% | 17.02% |
| Business | 14.02% | 21.28% |
| Education | 8.97% | 4.26% |

## Interpretation

`loan_purpose` looks roughly similar between the missing-`credit_score` rows and the full dataset — no single purpose stands out as driving the missingness.

`loan_status` does not look random, though: among rows missing `credit_score`, **Delinquent (23.40%) and Default (10.64%) together make up ~34%** of cases, versus only ~15% in the full dataset. Meanwhile "Current" loans are under-represented among the missing rows (36.17% vs. 62.14% overall). This suggests `credit_score` missingness is concentrated in loans that are already delinquent or in default, rather than missing completely at random — worth treating as **Missing Not At Random (MNAR)** rather than imputing it as if it were random.
