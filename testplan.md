# Helm Migration & CS1–CS2 Deployment Test Plan

## 1. Objective

The objective of this testing is to validate that the migration from the existing deployment model to Helm is functionally equivalent, deployment-safe, policy-compliant, and capable of deploying the application correctly across both CS1 and CS2.

The testing will verify that:

- Existing deployment configuration is correctly migrated to Helm.
- Required legacy properties and deployment behaviour are not lost.
- Helm charts render valid Kubernetes/OpenShift manifests.
- Environment-specific configuration is correct.
- Deployment policies are enforced before deployment.
- Deployment target resolution correctly identifies CS1 and CS2.
- Equivalent application versions and required configuration are deployed to both targets.
- Partial deployment failures are detected.
- Application readiness and service connectivity work after deployment.
- Rollback remains possible.
- Helm release-level tests can be used as an additional post-deployment verification layer.

---

# 2. Scope

## In Scope

The following areas are included:

- Helm chart structure
- `Chart.yaml`
- `values.yaml`
- environment-specific values files
- Helm templates
- rendered Kubernetes/OpenShift manifests
- legacy `.properties` and deployment configuration
- legacy application/deployment templates
- deployment scripts
- pipeline/shared-library changes
- ConfigMaps
- Secret/Vault references
- Services
- Routes/Ingress
- CPU and memory configuration
- readiness/liveness/startup probes
- policy-as-code validation
- CI/CD deployment gates
- deployment-target selection
- CS1 deployment
- CS2 deployment
- CS1/CS2 configuration parity
- canary/staged deployment where applicable
- rollback
- Helm release tests
- API/application smoke validation

## Out of Scope

Unless specifically required by the story:

- Full functional regression
- Full performance/load testing
- Infrastructure provisioning
- Penetration testing
- Destructive production testing

---

# 3. Test Strategy

## 3. Test Approach

Testing will be performed across multiple validation layers to verify migration completeness, deployment correctness, policy compliance, multi-target deployment and runtime health.

| Stage | Validation | Key Outcome |
|---|---|---|
| 1. Legacy Configuration Comparison | Compare existing properties, templates and deployment configuration with the new Helm implementation | Confirm no required configuration is lost during migration |
| 2. Helm Lint | Validate Helm chart structure and syntax | Chart is structurally valid |
| 3. Helm Template / Render | Render manifests using applicable environment values | Verify the effective Kubernetes/OpenShift configuration |
| 4. Schema Validation | Validate rendered resources against Kubernetes/OpenShift schema where tooling is available | Detect invalid resource definitions and field values |
| 5. Policy Validation | Execute configured policy-as-code controls | Non-compliant configuration is blocked before deployment |
| 6. Deployment Target Resolution | Validate the deployment plan/emulation for all expected targets | Confirm the release is targeted to the correct deployment locations |
| 7. CS1 / CS2 Deployment | Deploy to the required targets | Confirm deployment succeeds on both targets |
| 8. Readiness & Service Health | Validate pod readiness, Service routing and application health | Confirm deployed workloads are capable of serving traffic |
| 9. Helm Release Tests | Execute configured Helm test hooks where available | Validate release-level connectivity and health |
| 10. API Smoke Validation | Execute agreed critical API smoke tests | Confirm the deployed application is functionally reachable |
| 11. CS1 / CS2 Parity | Compare versions and effective deployment configuration across targets | Detect configuration/version drift |
| 12. Rollback / Recovery | Validate rollback and partial-failure recovery | Confirm the service can safely return to a stable state |

### Validation Principle

A successful Helm lint or Helm render alone will **not** be considered sufficient evidence of deployment correctness.

Validation will progressively cover:

**Configuration → Rendered Manifest → Policy → Deployment Target → Runtime Health → Multi-target Parity → Recovery**

### Key Quality Gates

- Required legacy configuration must be accounted for before migration sign-off.
- Mandatory policy violations must prevent deployment.
- Expected deployment targets must be resolved before deployment execution.
- CS1 and CS2 must run the expected release and configuration unless an approved difference exists.
- New workloads must become Ready before receiving traffic.
- Partial deployment failures must be clearly detectable.
- Critical API smoke validation must pass after deployment.
- Rollback/recovery behaviour must be defined and validated where applicable.
A successful Helm render alone will not be considered sufficient evidence of deployment correctness.

---

# 4. Legacy-to-Helm Migration Validation

The previous deployment implementation will be compared against the new Helm implementation.

For every relevant legacy configuration property, the following will be identified:

| Legacy Property | Environment | Previous Usage | New Helm/Pipeline Source | Rendered Destination | Migration Status |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Allowed migration statuses:

