# Cadence

These are proposed rituals. Nothing is scheduled by this repository.

| Trigger | Ritual | Result |
| --- | --- | --- |
| Once daily, company-local morning | Read last checkpoint; reconcile open work; select one next deliverable | One prioritized brief, or explicit no-op |
| On a task or code change | Build, review, release | Verified change or bounded defect list |
| After a deployment | Smoke check production URL and important links | Healthy release or rollback / incident record |
| End of daily cycle | Record shipped work, cost, failures and next step | Durable checkpoint; notify only for a shipment, meaningful change, failure or decision |
| Once weekly, inside the daily run | Portfolio review | Continue, maintain, pause or archive recommendation per project |

Start without an hourly agent loop for a static site. Add an inexpensive deterministic uptime check after launch; wake the agent for actionable failures. An hourly reasoning loop should have a demonstrated workload before being enabled.

A daily project target is a throughput goal. Count a launch only when its live artifact and acceptance evidence exist; count a draft separately. Budget maintenance alongside launches. Never manufacture a launch or abandon a broken release just to satisfy the daily count.
