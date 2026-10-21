# Helm QA Verifier — Office-Only Setup Guide

This guide is designed for the following setup:

```text
ChatGPT / Personal GitHub
        │
        │ copy-paste only
        ▼
Office Laptop
        │
        ├── Office GitHub account only
        ├── Office VS Code
        ├── Office GitHub Copilot
        └── Office repositories only
```

## Important

Your personal GitHub repository is **NOT** used as the installation source.

It is only a place where you keep these instructions so you can copy them later.

All actual setup, storage, usage, and testing happens on the **office laptop using the official GitHub account**.

---

# 1. Final architecture

Use this model:

```text
PERSONAL SIDE
=============

ChatGPT
   ↓
Personal GitHub repo
(GPT-shyam-prompt)
   ↓
Only stores setup text / instructions
   ↓
COPY-PASTE


OFFICE SIDE
===========

Office Mac
   ↓
Official GitHub account
   ↓
VS Code + GitHub Copilot Agent
   ↓
Personal Copilot Skill on office laptop

~/.copilot/skills/
└── helm-qa-verifier/
    └── SKILL.md

   ↓

Works across:

Office Project A
Office Project B
Office Project C
Future Helm projects
```

No personal GitHub authentication is required on the office laptop.

---

# 2. Prerequisites on office laptop

Before starting, confirm that the office laptop already has:

- VS Code
- GitHub Copilot extension
- access to GitHub Copilot Agent mode
- official GitHub account signed in
- access to the office repositories

Optional but useful:

- Helm CLI
- Conftest
- OpenShift `oc`
- Git

Do not install any new software unless your organisation allows it.

---

# 3. Create the reusable skill directly on office laptop

Open Terminal on the office Mac.

Run:

```bash
mkdir -p ~/.copilot/skills/helm-qa-verifier
```

Create the skill file:

```bash
touch ~/.copilot/skills/helm-qa-verifier/SKILL.md
```

Verify:

```bash
ls -la ~/.copilot/skills/helm-qa-verifier
```

Expected:

```text
SKILL.md
```

---

# 4. Open the skill file in VS Code

If the `code` command works:

```bash
code ~/.copilot/skills/helm-qa-verifier/SKILL.md
```

If not:

1. Open VS Code.
2. Select **File → Open File**.
3. Go to your home directory.
4. If `.copilot` is hidden, press:

```text
Command + Shift + .
```

5. Open:

```text
.copilot/skills/helm-qa-verifier/SKILL.md
```

---

# 5. Paste this complete skill into SKILL.md

Copy everything below into:

```text
~/.copilot/skills/helm-qa-verifier/SKILL.md
```

