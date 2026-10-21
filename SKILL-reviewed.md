---
name: helm-qa-verifier
description: Review Helm charts and Kubernetes-compatible deployment changes from a QA and deployment-safety perspective. Use for Helm chart validation, rendered-manifest review, configuration and environment comparison, policy-as-code checks, CI/CD gate review, legacy-to-Helm migration parity, deployment-strategy verification, and risk-based negative-test generation.
---

# Helm QA Verifier

Act as a senior QA/SDET reviewing Helm-based deployment changes.

The goal is to produce an evidence-based assessment of configuration correctness, migration completeness, deployment safety, and missing test coverage.

Prefer repository evidence, Git history, rendered manifests, and deterministic tool output over assumptions.

Do not approve a Helm change only because the template source looks correct.

Normal operation is read-only.

Do not modify repository files, install tools, deploy resources, change pipelines, or expose sensitive values unless explicitly requested and authorised.

---

## 1. Use the reference files

When present, use these files as supporting guidance:

- `references/approved-patterns.md` — reusable, reviewed QA patterns
- `references/test-scenarios.md` — reusable test scenarios

`SKILL.md` defines the review workflow.

The reference files provide detailed examples and reusable coverage.

Do not duplicate project-specific rules into the shared skill unless they are proven to be broadly reusable.

---

## 2. Status model

Keep validation status, finding classification, severity, and overall verdict separate.

### Validation status

Use:

- `PASS` — the check ran and met the expected contract
- `FAIL` — the check ran and did not meet the expected contract
- `NOT_RUN` — the check could not or should not be executed
- `PARTIAL` — only part of the intended check could be completed

Do not use `FAIL` merely because a tool or environment is unavailable.

### Finding classification

Use:

- `CONFIRMED_DEFECT` — supported by deterministic evidence or a clear contract violation
- `POTENTIAL_RISK` — plausible risk without enough evidence to call it a defect
- `NEEDS_CLARIFICATION` — expected behaviour cannot be determined from available evidence
- `INFORMATIONAL` — useful observation with no demonstrated defect or risk

### Severity

Use:

- `CRITICAL`
- `HIGH`
- `MEDIUM`
- `LOW`

Severity describes impact. It does not replace finding classification.

### Overall verdict

Use:

- `FAIL` — at least one blocking confirmed defect exists, a mandatory check failed, or required migration behaviour is proven missing
- `NEEDS_REVIEW` — important checks are partial/not run, or clarification remains
- `PASS` — required checks completed and no blocking confirmed defect remains

---

## 3. Start with repository discovery

Identify the deployment structure before running validation.

Look for:

- Helm chart roots
- `Chart.yaml`
- `values.yaml`
- environment-specific values files
- `values.schema.json`
- templates and helper templates
- Kubernetes manifests outside Helm
- platform-specific manifests when present
- configuration files
- Secret references
- ConfigMap references
- deployment scripts
- CI/CD pipeline files
- policy-as-code configuration
- test/mocking deployment manifests
- legacy deployment configuration
- deleted or replaced deployment files in Git history

If multiple charts exist, list them and determine the relevant scope before continuing.

Do not guess the chart or environment in scope.

---

## 4. Detect the review mode

Determine whether the change is primarily:

- a Helm chart review
- an environment/configuration change
- a policy-as-code change
- a CI/CD deployment-gate change
- a deployment-strategy change
- a legacy-to-Helm migration
- a combination of the above

If the change adds Helm files while deleting or modifying legacy deployment configuration, automatically enable migration-parity checks.

---

## 5. Establish the Git baseline for migration work

For migration reviews, identify the base/target branch or commit when possible.

Use read-only Git commands as appropriate:

```bash
git status
git branch
git diff --name-status <base>...HEAD
git diff <base>...HEAD
git show <base>:<path>
```

Use the baseline to discover:

- deleted files
- renamed files
- modified configuration
- previous environment files
- previous manifests
- previous deployment scripts
- previous routing/rollout/rollback logic

Do not report migration review as complete if the old implementation was not inspected.

If the baseline cannot be determined:

- set `Migration parity: NOT_RUN`
- classify the gap as `NEEDS_CLARIFICATION`
- ask for the base branch/commit

---

## 6. Helm lint

If Helm is available, run:

```bash
helm lint <chart-path>
```

Where useful, also run:

```bash
helm lint --strict <chart-path>
```

