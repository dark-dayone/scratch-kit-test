# Project rules

## Workflow
- Follow the seven stages in docs/workflow.md: spec, plan, tests first, small slices, gates, human review, release.
- Do not write implementation code until a spec and a plan exist in the feature folder and the human has approved the plan.
- If the spec is unclear, ask questions first. Restate the spec in your own words before planning.
- Work in small slices: one slice per branch, one commit per slice, and the commit message names the spec item it covers.
- Write tests from the spec before the implementation. Commit them first.
- Run the full test suite after each slice and fix failures using the real output. Do not claim something works without running it.
- At the end of a session, write a short progress note in the feature folder (docs/templates/progress-note.md).

## Security
- Never read, print or commit secrets, keys or credentials. Never ask for production credentials.
- Do not add a dependency without asking. Confirm any package actually exists and is current before proposing it.
- Validate all input. Check authorization on the server for every action. Use parameterized queries.
- Do not write sensitive data to logs or error messages.
- Stay inside the project directory and the current branch. Do not run commands that touch anything outside the repo.

## Code
- Keep structure proportional to the size of the feature. Do not add layers, patterns or abstractions the spec does not need.
- Do not build anything the spec lists as a non-goal.
- API clients are generated from the OpenAPI contract. Never hand-edit generated code.
- Pin exact dependency versions (== in requirements.txt) and commit lockfiles (package-lock.json, pubspec.lock). The vulnerability scan skips unpinned packages.
- Analytics: log only the events the spec lists, with no personal data.

## When something fails
- If CI cannot run (out of Actions minutes, runner outage), keep working. Continue slice by slice on branches, stacked if needed, and run `scripts/check.sh` after every slice, fixing failures from the real output. Do not mark any pull request ready, and never ask to disable, bypass or edit the ruleset or to merge another way. When CI is available again, the human marks the branch ready and CI runs the same checks for real. Local results are feedback for the developer, never a substitute for `CI gate`.
- Open pull requests as drafts. Only the human marks one ready, which is what starts CI.
- Run `scripts/check.sh` before every push, so CI mostly confirms what already passed.
- Record it in docs/failure-log.md using docs/templates/failure-log-entry.md, including which stage it originated from.

## Where things are
- Workflow: docs/workflow.md
- Templates: docs/templates/
- Feature folders: docs/features/<feature-name>/ (spec, plan, review notes, progress notes)
