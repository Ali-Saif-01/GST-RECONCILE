# GST Reconcile 

**From reconciliation to resolution.**

GST Reconcile is a hackathon MVP that compares a purchase register with GST filing data, classifies reconciliation exceptions, groups them by supplier, estimates the exposure associated with those exceptions, and generates a supplier follow-up draft.

## Run

```bash
cd GST_Reconcile_FINAL
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 90-second demo

1. Open the app.
2. Keep **Use demo data** enabled.
3. Click **Run Reconciliation**.
4. Show the four headline metrics.
5. Show the **Supplier Chase Queue**.
6. Select a high-priority exception.
7. Explain the exception and exposure.
8. Click **Generate Supplier Follow-up**.
9. Download the reconciliation CSV.

## Architecture

Financial logic is deterministic: GSTIN/invoice normalization, matching, exception classification, tolerance checks, exposure calculations, and supplier prioritization are implemented in Python/Pandas. The explanation and supplier message are generated from the already-computed exception data; no external API is required.

## Important positioning

GST reconciliation itself is not presented as novel. The product focuses on the operational layer after reconciliation: **exception → priority → supplier action**.

Exposure shown by the prototype is a reconciliation metric based on supplied records. It is not a legal determination of ITC claimability, tax liability, or filing correctness. Human review remains required.

## Demo data

The included CSVs are controlled hackathon demo data containing matched records and deliberate exception cases. They are not real taxpayer records.
