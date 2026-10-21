# Helm QA Verifier — Office Laptop Setup Guide

This guide sets up the reusable `helm-qa-verifier` GitHub Copilot Agent Skill on a Mac office laptop so it can be used across multiple projects in VS Code.

> **Important security note**
>
> Use this only if your company policy allows access to your personal GitHub repository from the office laptop.
> Do not copy internal company URLs, source code, secrets, credentials, screenshots, or proprietary policies into the public repository.
> Keep the public skill generic. Let it inspect project-specific rules only inside the office repository.

---

## Target setup

```text
Personal GitHub
meghashyamnb/GPT-shyam-prompt
└── skills/
    └── helm-qa-verifier/
        └── SKILL.md
              │
              │ install
              ▼
Office Mac
~/.copilot/skills/
└── helm-qa-verifier/
    └── SKILL.md
              │
              ▼
VS Code + GitHub Copilot Agent
├── Office Project A
├── Office Project B
└── Office Project C
```

The personal skill location `~/.copilot/skills` is available across projects.

---

# PART 1 — Before using the office laptop

## Step 1 — Confirm the skill exists in your GitHub repository

Open:

```text
https://github.com/meghashyamnb/GPT-shyam-prompt
```

The repository should contain:

```text
skills/
└── helm-qa-verifier/
    └── SKILL.md
```

If it does not exist yet, create it in GitHub with this path:

```text
skills/helm-qa-verifier/SKILL.md
```

The file must be named exactly:

```text
SKILL.md
```

The top of the file must contain YAML frontmatter similar to:

```yaml
---
name: helm-qa-verifier
description: Review Helm charts, Kubernetes/OpenShift deployment configuration, and DeploymentConfig-to-Helm migrations from a QA and deployment-safety perspective.
---
```

The `name` should match the directory name:

```text
helm-qa-verifier
```

---

# PART 2 — Office laptop prerequisites

## Step 2 — Open Terminal

On Mac:

```text
Command + Space
```

Search:

```text
Terminal
```

Open it.

---

## Step 3 — Check GitHub CLI

Run:

```bash
gh --version
```

### Expected

You should see a GitHub CLI version.

For the `gh skill` commands, use GitHub CLI **2.90.0 or later**.

Also check whether the skill command exists:

```bash
gh skill --help
```

If this works, continue to **Step 4**.

If `gh` is missing or `gh skill` is unavailable, use **PART 4 — Manual installation fallback** below.

> Do not install or upgrade software on the office laptop unless company policy allows it.

---

## Step 4 — Check GitHub authentication

Run:

```bash
gh auth status
```

If already authenticated and allowed by company policy, continue.

If authentication is required:

```bash
gh auth login
```

Follow the GitHub prompts.

> If your organisation does not allow signing into a personal GitHub account on the office laptop, do not bypass that restriction. Use an approved internal repository or the manual method only if public GitHub access itself is allowed.

---

# PART 3 — Preferred installation using `gh skill`

## Step 5 — Preview the skill before installing

Run:

```bash
gh skill preview meghashyamnb/GPT-shyam-prompt helm-qa-verifier
```

Read the output.

Confirm that:

- the skill name is `helm-qa-verifier`
- it contains only generic Helm/Kubernetes/QA instructions
- it contains no unexpected scripts
- it contains no internal company information

Do not continue if the content is different from what you expect.

---

## Step 6 — Install the skill at user scope

Run:

```bash
gh skill install meghashyamnb/GPT-shyam-prompt helm-qa-verifier \
  --agent github-copilot \
  --scope user
```

Why `--scope user`?

Because this installs the skill in your user-level Copilot area so it can be used across multiple projects instead of only the current repository.

---

## Step 7 — Verify installation

Run:

```bash
gh skill list --agent github-copilot --scope user
```

You should see:

```text
helm-qa-verifier
```

Also verify the local folder:

```bash
ls -la ~/.copilot/skills/helm-qa-verifier
```

Expected:

```text
SKILL.md
```

You can inspect it:

```bash
cat ~/.copilot/skills/helm-qa-verifier/SKILL.md
```

---

# PART 4 — Manual installation fallback

Use this only if `gh skill` is unavailable but your office policy allows access to the public repository.

## Option A — Clone and copy

Run:

```bash
cd ~
```

Clone the repository:

```bash
git clone https://github.com/meghashyamnb/GPT-shyam-prompt.git
```

Create the Copilot skills folder:

```bash
mkdir -p ~/.copilot/skills
```

Copy the skill:

```bash
cp -R ~/GPT-shyam-prompt/skills/helm-qa-verifier ~/.copilot/skills/
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

## Option B — If the repository was already cloned

Go to the cloned repository:

```bash
cd /path/to/GPT-shyam-prompt
```

Then run:

```bash
mkdir -p ~/.copilot/skills
cp -R skills/helm-qa-verifier ~/.copilot/skills/
```

Verify:

```bash
ls -la ~/.copilot/skills/helm-qa-verifier
```

---

# PART 5 — VS Code setup

## Step 8 — Open VS Code

Open any office project in VS Code.

---

## Step 9 — Reload VS Code

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

## Step 10 — Confirm Agent Skills are visible

Open GitHub Copilot Chat.

Use:

```text
Command + Shift + P
```

Search for:

```text
Chat: Configure Skills
```

or open the Copilot/Agent customization view and find:

```text
Skills
```

Confirm that:

```text
helm-qa-verifier
```

is visible.

If it is not visible, see the troubleshooting section below.

---

# PART 6 — First safe test

## Step 11 — Use a read-only prompt first

Open a Helm project in VS Code.

In Copilot Agent mode, paste:

```text
Use the /helm-qa-verifier skill.

Inspect this repository and identify:
- Helm chart location
- Chart.yaml
- values.yaml
- environment-specific values files
- templates
- Deployment configuration
- Service/Route configuration
- ConfigMap and Secret templates
- Conftest/OPA/Rego policy configuration

Do not modify any files.
Do not deploy anything.
Do not run any commands yet.

First tell me:
1. what files you found,
2. what you intend to validate,
3. what commands you would like to run.
```

### Expected result

Copilot should:

- identify the Helm chart
- explain what it wants to validate
- avoid changing files
- avoid deployment
- ask before running shell commands

---

# PART 7 — Run Helm validation

## Step 12 — Check whether Helm CLI is available

In Terminal:

```bash
helm version
```

If Helm is available, continue.

If it is not installed, the skill can still review files, but it cannot execute actual Helm lint/render validation.

Do not install Helm unless permitted by company policy.

---

## Step 13 — Let Copilot run read-only Helm checks

Paste:

```text
Use the /helm-qa-verifier skill.

Perform a read-only Helm QA review.

You may run:
- helm lint
- helm template

Do not:
- helm install
- helm upgrade
- helm uninstall
- kubectl apply
- oc apply
- modify files
- expose Secret values

Review the rendered Deployment and report:
- Helm lint result
- Helm rendering result
- critical issues
- warnings
- missing configuration
- environment-specific risks
- recommended negative tests
```

If Copilot asks permission to run commands, review the command before approving it.

Safe examples:

```bash
helm lint ./chart
```

```bash
helm template qa-test ./chart -f values.yaml --debug
```

Potentially unsafe commands that should NOT be approved for normal review:

```bash
helm install
helm upgrade
helm uninstall
kubectl apply
kubectl delete
oc apply
oc delete
```

---

# PART 8 — Conftest / OPA validation

## Step 14 — Check whether Conftest exists

Run:

```bash
conftest --version
```

If available, ask Copilot:

```text
Use the /helm-qa-verifier skill.

Render the Helm chart using the correct environment values and run Conftest against the rendered manifest if the repository configuration supports it.

Do not deploy anything.

Report:
- policies discovered
- manifest validated
- policy PASS/FAIL
- violated rules
- exact configuration location
- recommended negative tests
```

If Conftest is not installed, the skill should report:

```text
Policy validation: NOT RUN
```

rather than trying to install it automatically.

---

# PART 9 — Use it for your Helm migration

For a DeploymentConfig-to-Helm migration, paste:

```text
Use the /helm-qa-verifier skill.

This project is migrating from the previous DeploymentConfig/deployment setup to Helm.

Compare old and new behaviour.

Focus on:
- replicas
- image and tag
- labels
- annotations
- environment variables
- resource requests and limits
- readiness/liveness/startup probes
- ConfigMaps
- Secrets
- Vault behaviour
- Services
- Routes
- deployment strategy
- canary behaviour
- traffic switching
- rollback
- environment-specific values
- Conftest/OPA policy validation

Do not compare syntax only.
Compare the effective deployment behaviour.

