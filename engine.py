import io
import re
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
REQUIRED = ["Supplier Name", "Supplier GSTIN", "Invoice Number", "Invoice Date", "Taxable Value", "Tax Rate", "CGST", "SGST", "IGST", "ITC Amount"]


def norm_text(value):
    if pd.isna(value):
        return ""
    return re.sub(r"[^A-Z0-9]", "", str(value).upper())


def clean_numeric(df):
    for col in ["Taxable Value", "Tax Rate", "CGST", "SGST", "IGST", "ITC Amount"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df


def validate_columns(df, label):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"{label} is missing: {', '.join(missing)}")


def load_file(uploaded):
    if uploaded.name.lower().endswith(".xlsx"):
        return pd.read_excel(uploaded)
    return pd.read_csv(uploaded)


def load_demo():
    books = pd.read_csv(BASE / "data" / "purchase_register.csv")
    filing = pd.read_csv(BASE / "data" / "gstr2b_demo.csv")
    return books, filing


def reconcile(books, filing, tolerance=1.0):
    books = books.copy()
    filing = filing.copy()
    validate_columns(books, "Purchase Register")
    validate_columns(filing, "GST Filing")
    books = clean_numeric(books)
    filing = clean_numeric(filing)

    for df in (books, filing):
        df["_gstin"] = df["Supplier GSTIN"].map(norm_text)
        df["_inv"] = df["Invoice Number"].map(norm_text)
        df["_key"] = df["_gstin"] + "|" + df["_inv"]

    filing_map = filing.drop_duplicates("_key", keep="first").set_index("_key")
    results = []
    filing_keys = set(filing["_key"])

    for _, row in books.iterrows():
        key = row["_key"]
        base = row.to_dict()
        base.update({"Exception Type": "MATCHED", "Filing Taxable Value": 0.0, "Filing ITC Amount": 0.0, "Exposure": 0.0, "Explanation": "Invoice matched successfully.", "Recommended Action": "No action required."})
        if key not in filing_map.index:
            base.update({"Exception Type": "MISSING_IN_2B", "Exposure": float(row["ITC Amount"]), "Explanation": "Purchase invoice is present in the books but no matching filing record was found.", "Recommended Action": "Contact supplier and request filing confirmation/correction."})
        else:
            fr = filing_map.loc[key]
            base["Filing Taxable Value"] = float(fr["Taxable Value"])
            base["Filing ITC Amount"] = float(fr["ITC Amount"])
            taxable_diff = abs(float(row["Taxable Value"]) - float(fr["Taxable Value"]))
            itc_diff = abs(float(row["ITC Amount"]) - float(fr["ITC Amount"]))
            if taxable_diff > tolerance or itc_diff > tolerance:
                base.update({"Exception Type": "VALUE_MISMATCH", "Exposure": float(row["ITC Amount"]), "Explanation": f"Invoice was found, but the supplied taxable value / ITC differs beyond the ₹{tolerance:,.0f} tolerance.", "Recommended Action": "Ask supplier to confirm the invoice and filing values."})
        results.append(base)

    # Filing-only records
    for _, row in filing.iterrows():
        if row["_key"] not in set(books["_key"]):
            base = {c: row.get(c, "") for c in REQUIRED}
            base.update({"Exception Type": "MISSING_IN_BOOKS", "Filing Taxable Value": float(row["Taxable Value"]), "Filing ITC Amount": float(row["ITC Amount"]), "Exposure": float(row["ITC Amount"]), "Explanation": "Filing record was found without a matching purchase-register record.", "Recommended Action": "Verify whether the invoice belongs in the purchase register before taking action."})
            results.append(base)

    out = pd.DataFrame(results)
    if out.empty:
        return out
    # Duplicate candidates in the purchase register.
    dup_keys = set(books.loc[books["_key"].duplicated(keep=False), "_key"])
    out.loc[out.apply(lambda r: norm_text(r.get("Supplier GSTIN")) + "|" + norm_text(r.get("Invoice Number")) in dup_keys and r["Exception Type"] == "MATCHED", axis=1), "Exception Type"] = "DUPLICATE_CANDIDATE"
    out.loc[out["Exception Type"] == "DUPLICATE_CANDIDATE", "Explanation"] = "More than one purchase-register row shares the normalized GSTIN + invoice number key."
    out.loc[out["Exception Type"] == "DUPLICATE_CANDIDATE", "Recommended Action"] = "Review the duplicate candidate before final accounting treatment."
    out["Priority"] = out.apply(priority, axis=1)
    return out


def priority(row):
    et = row.get("Exception Type", "")
    exposure = float(row.get("Exposure", 0) or 0)
    if et == "MISSING_IN_2B" and exposure >= 50000:
        return "HIGH"
    if et in {"MISSING_IN_2B", "VALUE_MISMATCH", "MISSING_IN_BOOKS", "DUPLICATE_CANDIDATE"}:
        return "MEDIUM"
    return "LOW"


def explain(row):
    return {
        "MISSING_IN_2B": "This invoice exists in the purchase register but was not found in the supplied filing data. The next operational step is supplier follow-up.",
        "VALUE_MISMATCH": "The invoice matched on GSTIN and normalized invoice number, but the supplied values differ beyond tolerance. Ask the supplier to confirm the values and filing record.",
        "MISSING_IN_BOOKS": "The filing contains a record that is not present in the purchase register. Verify whether the purchase belongs in the books before taking action.",
        "DUPLICATE_CANDIDATE": "Multiple purchase-register rows share the same normalized matching key. Review for a duplicate before final treatment.",
        "MATCHED": "The invoice matched the supplied filing record within the configured tolerance.",
    }.get(row.get("Exception Type"), "Review this exception using the underlying records.")


def supplier_email(row):
    supplier = row.get("Supplier Name", "Supplier")
    invoice = row.get("Invoice Number", "the invoice")
    et = row.get("Exception Type", "exception")
    if et == "MISSING_IN_2B":
        issue = "the invoice is present in our purchase records but was not found in the supplied GST filing data"
    elif et == "VALUE_MISMATCH":
        issue = "the invoice was found, but the values in our records and the supplied filing data differ"
    else:
        issue = "we found a reconciliation exception that needs confirmation"
    return f"Subject: GST reconciliation confirmation required — {invoice}\n\nHi {supplier} team,\n\nDuring our GST reconciliation, we noticed that {issue}. Could you please verify the invoice and filing details and confirm the correction/status?\n\nInvoice: {invoice}\nException: {et}\n\nPlease share the updated filing/invoice details if a correction is required.\n\nThanks,\nFinance Team"


