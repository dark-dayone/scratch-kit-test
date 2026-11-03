# Agentic Software Delivery Workflow

Short form of the master document. Numbers are directional: most evidence is recent preprints and vendor material. Items marked *(not verified)* or *(design decision)* are not backed by research.

## 1. Principles

- The human owns correctness, security and maintainability. Agents are fallible and never trusted blindly.
- All seven stages carry equal weight until our own failure log shows where to focus. The spec is a likely bottleneck (one study found 46.7% of agent runs failed at requirement clarification or planning), but that is an inference, not proof.
- Real execution results outrank AI opinion. Feeding actual test output back to the agent was the strongest measured gain (63% to 94% solve rate in one harness study). An AI reviewing code it has not run gave no gain.
- Tests derive from the spec, not from the code. Tests written after the code tend to copy the code's bugs.
- Work in small slices so every change is reviewable.

## 2. The seven stages

1. **Spec.** What it must do, must never do, and how we will know it works. Use `templates/feature-spec.md`. The agent interviews the human first and restates the spec in its own words.
2. **Plan.** The agent fills in `templates/implementation-plan.md`. The human reviews architecture and approves every new dependency.
3. **Tests first.** Written from the spec before the implementation, by a different tool from the one that writes the code. Committed first.
4. **Implementation in small slices.** One slice per branch, one commit per slice, each commit message naming the spec item it covers. Real test output goes back to the agent after every slice.
5. **Automated gates.** `.github/workflows/ci.yml`: tests, type checks, lint, static security analysis, secret scan, dependency audit, vulnerability scan. A second AI review is an extra opinion only.
6. **Human review, scaled to risk.** `templates/review-checklist.md`. Anything touching authentication, money, personal data or permissions gets a careful read of the actual code.
7. **Safe release.** Staged rollout, monitoring, a known rollback path.

## 3. Security layer (runs through every stage)

- **Spec:** abuse cases, data rules, authentication rules.
- **Plan:** proposed dependencies and services, each approved by a human.
- **Implementation:** agents run sandboxed, in isolated worktrees, with least privilege, and never see real production keys. Third-party plugins and tool servers are vetted first.
- **Gates:** secret scanning, dependency check (hallucinated package names are a real attack route), static security analysis.
- **Review:** careful human read of high-risk areas.
- **Release:** staged rollout, monitoring, quick rollback.

## 4. Records (mostly automated)

Each feature has a folder `docs/features/<feature-name>/` holding `spec.md`, `plan.md`, a review note and progress notes. Tests are committed before implementation. CI saves gate results. Agent session transcripts are saved for each run. Keep notes to a few lines.

## 5. Failure log

Every failure gets an entry in `docs/failure-log.md`, using `templates/failure-log-entry.md`, tagged with the stage it originated from. Trace backwards: was it in the spec, the plan, a test, the code, a gate, the review, or the release?

## 6. Improvement loop

- Runs after every finished project, and whenever three failure log entries share the same stage of origin.
- An agent proposes one small change, citing failure log entries (`templates/improvement-proposal.md`). **The human approves every change.**
- Keep the rules file short. AI-written context files reduced success in one study. If a rule can be a failing check, make it a check.
- This workflow is reviewed every three months.

## 7. Two-tool setup (Claude Pro and ChatGPT Plus, about $20 each)

- One tool builds, the other checks. The tool that writes the tests never writes the implementation for the same feature. Swap roles each feature.
- Spend limited usage on the spec interview, the plan and the security review first.
- Handoff lives in the repo (spec, plan, progress note) so either tool can continue.
- Keep a weekly limits log (`docs/limits-log.md`). Published allowances are incomplete and change often.

## 8. Roles of the files

`CLAUDE.md` and `AGENTS.md` (same content) are the short rules file agents read automatically. Everything else is under `docs/`.

## 9. Git and GitHub