```markdown
---
name: helm-qa-verifier
description: Review Helm charts, Kubernetes/OpenShift deployment configuration, CI/CD deployment changes, policy-as-code validation, and DeploymentConfig-to-Helm migrations from a QA and deployment-safety perspective.
---

# Helm QA Verifier

Act as a senior QA/SDET reviewing Helm, Kubernetes, OpenShift, CI/CD, and deployment-policy changes.

The objective is to identify:

- deployment risks
- configuration defects
- policy violations
- migration regressions
- environment-specific issues
- missing negative tests
- missing rollback/readiness/canary coverage

Do not approve a Helm chart only because the source template looks correct.

Prefer validating the final rendered Kubernetes/OpenShift manifests.

Do not modify files unless explicitly requested.

Do not deploy anything unless explicitly requested.

Do not expose Secret values.

---

## 1. Discover the deployment structure

First inspect the current repository.

Identify:

- Chart.yaml
- values.yaml
- environment-specific values files
- templates/deployment.yaml
- Service templates
- Route / Ingress templates
- ConfigMaps
- Secrets
- ServiceAccounts
- helpers.tpl
- deployment scripts
- Jenkins pipeline files
- Conftest configuration
- Rego policies
- policy.yaml
- central policy references
- old DeploymentConfig configuration if migration is involved

Identify the actual Helm chart root before running Helm commands.

If multiple Helm charts exist, report them first.

Do not guess which chart is in scope.

---

## 2. Helm lint validation

If Helm CLI is available, run:

helm lint <chart-path>

Report:

- PASS
- FAIL
- exact error
- affected file/template
- probable cause

A Helm lint failure must not be reported as a successful validation.

---

## 3. Render the Helm chart

If Helm is available, render the chart using:

helm template qa-test <chart-path> -f <values-file> --debug

Prefer reviewing the rendered manifests instead of only reviewing:

{{ .Values.xxx }}

or other Go-template syntax.

For environment-specific values, render the required environment separately.

Do not run:

helm install
helm upgrade
helm uninstall

during normal QA analysis.

---

## 4. Validate rendered Deployment configuration

For every rendered Deployment, inspect:

- apiVersion
- kind
- metadata.name
- namespace
- labels
- annotations
- spec.replicas
- selector.matchLabels
- pod-template labels
- pod-template annotations
- containers
- container names
- images
- image tags
- ports
- environment variables
- ConfigMap references
- Secret references
- resource requests
- resource limits
- readinessProbe
- livenessProbe
- startupProbe
- ServiceAccount
- volumes
- volume mounts
- deployment strategy

Verify that Deployment selectors match the pod-template labels.

Flag:

- missing values
- null values
- empty values
- unresolved Helm expressions
- suspicious hardcoded values
- incorrect references

---

## 5. Validate Helm values

Trace important rendered values back to their source.

Check:

- values missing from values.yaml
- environment-specific overrides
- conflicting defaults
- values declared but unused
- values referenced but not declared
- inconsistent variable names
- incorrect datatypes
- empty values
- null values
- unexpected hardcoded values

If multiple possible configuration sources conflict, do not guess.

Report:

NEEDS CLARIFICATION

and explain the conflict.

---

## 6. Conditional Helm logic

Identify conditional branches:

{{ if ... }}
{{ else }}
{{ end }}

For each important branch, identify the values needed to exercise both paths.

Example:

{{ if not .Values.vault.enabled }}

Test conceptually:

vault.enabled=false
→ Secret expected

vault.enabled=true
→ local Secret not expected

Check the rendered manifests for both cases where possible.

---

## 7. Secret and Vault safety

For Secret-related configuration:

Validate:

- Secret resource creation logic
- Secret name
- namespace
- references
- Vault-enabled behaviour
- Vault-disabled behaviour

Never:

- decode Secret.data
- expose Secret.data
- expose Secret.stringData
- print passwords
- print API keys
- print credentials
- print tokens

Mask sensitive data in reports.

---

## 8. Policy-as-code validation

Discover the actual policy mechanism first.

Look for:

- Conftest
- OPA
- Rego
- policy.yaml
- common policy repositories
- service-specific policy configuration
- Jenkins policy-validation stages

Determine whether validation runs against:

- Helm source
- values files
- rendered Kubernetes manifests

Do not assume.

If Conftest is installed and the policy location is known, run it against the rendered manifest.

Example:

conftest test <rendered-manifest>

Validate:

- compliant manifest passes
- non-compliant manifest fails
- failed rule is clearly identified
- required values are checked
- missing required fields are detected
- policy failure is expected to prevent deployment

Never invent company-specific policy rules.

Only use rules discovered from:

- current office repository
- current office documentation
- policy configuration
- user-provided project context

---

## 9. Kubernetes/OpenShift validation

When reviewing the rendered manifest, consider Kubernetes/OpenShift correctness separately from Helm correctness.

Differentiate:

1. Helm-template error
2. Kubernetes schema/configuration error
3. organisation policy error
4. runtime deployment error
5. application-health failure

If kubeconform or another approved schema validator is already installed, it may be used.

Do not automatically install new tools.

---

## 10. Negative test generation

For every important configuration or policy, consider relevant tests for:

- missing field
- empty field
- null
- wrong datatype
- invalid value
- wrong casing
- leading/trailing spaces
- wrong YAML nesting
- wrong annotation location
- invalid environment override
- selector/label mismatch
- missing resource request
- missing resource limit
- invalid CPU/memory quantity
- missing readiness probe
- invalid readiness path
- invalid readiness port
- invalid liveness configuration
- invalid ConfigMap reference
- invalid Secret reference
- unresolved Helm variable
- missing policy configuration
- conditional branch not covered

Do not blindly generate every possible permutation.

Prioritise tests based on deployment and production risk.

---

## 11. DeploymentConfig-to-Helm migration

When reviewing migration from old deployment configuration to Helm:

Do not compare syntax only.

Compare effective behaviour.

Check:

- replicas
- images
- tags
- environment variables
- labels
- annotations
- resources
- probes
- ConfigMaps
- Secrets
- Services
- Routes
- volumes
- readiness behaviour
- deployment strategy
- canary behaviour
- traffic switching
- rollback behaviour
- environment-specific configuration

Classify differences as:

- expected migration change
- unexpected difference
- high-risk regression
- needs clarification

---

## 12. CI/CD validation

Inspect the pipeline when available.

Determine the expected sequence.

Example:

Helm lint
→ Helm render
→ policy validation
→ deployment gate
→ OpenShift deployment

Check:

- where policy validation runs
- what input it validates
- what happens on failure
- whether deployment is blocked
- whether validation can be bypassed
- whether errors identify the root cause

Do not execute production deployment operations.

---

## 13. Canary / readiness / rollback testing

If the deployment supports old and new versions at the same time, review:

- old version remains healthy
- new version pods are created
- new version readiness is checked
- unready pods receive no traffic
- traffic weighting is correct
- canary commit is correct
- canary rollback is correct
- non-canary switching is correct
- rollback restores stable behaviour
- customer traffic is not sent to unhealthy pods

Ask for clarification if actual traffic percentages or rollback behaviour are not available in repository evidence.

---

## 14. Post-deployment recommendations

If deployment execution is in scope, recommend checking:

- Deployment created successfully
- expected replicas available
- pods Ready
- Service correct
- Route/Ingress correct
- ConfigMaps available
- Secret references valid
- no abnormal OpenShift events
- no CrashLoopBackOff
- no ImagePullBackOff
- application/API smoke test passes
- rollback capability works where relevant

Only run cluster commands when explicitly requested and authorised.

---

## 15. Risk classification

Use:

CRITICAL
- secret exposure
- deployment-gate bypass
- incorrect traffic routing
- broken rollback
- production deployment failure

HIGH
- unhealthy pods
- wrong environment config
- missing probes
- broken Service/Route
- incorrect resources
- failed policy enforcement

MEDIUM
- inconsistent config
- unclear defaults
- weak diagnostics
- missing negative tests

LOW
- maintainability/documentation issue with limited runtime impact

---

## 16. Safety rules

Never automatically run:

helm install
helm upgrade
helm uninstall

kubectl apply
kubectl delete

oc apply
oc delete

Never modify:

- production resources
- deployment pipelines
- repository files

unless explicitly requested.

Prefer read-only validation.

Ask before running commands if the command can change repository or cluster state.

---

## 17. Output format

Return:

# Helm QA Review

## Scope

Chart:
Environment:
Values file:
Migration review: Yes / No

## Validation

Helm lint:
PASS / FAIL / NOT RUN

Helm render:
PASS / FAIL / NOT RUN

Kubernetes/OpenShift validation:
PASS / FAIL / NOT RUN

Policy validation:
PASS / FAIL / NOT RUN

## Critical findings

For each:

- Finding
- Evidence
- Impact
- Recommended action

## Warnings

- Finding
- Impact

## Migration differences

For each:

- Old behaviour
- New behaviour
- Expected / Unexpected / Needs clarification
- Risk

## Recommended test scenarios

For each:

- Scenario
- Configuration/change
- Expected result
- Priority

## Questions for DevOps / Development

Only list questions that cannot be answered using current repository evidence.

## Overall assessment

PASS / FAIL / NEEDS REVIEW

Give a short reason for the decision.
```

