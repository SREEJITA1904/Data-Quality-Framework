
# Data Quality Monitoring Framework 

📌 Demonstrates **data governance, reporting continuity, and quality checks** using Python & pandas.  
This project aligns with real-world **Data Analyst roles in BFSI (like Barclays)** where data quality, lineage, and compliance are key.

## What is included
- data/customers.csv  (sample customers)
- data/orders.csv     (sample orders with some deliberate issues)
- dq_checks.py        (script that runs the checks and writes CSV + HTML reports into /output)
- requirements.txt
- data_dictionary.md
- metric_definitions.md
- output/              (where result files are written)

## 🚀 How to Run (Quick Start)
```bash
# clone this repo
git clone https://github.com/SREEJITA1904/Data-Quality-Framework.git
cd Data-Quality-Framework

# (optional) create a virtual env
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run DQ checks
python dq_checks.py

✅ Open output/dq_summary_latest.html → interactive summary report
✅ Or output/dq_results_latest.csv → raw results table

## What the script checks
- row_count: how many rows in the table
- null_count: how many nulls per column
- duplicate_pk: duplicates based on primary key
- domain_check: values outside the allowed domain (e.g., status)
- date_parse: whether dates parse correctly
- numeric_parse: numeric parsing and negative value count
- referential_integrity: foreign keys that don't have matching parent keys

👉 [View Sample HTML Report](output/example_dq_summary.html)


## Next steps (improve)
- Hook the script to a SQL database and run checks via queries
- Add GitHub Actions to run daily and push results to storage
- Build a Power BI dashboard from output CSV (see project notes)
