# Role and runtime contract

The executable schema is [temporal.schema.json](../schemas/temporal.schema.json), generated from the backend's `AgentConfig`. A role is a `SKILL.md`/`temporal.yaml` pair. The root routing skill has no temporal.yaml and is not a scheduled agent.

## Triggers

```yaml
# Daily in a specific timezone; weekly example: expression: "0 10 * * 1"
trigger:
  type: cron
  expression: "0 9 * * *"
  timezone: America/Los_Angeles
```

```yaml
# Every fifteen minutes
trigger:
  type: interval
  seconds: 900
```

```yaml
# Matched by an authenticated adapter or explicit operator command
trigger:
  type: event
  name: issue.prioritized
```

```yaml
trigger:
  type: manual
```

Cron uses five numeric fields: minute, hour, day, month, weekday (Sunday=0). Values, lists, ranges, `*` and steps are supported; named months/weekdays and extension syntax are not. Interval bounds are 60 seconds to seven days. Cron/interval schedules use Temporal SKIP overlap and are synchronized paused. Manual/event roles cannot accidentally acquire timer schedules.

The backend validates IDs against department paths, rejects duplicate IDs, malformed frontmatter, unknown fields, invalid triggers and escaping symlinks. A role's digest covers the effective private overrides, working directory and every supporting file inside its folder. Existing scheduled revisions stop if those inputs change; resynchronize deliberately.

## Private bindings

A runtime configuration binds public workspace keys to real checkouts:

```yaml
instance_id: my-company
skills_dir: ../company-os
allow_live: false
workspaces:
  project: /path/to/product
agent_overrides:
  engineering-discovery:
    paused: true
    trigger:
      type: cron
      expression: "0 9 * * *"
      timezone: America/Los_Angeles
```

Private overrides may change workspace, paused state and trigger. They cannot replace instructions or relax sandbox/time limits. Keep deployment/approval identities in the private project's configuration. Use a distinct instance_id and task_queue for each project worker. The instance ID namespaces timer and event workflow IDs; task queues route executions to the correct worker.

## Backend commands

- `coos validate`: validate the whole nested catalog and effective bindings.
- `coos run engineering-planner`: dry-run a selected role; explicit `--live` needs worker `allow_live`.
- `coos schedules`: synchronize cron/interval roles as paused dry-run schedules. `--live` still synchronizes paused.
- `coos event issue.prioritized --event-id ISSUE-123-plan-v1`: dry-run matching event roles. `--context-file` supplies JSON; `--live` requires enabled private bindings and worker permission.
- `coos resume-schedule ROLE --confirm-legacy-disabled`: activate a reviewed timer after private `paused: false`, synchronization and scheduler cutover.

Event IDs are stable deduplication keys: the same event/role cannot create duplicate sessions. Generic events do not verify platform approvals; the existing delivery controller verifies native human comments before implementation/release. The backend supplies model permissions separately. A timer or skill file never grants permission to publish posts, send messages, deploy, change credentials or spend money.
