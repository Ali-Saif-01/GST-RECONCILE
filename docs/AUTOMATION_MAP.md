# Automation Map

## Current workflow

Collect purchase invoices
→ collect GST filing data
→ compare records
→ find mismatches
→ investigate each mismatch
→ prioritize suppliers
→ contact suppliers
→ track resolution

## GST Reconcile automates

**Data ingestion** — accepts the two source datasets.

**Normalization** — standardizes GSTIN and invoice-number formatting.

**Reconciliation** — deterministic GSTIN + normalized invoice matching with value tolerance.

**Exception detection** — identifies missing records, value mismatches, and duplicate candidates.

**Exposure calculation** — aggregates the ITC/exposure amount associated with exceptions from supplied records.

**Supplier prioritization** — converts invoice-level exceptions into a supplier chase queue.

**Explanation** — turns the already-computed exception into plain-language reasoning.

**Follow-up draft** — creates a supplier message using the exception data.

## Human-in-the-loop

Final financial review, supplier communication approval, tax/accounting decisions, and final filing decisions remain with a human.

## Why this is the right step

The repetitive part is not only matching. The high-friction operational step is moving from a spreadsheet full of exceptions to a clear list of suppliers and actions. The MVP targets that transition.
