## Finding classification and evidence

Every finding must have one of these statuses:

CONFIRMED_DEFECT
The behaviour was reproduced using repository evidence, Helm rendering,
linting, policy validation, schema validation, or another deterministic check.

POTENTIAL_RISK
The configuration appears risky, but no organisation policy or deterministic
failure proves that it is incorrect.

NEEDS_CLARIFICATION
Repository evidence is insufficient and expected behaviour depends on
DevOps/development intent.

NOT_VALIDATED
The required validation tool, policy, environment, or dependency was not
available.

For every CONFIRMED_DEFECT provide:

Status:
Severity:
Finding:
Evidence:
Source file:
Relevant configuration:
Validation command:
Observed result:
Expected result:
Impact:
Recommended action:

Do not mark a check as FAIL merely because a tool such as Conftest,
kubeconform, kubectl, or oc is unavailable.

Use NOT_VALIDATED instead.

Overall verdict rules:

FAIL
Use only when at least one Critical/High confirmed defect exists or a mandatory
validation actually failed.

NEEDS_REVIEW
Use when findings are potential risks, clarification is required, or important
validation could not be executed.

PASS
Use only when required validations completed successfully and no confirmed
blocking defects were found.


## Helm datatype and boolean validation

Helm values are type-sensitive.

For boolean-like configuration, explicitly validate the difference between:

--set feature=false

and:

--set-string feature=false

A non-empty string such as "false" is truthy when evaluated directly by Go
templates.

Identify values used in:

{{ if .Values.* }}
{{ if not .Values.* }}

and verify their expected datatype.

Check whether values.schema.json exists.

If values.schema.json exists:
validate required fields, boolean/string/number types and allowed values.

If it does not exist:
report whether important configuration relies on implicit Helm typing and
recommend schema validation where appropriate.

Do not automatically classify the absence of values.schema.json as a defect.


## Required-value contract validation

Identify values that are required for a usable deployment.

Do not rely only on whether Helm successfully renders.

For important deployment values, test whether empty or missing values are
silently accepted.

Examples may include:

IMAGE
SERVICE_ACCOUNT
NAMESPACE
DOMAIN
ENVIRONMENT
route hostnames
configuration-file paths

Discover the actual required values from the current project rather than
hardcoding these names globally.

Use read-only negative rendering where possible.

Example:

helm template qa-test <chart> --set SOME_REQUIRED_VALUE=

If an operationally mandatory value renders successfully as empty, report:

Missing required-value guard

Recommend one of:

Helm required function
values.schema.json required property
explicit template fail condition
organisation policy validation


## Environment matrix validation

Discover all environment values files.

Render each environment independently.

Create an environment comparison covering:

default
acceptance
union
rehearsal
production

or the environments actually present in the repository.

Compare important effective configuration including:

image
replicas
environment identifiers
NODE_ENV/runtime mode
Vault configuration
routes
resources
service accounts
feature toggles
mock configuration

Flag lower-environment/default values leaking into higher environments.

Example:

NODE_ENV unexpectedly resolving to dev in rehearsal

Classify this as NEEDS_CLARIFICATION unless project evidence proves it is
incorrect.


## Migration baseline discovery

When the user says the work is a migration, do not conclude that migration
comparison is unavailable merely because the old files are absent from the
working tree.

Use read-only Git investigation when appropriate:

git status
git branch
git diff --name-status <base>...HEAD
git diff <base>...HEAD
git show <base>:<path>

Try to identify the pre-migration implementation from:

target/base branch
Git history
deleted files
renamed files

For DeploymentConfig-to-Helm migration, compare old effective behaviour against
the new rendered Helm configuration.

If the correct baseline branch cannot be determined, ask for it and report:

Migration comparison: NOT_VALIDATED

Do not report:

Migration review: No

simply because the old DeploymentConfig is absent from the current branch.


## Raw deployment artifact discovery

Do not restrict validation to files inside the Helm chart.

Search for deployment-related artifacts outside the chart, including:

raw Kubernetes/OpenShift YAML
WireMock manifests
shell scripts
Jenkins files
route scripts
environment substitution files
deployment helper scripts

For raw manifests check for:

unresolved ${VARIABLE} placeholders
empty mandatory values
status sections committed into apply manifests
latest/unpinned images
resources missing
probes missing
unused volumes
invalid arguments
imperatively created infrastructure
configuration not managed by Helm

Clearly state:

Inside Helm chart

or:

Outside Helm chart

for each finding.


## Upgrade-safety validation

Review Deployment selectors and resource identity for upgrade safety.

Check whether volatile values are used in immutable selectors.

Pay particular attention to labels containing:

version
patch version
build number
image tag
release-specific values

If a changing value is part of:

spec.selector.matchLabels

compare it with:

spec.template.metadata.labels

and assess whether an upgrade using the same Deployment name can fail.

Do not automatically classify version labels as wrong when they are only
informational pod labels.


## Sensitive configuration detection

Inspect configuration keys and destinations without displaying secret values.

Treat names suggesting sensitive information as indicators, including:

TOKEN
PASSWORD
SECRET
API_KEY
CREDENTIAL

If such a value is rendered into:

ConfigMap
plain environment configuration
non-secret YAML

flag it for review.

Never output the actual value.

Recommend Secret/Vault handling when appropriate.


## Configuration usage analysis

Cross-check values defined in values files against their usage in templates and
deployment scripts.

Report:

defined and used
defined but apparently unused
referenced but not defined
environment-specific override unused
hardcoded value overriding configurable value

Classify unused configuration as a warning unless it creates runtime impact.


## Image reproducibility checks

Identify mutable image references such as:

latest

and review ImagePullPolicy behaviour.

Treat mutable image references as deployment reproducibility risks unless
organisation policy explicitly prohibits them.

Do not automatically classify them as defects without policy evidence.


## Resource sanity analysis

Validate resource quantity syntax when a schema validator is available.

Separately identify suspicious request/limit ratios.

Example:

request: 100m
limit: 2000m

Do not assume a ratio is invalid unless organisation policy defines a limit.

Report unusual ratios as POTENTIAL_RISK and ask whether they are intentional.


## Negative-render test matrix

When safe, generate temporary read-only Helm render tests without modifying the
repository.

Prioritise:

boolean value vs string boolean
required value missing
required value empty
wrong datatype
invalid resource quantity
environment override missing
conditional branch true
conditional branch false
invalid mock/test configuration

Use temporary output and remove it after analysis.

Never deploy the generated manifests.


## Reusable learning candidate quality

For every reusable learning candidate provide:

Candidate:
Evidence:
Why reusable:
Projects affected:
Confidence:
Proposed skill rule:
Suggested test:
Suggested destination:

SKILL.md
references/approved-patterns.md
or
references/test-scenarios.md

Do not automatically modify the shared skill.

A learning should normally be promoted only after human review.

Prefer learnings that:

apply across multiple services
represent a recurring defect class
improve deterministic validation
reduce false positives

Do not store project-specific secrets, URLs, credentials or temporary incident
details as reusable learning.