- MIGRATED
- RENAMED
- DERIVED
- EXTERNALISED
- INTENTIONALLY_REMOVED
- NOT_APPLICABLE
- MISSING
- NEEDS_CLARIFICATION

### Expected Result

Every required legacy property must have an identified replacement or approved outcome.

A required configuration item marked as `MISSING` will be treated as a migration defect.

---

# 5. Legacy Deployment Behaviour Parity

The legacy deployment/application template and deployment scripts will be compared with the new rendered Helm resources.

The following areas will be validated:

| Area | Verification |
|---|---|
| Replicas | Existing intended behaviour is preserved |
| Image | Correct repository/version is used |
| Labels | Required labels are preserved |
| Selectors | Correct and upgrade-safe |
| Environment Variables | Required configuration is preserved |
| ConfigMaps | Required configuration is available |
| Secret/Vault | References remain correct and secure |
| CPU/Memory | Values preserved or approved changes documented |
| Readiness Probe | Health/readiness behaviour preserved |
| Liveness Probe | Runtime health behaviour preserved |
| Volumes | Required volume/mount behaviour preserved |
| Service | Selectors and ports correct |
| Route/Ingress | Host, backend and TLS configuration correct |
| Deployment Strategy | Equivalent or approved replacement |
| Rollback | Existing recovery capability preserved |

---

# 6. Helm Static Validation

## Helm Lint

Run Helm lint against the chart.

Example:

`helm lint <chart>`

Where useful:

`helm lint --strict <chart>`

### Validate

- No Helm syntax errors
- Chart metadata is valid
- Templates are structurally valid
- Warnings are reviewed
- Strict-mode issues are understood

---

# 7. Helm Render Validation

Render every applicable configuration independently.

Example:

`helm template <release> <chart> -f <values-file>`

### Validate

- No unresolved Helm expressions
- No unexpected empty mandatory values
- Correct resource names
- Correct namespace/project configuration
- Correct environment-specific values
- Correct Services and Routes
- Correct ConfigMap/Secret references
- Correct resources and probes

---

# 8. Helm Values Negative Testing

High-risk Helm values will be tested with invalid or boundary inputs.

Test scenarios include:

- Required value missing
- Required value empty
- Null value
- Wrong datatype
- Invalid CPU quantity
- Invalid memory quantity
- Missing environment override
- Invalid hostname
- Invalid service account
- Invalid conditional input

## Boolean Type Validation

For boolean configuration, compare:

`--set FLAG=false`

with:

`--set-string FLAG=false`

### Expected Result

A string value such as `"false"` must not unintentionally activate a Helm conditional intended for boolean `true`.

---

# 9. Environment Configuration Validation

Each available environment-specific values file will be rendered independently.

Compare effective configuration for:

| Configuration | Environment 1 | Environment 2 | Environment 3 | Environment 4 |
|---|---|---|---|---|
| Image/Tag |  |  |  |  |
| Replicas |  |  |  |  |
| Runtime Environment |  |  |  |  |
| CPU Request |  |  |  |  |
| CPU Limit |  |  |  |  |
| Memory Request |  |  |  |  |
| Memory Limit |  |  |  |  |
| Service Account |  |  |  |  |
| Secret Provider |  |  |  |  |
| Route/Domain |  |  |  |  |
| Feature Toggles |  |  |  |  |

### Expected Result

Environment-specific configuration must not unintentionally inherit inappropriate default or lower-environment values.

---

# 10. Kubernetes/OpenShift Resource Validation

Rendered resources will be reviewed for:

- API version
- Resource kind
- Resource name
- Namespace/project
- Labels
- Annotations
- Replica count
- Selectors
- Pod-template labels
- Container image
- Ports
- Environment variables
- Service account
- ConfigMaps
- Secret references
- CPU/memory requests
- CPU/memory limits
- Readiness probe
- Liveness probe
- Startup probe where applicable
- Volumes and volume mounts
- Deployment strategy

Schema validation will be performed where an approved validator is available.

---

# 11. Policy-as-Code Validation

The policy mechanism configured for the deployment will be validated.

Test scenarios:

| Scenario | Expected Result |
|---|---|
| Valid manifest | PASS |
| Required field missing | FAIL |
| Incorrect required value | FAIL |
| Incorrect case | FAIL where case-sensitive |
| Incorrect YAML location | FAIL |
| Multiple policy violations | Violations clearly reported |
| Policy unavailable | Behaviour follows pipeline design |
| Policy failure | Deployment must not proceed when policy is mandatory |

### Expected Result

Mandatory policy validation must run before deployment and must prevent non-compliant manifests from being deployed.

