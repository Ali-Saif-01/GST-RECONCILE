# Business Plan — GST Reconcile

## Problem
Finance teams can spend substantial effort comparing purchase records with GST filing data. The operational problem does not end when a mismatch is found: someone still needs to understand the exception, decide its priority, identify the supplier, and contact them.

## Target customers
- Small and mid-sized businesses with recurring vendor purchases
- Internal finance/accounting teams
- CA and accounting firms managing multiple clients

## Product
GST Reconcile ingests purchase-register and filing data, performs deterministic matching, identifies exceptions, groups them by supplier, prioritizes the supplier chase queue, and drafts follow-up communication.

## Automation choice
Automate the repetitive comparison and exception-to-action preparation. Keep final accounting/tax decisions human-reviewed.

## Differentiation hypothesis
The product is not claiming that GST reconciliation is new. Its focus is the workflow immediately after reconciliation: **what happened, how important is it, who needs attention, and what message should be sent?**

## Business model hypothesis
Illustrative validation hypothesis:
- Starter: ₹999/month
- Growth: ₹2,499/month
- CA / multi-client: custom

These are hypotheses to test with customers, not established market pricing.

## Success metrics
- Reconciliation time saved per month
- Exception detection precision on customer data
- Supplier-response rate after follow-up
- Time from exception detection to resolution
- Monthly active businesses / client accounts

## Risks
- Input data quality
- Tax-rule changes
- False matches if normalization rules are too aggressive
- Customer trust around financial data
- Need for human review before accounting/tax action

## Next steps
1. Test with real anonymized datasets.
2. Add configurable matching rules.
3. Add supplier-response tracking.
4. Integrate with accounting systems.
5. Add audit logs and role-based controls.