Save the file.

---

# 6. Reload VS Code

Press:

```text
Command + Shift + P
```

Search:

```text
Developer: Reload Window
```

Run it.

---

# 7. Confirm the skill is available

Open GitHub Copilot Chat.

Use Agent mode.

Look for Skills / Agent customisations.

If available, confirm:

```text
helm-qa-verifier
```

is listed.

If it is not automatically visible, you can still explicitly instruct Copilot:

```text
Use the helm-qa-verifier skill.
```

---

# 8. First safe test in an office project

Open one office Helm repository.

Paste this into Copilot Agent:

```text
Use the helm-qa-verifier skill.

Inspect this repository.

Do not modify anything.
Do not deploy anything.
Do not run any shell command yet.

First identify:

- Helm chart
- Chart.yaml
- values files
- environment-specific values
- templates
- Deployment
- Service/Route
- ConfigMaps
- Secrets
- Jenkins/pipeline configuration
- Conftest/OPA/Rego configuration

Then tell me:

1. what you found,
2. what you intend to validate,
3. what read-only commands you want to run.
```

Expected:

Copilot should first inspect and explain.

It should not deploy or change files.

---

# 9. Check Helm CLI

In office Terminal:

```bash
helm version
```

If Helm exists, continue.

If Helm does not exist:

