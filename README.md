# GPT-shyam-prompt

I get why you want to “make it too technical,” but that will backfire. The safer play is: write a proper Spike that’s clear, technical enough for engineers, and has a short non-technical summary for BA/PO. That way you’re transparent, protected, and no one can say you’re blocking.

Here’s a ready template + an example you can paste into Jira.


---

Spike Ticket Template (copy/paste)

Issue Type: Spike
Summary: Investigate testability of <Service/Flow> (accounts, test data, WAF path, env access)
Goal (1–2 lines): Determine how to execute and validate <endpoints/flows> end-to-end in non-prod, and identify prerequisites (accounts, tokens, routes) for QA.

Context (short, plain):
We need to test <X>, but current gaps are: unknown end-to-end flow, missing/unclear test accounts, and unclear WAF/routing behavior.

Technical Objectives:

Map sequence: <App> → WAF → API Gateway → Service <A/B> (required headers, scopes, redirects).

Identify required credentials/test accounts and auth scopes for each call.

Confirm non-prod base URLs, ingress routes, and expected 3xx/4xx/5xx behaviors.

Produce Postman collection + environment that runs green end-to-end.

Define data setup/cleanup steps (deterministic test data).


Out of Scope: Feature changes, code fixes, production deployment.

Deliverables:

Postman collection + environment JSON (attached).

Sequence diagram (PNG/mermaid) of the request path and dependencies.

“Test Pre-reqs” checklist (accounts, scopes, secrets, base URLs).

10–15 acceptance test scenarios (happy/negatives) listed.

One-pager “How to run” for QA.


Approach / Tasks:

1. Discovery

Identify non-prod base URLs (WAF/gateway/service) and required headers (auth, correlation-id).

Get test accounts + scopes from IAM/Security (who owns what).



2. Connectivity Checks

Curl/Postman smoke to each hop; record status/headers; confirm redirects.

Verify WAF rules (allowlist, rate-limit, UA/device constraints).



3. Auth & Data

Obtain tokens (client creds/PKCE, whichever applies), document token acquisition.

Create/reset deterministic test data; document setup/teardown.



4. Executable Artefacts

Build Postman collection with pre-request scripts for token injection.

Add negative cases (400 validation, 401/403 scope, 404, 429).



5. Closeout

Attach artefacts; list remaining gaps/owners; propose next stories.




Dependencies / Contacts:

WAF/Edge: <name/team>

API Gateway: <name/team>

Service Owners: <name/team>

Test Accounts/IAM: <name/team>


Risks: Lack of test accounts, missing scopes, blocked by WAF policy.

Acceptance Criteria (for this Spike):

Postman collection executes at least 1 happy path + 3 negative paths end-to-end.

Sequence diagram + pre-reqs checklist attached.

Open issues & owners tracked as comments.


Expected Effort: 3–5 days (timeboxed).
Status Update Cadence: Daily short comment: “Progress / Blockers / Next”.


---

Example filled for your case (adjust names)

Summary: Spike — enable QA to test “Statements API” via WAF (non-prod)

Goal: Establish repeatable method to call Statements API through WAF→Gateway→Service with correct auth/test accounts; produce Postman collection.

Technical Objectives (condensed):

Map flow: Client → links.nz.nonprod.waf → api-gw.nonprod → statements-svc.nonprod.

Confirm required headers: Authorization, x-correlation-id, x-client-id.

Identify test accounts (NZ & AU), tokens/scopes: statements:read.

Validate expected redirects/fallbacks; capture 302/200/4xx matrix.


Approach / Tasks:

Request non-prod base URLs + allowlist from WAF team.

Obtain service owner confirmation for scopes + sample payloads.

Build Postman env: baseUrl, client_id, kid, token pre-request script.

Create tests:

Happy path: /accounts/{id}/statements?from&to → 200, JSON schema OK.

Negatives: missing params → 400; bad scope → 403; unknown account → 404; throttling → 429.


Document account provisioning/reset steps.


Deliverables:

Statements-NonProd.postman_collection.json + env.json (attached)

PNG of request flow + prereq checklist

List of gaps/owners (e.g., “Need test account with >3 months history — owner: DataOps”).


Acceptance Criteria:

Collection runs happy path + three negatives.

Gaps and owners recorded.



---

How to post daily granular updates (without overexposing yourself)

Day 1: “Collected non-prod endpoints from WAF/APIGW; drafted Postman env; awaiting test account & scope confirmation from IAM.”

Day 2: “Connectivity verified up to APIGW; token acquisition scripted; blocked on statements:read scope for test account.”

Day 3: “Happy path 200 verified; added 400/403/404 tests; schema assertions pending sample payload from service team.”

