# EDA Categorical Frequencies — wildcat_loans_clean.csv

Output of `scripts/eda_categorical_frequencies.py` run against `02_Data/Raw/wildcat_loans_clean.csv`. Percentages rounded to one decimal place.

## loan_purpose

| loan_purpose | Count | Percent |
|---|---|---|
| Home Improvement | 724 | 30.9% |
| Auto | 603 | 25.8% |
| Personal | 475 | 20.3% |
| Business | 328 | 14.0% |
| Education | 210 | 9.0% |

## loan_status

| loan_status | Count | Percent |
|---|---|---|
| Current | 1454 | 62.1% |
| Paid Off | 532 | 22.7% |
| Delinquent | 248 | 10.6% |
| Default | 106 | 4.5% |

## state

| state | Count | Percent |
|---|---|---|
| PA | 384 | 16.4% |
| NJ | 272 | 11.6% |
| NY | 264 | 11.3% |
| TX | 132 | 5.6% |
| FL | 128 | 5.5% |
| CA | 115 | 4.9% |
| DE | 97 | 4.1% |
| VA | 94 | 4.0% |
| MD | 92 | 3.9% |
| MA | 87 | 3.7% |
| NC | 81 | 3.5% |
| IL | 78 | 3.3% |
| OH | 75 | 3.2% |
| CT | 71 | 3.0% |
| GA | 70 | 3.0% |
| MI | 50 | 2.1% |
| WA | 48 | 2.1% |
| AZ | 45 | 1.9% |
| CO | 43 | 1.8% |
| MN | 39 | 1.7% |
| Pennsylvania | 25 | 1.1% |
| Florida | 14 | 0.6% |
| New Jersey | 13 | 0.6% |
| New York | 12 | 0.5% |
| California | 5 | 0.2% |
| Illinois | 4 | 0.2% |
| Texas | 2 | 0.1% |

## Data quality note

The `state` column mixes two-letter abbreviations (e.g. `PA`, `NJ`, `NY`) with full state names (e.g. `Pennsylvania`, `New Jersey`, `New York`) for the same states. As printed, these are counted as separate categories, which understates each state's true share — e.g. `PA` (384, 16.4%) and `Pennsylvania` (25, 1.1%) together represent one state, ~17.5% of rows. Standardizing `state` to one format before further analysis would give a more accurate picture.