Return:
1. expected differences,
2. unexpected differences,
3. high-risk regressions,
4. negative test cases,
5. questions that require DevOps clarification.
```

---

# PART 10 — Use it in multiple projects

Once installed under:

```text
~/.copilot/skills/helm-qa-verifier
```

you do NOT need to copy the skill into every project.

Open another project in VS Code and ask:

```text
Use the /helm-qa-verifier skill to review this Helm project.
```

The same personal skill should be available.

---

# PART 11 — Updating the skill later

If you update `SKILL.md` in:

```text
meghashyamnb/GPT-shyam-prompt
```

and you installed using `gh skill`, update it with:

```bash
gh skill update helm-qa-verifier
```

If needed, update all installed skills:

```bash
gh skill update --all
```

Then reload VS Code:

```text
Command + Shift + P
```

Run:

```text
Developer: Reload Window
```

---

# PART 12 — Updating when using the manual clone method

If you used the clone/copy approach:

```bash
cd ~/GPT-shyam-prompt
git pull
```

Then replace the installed skill:

```bash
rm -rf ~/.copilot/skills/helm-qa-verifier
cp -R ~/GPT-shyam-prompt/skills/helm-qa-verifier ~/.copilot/skills/
```

Reload VS Code afterward.

---

# PART 13 — Troubleshooting

## Problem 1 — `gh: command not found`

GitHub CLI is not installed.

Use the manual installation method if allowed, or ask your company support team whether GitHub CLI can be installed.

---

## Problem 2 — `unknown command "skill" for "gh"`

Your GitHub CLI version may be too old.

Check:

```bash
gh --version
```

`gh skill` currently requires GitHub CLI 2.90.0 or later.

If upgrades are blocked by office policy, use the manual installation method.

---

## Problem 3 — Skill is installed but VS Code does not show it

Check:

```bash
ls -la ~/.copilot/skills/helm-qa-verifier
```

Confirm:

```text
SKILL.md
```

exists.

Check the first lines:

```bash
head -10 ~/.copilot/skills/helm-qa-verifier/SKILL.md
```

Confirm:

```yaml
---
name: helm-qa-verifier
description: ...
---
```

Then reload VS Code:

```text
Command + Shift + P
Developer: Reload Window
```

Also search:

```text
Chat: Configure Skills
```

and verify the skill is enabled.

---

## Problem 4 — Copilot does not automatically use the skill

Explicitly call it:

```text
Use the /helm-qa-verifier skill to review this chart.
```

The description controls automatic skill selection, so explicit invocation is useful while testing.

---

## Problem 5 — `helm` not found

Check:

```bash
which helm
```

If nothing is returned, Helm is not available in your shell.

The skill can still review source files, but it cannot run:

```bash
helm lint
helm template
```

Do not install Helm unless company policy permits it.

---

## Problem 6 — `conftest` not found

Check:

```bash
which conftest
```

If unavailable, continue with Helm validation and report:

```text
Policy validation: NOT RUN
```

Do not automatically install Conftest.

---

# PART 14 — Security checklist

Before using this setup on an office project, confirm:

- [ ] Company policy allows GitHub Copilot Agent mode.
- [ ] Company policy allows access to your personal/public GitHub repository.
- [ ] The public skill contains no company-specific information.
- [ ] No production secrets are copied into prompts.
- [ ] Secret values are never displayed or decoded.
- [ ] You review shell commands before approving them.
- [ ] `helm install/upgrade/uninstall` are not used for QA review.
- [ ] `kubectl apply/delete` are not used for QA review.
- [ ] `oc apply/delete` are not used for QA review.
- [ ] The skill stays read-only unless you explicitly request changes.

---

# PART 15 — Quick setup commands

If everything is already available, these are the main commands:

```bash
# 1. Check GitHub CLI
gh --version

# 2. Check authentication
gh auth status

# 3. Preview skill
gh skill preview meghashyamnb/GPT-shyam-prompt helm-qa-verifier

# 4. Install for GitHub Copilot across projects
gh skill install meghashyamnb/GPT-shyam-prompt helm-qa-verifier \
  --agent github-copilot \
  --scope user

# 5. Verify installation
gh skill list --agent github-copilot --scope user

# 6. Verify local files
ls -la ~/.copilot/skills/helm-qa-verifier

# 7. Check Helm
helm version

# 8. Check Conftest if needed
conftest --version
```

Then reload VS Code and test with:

```text
Use the /helm-qa-verifier skill.

Inspect this repository.
Do not modify anything and do not deploy anything.

First tell me the Helm chart, values files, templates and policy configuration you found, and what you intend to validate.
```

---

# PART 16 — Daily use prompt

After setup, this can be your standard prompt:

```text
Use the /helm-qa-verifier skill.

Review the current Helm changes from a QA perspective.

Perform only read-only checks.

Validate:
- helm lint
- rendered Helm manifests
- values and environment overrides
- Deployment configuration
- selectors/labels
- annotations
- resources
- probes
- ConfigMaps and Secret references
- conditional templates
- Conftest/OPA policies if available
- old-vs-new migration behaviour where applicable

Do not deploy anything.
Do not modify files.
Do not expose secret values.

Give me:
1. PASS/FAIL/NOT RUN for each validation,
2. critical findings,
3. warnings,
4. migration differences,
5. recommended negative tests,
6. questions for DevOps only where repository evidence is insufficient.
```

---

# Final expected result

After setup, your machine should have:

```text
~/.copilot/skills/
└── helm-qa-verifier/
    └── SKILL.md
```

And the skill should be reusable from any VS Code project with:

```text
Use the /helm-qa-verifier skill ...
```
