# Helm QA Verifier — Learning Backlog

This file captures **candidate learnings** discovered during real Helm/deployment reviews.

It is intentionally separate from:

- `SKILL.md` — how the agent performs reviews
- `references/approved-patterns.md` — reviewed and approved reusable knowledge
- `references/test-scenarios.md` — reviewed and approved reusable test scenarios

The learning backlog is a temporary staging area.

Nothing in this file should automatically change team standards.

---

# Purpose

Use this file to capture:

- confirmed defects found by the skill
- confirmed defects missed by the skill
- false positives
- repeated clarification questions
- useful DevOps/Platform answers
- new migration patterns
- new policy-validation patterns
- new CI/CD failure patterns
- post-deployment issues
- reusable test scenarios
- recurring unsafe defaults
- recurring gaps in evidence
- new tool capabilities
- opportunities to reduce noisy output

The goal is to continuously improve review quality without allowing the skill to silently rewrite itself.

---

# Governance

A backlog item should only move into:

- `SKILL.md`
- `references/approved-patterns.md`
- `references/test-scenarios.md`

after human review.

Recommended reviewers:

- QA/SDET
- DevOps/Platform when infrastructure assumptions are involved
- Security when secret/policy/security behaviour is involved
- application developers when application runtime behaviour is involved

Do not add:

- secrets
- passwords
- tokens
- credentials
- private keys
- confidential URLs
- production-sensitive values
- personal data
- incident-specific sensitive details
- copied secret contents
- unrestricted internal logs

Sanitise examples before storing them.

---

# Learning lifecycle

```text
Real review
    ↓
Skill finding / human finding / false positive / clarification
    ↓
Learning backlog entry
    ↓
Human verification
    ↓
Decision
    ├── Reject
    ├── Keep watching
    ├── Add to SKILL.md
    ├── Add to approved-patterns.md
    └── Add to test-scenarios.md
    ↓
PR review
    ↓
Merge
    ↓
Version/changelog update
```

---

# Backlog status values

Use one of:

- `NEW`
- `NEEDS_EVIDENCE`
- `READY_FOR_REVIEW`
- `APPROVED`
- `REJECTED`
- `DUPLICATE`
- `PROJECT_SPECIFIC`
- `PROMOTED`
- `WATCHING`

Meaning:

## NEW

Candidate was just discovered and has not been reviewed.

## NEEDS_EVIDENCE

The idea may be useful, but there is not enough evidence yet.

## READY_FOR_REVIEW

Evidence is sufficient for team review.

## APPROVED

The team agrees the learning is reusable and should be promoted.

## REJECTED

The candidate was incorrect, unsafe, too narrow, or not useful.

## DUPLICATE

Already covered elsewhere.

## PROJECT_SPECIFIC

Useful only to one project and should remain there rather than enter the shared skill.

## PROMOTED

Already added to `SKILL.md`, `approved-patterns.md`, or `test-scenarios.md`.

## WATCHING

Interesting recurring signal, but the team wants more examples before making it a standard.

---

# Learning categories

Use one of:

- `MISSED_DEFECT`
- `CONFIRMED_DEFECT_PATTERN`
- `FALSE_POSITIVE`
- `MIGRATION_PATTERN`
- `HELM_PATTERN`
- `CONFIGURATION_PATTERN`
- `POLICY_PATTERN`
- `CI_CD_PATTERN`
- `DEPLOYMENT_PATTERN`
- `ROLLBACK_PATTERN`
- `CANARY_PATTERN`
- `SECURITY_PATTERN`
- `RESOURCE_PATTERN`
- `PROBE_PATTERN`
- `ENVIRONMENT_PATTERN`
- `TOOLING_PATTERN`
- `REPORTING_IMPROVEMENT`
- `TEST_SCENARIO`
- `QUESTION_RESOLVED`

---

# Priority

Use:

- `P0` — serious correctness/safety issue that should be incorporated quickly
- `P1` — high-value reusable learning
- `P2` — useful improvement
- `P3` — minor refinement

---

# Confidence

Use:

- `HIGH` — reproduced or confirmed by authoritative evidence
- `MEDIUM` — supported by evidence but not broadly confirmed
- `LOW` — hypothesis or single observation

---

# Learning entry template

Copy this section for every new candidate.

