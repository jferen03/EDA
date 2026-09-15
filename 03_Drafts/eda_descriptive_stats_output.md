# EDA Descriptive Statistics — wildcat_loans_clean.csv

Output of `scripts/eda_descriptive_stats.py` run against `02_Data/Raw/wildcat_loans_clean.csv`. All values rounded to two decimal places.

| Statistic | loan_id | borrower_id | loan_amount | interest_rate | loan_term_months | credit_score | debt_to_income_ratio | annual_income |
|---|---|---|---|---|---|---|---|---|
| count | 2340.00 | 2340.00 | 2340.00 | 2340.00 | 2340.00 | 2293.00 | 2340.00 | 2340.00 |
| mean | 1170.50 | 1258.05 | 68398.49 | 11.89 | 68.69 | 674.39 | 0.32 | 155095.67 |
| std_dev | 675.64 | 732.22 | 92614.38 | 4.49 | 27.29 | 75.98 | 0.14 | 182699.38 |
| min | 1.00 | 1.00 | 2073.62 | 4.50 | 36.00 | 500.00 | 0.08 | 24014.42 |
| 25th_percentile | 585.75 | 619.75 | 24498.05 | 8.10 | 36.00 | 614.00 | 0.20 | 32742.90 |
| median | 1170.50 | 1253.50 | 40691.79 | 11.52 | 60.00 | 676.00 | 0.32 | 42624.11 |
| 75th_percentile | 1755.25 | 1895.50 | 60596.09 | 15.34 | 84.00 | 725.00 | 0.44 | 255153.52 |
| max | 2340.00 | 2525.00 | 499030.58 | 20.98 | 120.00 | 850.00 | 0.55 | 649768.69 |

## Notes

- `credit_score`'s count (2293) is lower than the rest (2340) because of the 47 missing values identified in the missingness analysis — pandas' `describe()` excludes NaNs from these stats.
- `loan_id` and `borrower_id` are identifier columns, not measurements, so their descriptive stats (e.g. mean, std_dev) aren't meaningful on their own — they're included here because they're numeric columns, but should generally be excluded from any actual analysis.
- `loan_amount` ranges from about $2,073.62 to $499,030.58, with a median of $40,691.79 and a mean of $68,398.49 — the mean being well above the median indicates the distribution is right-skewed (a smaller number of very large loans pull the average up).