---

# 12. Deployment Target Resolution – CS1 and CS2

The deployment pipeline/emulation logic will be validated to confirm where the deployment will be executed.

The DevTrain/emulation mechanism should allow target resolution to be inspected before actual deployment.

| Target | Expected Deployment | Namespace/Project | Chart Version | Image Version | Values Source | Result |
|---|---|---|---|---|---|---|
| CS1 | Yes |  |  |  |  |  |
| CS2 | Yes |  |  |  |  |  |

### Validate

- CS1 is correctly resolved.
- CS2 is correctly resolved.
- Both are selected when dual-target deployment is required.
- Incorrect targets are not selected.
- Correct namespace/project is resolved for each target.
- Correct Helm values are supplied to each target.
- Correct image/version is supplied.
- Deployment target resolution can be verified before deployment.

---

# 13. CS1–CS2 Deployment Parity

After deployment, compare the effective state between CS1 and CS2.

| Item | CS1 | CS2 | Expected |
|---|---|---|---|
| Application Version |  |  | Match |
| Helm/Chart Version |  |  | Match |
| Image |  |  | Match |
| Replicas |  |  | Match or approved difference |
| CPU/Memory |  |  | Match or approved difference |
| Probes |  |  | Equivalent |
| Service |  |  | Equivalent |
| Configuration |  |  | Equivalent |
| Secret References |  |  | Correct |
| Policy Status |  |  | PASS |
| Pod Readiness |  |  | PASS |

Differences must be classified as:

- Intentional
- Target-specific
- Configuration drift
- Defect

---

# 14. Partial Deployment Failure

## Scenario: CS1 Succeeds and CS2 Fails

Validate:

- Pipeline clearly identifies partial deployment.
- Deployment is not reported as fully successful.
- Versions running on CS1 and CS2 are visible.
- Expected rollback/recovery logic is triggered or documented.
- Appropriate failure diagnostics are available.

## Scenario: CS1 Fails

Validate the agreed behaviour:

- Should CS2 deployment continue?
- Should deployment stop immediately?
- Should CS1 be rolled back?
- Should both targets remain on the previous version?

This behaviour must be agreed with the deployment/platform team.

---

# 15. Deployment Idempotency

Repeat the same deployment without changing configuration.

### Expected Result

- No duplicate resources
- No unexpected resource replacement
- No unintended configuration changes
- No version drift
- CS1 and CS2 remain consistent
- Re-running the deployment remains safe

---

# 16. Readiness and Availability

Validate:

- New pods become Ready.
- New pods do not receive traffic before readiness succeeds.
- Failed readiness prevents traffic.
- Expected replica count becomes available.
- Existing stable version remains available during rollout where required.
- Services route only to appropriate pods.

Where applicable also review:

- maxUnavailable
- maxSurge
- terminationGracePeriodSeconds
- graceful shutdown
- preStop behaviour

---

# 17. Canary / Staged Deployment

Where canary or staged deployment is supported:

## Healthy New Version

Expected:

- New pods become Ready.
- Stable version remains available.
- Traffic is shifted according to intended strategy.
- Promotion occurs only after successful validation.

## Unhealthy New Version

Expected:

- Unhealthy version does not receive unintended traffic.
- Stable version continues serving.
- Promotion does not occur.

## Commit / Promotion

Expected:

- New version becomes active.
- Traffic routing changes correctly.

---

# 18. Rollback Validation

Validate:

- Correct previous release/version is identified.
- Previous configuration remains usable.
- Pods become healthy after rollback.
- Service/Route points to the expected stable version.
- No obsolete resources interfere with traffic.

Where safe, validate rollback after:

- Failed deployment
- Failed CS1 deployment
- Failed CS2 deployment
- Partial CS1/CS2 deployment

---

# 19. Helm Release Tests

The Helm chart will be checked for Helm release tests.

Recommended structure:

`templates/tests/test-service-health.yaml`

Optional additional tests may include:

`templates/tests/test-release-version.yaml`

## Service Health Helm Test

The test should validate:

Helm Test Job/Pod  
→ Service DNS  
→ Service Port  
→ Application Health Endpoint  
→ Successful Response

Example execution in an authorised environment:

`helm test <release-name> --logs`

## Release Version Test

Where the application exposes a safe version/build endpoint:

Expected Version  
→ Deployed Service  
→ Version Endpoint  
→ Actual Version Comparison

This can also be used to verify CS1 and CS2 version parity.

### Helm Test Status

Use:

- CONFIGURED
- NOT_CONFIGURED
- NOT_RUN
- PASS
- FAIL

Absence of Helm release tests alone is not considered a deployment defect.

