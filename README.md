# CompanyOS

A company organized as agent skills. Each role is one folder containing **SKILL.md** (how it works) and **temporal.yaml** (when it runs). Inspired by [gstack](https://github.com/garrytan/gstack); arranged by department, with a separate Temporal/Codex runtime.

```text
company-os/
├── SKILL.md                       # route a request to a role
├── executive/ceo/                 # company direction and subordinate role design
├── governance.yaml                # founder-owned role-editing scopes
├── engineering/
│   ├── manager/                   # department priorities and role evolution
│   ├── discovery/                 # daily evidence → backlog
│   ├── planner/                   # prioritized issue → plan
│   ├── developer/                 # approved plan → draft PR
│   ├── reviewer/                  # PR → code review
│   ├── qa/                        # implementation → test evidence
│   ├── release/                   # staging evidence → release brief
│   └── retrospective/             # weekly engineering review
├── operations/
│   ├── manager/                   # operating readiness and role evolution
│   ├── project-setup/             # new company/project bootstrap
│   └── portfolio-review/          # daily priorities and role handoffs
├── sales/
│   ├── manager/                   # growth experiments and role evolution
│   ├── linkedin/                  # weekly content/outreach drafts
│   └── seo/                       # weekly search/content proposals
├── schemas/temporal.schema.json   # executable manifest contract
├── scripts/                       # catalog validation and legacy lock helper
├── docs/                          # operating contracts and migration
├── standards/                     # release standards
└── templates/                     # project briefs and CI starter files
```

Every role directory has the same two-file interface. Supporting `references/`, `scripts/` or `assets/` belong inside a role only when useful. Add deeper levels as the company grows; stable IDs follow the relative path (`engineering/qa` → `engineering-qa`).

## One role

`engineering/developer/SKILL.md` is a normal skill with `name` and `description` frontmatter plus instructions. Its adjacent configuration is:

```yaml
version: 2
id: engineering-developer
workspace: project
trigger:
  type: event
  name: plan.approved
paused: true
timeout_seconds: 2700
sandbox: workspace-write
session: new
```

SKILL.md is the source you edit. Unlike gstack's generated skill variants, this catalog does not need `.tmpl` files yet. See [upstream mapping and attribution](docs/gstack.md).

## How it runs

The private backend recursively discovers role pairs from `skills_dir`, validates them, and starts bounded Codex sessions through Temporal. It supports manual invocation, named events, intervals and timezone-aware cron schedules. All role schedules start paused. Event sources are native adapters/operator commands; a label such as `plan.approved` is not approval evidence by itself.

The frontend delivery adapter connects prioritized Linear issues to planner → approved plan → developer → QA → CI/staging → exact-SHA human approval → production. Reviewer, release-brief and sales events can be invoked through the generic event interface; automatic GitHub/LinkedIn/Search Console webhook ingestion is not installed by this repository.

## Repository boundaries

- **This public repository:** generic skills, triggers, contracts and examples. One source of truth for role behavior.
- **Private runtime:** Temporal workflows, Codex sessions and journals. Native integrations live in project adapters. It loads this catalog instead of copying prompts.
- **Private company/project context:** checkout paths, destinations, account IDs, approvers, priorities and role overrides. Credentials remain in secret stores.
- **Product repositories:** source, tests, previews and deployment workflows. The landing kit remains a separate design library.

Start with [the root routing skill](SKILL.md), [runtime configuration](docs/runtime.md) and [migration notes](docs/migration.md). Run `python scripts/validate.py` after installing PyYAML and jsonschema. Skills are independently readable without Temporal; host-specific discovery/installation is separate from backend recursive loading.

## Organization and evolution

The [organization contract](docs/organization.md) defines the CEO, three department managers, reporting cadence and scoped role changes. Managers can prepare subordinate role changes in isolated catalog branches; the CEO can redesign subordinate departments. Changes remain reviewed before adoption, and new roles start paused. Bind management roles to a dedicated `catalog` checkout, separately from product workspaces.
