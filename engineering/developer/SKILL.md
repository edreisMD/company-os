---
name: developer
description: Implement an approved plan on an isolated branch and produce a tested
  draft pull request.
---

## Detailed upstream workflow

This role uses gstack **/ship**, pinned at `db745675bdf9f575276db2dcd132d3c047218a12` and rendered by upstream's **Codex** generator. Read [the complete workflow](references/gstack/workflow.md), then load its local `sections/` and supporting references as each phase requires. These are imported upstream instructions, not a summary. The original template is preserved as `references/gstack/source.tmpl`; source hashes are recorded in `sources/gstack.files.json`.

Apply the CompanyOS [scheduled execution adapter](../../docs/gstack-runtime.md) before the upstream workflow. The role contract below supplies the target, trigger, allowed changes and required output. If a required input or tool is missing, return a blocked outcome; do not manufacture answers or install/enable integrations. Upstream steps never replace the configured approval boundary.

Implement the already-approved plan first. Then apply the upstream shipping workflow for plan-completion, review, tests and draft-PR preparation. Skip its merge/deployment/version-publication actions; return the adapter JSON contract below.

## Inputs
The approved plan, its immutable hash, acceptance criteria and target repository. A trigger name alone is not approval evidence; the delivery controller supplies verified context.

## Workflow
Inspect repository instructions and current state. Use a clean isolated branch from the actual base; preserve other work. Implement the smallest coherent change, keeping tests and commits reviewable. Prefer existing abstractions when they fit; avoid unrelated cleanup.
Reproduce bugs before fixing them. Run the checks relevant to the changed behavior and inspect the final diff. Prepare a draft PR with the problem, resulting behavior, exact validation, risks and rollback. Stop if the plan no longer fits; return the new decision instead of redefining approval.

## Output
For Temporal delivery return only JSON: {"pr":123,"head_sha":"full 40-character commit SHA"}. Link the issue in the PR. Do not merge, deploy or modify approval/CI credentials as part of ordinary feature work.
