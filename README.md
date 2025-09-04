
# Data Quality Monitoring Framework - Sample Project

This mini-project demonstrates a simple Data Quality (DQ) framework using CSV files, Python and pandas.
It is intentionally lightweight so you can run it on your laptop without Databricks or SAS.

## What is included
- data/customers.csv  (sample customers)
- data/orders.csv     (sample orders with some deliberate issues)
- dq_checks.py        (script that runs the checks and writes CSV + HTML reports into /output)
- requirements.txt
- data_dictionary.md
- metric_definitions.md
- output/              (where result files are written)

## How to run (basic)
1. Install Python (3.8+) if you don't have it.
   - Windows: https://www.python.org/downloads/
   - Linux: use your package manager (apt, yum, etc.)

2. Open a terminal (Command Prompt on Windows or Terminal on Mac/Linux) and change to the project folder:
   ```bash
   cd dq_project
   ```

3. (Optional but recommended) create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\\Scripts\\activate
   # mac / linux:
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the DQ checks script:
   ```bash
   python dq_checks.py
   ```

6. Open the output HTML summary:
   - `output/dq_summary_latest.html` in your browser to see a simple report.
   - `output/dq_results_latest.csv` contains the raw check rows.

## What the script checks
- row_count: how many rows in the table
- null_count: how many nulls per column
- duplicate_pk: duplicates based on primary key
- domain_check: values outside the allowed domain (e.g., status)
- date_parse: whether dates parse correctly
- numeric_parse: numeric parsing and negative value count
- referential_integrity: foreign keys that don't have matching parent keys

## Next steps (improve)
- Hook the script to a SQL database and run checks via queries
- Add GitHub Actions to run daily and push results to storage
- Build a Power BI dashboard from output CSV (see project notes)
