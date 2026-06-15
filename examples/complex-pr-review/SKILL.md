---
name: complex-pr-review
description: >-
  Review pull requests for correctness, security, and maintainability using team standards.
  Use when author asks for PR review, code review before merge, or review checklist for a
  pull request.
disable-model-invocation: true
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: moderate tool calls; prefer scripts for repeatable checks; read-only git; no merge or push without explicit approval
---

# Complex Pr Review

## Quick Start

1. RUN scripts/fetch_pr.sh with pr_number to get diff and file list
2. READ references/standards.md for review criteria
3. RUN scripts/check_diff.py on changed files
4. COMPARE diff hunks to standards; LIST findings by severity
5. GENERATE review at assets/review-output.md with summary and next steps

## Workflow

### Step 1
RUN scripts/fetch_pr.sh with pr_number to get diff and file list

### Step 2
READ references/standards.md for review criteria

### Step 3
RUN scripts/check_diff.py on changed files

### Step 4
COMPARE diff hunks to standards; LIST findings by severity

### Step 5
GENERATE review at assets/review-output.md with summary and next steps

### Step 6
VALIDATE review includes Critical, Suggestion, and Nice-to-have sections

### Decision logic

```
IF gh not installed → FALLBACK git fetch and local branch diff
IF check_diff.py fails → REPORT script error; continue manual review
IF focus=security → FILTER findings to security only
IF zero changed files → REPORT F3; STOP
IF confidence < 0.4 on security finding → ESCALATE to author
```

## Inputs

**Required**

- pr_number: number — pull request identifier — validation: positive integer
- repo_path: path — repository root — validation: git repo with gh or git remote

**Optional**

- focus: enum — security | performance | style | full — default: full
- standards_file: path — override standards — default: references/standards.md

## Outputs

Profile: `hybrid`

Return artifacts plus a narrative summary.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| code_exec | fetch_pr.sh, check_diff.py, git | read-only unless author approves |
| file_read | standards.md, changed source files | required |
| file_write | assets/review-output.md | review artifact |
| sub_skill_call | medium-commit-message | suggest commit message fixes |
| ask_user | Clarify PR number or focus | when inputs missing |

## Sub-skills

- **S1 fetch-pr** — Fetch PR diff and metadata
- **S2 run-checks** — Run automated review script
- **S3 analyze-diff** — Review diff against standards
- **S4 compose-review** — Format review for author

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | fetch script exits 404 or unknown PR | ask author to verify pr_number |
| F2 | standards_file not readable | use built-in minimal checklist in workflow |
| F3 | zero changed files in PR | report empty PR; ask author to confirm |
| F4 | check_diff.py non-zero exit | log stderr; continue manual review |

## Verification

| Test | Expected |
|------|----------|
| Test 1: small docs PR | review with no critical findings |
| Test 2: missing pr_number | ask author |
| Test 3: focus=security | only security findings listed |

## Dependencies

- `medium-commit-message`

## Additional Resources

- [IR source](references/ir.md)
