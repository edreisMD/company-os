---
name: retrospective
description: Review a week of engineering outcomes, delivery bottlenecks and failures
  to recommend concrete improvements.
---

## Detailed upstream workflow

This role uses gstack **/retro**, pinned at `db745675bdf9f575276db2dcd132d3c047218a12` and rendered by upstream's **Codex** generator. Read [the complete workflow](references/gstack/workflow.md), then load its local `sections/` and supporting references as each phase requires. These are imported upstream instructions, not a summary. The original template is preserved as `references/gstack/source.tmpl`; source hashes are recorded in `sources/gstack.files.json`.

Apply the CompanyOS [scheduled execution adapter](../../docs/gstack-runtime.md) before the upstream workflow. The role contract below supplies the target, trigger, allowed changes and required output. If a required input or tool is missing, return a blocked outcome; do not manufacture answers or install/enable integrations. Upstream steps never replace the configured approval boundary.

## Inputs
The project's previous report, recent commits, PRs, checks, incidents and real usage/cost evidence.

## Workflow
Separate shipped work from proposals. Summarize throughput, review age, change failures, PR sizes and frequently changed components where evidence is available. Compare with the prior period and explain uncertainty; do not invent productivity scores.
Identify the most useful delivered change and recurring friction. Propose at most three priorities with owners or role handoffs, and recommend continue/maintain/pause where warranted. Do not use commit volume as a proxy for individual worth.

## Output
A private weekly report with evidence, trends and concrete decisions. No code changes, deployments, issue closure or unsolicited messages.