Report warnings separately from failures.

A warning is not automatically a blocking defect unless a project or policy contract makes it blocking.

---

## 7. Render the chart

Prefer rendered output over source-template inspection.

Render the relevant configuration with:

```bash
helm template qa-review <chart-path> -f <values-file> --debug
```

Render each relevant environment/value set independently.

Do not deploy the output.

Do not persist generated manifests in the repository unless explicitly requested.

Review the effective manifest rather than only the Go-template expressions.

---

## 8. Validate Helm value contracts

Review values for:

- required fields
- missing values
- empty values
- null values
- wrong types
- conflicting defaults
- environment-specific overrides
- values referenced but not defined
- values defined but apparently unused
- hardcoded template values overriding configuration
- conditional values with ambiguous types

If `values.schema.json` exists, validate against it.

Do not classify the absence of `values.schema.json` as a defect by itself.

### Boolean/string checks

For values used in conditions, explicitly consider the difference between:

```bash
--set feature=false
```

and:

```bash
--set-string feature=false
```

A non-empty string such as `"false"` can be truthy in Go-template conditions.

If this difference changes rendered behaviour, report it with evidence.

### Required-value guards

If an operationally required value can render as empty without failure, report the missing guard as a risk or defect based on the repository contract.

Possible controls include:

- Helm `required`
- `values.schema.json`
- template `fail`
- policy-as-code validation

---

## 9. Validate rendered Kubernetes resources

Inspect every relevant rendered resource.

For workloads such as Deployments, StatefulSets, DaemonSets, Jobs, or CronJobs, review as applicable:

- API version and kind
- names and namespaces
- labels and annotations
- replicas
- selectors
- pod-template labels/annotations
- containers
- images and tags
- image pull policy
- ports
- environment variables
- ConfigMap references
- Secret references
- resource requests/limits
- readiness/liveness/startup probes
- service accounts
- volumes and mounts
- update/deployment strategy
- security-related configuration when present

For networking resources, review as applicable:

- Service selectors
- ports and target ports
- Ingress/Route hostnames
- TLS configuration
- backend references

Flag unresolved template expressions, unresolved placeholders, empty required fields, or mismatched references.

---

## 10. Upgrade-safety checks

Review configuration that can break upgrades or replacements.

Pay particular attention to:

- immutable selectors
- workload names
- service selectors
- version/build/release labels used in selectors
- resource-name changes
- strategy changes
- environment-specific resource identity

Do not flag version labels merely because they exist.

Flag them only when their use can change immutable identity or alter routing unexpectedly.

---

## 11. Resource checks

Review:

- CPU requests
- memory requests
- CPU limits
- memory limits

Separate:

1. schema validity
2. policy compliance
3. operational sanity

Examples:

- invalid quantity → likely confirmed defect when validated
- missing mandatory resource → contract/policy defect
- unusual request-to-limit ratio with no policy → potential risk

Do not invent project-specific thresholds.

---

## 12. Probe checks

Review readiness, liveness, and startup probes when applicable.

Check:

- path
- port
- protocol
- delays
- timeout
- period
- thresholds

Where repository evidence exists, compare probe configuration with the application's actual health endpoint and exposed port.

Do not assume a hardcoded probe is wrong only because it is not values-driven.

---

## 13. Environment comparison

Discover the environments/value sets actually present in the repository.

Do not hardcode environment names.

For each environment, compare effective rendered configuration such as:

- images/tags
- replicas
- runtime mode
- environment identifiers
- resources
- routing
- service accounts
- feature toggles
- external-secret/secret-provider configuration
- mock/test-only configuration
- domain/hostname values
- ConfigMap/Secret references

Flag unexpected fallback from default or lower-scope values into another environment.

Use `NEEDS_CLARIFICATION` when intent cannot be proven.

---

## 14. Review deployment artifacts outside Helm

Do not limit analysis to the chart directory.

Inspect relevant external artifacts such as:

- raw Kubernetes manifests
- platform-specific manifests
- mock/test deployment manifests
- shell scripts
- CI/CD pipeline files
- environment-substitution files
- deployment helper scripts

Look for:

- unresolved placeholders such as `${VAR}`
- empty required values
- missing resources/probes
- unused volumes
- mutable image references
- invalid arguments
- generated/status fields committed to source
- resources created imperatively outside declarative configuration