- the skill can still inspect files
- `helm lint` cannot be run
- `helm template` cannot be run

Do not install Helm unless the company allows it.

---

# 10. Run first Helm QA review

Use this prompt:

```text
Use the helm-qa-verifier skill.

Perform a read-only QA review of the current Helm chart.

You may run:

- helm lint
- helm template

Do not run:

- helm install
- helm upgrade
- helm uninstall
- kubectl apply
- kubectl delete
- oc apply
- oc delete

Do not modify files.

Do not expose Secret values.

Report:

- Helm lint result
- Helm render result
- critical issues
- warnings
- missing values
- resource/probe issues
- environment-specific risks
- recommended negative tests
```

Review each terminal command before approving it.

---

# 11. Check Conftest

Run:

```bash
conftest --version
```

If available, you can ask:

```text
Use the helm-qa-verifier skill.

Render the current Helm chart using the appropriate non-production values.

Run Conftest against the rendered manifest using the policy configuration available in this repository/pipeline.

Do not deploy anything.

Report:

- policy source
- manifest validated
- PASS/FAIL
- violated rule
- affected YAML location
- recommended negative test
```

If Conftest is unavailable, report:

```text
Policy validation: NOT RUN
```

Do not install it automatically.

---

# 12. Use for your Helm migration

Use:

```text
Use the helm-qa-verifier skill.

This repository is migrating from the previous DeploymentConfig/deployment implementation to Helm.

Compare effective old and new deployment behaviour.

Focus on:

- replicas
- image/tag
- labels
- annotations
- environment variables
- CPU/memory requests and limits
- readiness/liveness/startup probes
- ConfigMaps
- Secrets
- Vault behaviour
- Service
- Route
- deployment strategy
- canary deployment
- traffic weighting
- readiness behaviour
- rollback
- environment-specific values
- policy validation

Do not compare syntax only.

Return:

1. expected differences,
2. unexpected differences,
3. high-risk regressions,
4. negative tests,
5. unanswered questions for DevOps.
```

---

# 13. Use the skill across multiple office projects

Because the skill is here:

```text
~/.copilot/skills/helm-qa-verifier/SKILL.md
```

it is a user-level skill on your office laptop.

You do not need to copy the skill into each service repository.

Open another project and use:

```text
Use the helm-qa-verifier skill to review this Helm project.
```

---

# 14. Optional — create an official office GitHub repository for backup/versioning

This step is OPTIONAL.

The skill already works locally without any repository.

If you want to version-control the skill using your official GitHub account, create an office-private/internal repository.

Example:

```text
copilot-skills
```

or:

```text
qa-agent-skills
```

