
# dq_checks.py
import os
import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

DATA_DIR = "data"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Simple config for tables - edit paths/keys according to your CSVs
TABLES = {
    "customers": {
        "path": f"{DATA_DIR}/customers.csv",
        "pk": ["customer_id"],
        "date_cols": ["signup_date"]
    },
    "orders": {
        "path": f"{DATA_DIR}/orders.csv",
        "pk": ["order_id"],
        "fks": {"customer_id": ("customers", "customer_id")},
        "date_cols": ["order_date"],
        "numeric_cols": ["amount"],
        "domains": {"status": ["Placed", "Delivered", "Cancelled"]}
    }
}

results = []

def load_table(path):
    if not os.path.exists(path):
        logging.error("Missing file: %s", path)
        return None
    return pd.read_csv(path)

def run_checks(name, cfg):
    df = load_table(cfg["path"])
    if df is None:
        return
    nrows = len(df)
    results.append({"table": name, "check": "row_count", "status": "ok", "value": nrows, "details": ""})

    # Null counts
    nulls = df.isnull().sum()
    for col, cnt in nulls.items():
        status = "fail" if cnt > 0 else "ok"
        results.append({"table": name, "check": "null_count", "column": col, "status": status, "value": int(cnt), "details": ""})

    # Duplicates on PK
    if "pk" in cfg:
        dup_count = df.duplicated(subset=cfg["pk"]).sum()
        status = "fail" if dup_count > 0 else "ok"
        results.append({"table": name, "check": "duplicate_pk", "column": ",".join(cfg["pk"]), "status": status, "value": int(dup_count), "details": ""})

    # Domain checks
    for col, allowed in cfg.get("domains", {}).items():
        if col in df.columns:
            vals = set(df[col].dropna().unique())
            invalid = vals - set(allowed)
            status = "fail" if invalid else "ok"
            results.append({"table": name, "check": "domain_check", "column": col, "status": status, "value": len(invalid), "details": str(list(invalid))})

    # Date parsing checks
    for col in cfg.get("date_cols", []):
        if col in df.columns:
            parsed = pd.to_datetime(df[col], errors="coerce")
            bad = parsed.isna().sum()
            status = "fail" if bad > 0 else "ok"
            results.append({"table": name, "check": "date_parse", "column": col, "status": status, "value": int(bad), "details": ""})

    # Numeric checks
    for col in cfg.get("numeric_cols", []):
        if col in df.columns:
            coerced = pd.to_numeric(df[col], errors="coerce")
            nan_count = coerced.isna().sum()
            neg_count = (coerced < 0).sum()
            status = "fail" if nan_count > 0 else "ok"
            results.append({
    "table": name,
    "check": "numeric_parse",
    "column": col,
    "status": status,
    "value": int(nan_count),
    "details": f"negatives={int(neg_count)}"
})


    # Referential Integrity
    for fk_col, (ref_table, ref_col) in cfg.get("fks", {}).items():
        ref_cfg = TABLES.get(ref_table)
        if ref_cfg:
            ref_df = load_table(ref_cfg["path"])
            if ref_df is None:
                continue
            orphan_count = (~df[fk_col].isin(ref_df[ref_col])).sum()
            status = "fail" if orphan_count > 0 else "ok"
            results.append({"table": name, "check": "referential_integrity", "column": fk_col, "status": status, "value": int(orphan_count), "details": f"ref={ref_table}.{ref_col}"})

def main():
    for tname, cfg in TABLES.items():
        run_checks(tname, cfg)

    dfres = pd.DataFrame(results).fillna("")
    timestamp = datetime.now().isoformat(timespec='seconds').replace(':','-')
    out_csv = f"{OUTPUT_DIR}/dq_results_{timestamp}.csv"
    dfres.to_csv(out_csv, index=False)
    # also write a latest copy and a simple HTML
    dfres.to_csv(f"{OUTPUT_DIR}/dq_results_latest.csv", index=False)
    html = dfres.to_html(index=False)
    with open(f"{OUTPUT_DIR}/dq_summary_{timestamp}.html", "w") as f:
        f.write("<h2>Data Quality Check Results</h2>\\n")
        f.write(html)
    with open(f"{OUTPUT_DIR}/dq_summary_latest.html", "w") as f:
        f.write("<h2>Data Quality Check Results (latest)</h2>\\n")
        f.write(html)
    logging.info("Wrote results to %s and HTML summary", out_csv)

if __name__ == "__main__":
    main()
