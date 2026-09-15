# EDA Date Conversion — wildcat_loans_clean.csv

Output of `scripts/eda_convert_dates.py` run against `02_Data/Raw/wildcat_loans_clean.csv`.

## origination_date type check

| | Data type |
|---|---|
| Before conversion | object (text) |
| After conversion | datetime64[ns] |

**Result:** `origination_date` was stored as text (`object`) and was converted to a proper `datetime64` type.

```
Before: origination_date is stored as object
After:  origination_date converted to datetime64[ns]
Converted origination_date from text (object) to datetime.
```
