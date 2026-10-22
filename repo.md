Use the helm-qa-verifier skill.

Review the test plan at:

docs/test-plans/helm-migration-cs1-cs2-test-plan.md

against the ACTUAL implementation in this repository.

This is a test-plan gap analysis.

Operate in read-only mode.
Do not modify files.
Do not deploy anything.
Do not run state-changing commands.

Do not simply review the wording of the test plan.

Inspect the repository and determine whether the test plan covers the
actual deployment implementation.

Review:

1. Helm charts and templates
2. values.yaml and all environment-specific values files
3. legacy configuration and deleted files using Git history/base branch
4. legacy properties files
5. old deployment/application templates
6. deployment scripts and helper functions
7. CI/CD pipeline configuration
8. deployment target resolution
9. CS1 and CS2 deployment logic
10. DevTrain/emulation logic
11. policy-as-code configuration
12. Kubernetes/OpenShift resources
13. ConfigMaps and Secret/Vault references
14. Services and Routes/Ingress
15. readiness/liveness/startup probes
16. resource requests and limits
17. rollout/canary/staged deployment logic
18. rollback logic
19. Helm test configuration
20. application smoke-test capability
21. observability/configuration required for deployment verification

For every implementation behaviour discovered, determine whether it is
covered by the test plan.

Produce:

## Test Plan Coverage Matrix

| Implementation Area | Repository Evidence | Covered in Test Plan? | Test Plan Section | Gap | Priority |

Use:

COVERED
PARTIALLY_COVERED
NOT_COVERED
NOT_APPLICABLE
NEEDS_CLARIFICATION

Then specifically identify:

## Missing Test Scenarios

For each:
- priority
- scenario
- repository evidence
- risk
- expected result
- recommended test-plan section

## Over-Testing / Not Applicable

Identify test-plan scenarios that are not relevant to this repository.

Do not keep generic tests just because they appear in the test plan.

## Migration Coverage Gaps

Verify whether the plan covers:
- every deleted legacy property/configuration source
- deployment-template migration
- script/function migration
- environment-specific migration

## CS1 / CS2 Coverage Gaps

Verify whether the plan covers the actual target-resolution mechanism,
target-specific configuration, partial deployment behaviour, version/config
parity, rollback and failure handling.

## Helm Release Test Opportunities

Check whether templates/tests or helm.sh/hook:test already exist.

If not, identify which release-level tests would provide real value based on
the actual service implementation.

Do not invent endpoints.

## Final Assessment

Test plan completeness:
COMPLETE / NEEDS_UPDATE / MAJOR_GAPS

Give:
- P0 gaps
- P1 gaps
- P2 improvements
- clarification questions

Do not modify the test plan.
