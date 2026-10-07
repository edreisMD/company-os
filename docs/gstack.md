# gstack fork and reproducible workflow imports

Fork: https://github.com/edreisMD/gstack
Upstream: https://github.com/garrytan/gstack
Pinned revision: `db745675bdf9f575276db2dcd132d3c047218a12` (MIT; see [license](../GSTACK-LICENSE)).

CompanyOS now imports complete upstream workflows rather than using concise original substitutes. The fork preserves upstream layout and generator so updates remain straightforward. CompanyOS is the organized execution catalog: each department role retains SKILL.md and temporal.yaml, with its full rendered upstream workflow and supporting files under references/gstack. The root skill tree is therefore organized by company responsibility without breaking upstream runtime paths by moving its implementation files.

| CompanyOS role | Upstream workflow |
|---|---|
| executive/ceo | plan-ceo-review |
| engineering/manager | autoplan |
| engineering/discovery | office-hours |
| engineering/planner | plan-eng-review |
| engineering/developer | ship after approved implementation |
| engineering/reviewer | review |
| engineering/qa | qa-only |
| engineering/release | ship readiness, no release side effects |
| engineering/retrospective | retro |
| operations/manager | health |
| operations/project-setup | setup-deploy inspection |

Growth manager, LinkedIn, SEO and portfolio-review remain CompanyOS-native: this upstream does not supply equivalent business roles. Do not label those as imported gstack agents. Developer's implementation contract also remains CompanyOS-specific; /ship supplies the detailed completion/test/review/PR workflow, not a general implementation agent.

## Reproduce and update

Read sources/gstack.lock.json, check out its exact revision from the fork, then run `python scripts/import_gstack.py --source /path/to/gstack`. It invokes upstream `bun scripts/gen-skill-docs.ts --host codex` into a temporary directory and imports complete selected workflows, generated sections and original supporting resources. No global skill installation or setup script runs. Bun is required only for regeneration, not hash validation. CI runs `python scripts/import_gstack.py --check` to verify every imported file against the recorded snapshot hashes.

Generated workflow.md files preserve upstream instructions byte-for-byte; source.tmpl preserves the editable upstream template. Keep CompanyOS scheduling/permission differences in the role wrapper and [runtime adapter](gstack-runtime.md), rather than maintaining a silently simplified fork of the content. Upstream Codex support is marked experimental by its host definition; runtime helper installation and live compatibility still need a separate smoke test.

The existing Temporal role manifests remain the executable schedules/events. Full gstack /autoplan supplies its internal sequential review phases; importing it does not install a separate multi-agent DAG engine. All role schedules remain paused. See the [Orca assessment](orca-assessment.md) for the proposed visualization and agent-runtime integration.
