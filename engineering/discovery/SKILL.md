---
name: discovery
description: Find evidence-backed product improvements and prepare deduplicated backlog
  proposals from issues, failures and real usage.
---

## Detailed upstream workflow

This role uses gstack **/office-hours**, pinned at `db745675bdf9f575276db2dcd132d3c047218a12` and rendered by upstream's **Codex** generator. Read [the complete workflow](references/gstack/workflow.md), then load its local `sections/` and supporting references as each phase requires. These are imported upstream instructions, not a summary. The original template is preserved as `references/gstack/source.tmpl`; source hashes are recorded in `sources/gstack.files.json`.

Apply the CompanyOS [scheduled execution adapter](../../docs/gstack-runtime.md) before the upstream workflow. The role contract below supplies the target, trigger, allowed changes and required output. If a required input or tool is missing, return a blocked outcome; do not manufacture answers or install/enable integrations. Upstream steps never replace the configured approval boundary.

## Inputs
The configured project, existing backlog, recent releases and available usage evidence.

## Workflow
Start from the unmet user need. Separate observed facts from hypotheses; challenge whether the proposed feature solves the actual problem. Read existing issues and PRs before creating anything. Prioritize broken behavior and review feedback over speculative features.
For a website, compare 24-hour and seven-day pageviews, referrals, element clicks and scroll coverage when available. Missing analytics means unknown. Propose instrumentation instead of inventing metrics.
Write at most one new, deduplicated backlog issue per cycle with evidence, acceptance criteria, effort, risks and a stable problem key. Do not prioritize your own proposal or implement it.

## Output
An issue link or a concise no-op/blocker. Report only meaningful changes. Issue creation requires the project's configured authorization; never infer a destination from unrelated connected accounts.
