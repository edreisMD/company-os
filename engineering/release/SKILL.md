---
name: release
description: Prepare a release decision from exact-revision CI, review and staging
  evidence, including rollback readiness.
---

## Inputs
Exact commit/image identity, successful non-skipped CI jobs, staging smoke evidence, review results and rollback target.

## Workflow
Verify all evidence refers to the same revision. Check the diff is final and no later changes invalidate tests or approvals. Describe the user-visible change and release risks; confirm the immutable artifact and previous healthy revision.
Prepare the founder's approval request in the configured native platform. The deterministic release controller, not this skill, verifies human approval and executes merge/promotion. Never treat a skipped deployment as a release or a mutable tag as evidence of a tested image.

## Output
A concise release brief with exact SHA/digest, evidence links and rollback, or concrete blocking conditions. Do not approve yourself, merge, deploy or send messages outside the invocation's authorization.
