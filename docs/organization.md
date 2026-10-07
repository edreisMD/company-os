# A company that can improve its organization

Start with four leadership roles and the existing eleven specialists. These are responsibility definitions, not a requirement to run fifteen agents every day. Activate only the roles justified by actual work. The founder owns purpose, spending authority, governance and release approval. The CEO owns company outcomes; department managers own work allocation and the quality of their subordinate roles.

| Organization | Manager | Initial responsibilities | Cadence |
|---|---|---|---|
| Executive | CEO | Direction, product priorities, department design, stop/continue decisions | Weekdays 07:00; Monday strategy review |
| Engineering | Engineering manager | Discovery, planning, development, review, QA and release readiness | Weekdays 08:00; weekly improvement review |
| Operations | Operations manager | Setup, portfolio triage, automation health, costs and administration | Weekdays 08:30; Friday operating review |
| Growth (`sales/`) | Sales manager | Demand evidence, search, audience content and experiments | Monday/Wednesday/Friday 09:00 |

Times default to America/Los_Angeles and are configurable. Cron offsets are planning conventions, not dependency guarantees: a manager must read the actual date/status of the last report and mark stale inputs. Engineering specialists follow events; do not poll every specialist daily. For a personal website, initially enable only the engineering/discovery cycle and a weekly CEO/manager review when it provides useful decisions. Keep Growth and additional specialists paused until there is a concrete experiment.

## Editable organization

`governance.yaml` is the founder-owned map of role-editing authority. The CEO can propose changes to any subordinate department, including its manager. Department managers can propose creating, editing or retiring contributor roles only inside their department; they cannot edit themselves or any other manager. All governance, shared runtime/schema/scripts/CI and executive changes are outside that scope. New departments require a founder-reviewed governance change.

A manager works in an isolated branch of the configured catalog, not the checkout currently watched by the runtime. Its private `catalog` workspace binding must point to that working checkout. For company-specific behavior, use a private catalog fork with the same folder contract; upstream only reusable improvements to this public framework. Do not put private strategy or run reports into public role files.

For each structural change, record the demonstrated bottleneck, expected result, cost/run budget estimate, owner, trial review date and rollback. Prefer changing or retiring an existing role to creating more agents. The initial limit is twelve role folders per department, including managers. One open organization proposal per manager is sufficient. New agents start paused; activating a new agent remains an explicit runtime decision.

## Change procedure

1. Read the configured trusted base revision, private company objective and existing open proposals. Create or reuse an isolated branch.
2. Edit only subordinate role folders. Every role requires SKILL.md and temporal.yaml. Retiring a running role first requires a merged pause, schedule reconciliation and verification that no execution is active; delete in a later change.
3. Commit the candidate and run the scope checker from the trusted base checkout: `python scripts/check_org_change.py --repo /path/to/candidate --base BASE_SHA --head HEAD --actor engineering-manager`. Actor identity comes from the authenticated dispatcher/reviewer, not arbitrary PR text. Run full catalog validation too.
4. Open a draft PR with generic content and link the evidence in the appropriate private platform. A human reviews the exact revision. Role authors do not approve or merge their own changes.
5. Apply the approved catalog revision through the operator/deployment process. The generic backend discovers the new definitions, updates changed timers and pauses removed timers. It does not pull arbitrary agent branches.
6. At the trial review date, compare real results to the hypothesis and keep, revise or retire the role.

The checker validates paths and execution-setting changes against the base governance file. It is a review tool, not an identity provider or an OS security boundary. A prompt and shared GitHub credentials cannot enforce separation. Before unattended auto-merging, use independent bot identities, protected branches and a trusted dispatcher that binds the authenticated actor to the checked revision. No automatic merge or communication bus is installed here.

## Reports and handoffs

Keep reports in the private company context with role, run ID, observed period, evidence links, decisions, proposed recipient, requested action and required approvals. Reuse native issues/PRs for durable work. Until a communication adapter is configured, handoffs remain explicit proposals. Do not infer completion from a sent event, and do not create new chats or send messages merely because another skill lists a recipient.

Autonomy grows through an evidence → proposal → review → applied configuration → measurement loop. Scheduling, organizational authority and external action permissions remain distinct. This release defines the hierarchy and its change process; all new schedules ship paused.
