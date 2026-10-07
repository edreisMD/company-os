---
name: planner
description: Turn a prioritized issue into an implementation plan covering architecture,
  edge cases, tests and rollback before coding.
---

## Detailed upstream workflow

This role uses gstack **/plan-eng-review**, pinned at `db745675bdf9f575276db2dcd132d3c047218a12` and rendered by upstream's **Codex** generator. Read [the complete workflow](references/gstack/workflow.md), then load its local `sections/` and supporting references as each phase requires. These are imported upstream instructions, not a summary. The original template is preserved as `references/gstack/source.tmpl`; source hashes are recorded in `sources/gstack.files.json`.

Apply the CompanyOS [scheduled execution adapter](../../docs/gstack-runtime.md) before the upstream workflow. The role contract below supplies the target, trigger, allowed changes and required output. If a required input or tool is missing, return a blocked outcome; do not manufacture answers or install/enable integrations. Upstream steps never replace the configured approval boundary.

## Inputs
A prioritized issue, the repository and project constraints. Resolve the target from the supplied context; ask only when it is genuinely ambiguous.

## Workflow
Challenge scope first: identify the smallest useful change and compare credible alternatives. Review architecture and data flow, code quality and reuse, test coverage and failure paths, then performance where relevant. Explain the important tradeoffs and recommend an option.
List acceptance criteria, affected files, edge cases, validation commands, migration risks and rollback. For stateful work, trace errors and partial completion. Do not implement the plan or quietly expand the issue.

## Output
For the Temporal delivery adapter, return only JSON: {"plan":"Markdown implementation plan"}. The adapter publishes the exact plan and waits for human approval of its hash. Interactive invocations may present the plan directly. Changed scope requires a revised plan and approval.
