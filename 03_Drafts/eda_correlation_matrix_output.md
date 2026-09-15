# EDA Correlation Matrix — wildcat_loans_clean.csv

Output of `scripts/eda_correlation_matrix.py` run against `02_Data/Raw/wildcat_loans_clean.csv`. `loan_id` and `borrower_id` excluded as identifiers. All values rounded to two decimal places.

## Correlation matrix

| | loan_amount | interest_rate | loan_term_months | credit_score | debt_to_income_ratio | annual_income |
|---|---|---|---|---|---|---|
| loan_amount | 1.00 | -0.01 | 0.00 | 0.03 | -0.01 | 0.02 |
| interest_rate | -0.01 | 1.00 | 0.01 | -0.84 | -0.00 | 0.05 |
| loan_term_months | 0.00 | 0.01 | 1.00 | -0.01 | 0.02 | -0.00 |
| credit_score | 0.03 | -0.84 | -0.01 | 1.00 | 0.00 | -0.04 |
| debt_to_income_ratio | -0.01 | -0.00 | 0.02 | 0.00 | 1.00 | -0.01 |
| annual_income | 0.02 | 0.05 | -0.04 | -0.01 | -0.01 | 1.00 |

## Three strongest correlations

| Rank | Variable 1 | Variable 2 | Correlation |
|---|---|---|---|
| 1 | interest_rate | credit_score | -0.84 |
| 2 | interest_rate | annual_income | +0.05 |
| 3 | credit_score | annual_income | -0.04 |

## Interpretation

There is exactly one meaningful relationship in this dataset: `interest_rate` and `credit_score` are strongly negatively correlated (-0.84) — borrowers with higher credit scores are charged noticeably lower interest rates, which lines up with standard risk-based pricing and with the loan_status patterns seen earlier (lower scores → higher rates → more delinquency/default).

Every other pair is close to zero (the #2 and #3 strongest correlations are only ±0.04–0.05), meaning `loan_amount`, `loan_term_months`, `debt_to_income_ratio`, and `annual_income` are essentially uncorrelated with each other and with the rest of the numeric fields in this dataset. `credit_score` and `interest_rate` are the only two variables that move together in any meaningful way.