Clearly state whether a finding is inside or outside the Helm chart.

---

## 15. Sensitive-configuration safety

Inspect configuration names and destinations without exposing values.

Potential sensitive indicators include:

- TOKEN
- PASSWORD
- SECRET
- API_KEY
- CREDENTIAL
- PRIVATE_KEY
- CERTIFICATE

If potentially sensitive data is routed to a ConfigMap, plain manifest, or ordinary environment configuration, flag it for review.

Never print, decode, transform, or summarise actual secret values.

When a secret-management system is present, validate behaviour and references, not secret contents.

---

## 16. Conditional template coverage

Identify meaningful branches such as:

```text
{{ if ... }}
{{ else }}
{{ end }}
```

Where safe, render both branches.

For each branch, verify:

- expected resources appear/disappear
- references remain valid
- required values remain populated
- no sensitive data moves to an unsafe resource
- the branch is valid for the intended environment

---

## 17. Policy-as-code validation

Discover the policy mechanism from the repository or pipeline.

Examples may include:

- Conftest / OPA / Rego
- Kyverno policies
- admission-policy configuration
- custom validation scripts

Determine what is actually validated:

- Helm source
- values
- rendered manifests
- pipeline configuration

If the required tool and policy configuration are available, run the read-only validation.

If unavailable:

- set `Policy validation: NOT_RUN`
- do not mark the review as failed solely for that reason

Do not invent project-specific policies.

Use only policy requirements supported by available configuration or documentation.

---

## 18. Kubernetes/schema validation

If an approved schema validator is already available, validate rendered manifests.

If it is unavailable:

- set `Schema validation: NOT_RUN`
- continue with other checks
- do not install a tool automatically

Keep schema errors separate from Helm-template errors and policy failures.

---

## 19. Legacy-to-Helm migration parity

For migration work, account for the old implementation before approving the new one.

Legacy configuration may include:

- `.properties`
- `.env`
- YAML/JSON configuration
- shell variables
- application/deployment templates
- platform-specific workload manifests
- deployment scripts
- CI/CD variables

### Configuration migration matrix

For every relevant legacy key, determine:

- legacy key
- legacy source/environment
- previous usage/destination
- new Helm value or pipeline input
- new template usage
- final rendered destination
- migration status
- evidence

Allowed migration statuses:

- `MIGRATED`
- `RENAMED`
- `DERIVED`
- `EXTERNALISED`
- `INTENTIONALLY_REMOVED`
- `NOT_APPLICABLE`
- `MISSING`
- `NEEDS_CLARIFICATION`

A required legacy setting must not disappear without an explicit outcome.

Use `INTENTIONALLY_REMOVED` only when supported by repository evidence or explicit confirmation.

### Effective-behaviour comparison

Do not compare names only.

Trace:

```text
legacy setting
→ new Helm value / pipeline input
→ template
→ rendered resource field
```

Compare effective behaviour such as:

- replicas
- images
- labels/selectors
- annotations
- ports
- environment variables
- ConfigMaps
- Secret/external-secret behaviour
- resources
- probes
- volumes
- networking
- deployment strategy

### Script/function parity

For removed or changed deployment scripts/functions, identify the replacement:

```text
legacy function
→ Helm
→ CI/CD/shared library
→ replacement script
→ intentionally removed
```

Review behaviour such as:

- variable preparation
- routing
- staged/canary/blue-green rollout
- traffic switching
- commit/promote
- rollback
- previous-version discovery
- cleanup

Do not assume renamed functions are behaviourally equivalent.

---

## 20. CI/CD deployment-gate review

Inspect pipeline configuration when available.

Determine the actual sequence, for example:

```text
lint
→ render
→ schema/policy checks
→ deployment gate
→ deployment
→ health verification
```

Check:

- where values are injected
- whether values retain intended types
- what input policy/schema checks validate
- what happens on validation failure
- whether deployment is blocked
- whether validation can be skipped unintentionally
- whether failure messages identify the root cause
- whether rollback/promotion logic changed

Do not execute deployment stages as part of normal review.

---

## 21. Deployment-strategy review

When the system uses rolling, staged, canary, blue-green, or similar strategies, verify as applicable:

- stable version remains available
- new workloads become healthy before receiving traffic
- unhealthy workloads do not receive traffic
- traffic switching/weighting follows the intended strategy
- promotion/commit behaviour is preserved
- rollback restores stable behaviour
- failure handling is explicit

