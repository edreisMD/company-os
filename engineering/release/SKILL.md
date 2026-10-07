---
name: release
description: Prepare a release decision from exact-revision CI, review and staging
  evidence, including rollback readiness.
---

## Detailed upstream workflow

This role uses gstack **/ship**, pinned at `db745675bdf9f575276db2dcd132d3c047218a12` and rendered by upstream's **Codex** generator. Read [the complete workflow](references/gstack/workflow.md), then load its local `sections/` and supporting references as each phase requires. These are imported upstream instructions, not a summary. The original template is preserved as `references/gstack/source.tmpl`; source hashes are recorded in `sources/gstack.files.json`.

Apply the CompanyOS [scheduled execution adapter](../../docs/gstack-runtime.md) before the upstream workflow. The role contract below supplies the target, trigger, allowed changes and required output. If a required input or tool is missing, return a blocked outcome; do not manufacture answers or install/enable integrations. Upstream steps never replace the configured approval boundary.

Use shipping checks to produce release-readiness evidence for the exact candidate revision. This role does not perform the upstream shipping or deployment actions itself.

## Inputs
Exact commit/image identity, successful non-skipped CI jobs, staging smoke evidence, review results and rollback target.

## Workflow
Verify all evidence refers to the same revision. Check the diff is final and no later changes invalidate tests or approvals. Describe the user-visible change and release risks; confirm the immutable artifact and previous healthy revision.
Prepare the founder's approval request in the configured native platform. The deterministic release controller, not this skill, verifies human approval and executes merge/promotion. Never treat a skipped deployment as a release or a mutable tag as evidence of a tested image.

## Output
A concise release brief with exact SHA/digest, evidence links and rollback, or concrete blocking conditions. Do not approve yourself, merge, deploy or send messages outside the invocation's authorization.
