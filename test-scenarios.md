# Helm QA Verifier — Reusable Test Scenarios

This file contains reusable test scenarios aligned with the current `helm-qa-verifier` skill.

Apply only scenarios relevant to the repository being reviewed.

Do not blindly execute every scenario.

Prioritise based on deployment risk, migration scope, policy requirements, and environment impact.

---

# 1. Helm chart discovery

## Scenario: Identify chart root

Given a repository contains one or more Helm charts, identify:

- Chart.yaml
- values.yaml
- environment values files
- templates
- helper templates
- raw deployment artifacts
- pipeline/policy files

Expected: correct chart root identified before validation begins.

---

# 2. Helm lint

## Valid chart

Run:

```bash
helm lint <chart>
```

Expected: PASS.

## Strict lint

Run:

```bash
helm lint --strict <chart>
```

Expected: warnings promoted according to Helm strict behaviour.

---

# 3. Helm rendering

## Default values render

```bash
helm template qa-test <chart>
```

Expected: render succeeds without unresolved Helm expressions.

## Environment values render

For each environment:

```bash
helm template qa-test <chart> -f <environment-values>
```

Expected: render succeeds and effective configuration matches the environment.

---

# 4. Required values

## Required value missing

Omit a required value.

Expected: render, schema, or policy validation fails where the field is mandatory.

## Required value empty

Set the required value to empty.

Expected: chart fails fast if empty value would make deployment unusable.

## Required value null

Expected: reject or explicitly handle according to contract.

---

# 5. Datatype validation

## Wrong datatype

Provide string where boolean/number is expected.

Expected: schema or template validation detects incorrect type where type enforcement exists.

## Boolean false

```bash
--set FLAG=false
```

Expected: feature disabled.

## String "false"

```bash
--set-string FLAG=false
```

Expected: behaviour explicitly verified.

If string `"false"` causes enabled behaviour, flag defect/risk.

## Boolean true

```bash
--set FLAG=true
```

Expected: feature enabled.

## String "true"

```bash
--set-string FLAG=true
```

Expected: chart handles type intentionally.

---

# 6. values.schema.json

Test:

- required property missing
- wrong type
- invalid enum
- boundary value

Expected: schema behaviour matches contract.

---

# 7. Environment matrix

Render every available environment independently.

Typical environments:

- default
- acceptance
- union
- rehearsal
- production

Compare:

- image/tag
- replicas
- runtime mode
- environment identifiers
- resources
- Vault
- routes
- service account
- feature toggles
- mock settings

---

# 8. Environment fallback leakage

Remove an environment override.

Expected: determine whether default/lower-environment configuration leaks into higher environment.

Example risk:

`NODE_ENV=dev` unexpectedly appearing in rehearsal or production.

---

# 9. Legacy property discovery

For each deleted legacy `.properties` file:

- list all keys
- determine old usage
- map to new Helm/pipeline configuration
- identify rendered destination

Expected status for each key:

- MIGRATED
- RENAMED
- DERIVED
- EXTERNALISED
- INTENTIONALLY_REMOVED
- NOT_APPLICABLE
- MISSING
- NEEDS_CLARIFICATION

---

# 10. Environment-specific property migration

Compare independently:

```text
acceptance.properties
→ values-acceptance.yaml

union.properties
→ values-union.yaml

rehearsal.properties
→ values-rehearsal.yaml

production.properties
→ values-production.yaml
```

Expected: required settings accounted for in every environment.

---

# 11. Legacy property missing from Helm

A key exists in legacy properties but no new value, pipeline input, or rendered equivalent exists.

Expected: status `MISSING`.

If required for deployment behaviour, migration must FAIL.

---

# 12. Legacy property renamed

Trace:

```text
old property
→ new value
→ template
→ rendered destination
```

Expected: status `RENAMED` or `DERIVED`.

---

# 13. Legacy property externalised

Old property is now supplied by pipeline/shared library/platform.

Expected: evidence for new source.

If no evidence exists: `NEEDS_CLARIFICATION`.

---

# 14. Intentionally removed property

Legacy setting no longer required.

Expected: mark `INTENTIONALLY_REMOVED` only with repository or team evidence.

---

# 15. Legacy application-template parity

Compare old template/DeploymentConfig with new rendered Helm output.

Verify:

- replicas
- labels
- selectors
- annotations
- image/tag
- ports
- environment variables
- ConfigMaps
- Secrets/Vault
- resources
- probes
- volumes
- Services
- Routes
- deployment strategy
- readiness behaviour

---

# 16. Script/function migration

