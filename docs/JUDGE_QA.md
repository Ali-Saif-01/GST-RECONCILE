# Judge Q&A

### 1. Isn't this already in Tally or Zoho?
Yes. We are not claiming reconciliation itself is new. Our focus is the operational layer after reconciliation: prioritizing supplier exceptions and preparing the next action.

### 2. Why AI?
We don't need AI for financial calculations. Deterministic code is easier to audit. AI-style assistance is useful for turning an already-computed exception into a clear explanation or supplier message.

### 3. What if AI is wrong?
The prototype does not let AI decide the financial result. The exception and exposure are computed by deterministic rules. Communication is still reviewed by a human.

### 4. How do you calculate exposure?
For the prototype, exposure is derived from the ITC amount supplied in the purchase data for exception records. It is a reconciliation metric, not a legal claimability determination.

### 5. Is this tax advice?
No. It is a reconciliation and workflow prototype. Final tax/accounting treatment remains with the business's finance or tax professional.

### 6. Who pays?
The initial customer hypothesis is SMB finance teams and CA/accounting firms. The exact price points are hypotheses we would validate through pilots.

### 7. Why would customers use it if accounting software already reconciles?
The hypothesis is that the unresolved operational work after reconciliation is valuable enough to productize: supplier prioritization, explanations, communication drafts and resolution tracking.

### 8. What is the moat?
Over time: supplier history, exception patterns, configurable matching rules, audit trails, response tracking and integrations. The MVP is demonstrating the workflow, not claiming a finished moat.

### 9. What if source data is wrong?
The system reports what the supplied records show. It does not silently invent missing information. Users can inspect the underlying rows and correct the source data.

### 10. How does it scale?
The core operations are tabular and deterministic, so the engine can move from demo CSVs to database/API ingestion. Production scaling would also require security, audit logging and integration work.

### 11. What would you integrate with?
Accounting/ERP systems, GST data workflows and email/task systems, subject to customer and compliance requirements.

### 12. What happens after the supplier responds?
The next product layer would track the response, attach supporting documents, rerun reconciliation, and close the exception with an audit trail.

### 13. Biggest limitation?
The MVP is based on supplied datasets and simplified matching rules. Production tax workflows need more extensive validation, integrations and controls.

### 14. What would you build next?
Supplier response tracking, audit history, configurable matching rules, accounting integrations and controlled multi-client workflows.

### 15. How did you validate the problem?
The hackathon brief itself frames the task around automatically matching purchase invoices to GST filings and telling the business which suppliers to chase. The prototype directly targets that requested workflow.
