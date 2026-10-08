# CompanyOS

A company organized as agent skills. Each role contains **SKILL.md** (how it works), **agent.yaml** (runtime-neutral execution metadata) and **temporal.yaml** (compatible Temporal configuration). Built from [our gstack fork](https://github.com/edreisMD/gstack), with complete upstream Codex workflows arranged behind department roles and a separate runtime.

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
├── teams/                         # frontend and open-source workflow graphs
├── schemas/                       # agent, team and Temporal contracts
├── scripts/                       # catalog validation and legacy lock helper
├── docs/                          # operating contracts and migration
├── standards/                     # release standards
└── templates/                     # project briefs and CI starter files
```

Every role directory has the same skill and configuration interface. Supporting `references/`, `scripts/` or `assets/` belong inside a role only when useful. Add deeper levels as the company grows; stable IDs follow the relative path (`engineering/qa` → `engineering-qa`).

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

SKILL.md contains the CompanyOS role contract. Mapped roles load complete generated gstack workflows from references/gstack; their upstream `.tmpl` sources and supporting sections are preserved. Edit CompanyOS contracts locally and regenerate upstream snapshots through the pinned importer. See [upstream mapping and attribution](docs/gstack.md).

## How it runs

[ceo](docs/ceo.md) coordinates objectives across projects through one Pi conversation, while Orca runs and exposes the workers. It reads agent.yaml and team.yaml at exact catalog commits. Private installation configuration binds projects to teams and configured harnesses. Teams include independent review and QA plus artifact-bound plan, release and publication decisions. The ceo pilot keeps the Temporal backend paused.

The private backend recursively discovers role pairs from `skills_dir`, validates them, and starts bounded Codex sessions through Temporal. It supports manual invocation, named events, intervals and timezone-aware cron schedules. All role schedules start paused. Event sources are native adapters/operator commands; a label such as `plan.approved` is not approval evidence by itself.

The frontend delivery adapter connects prioritized Linear issues to planner → approved plan → developer → QA → CI/staging → exact-SHA human approval → production. Reviewer, release-brief and sales events can be invoked through the generic event interface; automatic GitHub/LinkedIn/Search Console webhook ingestion is not installed by this repository.

## Repository boundaries

- **This public repository:** generic skills, triggers, contracts and examples. One source of truth for role behavior.
- **Runtime:** public ceo harness or the private Temporal backend. Installation state, sessions, journals and native account bindings remain private. Both read this catalog instead of duplicating prompts.
- **Private company/project context:** checkout paths, destinations, account IDs, approvers, priorities and role overrides. Credentials remain in secret stores.
- **Product repositories:** source, tests, previews and deployment workflows. The landing kit remains a separate design library.

Start with [the root routing skill](SKILL.md), [runtime configuration](docs/runtime.md) and [migration notes](docs/migration.md). Run `python scripts/validate.py` after installing PyYAML and jsonschema. Skills are independently readable without Temporal; host-specific discovery/installation is separate from backend recursive loading.

## Organization and evolution

The [organization contract](docs/organization.md) defines the CEO, three department managers, reporting cadence and scoped role changes. Managers can prepare subordinate role changes in isolated catalog branches; the CEO can redesign subordinate departments. Changes remain reviewed before adoption, and new roles start paused. Bind management roles to a dedicated `catalog` checkout, separately from product workspaces.

An installation may explicitly authorize ceo's scoped organization experiments, publishing generic changes to ceo/active and activating exact commits for future goals. That private founder grant, its validation rules and rollback are described in [ceo teams](docs/ceo.md); a role cannot change its own authority.

For the proposed visual company console and runtime integration, see the [Orca source assessment and pilot criteria](docs/orca-assessment.md).
