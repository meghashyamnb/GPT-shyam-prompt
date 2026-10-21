# Helm QA Verifier — Approved Reusable Patterns

This file contains reusable QA patterns approved for use with the `helm-qa-verifier` skill.

Its purpose is to preserve stable team learning without bloating `SKILL.md` with every example.

## Governance

Add a pattern only when it is:

- reusable across more than one service or repository
- technically verified
- safe for repeated use
- free of secrets, credentials, internal URLs, or production-sensitive values
- reviewed by QA and, where relevant, DevOps/Platform

Do not add:

- one-off incident details
- project-specific values that are not broadly reusable
- secrets or credentials
- confidential internal endpoints
- assumptions that have not been validated

A project-specific rule should remain in that project's repository or documentation unless it clearly applies organisation-wide.

---

# 1. Finding classification must reflect evidence

Every finding should be classified as one of:

- `CONFIRMED_DEFECT`
- `POTENTIAL_RISK`
- `NEEDS_CLARIFICATION`
- `NOT_VALIDATED`

A missing tool or unavailable environment is not the same as a failed validation.

Examples:

- Conftest unavailable → `NOT_VALIDATED`
- kubeconform unavailable → `NOT_VALIDATED`
- rendered invalid manifest → `CONFIRMED_DEFECT`
- unusual CPU ratio with no policy → `POTENTIAL_RISK`

Do not mark a review as FAIL only because optional validation tooling could not be executed.

---

# 2. Overall verdict must be evidence-based

Use:

- `FAIL` when a Critical/High confirmed defect exists, a mandatory validation fails, or required migration behaviour is proven missing.
- `NEEDS_REVIEW` when important checks are not validated or clarification remains.
- `PASS` only when required checks completed successfully and no blocking defect remains.

---

# 3. Rendered output is more important than template appearance

Prefer:

```text
helm lint
→ helm template
→ rendered manifest
```

over source-template inspection alone.

A template can look correct while rendering empty values, wrong types, missing resources, invalid selectors, wrong environment configuration, or unintended conditional branches.

---

# 4. Successful Helm rendering does not prove deployability

Treat validation as separate layers:

```text
Helm lint
→ Helm render
→ Kubernetes/OpenShift schema validation
→ policy validation
→ deployment/runtime validation
```

`helm template` can succeed even when Kubernetes/OpenShift or organisation policies would reject the output.

---

# 5. Boolean-looking strings are not booleans

A Helm value such as:

```yaml
feature: "false"
```

is a string.

A non-empty string can evaluate as truthy in Go-template conditions.

Compare:

```bash
--set feature=false
```

with:

```bash
--set-string feature=false
```

Review values used in:

```text
{{ if .Values.* }}
{{ if not .Values.* }}
```

Negative tests:

- boolean `false`
- string `"false"`
- boolean `true`
- string `"true"`
- missing value
- null value

---

# 6. Required deployment values should fail fast

Important deployment values should not silently render as empty.

Examples may include:

- image
- namespace
- service account
- environment
- domain
- route hostname
- configuration file path
- Vault namespace/path

Deliberately render with required values missing or empty.

Recommended controls where appropriate:

- Helm `required`
- `values.schema.json`
- template `fail`
- policy validation

---

# 7. Use values.schema.json when type contracts matter

If `values.schema.json` exists, use it as an explicit contract.

Validate:

- required properties
- types
- enums
- numeric boundaries
- allowed values

Absence of `values.schema.json` is not automatically a defect.

---

# 8. Every environment must be validated independently

Do not assume acceptance success proves union, rehearsal, or production correctness.

Render each available environment independently.

Compare:

- image/tag
- replicas
- runtime environment
- resources
- Vault
- routes
- service accounts
- feature toggles
- mock configuration
- environment identifiers

Defaults from lower environments may leak into higher environments.

---

# 9. Legacy properties require migration accountability

During legacy-to-Helm migration, every old property must have an explicit outcome.

Allowed statuses:

- `MIGRATED`
- `RENAMED`
- `DERIVED`
- `EXTERNALISED`
- `INTENTIONALLY_REMOVED`
- `NOT_APPLICABLE`
- `MISSING`
- `NEEDS_CLARIFICATION`

Deleted `.properties` files can hide missing deployment behaviour.

Nothing should disappear without explanation.

A required property with status `MISSING` is a migration defect.

---

# 10. Compare effective behaviour, not property names

A legacy property may be renamed, transformed, or injected by the pipeline.

Trace:

```text
legacy property
→ Helm value / pipeline variable
→ template
→ rendered Kubernetes/OpenShift field
```

Example:

```text
CPU_REQUEST
→ resources.requests.cpu
→ deployment.yaml
→ spec.template.spec.containers[].resources.requests.cpu
```

The final rendered behaviour is the real comparison target.

---

# 11. Git history is part of migration testing

When old files are deleted from the feature branch, use Git history/base branch to recover the migration baseline.

Useful read-only commands:

```bash
git diff --name-status <base>...HEAD
git diff <base>...HEAD
git show <base>:<path>
```

Do not report migration as out of scope simply because old files are absent from the working tree.

If the base branch cannot be determined, report:

`Migration comparison: NOT_VALIDATED`

---

# 12. Deleted legacy templates require behavioural parity

When legacy files such as `application-template.yaml`, DeploymentConfig YAML, or Service/Route YAML are removed, compare their effective behaviour with rendered Helm resources.

