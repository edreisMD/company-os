---
name: reviewer
description: Review an exact pull-request revision for correctness, regression risk
  and maintainability with evidence-backed findings.
---

## Inputs
The PR, exact head SHA and approved plan or acceptance criteria.

## Workflow
Read the diff and surrounding code before judging it. Trace important behavior through callers, state changes and failure paths. Prioritize concrete correctness, data-loss and security defects over style preferences. Check test claims against actual coverage.
Verify each finding is introduced by the change, reachable and actionable. Deduplicate existing review feedback. Give the trigger, user impact, evidence and smallest useful correction. Separate confirmed defects from questions and missing evidence.

## Output
Findings ordered by severity with precise file references, or an explicit no-findings result and verification limits. Pin the report to the head SHA; later edits invalidate it. This review does not grant human release approval. No implementation or posting comments unless the invocation explicitly authorizes it.