For modified/deleted deployment scripts map old behaviour to replacement.

Cover:

- standard variable setup
- route creation
- test route creation
- canary deployment
- service weighting
- canary commit
- rollback
- new-version switching
- previous-object discovery

Expected: no required behaviour disappears silently.

---

# 17. Script parameter parity

Compare old and new function parameters, defaults, return/exit behaviour, and failure handling.

Expected: do not assume rename means equivalent behaviour.

---

# 18. Raw manifest placeholder

Raw YAML contains `${VARIABLE}`.

Expected: confirm substitution occurs before apply.

If unresolved: deployment risk.

---

# 19. Raw manifest missing resources

Container has no requests/limits.

Expected: policy/schema result according to project rules.

If no policy: operational risk.

---

# 20. Raw manifest missing probes

Container has no readiness/liveness probe.

Expected: compare with service requirements and policy.

---

# 21. Raw manifest mutable image

Image uses `latest`.

Expected: `POTENTIAL_RISK` unless policy prohibits it.

---

# 22. Raw manifest status section

Apply manifest contains committed `status:`.

Expected: report as noisy/unnecessary unless intentionally required.

---

# 23. Raw manifest unused volume

Volume defined but not mounted.

Expected: warning for dead configuration.

---

# 24. Container image/tag

Test:

- image missing
- tag missing
- mutable tag

Expected: required-value or reproducibility result as appropriate.

---

# 25. Deployment replicas

Test:

- valid replicas
- missing replicas
- zero replicas
- invalid datatype

Expected: behaviour follows schema/policy/design.

---

# 26. Selector-label parity

Deployment selector and pod labels differ.

Expected: validation/deployment failure.

---

# 27. Immutable selector upgrade safety

Selector contains patch version/build/image tag.

Change the volatile value.

Expected: identify potential immutable-selector upgrade failure.

---

# 28. CPU request

Test:

- valid CPU request
- missing CPU request
- empty CPU request
- invalid CPU quantity such as `2cores`

Expected: schema/policy behaviour as appropriate.

---

# 29. Memory request

Repeat equivalent tests for memory.

---

# 30. CPU/memory limits

Validate:

- missing limit
- empty limit
- invalid quantity
- request/limit relationship where applicable

---

# 31. Suspicious request/limit ratio

Example:

```text
request=100m
limit=2000m
```

Expected: `POTENTIAL_RISK` unless policy proves invalid.

---

# 32. Readiness probe

Validate:

- correct path
- correct port
- correct protocol
- timeout
- period
- failure threshold

Negative tests:

- missing
- wrong path
- wrong port
- empty value
- environment mismatch

---

# 33. Liveness probe

Repeat equivalent checks.

---

# 34. Startup probe

Where applicable test:

- valid configuration
- missing when required
- invalid path/port

---

# 35. ConfigMap reference

Test:

- valid reference
- missing ConfigMap
- wrong name

Expected: reference behaviour identified.

---

# 36. Secret reference

Test:

- valid Secret reference
- missing Secret
- wrong Secret name

Never display secret values.

---

# 37. Sensitive key in ConfigMap

Use key names suggesting:

- TOKEN
- PASSWORD
- SECRET
- API_KEY
- CREDENTIAL

Expected: flag destination for Secret/Vault review.

Do not print value.

---

# 38. Vault disabled path

Given Vault disabled, expected local/non-Vault secret behaviour should appear.

---

# 39. Vault enabled path

Given Vault enabled, expected Vault configuration should appear and local Secret behaviour should match design.

---

# 40. Vault boolean/string regression

Compare:

```bash
--set E_VAULT=false
```

with:

```bash
--set-string E_VAULT=false
```

Expected: intentionally defined behaviour.

---

# 41. Conditional branch coverage

For every important Helm `if/else`:

- render true path
- render false path

Expected: both branches produce valid expected resources.

---

# 42. Defined-but-unused value

Value exists in values file but is not consumed.

Expected: warning for dead configuration.

---

# 43. Referenced-but-undefined value

Template references undefined value.

Expected: render result reviewed for empty/default/unexpected behaviour.

---

# 44. Unused environment override

Environment values file overrides value that is never consumed.

Expected: warning.

---

# 45. Hardcoded value overrides configurable value

Template hardcodes value despite corresponding values entry.

Expected: maintainability/environment risk.

---

# 46. Service validation

Check:

- selectors
- ports
- targetPort
- service name
- labels

Negative tests:

- selector mismatch
- wrong targetPort
- missing port

---

# 47. Route/Ingress validation