- **Host:** GitHub on a paid plan (Pro for a personal account, Team for an organization, each listed at about $4 per user per month; confirm on GitHub's pricing page). Client code only in private repositories. On the free plan, rulesets are not enforced on private repositories.
- **Branching:** one short-lived branch per slice, merged through a pull request within a day or two, into a protected `main` that is always deployable. Pull requests are mandatory for agent-written code. Git Flow is rejected for this size and style of work. Start with one agent per feature; add a git worktree per agent only if two agents collide.
- **Ruleset on `main`:**
  1. Require a pull request, with zero required approvals while working alone (an author generally cannot approve their own pull request; confirm at setup). Raise to one when a second person joins.
  2. Dismiss stale approvals on new commits; require conversations resolved.
  3. Require one status check: `CI gate`.
  4. Require the branch to be up to date.
  5. Block force pushes and deletion of `main`.
  6. Squash merge, linear history.
  7. Empty bypass list. Log any emergency override as a failure.
- Agents get credentials that can push branches and open pull requests, but cannot edit rulesets or admin settings *(design decision)*.
- After setup, try a direct push to `main` on a scratch repo. It must be rejected.

## 10. Default stack and rules

Flutter (mobile and desktop), React with Next.js (web), Python with FastAPI (backend), Postgres, PostHog (product analytics).

1. **Contract-first API.** The OpenAPI contract is part of the spec. Typed clients are generated from it and never hand-edited. Generated types guarantee matching shapes, not correct behaviour.
2. **PostHog privacy.** Every spec lists exactly which events are logged, with no personal data. Autocapture off, inputs masked, IP capture controlled, session replay needs separate consent. Region chosen per client. Zimbabwe's data protection law has not been checked.
3. **PostHog is analytics only.** Errors, logs and uptime are separate (Sentry for errors).
4. **One client surface per project by default.** Dart, TypeScript, Python and SQL all need human review.

Standard gates *(not verified against current docs)*: Python: pytest, ruff, mypy, bandit, pip-audit. Next.js: strict TypeScript, ESLint, Vitest, Playwright. Flutter: analyze, test, format. Postgres: migrations as reviewable files, tested in CI.

## 11. CI and vulnerability checks

`ci.yml` runs on every pull request and push to `main`. It detects which layers exist (`api/`, `web/`, `mobile/`) and skips the rest. Jobs: secret scan (gitleaks CLI, pinned and checksum-verified), Python, web, mobile, and a dependency vulnerability scan (OSV-Scanner over all lockfiles). A final job `CI gate` passes only if every job passed or was skipped, and is the single required check.

Dependabot (`dependabot.yml`) opens weekly update pull requests. Dependabot **alerts** are a separate switch in each private repository's security settings and must be turned on by hand. Commit `pubspec.lock` and `package-lock.json`, and pin exact versions in Python `requirements.txt` files. OSV-Scanner skips packages that have no pinned version (seen in a local test), so unpinned requirements are not checked.

Not yet run on GitHub. Known gaps: browser end-to-end tests, mutation testing, deeper static analysis, an automatic check that new packages are real (a human approves new dependencies at the plan stage instead). Actions are pinned to major tags, not commit SHAs.

## 12. Deployment

- **Web (current):** Render for the API and Postgres, Vercel for Next.js. No client data on a database without point-in-time recovery, and a restore is tested before launch. Vercel's Hobby plan is non-commercial only, so client projects need Pro. Release flow *(design decision)*: merge to `main` deploys to staging, production is a deliberate step, rollback is redeploying the previous version, database changes are reversible migrations, secrets live in platform settings.
- **Mobile and desktop (current):** we install apps directly on client devices.
- **Android:** install with ADB or a direct install of the CI-built, checksummed APK. Register the company as an Android developer now (Google's developer verification is being rolled out, with a global extension planned for 2027; check Google's page for dates). Dart-only fixes ship as Shorebird patches. The signing key lives in CI secrets plus an encrypted backup, never in the repository.
- **Future target for mobile:** company-owned store accounts (Google Play organization account needs a D-U-N-S number; Apple Developer account).
- **Installs on client devices** *(design decisions)*: one versioned, checksummed package per release built by CI; a written install checklist per project; rollback by reinstalling the previous package; no production secrets baked into an app; a remote support method agreed before go-live; device security responsibilities stated in the handover.

## 13. Client acceptance, feedback and support

- **Acceptance:** a demo walking through the spec's acceptance criteria, then a confirmation email from the client naming the project, version and demo date. Save the email next to the spec.
- **Feedback** mostly arrives by WhatsApp and phone calls. Log every report the same day as a GitHub issue; send a WhatsApp summary after a call; triage as defect, spec gap, change request, question, or outage. Defects and spec gaps get a failure log entry. Every defect fix starts with a failing test that reproduces it.
- **Support options per client:** (A) a fixed free-fix period covering defects and urgent security fixes, or (B) ongoing paid maintenance covering fixes, dependency and security updates, backup and monitoring checks and agreed response times. Figures are set per client in the handover document.
- **Change requests:** fixed quotes agreed before work starts, kept light (a short message: what is included, price, date; the client approves by replying). Re-quote if scope grows.
- These are business and contract matters. This kit is not legal advice.

## 14. Not yet settled

Business figures (free-fix length, maintenance fee, response times, hosting cost owner, change request prices), the remote support tool, staging and restore-test routine, an uptime check tool, desktop installers and signing, the iOS path, a Dart client generator, Zimbabwe's data protection requirements, and the human skills needed to judge agent output. The master document keeps the full parked list.
