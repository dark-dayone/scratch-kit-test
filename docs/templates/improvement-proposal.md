# Template: Improvement Proposal

An agent fills this in after a project (or when three failure log entries share a stage), using evidence from the failure log. Each proposal changes one small thing. The human approves or rejects every proposal. Nothing in the workflow files changes without that approval. Save accepted and rejected proposals in an `improvements/` folder so the history is kept.

## 1. Proposal title

A short name for the change.

## 2. Evidence

Cite specific failure log entries, failed tests, rejected pull requests or bugs the human caught. A proposal with no concrete evidence is not valid. Do not rely on the agent's general impression of what went wrong.

| Failure log entry (date and title) | Stage of origin | What happened |
| --- | --- | --- |
| | | |

How many entries support this? One incident may be a one-off, so say so honestly and weigh it accordingly.

## 3. Diagnosis

What is the likely cause in the workflow, not just in the code? Separate what the evidence shows from what is a guess.

- **Confirmed by evidence:**
- **Plausible but unconfirmed:**

## 4. Proposed change

One small change to one file: which file, the exact wording before and after, and which stage it affects.

Before asking whether to add a rule to the instructions, ask whether the rule can be enforced as a failing check instead (a test, linter or type check). Checks beat instructions that an agent may ignore. Say which this is.

- [ ] This is better enforced as an automated check, and the proposal adds one
- [ ] This must be an instruction, because it cannot be checked automatically

## 5. Size check

The rules file must stay short and contain only what we want done differently from the agent's defaults.

- [ ] This change does not add information the agent could discover on its own
- [ ] This change does not contradict any existing rule
- [ ] Something older or less useful can be removed to make room

## 6. How we will know it worked

A measurable signal and the period to watch it, for example: no new failure log entries of this type across the next three features. State what result would mean the change should be reverted.

## 7. Human decision

- [ ] Approved
- [ ] Rejected
- [ ] Needs more evidence (wait for more projects)

Decision date and reason:

## 8. Follow-up

After the watch period, record whether the change worked, and keep or revert it.