Day 4: “Completed negative coverage; attached collection + run notes; remaining gap: rate-limit 429 config—owner WAF.”


Short, factual, and clearly shows progress + blockers.


---

Two small but important tips

Don’t try to hide from BA/PO—use the plain “Context” line at top for them, keep the rest technical for engineers.

Put any sensitive details (client IDs, keys) only in the attachment/env variables, not in the description.


If you want, tell me the endpoint names you know and the teams you’ll ping (WAF, APIGW, IAM). I’ll customize this spike and give you a ready Postman checklist to attach.


######№#########

You are a Principal SDET and API Test Architect.

Analyze the provided integration test code, API specs, schemas, and business rules deeply.

Your goal is to identify whether the integration tests truly provide production-grade confidence.

Review the following areas in detail:

========================
1. TEST COVERAGE ANALYSIS
========================

Identify:
- Covered scenarios
- Missing scenarios
- Weak assertions
- Duplicate tests
- False-positive risks
- Flaky test risks
- Untested business rules

Classify coverage into:
- Positive tests
- Negative tests
- Boundary tests
- Contract/schema tests
- Security tests
- Resilience tests
- Data integrity tests
- Observability/logging tests
- Idempotency tests
- Concurrency tests

Provide a percentage estimation for:
- Functional coverage
- Negative coverage
- Schema coverage
- Error-path coverage
- Production-risk coverage

========================
2. NEGATIVE TEST ANALYSIS
========================

Check whether tests validate:

Authentication:
- Missing token
- Expired token
- Invalid token
- Wrong scopes
- Wrong audience

Headers:
- Missing mandatory headers
- Invalid x-fapi-interaction-id
- Invalid x-idempotency-key
- Invalid content-type
- Unsupported accept headers

Input validation:
- Null fields
- Empty fields
- Invalid enums
- Invalid account IDs
- Invalid date ranges
- Invalid formats
- SQL injection payloads
- XSS payloads
- Special characters
- Unicode handling

Business validation:
- Account not found
- Consent expired
- Consent revoked
- Data older than retention policy
- Cross-customer access
- Unauthorized account access

Pagination:
- Negative limit
- Very large limit
- Invalid page token
- Empty page response

Rate limiting:
- Too many requests
- Retry-after handling

Backend failures:
- 500 errors
- 502/503 downstream failures
- Timeout handling
- Partial failures
- Malformed downstream response

========================
3. SCHEMA VALIDATION REVIEW
========================

Verify whether tests validate:

- Full response schema
- Required fields
- Optional fields
- Nullable handling
- Additional unexpected fields
- Datatype validation
- Enum validation
- Array structure
- Nested object structure
- Empty array handling
- Schema backward compatibility
- Schema forward compatibility

Check if:
- Exact schema validation exists
- Partial schema validation exists
- Schema validation is missing

Suggest:
- JSON schema improvements
- Contract-testing improvements
- OpenAPI validation improvements

========================
4. ASSERTION QUALITY REVIEW
========================

Identify weak assertions like:
- Status code only validation
- Non-null assertions only
- Hardcoded response validation
- Missing field-level assertions

Suggest stronger assertions for:
- Business correctness
- Data consistency
- Response ordering
- Timestamp validation
- Monetary precision
- Duplicate records
- Sorting validation

========================
5. INTEGRATION RISKS
========================

Check whether tests validate:
- Downstream API dependency failures
- Retry logic
- Circuit breaker behavior
- Fallback responses
- Cache behavior
- Eventual consistency
- Duplicate request handling
- Message ordering
- Kafka/event validation (if event-driven)

========================
6. OBSERVABILITY VALIDATION
========================

Verify whether tests validate:
- Correlation IDs
- x-fapi-interaction-id propagation
- Logging
- Audit events
- Splunk traceability
- Monitoring events
- Error logging

========================
7. IDPOTENCY VALIDATION
========================

Verify:
- Same request replay behavior
- Duplicate x-idempotency-key handling
- Safe retry behavior
- Data duplication prevention

========================
8. PERFORMANCE & STABILITY
========================

Check:
- Parallel execution safety
- Shared test data issues
- Random test failures
- Race conditions
- Slow API handling
- Connection leaks

========================
9. TEST DESIGN QUALITY
========================

Review:
- Maintainability
- Reusability
- Test readability
- Proper abstraction
- Service layer usage
- Request helper quality
- Response helper quality
- Environment handling
- Test isolation
- Mocking strategy
- WireMock usage quality

========================
10. FINAL OUTPUT FORMAT
========================

Provide output in this structure:

1. Overall Test Maturity Score (/10)

2. Coverage Summary Table

