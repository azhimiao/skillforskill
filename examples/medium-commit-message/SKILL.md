---
name: medium-commit-message
description: >-
  Generate conventional commit messages from staged git diffs. Use when author asks for a
  commit message, help writing a commit, or review before git commit.
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: Requires git; code_exec for git only, no push
---

# Medium Commit Message

## Quick Start

1. RUN `git status` and `git diff --staged` in repo_path
2. PARSE diff into changed files and change summary
3. CLASSIFY type as feat, fix, docs, test, refactor, or chore
4. GENERATE subject line max 72 chars in conventional format
5. VALIDATE imperative mood and optional body explaining why

## Workflow

### Step 1
RUN `git status` and `git diff --staged` in repo_path

### Step 2
PARSE diff into changed files and change summary

### Step 3
CLASSIFY type as feat, fix, docs, test, refactor, or chore

### Step 4
GENERATE subject line max 72 chars in conventional format

### Step 5
VALIDATE imperative mood and optional body explaining why

### Decision logic

```
IF no staged changes → ASK author to git add; STOP
IF not a git repo → REPORT F2; STOP
IF diff lines > 500 → SUMMARIZE by directory; ASK author for focus
IF type unclear → default chore; note in Rationale
```

## Inputs

**Required**

- repo_path: path — git repository — validation: contains .git

**Optional**

- scope: string — commit scope override — default: inferred from diff paths

## Outputs

Profile: `narrative`

Deliver with headings: `# Summary`, `# Details`, `# Next Steps`.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| code_exec | git status, git diff --staged | read-only git |
| ask_user | Stage files or narrow large diffs | when blocked |

## Sub-skills

- **S1 read-staged-diff** — Retrieve staged diff text
- **S2 classify-change** — Determine commit type and scope
- **S3 compose-message** — Format conventional commit message

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | git diff --staged empty | ask author to run git add |
| F2 | git command fails with not a repository | report path; suggest git init |
| F3 | diff exceeds 500 lines | summarize by directory; ask focus area |

## Verification

| Test | Expected |
|------|----------|
| Test 1: staged feat diff | feat(scope): subject |
| Test 2: empty staged | ask to stage |
| Test 3: docs-only diff | docs: subject |

## Additional Resources

- [IR source](references/ir.md)