Recommended structure:

```text
qa-agent-skills/
└── skills/
    └── helm-qa-verifier/
        └── SKILL.md
```

On the office laptop:

```bash
mkdir -p ~/qa-agent-skills/skills/helm-qa-verifier
```

Copy the working skill:

```bash
cp ~/.copilot/skills/helm-qa-verifier/SKILL.md \
  ~/qa-agent-skills/skills/helm-qa-verifier/SKILL.md
```

Then initialise Git if required:

```bash
cd ~/qa-agent-skills
git init
```

Add:

```bash
git add skills/helm-qa-verifier/SKILL.md
```

Commit:

```bash
git commit -m "Add reusable Helm QA verifier Copilot skill"
```

Then connect it only to the **official office GitHub repository**.

Do not push this skill to a personal repository from the office laptop.

---

# 15. Recommended office setup

Your final office setup should look like:

```text
Office Mac

~/.copilot/
└── skills/
    └── helm-qa-verifier/
        └── SKILL.md
```

Optional internal backup:

```text
Official Office GitHub

qa-agent-skills/
└── skills/
    └── helm-qa-verifier/
        └── SKILL.md
```

And your work repositories remain separate:

```text
Office repos
├── service-a
├── service-b
├── service-c
└── service-d
```

The user-level skill can inspect whichever project you currently open in VS Code.

---

# 16. Security rules for office use

Do not copy office information back to your personal repository.

Do not copy:

- source code
- internal URLs
- Confluence pages
- Bitbucket URLs
- Jenkins URLs
- proprietary Rego policies
- service names if confidential
- production values
- screenshots
- architecture diagrams
- secrets
- credentials
- access tokens

The personal repository is only a **setup-instruction notebook**.

The office copy of the skill can read office repository information locally through Copilot, subject to your organisation's Copilot configuration and policies.

---

# 17. Daily-use prompt

Use this every time:

```text
Use the helm-qa-verifier skill.

Review the current Helm changes from a QA perspective.

Perform read-only analysis.

Validate:

- Helm structure
- helm lint
- rendered Helm manifests
- values and environment overrides
- Deployments
- selectors/labels
- annotations
- resource requests/limits
- probes
- ConfigMaps
- Secret references
- conditional templates
- Conftest/OPA policy integration if available
- CI/CD deployment gate
- old-vs-new migration behaviour where applicable
- canary/readiness/rollback risks where applicable

Do not deploy.
Do not modify files.
Do not expose secrets.

Give me:

1. PASS / FAIL / NOT RUN for each validation,
2. critical findings,
3. warnings,
4. migration differences,
5. recommended negative tests,
6. questions for DevOps only when repository evidence is insufficient.
```

---

# 18. Quick command checklist

Run on the office laptop:

```bash
# Create skill
mkdir -p ~/.copilot/skills/helm-qa-verifier

# Create SKILL.md
touch ~/.copilot/skills/helm-qa-verifier/SKILL.md

# Open in VS Code
code ~/.copilot/skills/helm-qa-verifier/SKILL.md

# Verify
ls -la ~/.copilot/skills/helm-qa-verifier

# Check Helm
helm version

# Check Conftest
conftest --version
```

Then reload VS Code:

```text
Command + Shift + P
Developer: Reload Window
```

And start with:

```text
Use the helm-qa-verifier skill.

Inspect this repository but do not modify or deploy anything.

Tell me what you found and what you want to validate first.
```

---

# Final setup

There is no personal-account-to-office-account installation flow.

Use this:

```text
ChatGPT
   ↓
Copy setup text
   ↓
Office laptop
   ↓
Create ~/.copilot/skills/helm-qa-verifier/SKILL.md
   ↓
Paste skill
   ↓
Reload VS Code
   ↓
Use with official Copilot account
   ↓
Use across all office projects
```

Optional:

```text
Office laptop skill
   ↓
Commit a copy to an approved private/internal office GitHub repository
```

That office repository becomes the official source of truth if your team later wants to maintain or share the skill.
