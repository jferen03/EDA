# EDA Inspection — wildcat_loans_clean.csv

Output of `scripts/eda_inspect.py` run against `02_Data/Raw/wildcat_loans_clean.csv`.

## Shape (rows, columns)

2340 rows × 12 columns

## Column names and data types

| Column | Data type |
|---|---|
| loan_id | int64 |
| origination_date | object |
| borrower_id | int64 |
| loan_amount | float64 |
| interest_rate | float64 |
| loan_term_months | int64 |
| credit_score | float64 |
| debt_to_income_ratio | float64 |
| loan_purpose | object |
| loan_status | object |
| annual_income | float64 |
| state | object |

## Missing values per column

| Column | Missing values |
|---|---|
| loan_id | 0 |
| origination_date | 0 |
| borrower_id | 0 |
| loan_amount | 0 |
| interest_rate | 0 |
| loan_term_months | 0 |
| credit_score | 47 |
| debt_to_income_ratio | 0 |
| loan_purpose | 0 |
| loan_status | 0 |
| annual_income | 0 |
| state | 0 |

**Total missing values:** 47 (all in `credit_score`)