```markdown
## Learning: <short title>

**ID:** LB-YYYY-NNN  
**Status:** NEW  
**Category:** <category>  
**Priority:** P1  
**Confidence:** MEDIUM  
**Date discovered:** YYYY-MM-DD

### Context

Describe the review context in generic terms.

Do not include confidential service names or sensitive internal details unless the repository itself is restricted and this information is allowed.

### Trigger

What caused this learning candidate?

Examples:

- skill found a defect
- skill missed a defect
- tester found issue manually
- DevOps clarified expected behaviour
- pipeline failed
- deployment failed
- false positive was reported
- repeated question appeared across projects

### Skill behaviour

What did the skill do?

Examples:

- detected correctly
- missed completely
- classified severity incorrectly
- reported false positive
- asked unnecessary question
- could not validate
- produced weak evidence

### Actual outcome

What was eventually confirmed?

### Evidence

Summarise safe evidence.

Examples:

- Helm render difference
- Git diff
- policy result
- schema validation
- pipeline behaviour
- developer/DevOps confirmation
- post-deployment observation

Do not paste sensitive values.

### Reusable?

Yes / No / Unsure

### Why reusable

Explain why this applies beyond one project.

### Proposed improvement

Describe the proposed reusable rule, behaviour, or test.

### Proposed wording

Optional exact wording for `SKILL.md`, `approved-patterns.md`, or `test-scenarios.md`.

### Proposed destination

Choose one:

- SKILL.md
- references/approved-patterns.md
- references/test-scenarios.md
- project-specific documentation
- no change

### Validation needed

What must be checked before promoting this learning?

### Reviewer notes

Add review feedback here.

### Decision

Pending

### Promoted in

Leave blank until merged.

Example:

v1.4.0 / PR-123
```

---

# Metrics to capture per review

For substantial reviews, optionally record:

```text
Review date:
Repository/service:
Review type:

Confirmed defects found by skill:
Confirmed defects missed by skill:
Potential risks:
False positives:
Needs clarification:
Checks NOT_RUN:
Migration gaps:
Reusable learning candidates:
```

Use this data to measure whether the skill is getting:

- more accurate
- less noisy
- better at finding migration gaps
- better at producing evidence
- better at choosing the right severity
- better at asking only necessary questions

---

# Recommended promotion rules

Promote a learning to `SKILL.md` when it changes **how the agent should behave**.

Examples:

- always distinguish NOT_RUN from FAIL
- always inspect Git history for migration baselines
- always classify findings with evidence
- always avoid exposing Secret values

Promote a learning to `approved-patterns.md` when it captures **stable reusable knowledge**.

Examples:

- string `"false"` may behave differently from boolean `false`
- immutable selectors can break upgrades
- rendered output is more important than template appearance

Promote a learning to `test-scenarios.md` when it defines **a reusable test case**.

Examples:

- missing required value
- wrong environment override
- Vault enabled/disabled branch
- policy failure blocks deployment
- legacy property missing from Helm

Keep it project-specific when the learning depends on:

- one service's business rule
- one repository's naming convention
- one team's temporary deployment process
- environment-specific values that are not shared standards

---

# Quality checks before promotion

Before promoting any learning, confirm:

- [ ] The finding is technically correct.
- [ ] It is not already covered.
- [ ] It applies beyond one narrow case.
- [ ] It does not expose sensitive information.
- [ ] It does not encourage destructive commands.
- [ ] The proposed wording is precise.
- [ ] The change will not create obvious false positives.
- [ ] Evidence exists.
- [ ] Appropriate reviewers have checked it.
- [ ] `CHANGELOG.md` will be updated if promoted.

---

# Example 1 — Missed defect

## Learning: Legacy setting disappeared during migration

**ID:** LB-2026-001  
**Status:** READY_FOR_REVIEW  
**Category:** MISSED_DEFECT  
**Priority:** P0  
**Confidence:** HIGH  
**Date discovered:** 2026-10-21

### Context

A legacy deployment properties file was removed during migration to Helm.

### Trigger

A tester manually compared deleted properties against new Helm values.

### Skill behaviour

The skill reviewed the new Helm chart but did not account for every removed legacy key.

### Actual outcome

One required legacy setting had no Helm value, pipeline input, or rendered equivalent.

### Evidence

Git diff showed the legacy key was deleted. Search of the new chart and rendered manifests found no replacement.

### Reusable?

Yes

### Why reusable

Legacy configuration can silently disappear during migration in any service.

### Proposed improvement

Require a migration matrix for every legacy configuration key.

### Proposed destination

SKILL.md and references/test-scenarios.md

### Validation needed