Check:

- hostname
- backend service
- TLS configuration
- environment-specific hostname

Negative tests:

- empty hostname
- wrong backend
- wrong environment domain

---

# 48. Policy validation positive case

Manifest satisfies all discovered policies.

Expected: Conftest/OPA PASS.

---

# 49. Required policy field missing

Expected: FAIL.

---

# 50. Wrong policy value

Expected: FAIL where exact value required.

---

# 51. Policy wrong case

Expected: FAIL where case-sensitive.

---

# 52. Policy wrong whitespace

Expected: FAIL where spacing-sensitive.

---

# 53. Annotation at wrong YAML level

Example: top-level Deployment annotation instead of pod-template annotation.

Expected: FAIL when policy targets pod-template metadata.

---

# 54. Multiple policy violations

Expected: verify whether all violations are reported or validation stops early.

---

# 55. Policy configuration missing

Expected: behaviour matches pipeline design.

Report fail-closed, fail-open, or NOT_VALIDATED as appropriate.

---

# 56. Policy repository unavailable

Expected: deployment behaviour matches designed control.

Do not assume; verify.

---

# 57. Kubernetes schema validation

Where approved validator exists, validate rendered manifests.

Negative cases:

- invalid CPU quantity
- invalid field type
- unsupported field
- malformed resource

---

# 58. CI/CD policy gate

Introduce a safe non-production policy violation.

Expected:

- validation stage fails
- deployment stage does not execute
- existing deployment remains unchanged
- error identifies violated rule

---

# 59. Pipeline-required value injection

Values such as namespace/image/environment are injected by pipeline.

Expected: identify source and type.

If source cannot be proven: `NEEDS_CLARIFICATION`.

---

# 60. Pipeline boolean injection

Pipeline/shared library supplies boolean-like value.

Expected: determine whether it passes boolean or string.

Validate both if uncertain.

---

# 61. Canary start

Expected:

- stable version remains available
- new version pods created
- traffic behaviour follows strategy

---

# 62. New version not ready

Expected:

- unready pods receive no traffic
- stable version continues serving

---

# 63. Canary weighting

Expected: actual weighting matches configured behaviour.

---

# 64. Canary commit

Expected: new version becomes active according to design.

---

# 65. Canary rollback

Expected: stable version restored and traffic returns correctly.

---

# 66. Non-canary deployment

Expected: version switching remains correct when canary disabled.

---

# 67. Rollback script/function parity

Compare old and new rollback implementation.

Expected: required recovery behaviour preserved.

---

# 68. Route-creation script parity

Compare old and new route logic.

Expected: route behaviour preserved or intentionally changed.

---

# 69. Environment variable migration

For every legacy environment variable, trace old source to new rendered destination.

Expected: no required variable silently disappears.

---

# 70. Secret/Vault migration parity

Compare old secret source/destination with new approach.

Expected:

- sensitive values stay protected
- references remain correct
- no accidental ConfigMap/plain-text migration

---

# 71. Resource migration parity

Compare old vs new:

- CPU request
- CPU limit
- memory request
- memory limit

Expected: differences explained.

---

# 72. Probe migration parity

Compare old vs new readiness/liveness/startup behaviour.

Expected: differences explained and safe.

---

# 73. Route migration parity

Compare old vs new route/hostname/TLS behaviour.

Expected: environment behaviour preserved or intentionally changed.

---

# 74. Service migration parity

Compare:

- selector
- ports
- targetPort
- name
- labels

Expected: equivalent application routing.

---

# 75. Migration completeness summary

Report:

```text
Total legacy properties:
Migrated:
Renamed/derived:
Externalised:
Intentionally removed:
Needs clarification:
Missing:
```

Also report:

```text
Legacy script behaviours:
Covered:
Missing:
Needs clarification:
```

Expected: migration cannot PASS while required items remain `MISSING`.

---

# 76. Post-deployment pod health

Where authorised, verify:

- expected replicas
- pods Ready
- no CrashLoopBackOff
- no ImagePullBackOff
- readiness passes

---

# 77. Post-deployment Service/Route health

Verify:

- service endpoints
- route backend
- expected hostname
- TLS where applicable

---

# 78. Application/API smoke

After successful deployment, agreed smoke/API tests should pass.

---

# 79. Rollback verification

Where authorised, previous stable version should be restorable.

---

# 80. Reusable learning candidate

After substantial review, propose reusable learning only if it:

- applies across projects
- is verified
- improves deterministic validation
- reduces false positives

Do not automatically modify shared skill/reference files.