Compare:

- replicas
- labels
- selectors
- annotations
- image/tag
- ports
- environment variables
- resources
- probes
- ConfigMaps
- Secrets/Vault
- Services
- Routes
- volumes
- deployment strategy
- readiness behaviour

---

# 13. Deployment scripts require behavioural parity

A renamed or replaced deployment function is not automatically equivalent.

Compare old function/script against Helm, shared deployment library, replacement function, or intentionally removed behaviour.

Pay special attention to:

- standard variable definition
- route creation
- test routes
- canary weighting
- canary commit
- rollback
- version switching
- previous-object discovery

Review parameters, defaults, failure handling, and exit behaviour where evidence exists.

---

# 14. Deployment artifacts outside Helm must also be reviewed

Helm-only review is insufficient when deployment behaviour also exists in raw Kubernetes/OpenShift YAML, WireMock manifests, shell scripts, Jenkins files, route scripts, or environment substitution files.

Check for:

- unresolved `${VARIABLE}` placeholders
- empty mandatory values
- missing resources
- missing probes
- unused volumes
- mutable images
- invalid arguments
- committed `status:` blocks
- imperative infrastructure creation

---

# 15. Immutable selectors require upgrade-safety review

Volatile values should not be used carelessly in immutable Deployment selectors.

Review:

```text
spec.selector.matchLabels
```

against:

```text
spec.template.metadata.labels
```

Pay attention to:

- version
- patch version
- build number
- image tag
- release-specific labels

Version labels may be fine as informational pod labels but risky in selectors.

---

# 16. Sensitive values must not migrate into plain configuration

Migration can unintentionally move sensitive values from Secret/Vault handling into ConfigMaps or plain YAML.

Indicators include:

- TOKEN
- PASSWORD
- SECRET
- API_KEY
- CREDENTIAL
- PRIVATE_KEY

Inspect destination and usage without printing or decoding values.

---

# 17. Secret/Vault paths must be tested in both directions

Conditional Secret/Vault behaviour should be validated for both enabled and disabled paths.

Example:

```text
vault.enabled=false
→ local Secret expected

vault.enabled=true
→ local Secret not expected
```

Never expose Secret values while validating resource behaviour.

---

# 18. Resource syntax and resource policy are different checks

Separate syntactic/schema validity, organisation policy compliance, and operational sanity.

Example:

```text
request: 100m
limit: 2000m
```

may be syntactically valid but operationally suspicious.

Without policy evidence, classify unusual ratios as `POTENTIAL_RISK`, not defect.

---

# 19. Probe validation must include repository evidence

Health probes should be compared with actual application health endpoints and ports where evidence exists.

Check:

- path
- port
- protocol
- timeout
- delay
- thresholds

Do not assume a hardcoded probe is wrong simply because it is not values-driven.

---

# 20. Mutable image tags are reproducibility risks

Tags such as `latest` can make deployments non-reproducible.

Classify as `POTENTIAL_RISK` unless organisation policy explicitly prohibits mutable tags.

---

# 21. Configuration usage should be traced

Cross-check values against their usage.

Classify:

- defined and used
- defined but unused
- referenced but undefined
- environment override unused
- hardcoded value overriding configurable value

Unused configuration is normally a warning unless it causes runtime impact.

---

# 22. Conditional branches require explicit coverage

Every meaningful Helm conditional should have both paths reviewed.

A branch that is never rendered is not validated.

---

# 23. Policy validation must use actual repository/pipeline rules

Do not invent organisation-specific policy requirements.

Discover:

- Conftest
- OPA
- Rego
- `policy.yaml`
- central policy references
- Jenkins policy stages

Only validate rules supported by repository or documented evidence.

---

# 24. Policy failure should block deployment when it is a gate

When policy validation is intended as a deployment gate:

```text
policy failure
→ deployment stage must not execute
```

Confirm:

- validation failed
- deployment stage was skipped/stopped
- existing environment remained unchanged
- diagnostic output identified the violated rule

---

# 25. Canary/readiness/rollback must be behaviourally preserved

During deployment migration, validate:

- stable version remains healthy
- new pods become ready before traffic
- unready pods receive no traffic
- traffic weighting works
- canary commit works
- rollback restores stable behaviour
- non-canary switching remains correct

Do not assume shared-library replacements are equivalent without evidence.

---

# 26. Migration completeness requires explicit accounting

A migration review should end with measurable coverage.

Example:

```text
Total legacy properties:
Migrated:
Renamed/derived:
Externalised:
Intentionally removed:
Needs clarification:
Missing:
```

Also track environment parity, legacy script behaviour, and deleted template behaviour.

Migration cannot PASS while required properties or deployment behaviours remain `MISSING`.

---

# 27. Reusable learning must be controlled

The skill must not silently rewrite itself.

Use:

```text
review
→ reusable learning candidate
→ human verification
→ PR
→ team review
→ approved pattern/test update
```

Good reusable learnings include recurring migration defects, reusable negative tests, safe deterministic validation, deployment invariants, and recurring false-positive corrections.

Do not store secrets, credentials, internal URLs, production-sensitive values, or temporary incident details.

---

# 28. Read-only by default

Normal QA review should not mutate repositories or clusters.

Do not automatically run:

```text
helm install
helm upgrade
helm uninstall
kubectl apply
kubectl delete
oc apply
oc delete
```

Do not automatically install tools.

Any state-changing operation requires explicit user approval and authorisation.