Confirm the migration matrix approach on at least one additional migration.

### Decision

Pending

---

# Example 2 — False positive

## Learning: High CPU limit ratio is not automatically a defect

**ID:** LB-2026-002  
**Status:** APPROVED  
**Category:** FALSE_POSITIVE  
**Priority:** P1  
**Confidence:** HIGH  
**Date discovered:** 2026-10-21

### Context

A chart used a CPU request much smaller than its CPU limit.

### Trigger

The skill reported the ratio as a defect.

### Skill behaviour

Severity was too strong.

### Actual outcome

The configuration was valid and allowed by the platform.

### Evidence

Platform confirmation and successful deployment.

### Reusable?

Yes

### Why reusable

Resource ratios vary by workload and should not be treated as invalid without policy evidence.

### Proposed improvement

Classify unusual ratios as `POTENTIAL_RISK` unless policy or schema proves invalid.

### Proposed destination

references/approved-patterns.md

### Decision

Approved

---

# Example 3 — Helm boolean type issue

## Learning: Boolean-looking strings can change conditional behaviour

**ID:** LB-2026-003  
**Status:** APPROVED  
**Category:** HELM_PATTERN  
**Priority:** P0  
**Confidence:** HIGH  
**Date discovered:** 2026-10-21

### Context

A boolean-like Helm value was stored as the string `"false"`.

### Trigger

Rendered output changed depending on whether the value was passed as boolean or string.

### Skill behaviour

The skill detected the difference.

### Actual outcome

The string form caused the wrong conditional branch to render.

### Evidence

Comparison of:

```bash
--set FLAG=false
```

and:

```bash
--set-string FLAG=false
```

produced different resources.

### Reusable?

Yes

### Why reusable

This can affect any Helm chart using direct boolean conditions.

### Proposed improvement

Always examine datatype for values used in Helm `if` conditions.

### Proposed destination

references/approved-patterns.md and references/test-scenarios.md

### Decision

Approved

---

# Example 4 — Repeated clarification becomes knowledge

## Learning: Pipeline injects a required value

**ID:** LB-2026-004  
**Status:** PROJECT_SPECIFIC  
**Category:** QUESTION_RESOLVED  
**Priority:** P2  
**Confidence:** HIGH  
**Date discovered:** 2026-10-21

### Context

The chart appeared to have a missing required value.

### Trigger

The skill repeatedly asked where the value came from.

### Skill behaviour

Correctly requested clarification.

### Actual outcome

The CI/CD pipeline always injects the value.

### Evidence

Pipeline configuration and maintainer confirmation.

### Reusable?

No

### Why reusable

Not reusable globally; specific to that repository/pipeline.

### Proposed destination

Project-specific documentation

### Decision

Project-specific

---

# Example 5 — Validation tool unavailable

## Learning: Missing validator must not become a failed check

**ID:** LB-2026-005  
**Status:** APPROVED  
**Category:** REPORTING_IMPROVEMENT  
**Priority:** P1  
**Confidence:** HIGH  
**Date discovered:** 2026-10-21

### Context

A schema or policy validator was not installed.

### Trigger

Earlier review output implied the validation failed.

### Actual outcome

The check had never run.

### Reusable?

Yes

### Proposed improvement

Use `NOT_RUN` rather than `FAIL` when a validation tool or required dependency is unavailable.

### Proposed destination

SKILL.md and references/approved-patterns.md

### Decision

Approved

---

# Review retrospective prompt

At the end of a substantial review, the tester can ask the skill:

```text
Evaluate the quality of this review.

Identify:
1. confirmed findings with strong evidence,
2. findings that may be false positives,
3. defects that were found manually but not by the skill,
4. checks that could not be executed,
5. assumptions that were required,
6. repeated clarification questions,
7. reusable test scenarios missing from the current references,
8. reusable patterns that could improve future reviews.

Do not modify SKILL.md or the reference files.

Return learning-backlog candidates using the learning entry template.
```

---

# Backlog summary

Maintain a lightweight table for active items.

| ID | Title | Category | Priority | Status | Proposed destination |
|---|---|---|---|---|---|
| | | | | | |

Keep detailed entries below the table or in separate issues/PRs if the backlog grows large.

---

# Archive

Once an item is promoted or rejected, either:

- leave it here with final status for auditability, or
- move completed items to `learning-backlog-archive.md`

Choose one approach and use it consistently.

The preferred model is to keep this backlog focused on active learnings and use Git history/PRs as the long-term audit trail.