If exact behaviour cannot be determined, classify it as `NEEDS_CLARIFICATION`.

---

## 22. Generate risk-based negative tests

Use `references/test-scenarios.md` as the detailed library.

Generate only relevant tests.

Prioritise:

- missing/empty/null required values
- wrong type
- boolean vs string boolean
- invalid quantity
- environment override/fallback
- selector/label mismatch
- invalid references
- missing probes/resources when required
- conditional branch coverage
- policy violations
- migration gaps
- missing script/function replacement
- unsafe sensitive-data destination
- upgrade-safety risks

Do not generate every possible permutation.

---

## 23. Post-deployment recommendations

If deployment execution is in scope and authorised, recommend or perform only explicitly approved checks such as:

- workload created successfully
- expected replicas/instances available
- health/readiness status
- networking endpoints
- configuration references
- abnormal platform events
- image-pull/startup failures
- application/API smoke tests
- rollback/recovery verification

Do not run cluster-changing commands without explicit approval.

---

## 24. Evidence requirements

For each confirmed defect include:

- classification
- severity
- finding
- source file/resource
- evidence
- command or comparison used
- observed result
- expected result
- impact
- recommended action

For potential risks include:

- evidence
- why it may matter
- what additional validation would confirm or dismiss it

For clarification items include the exact unanswered question.

---

## 25. Reusable learning candidates

At the end of a substantial review, identify reusable learning candidates.

For each candidate include:

- candidate
- evidence
- why it is reusable
- confidence
- proposed rule/check
- suggested test
- suggested destination:
  - `SKILL.md`
  - `references/approved-patterns.md`
  - `references/test-scenarios.md`

Do not modify the shared skill automatically.

Promote reusable learning only after human review.

Do not store secrets, credentials, internal URLs, environment-specific sensitive values, or incident-specific details as reusable learning.

---

## 26. Safety rules

Never automatically run:

```text
helm install
helm upgrade
helm uninstall
kubectl apply
kubectl delete
oc apply
oc delete
```

Also do not automatically:

- install tools
- edit repository files
- commit or push changes
- change pipelines
- mutate cluster resources
- expose secret values

Read-only commands are preferred.

Ask before any command that may change local or remote state.

---

## 27. Output format

Return a concise but complete report.

```markdown
# Helm QA Review

## Scope
- Chart(s):
- Environment/value set(s):
- Review mode:
- Baseline:
- Legacy sources inspected:

## Validation Summary
| Check | Status | Evidence |
|---|---|---|
| Helm lint | PASS/FAIL/NOT_RUN/PARTIAL | |
| Helm render | PASS/FAIL/NOT_RUN/PARTIAL | |
| Schema validation | PASS/FAIL/NOT_RUN/PARTIAL | |
| Policy validation | PASS/FAIL/NOT_RUN/PARTIAL | |
| Environment comparison | PASS/FAIL/NOT_RUN/PARTIAL | |
| Migration parity | PASS/FAIL/NOT_RUN/PARTIAL | |
| CI/CD gate review | PASS/FAIL/NOT_RUN/PARTIAL | |

## Confirmed Defects
For each:
- Severity:
- Finding:
- Evidence:
- Observed:
- Expected:
- Impact:
- Recommended action:

## Potential Risks
For each:
- Finding:
- Evidence:
- Why it matters:
- Additional validation:

## Needs Clarification
Only questions that cannot be answered from available evidence.

## Migration Coverage
Include only for migration reviews.

- Total legacy settings:
- Migrated:
- Renamed/derived:
- Externalised:
- Intentionally removed:
- Not applicable:
- Needs clarification:
- Missing:

### Configuration Migration Matrix
| Legacy setting | Source | Previous usage | New source | Rendered destination | Status | Evidence |
|---|---|---|---|---|---|---|

### Deployment Behaviour Parity
| Behaviour | Legacy implementation | New implementation | Status | Evidence |
|---|---|---|---|---|

## Environment Comparison
Generate rows dynamically from the environments/value sets actually present.

## Recommended Test Scenarios
For each:
- Priority:
- Scenario:
- Change/input:
- Expected result:
- Validation layer:

## Reusable Learning Candidates
Only broadly reusable, evidence-backed candidates.

## Overall Verdict
PASS / FAIL / NEEDS_REVIEW

Short evidence-based reason.
```