---

# 20. API Smoke Testing

After successful deployment, execute agreed critical smoke tests.

Minimum recommended coverage:

- Health endpoint
- Readiness endpoint
- One critical successful API request
- Authentication/authorisation where applicable
- Critical dependency connectivity where appropriate

Helm tests do not replace full API regression testing.

---

# 21. Secret and Configuration Validation

Validate:

- Required ConfigMaps exist.
- Required Secret references exist.
- Secret/Vault configuration is correct.
- Conditional secret-provider behaviour is correct.
- Sensitive values are not accidentally placed in ConfigMaps.
- Secret values are not exposed in test evidence or logs.

Where applicable, validate both secret-provider enabled and disabled paths.

---

# 22. Upgrade Safety

Validate configuration that may affect upgrades.

Review:

- Immutable Deployment selectors
- Version/build labels in selectors
- Workload naming changes
- Service selector changes
- ConfigMap name changes
- Secret name changes
- Route/Ingress backend changes
- Resource-name changes

### Expected Result

A normal Helm upgrade should not unexpectedly require manual deletion or recreation of resources.

---

# 23. Observability

Validate where applicable:

- Application logs remain available.
- Deployment target can be identified.
- Metrics remain available.
- Tracing configuration remains valid.
- Required operational annotations remain present.
- CS1 and CS2 failures can be distinguished operationally.
- Deployment/policy failures provide useful diagnostics.

---

# 24. Priority Negative Scenarios

| Priority | Scenario |
|---|---|
| P0 | Required legacy property is not migrated |
| P0 | CS2 is missing from deployment target resolution |
| P0 | Wrong namespace/project selected |
| P0 | CS1 succeeds while CS2 fails |
| P0 | Rollback fails |
| P0 | Unready version receives traffic |
| P1 | Boolean `"false"` behaves as true |
| P1 | Required Helm value is empty |
| P1 | Wrong Service targetPort |
| P1 | Missing Secret reference |
| P1 | Invalid CPU/memory quantity |
| P1 | Policy violation does not stop deployment |
| P1 | Application version differs between CS1 and CS2 |
| P2 | Mutable image tag |
| P2 | Unused configuration |
| P2 | Helm release tests are not configured |

---

# 25. Entry Criteria

Testing can begin when:

- Helm migration changes are available.
- Legacy/base version is identifiable.
- Relevant Helm chart is available.
- Deployment requirements are understood.
- Required pipeline changes are available.
- Required policy configuration is accessible.
- Appropriate test/deployment environments are available.

---

# 26. Exit Criteria

Testing is complete when:

- No unresolved Critical/High confirmed defect remains.
- Required legacy properties are accounted for.
- Helm lint/render validation succeeds.
- Required policy checks pass.
- Deployment targets resolve correctly.
- CS1 deployment succeeds.
- CS2 deployment succeeds.
- Required CS1/CS2 parity is confirmed.
- Pods become healthy/Ready.
- Required Helm release tests or smoke tests pass.
- Rollback behaviour is validated or formally accepted.
- Remaining risks are documented and accepted.

---

# 27. Test Evidence

Capture evidence for:

- Helm lint
- Helm rendered manifests
- Migration property matrix
- Environment comparison
- Policy validation
- Deployment target-resolution/emulation
- CS1 deployment
- CS2 deployment
- CS1/CS2 application versions
- Pod readiness
- Helm test output
- API smoke result
- Rollback result

Sensitive values must not be included in evidence.

---

# 28. Final Test Summary

| Area | Result |
|---|---|
| Legacy Migration Parity | PASS / FAIL / NEEDS_REVIEW |
| Helm Lint | PASS / FAIL |
| Helm Render | PASS / FAIL |
| Schema Validation | PASS / FAIL / NOT_RUN |
| Policy Validation | PASS / FAIL / NOT_RUN |
| Deployment Target Resolution | PASS / FAIL |
| CS1 Deployment | PASS / FAIL |
| CS2 Deployment | PASS / FAIL |
| CS1/CS2 Parity | PASS / FAIL |
| Readiness / Health | PASS / FAIL |
| Helm Release Tests | PASS / FAIL / NOT_RUN / NOT_CONFIGURED |
| API Smoke | PASS / FAIL |
| Canary / Staged Deployment | PASS / FAIL / N/A |
| Rollback | PASS / FAIL / NOT_RUN |

### Defect Summary

Critical:

High:

Medium:

Low:

Needs Clarification:

### Overall Result

**PASS / FAIL / NEEDS_REVIEW**

### Comments

Add final release recommendation, known risks, accepted deviations, and outstanding follow-up actions.