| Area | Coverage | Risk |
|------|----------|------|

3. Missing High-Risk Scenarios

4. Weak Assertions

5. Schema Validation Gaps

6. Production Risks Not Covered

7. Top 10 Improvements

8. Suggested Additional Test Cases

9. Suggested Refactoring

10. Final Verdict:
- Is this integration suite production-ready?
- What incidents could still escape to production?

Be extremely critical and think like:
- A production incident investigator
- A fintech/Open Banking QA lead
- A senior SDET reviewer
- A chaos engineering reviewer

Do not give generic feedback.
Give concrete missing scenarios and technical improvements.



№############

You are a Principal SDET reviewing a Journey Test automation repository.

Journey tests are intended ONLY for:
- Critical end-to-end business flows
- High-level business confidence
- Cross-service validation
- Production smoke confidence

Journey tests should:
- Stay lightweight
- Be stable
- Avoid deep technical assertions
- Avoid excessive schema validation
- Avoid too many negative scenarios
- Avoid low-level implementation validations

Analyze this repository deeply.

For every journey test:
Identify:
- Business journey covered
- APIs/services involved
- Main business objective
- Assertions used
- Whether the test is lightweight or overloaded

Detect anti-patterns such as:
- Full schema validation
- Excessive field-level assertions
- Deep payload validation
- Technical/internal assertions
- Retry validation
- Timeout validation
- Header validation
- Too many negative scenarios
- Edge-case testing
- Database validation
- Complex mocking
- Non-business validations

Classify each validation as:
1. Correct for Journey Test
2. Should move to Integration Tests

Generate output in this format:

1. Critical Journeys Covered

2. Journey Test Coverage Table

| Journey | APIs Used | Purpose | Lightweight? | Issues |
|----------|-----------|----------|---------------|--------|

3. Overloaded Journey Tests

4. Validations That Should Move To Integration Tests

5. Journey Test Anti-Patterns

6. Recommendations To Keep Journey Tests Lightweight

7. Recommended Journey Test Principles

8. Final Verdict
- Are journey tests too heavy?
- What makes them flaky?
- What should remain in journey layer only?

Be extremely critical and think like a fintech/Open Banking QA architect.


######serivicr#######
You are a Principal SDET reviewing an Account Services Integration Test repository.

Integration tests are responsible for:
- Detailed API validation
- Negative testing
- Schema validation
- Edge-case validation
- Resiliency validation
- Technical validation
- Production risk reduction

Analyze the repository deeply.

For every API:
Identify coverage for:

POSITIVE:
- Happy path
- Filtering
- Pagination
- Valid authorization
- Business rule validation

NEGATIVE:
- Invalid account ID
- Missing headers
- Invalid headers
- Invalid dates
- Expired tokens
- Unauthorized access
- Cross-customer access
- Empty responses
- Downstream failures
- Timeout handling
- Retry handling
- 500/502/503 errors

SCHEMA:
- Required fields
- Optional fields
- Datatype validation
- Enum validation
- Nested objects
- Empty arrays
- Backward compatibility

TECHNICAL:
- Correlation IDs
- x-fapi-interaction-id propagation
- Logging validation
- Idempotency
- Retry behavior
- Parallel execution safety

Identify:
- Missing integration coverage
- Weak assertions
- Shallow validations
- Missing negative scenarios
- Production risks not covered

Generate output in this format:

1. APIs Covered

2. Integration Coverage Table

| API | Positive | Negative | Schema | Technical | Missing |
|-----|----------|-----------|---------|------------|---------|

3. Missing Negative Scenarios

4. Missing Schema Validation

5. Missing Technical Validation

6. Weak Assertions

7. High-Risk Production Gaps

8. Recommended Additional Integration Tests

9. Final Verdict
- Is integration coverage sufficient?
- What risks can escape to production?
- What should be added immediately?

Be extremely critical and think like a production incident investigator.


#####both####
Compare these two analyses:

1. Journey Test Analysis
2. Integration Test Analysis

Your goal:
- Identify validations incorrectly placed in journey tests
- Identify missing integration coverage
- Identify duplicated validations
- Identify high-risk gaps

Journey tests should:
- Validate only critical business flows
- Stay lightweight
- Avoid deep technical validation

Integration tests should:
- Handle detailed validation
- Handle negative scenarios
- Handle schema validation
- Handle resiliency testing

Generate:

1. Coverage Comparison Matrix

| Flow/API | Journey Coverage | Integration Coverage | Missing | Recommendation |

2. Validations To Move From Journey → Integration

3. Missing Integration Scenarios

4. Journey Test Simplification Recommendations

5. High-Risk Production Gaps

6. Final Architecture Recommendation

7. Final Verdict

