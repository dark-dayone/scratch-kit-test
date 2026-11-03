# Template: Implementation Plan

The agent fills this in after the spec is approved and before any code is written. Save it as `plan.md` in the feature folder. The human reviews it at stage two, because a wrong structure is expensive to fix later while a wrong line of code is cheap.

## 1. Spec reference

Link to the approved spec and restate in two or three sentences what is being built, in the agent's own words. If this differs from the spec, stop and resolve it now.

## 2. Approach

The proposed solution in plain language, and why this approach over the realistic alternatives. List at least one alternative that was considered and why it was not chosen.

## 3. Files and structure

| File or module | New or changed | Purpose |
| --- | --- | --- |
| | | |

Flag anything that adds a new layer, pattern or abstraction. Keep the structure proportional to the size of the feature.

## 4. Slices

Break the work into small slices, each independently reviewable and each on its own branch. For every slice, name the part of the spec it covers and the tests that prove it.

| Slice | Spec items covered | Tests that prove it |
| --- | --- | --- |
| 1 | | |
| 2 | | |

## 5. New dependencies and external services

Every new package, service or API needs human approval. For each, state why it is needed, confirm it exists and is actively maintained, and note its version.

| Dependency | Why needed | Verified real and current? | Approved by human |
| --- | --- | --- | --- |
| | | | |

If none are needed, write "None".

## 6. Data and security impact

- What data is read, written or stored?
- What authentication and authorization checks apply?
- Which abuse cases from the spec does each slice address?
- Does the agent need any credentials? (It should never see real production keys.)

## 7. Risks and unknowns

What could go wrong, what is unclear, and what assumption is the plan resting on? List anything the agent had to guess.

## 8. Rollout and rollback

How will this be released (staged, behind a flag, all at once)? How is it rolled back if it fails?

## 9. Human plan review

- [ ] The approach matches the spec and the restatement is accurate
- [ ] The structure is proportional and nothing surprising was added
- [ ] Each slice is small enough to review properly
- [ ] Every new dependency is approved
- [ ] Security and data impact are acceptable
- [ ] Approved to start implementation
