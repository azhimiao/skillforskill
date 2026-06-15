complex-pr-review

---

# 0. Compilation Target

```yaml
deploy_to: examples/complex-pr-review/
host: any
invocation: manual
disable-model-invocation: true
output_profile: hybrid
```

---

# 1. Intent（意图）

## Goal
Review pull requests for correctness, security, and maintainability using team standards.

## Context
Author asks for PR review, code review before merge, or review checklist for a pull request.

## Constraints
- 时间：single session, 5-15 min per PR
- 成本：moderate tool calls; prefer scripts for repeatable checks
- 精度：human review required for final merge decision
- 工具限制：read-only git; no merge or push without explicit approval

---

# 2. Inputs（输入定义）

## Required Inputs
- pr_number: number — pull request identifier — validation: positive integer
- repo_path: path — repository root — validation: git repo with gh or git remote

## Optional Inputs
- focus: enum — security | performance | style | full — default: full
- standards_file: path — override standards — default: references/standards.md

---

# 3. Outputs（输出定义）

**Profile:** hybrid

Return narrative review plus JSON artifact list with findings file path.

---

# 4. Skill Decomposition（能力拆解）

## S1: fetch-pr
- Goal: Fetch PR diff and metadata
- Inputs: pr_number, repo_path
- Outputs: diff_text, pr_title, changed_files
- Primary verb: run

## S2: run-checks
- Goal: Run automated review script
- Inputs: repo_path, changed_files
- Outputs: check_report
- Primary verb: run

## S3: analyze-diff
- Goal: Review diff against standards
- Inputs: diff_text, standards_file, focus
- Outputs: findings_list
- Primary verb: compare

## S4: compose-review
- Goal: Format review for author
- Inputs: findings_list, check_report
- Outputs: review_markdown
- Primary verb: generate

---

# 5. Execution Plan（执行流程）

1. RUN scripts/fetch_pr.sh with pr_number to get diff and file list
2. READ references/standards.md for review criteria
3. RUN scripts/check_diff.py on changed files
4. COMPARE diff hunks to standards; LIST findings by severity
5. GENERATE review at assets/review-output.md with summary and next steps
6. VALIDATE review includes Critical, Suggestion, and Nice-to-have sections

---

# 6. Decision Logic（决策系统）

```
IF gh not installed → FALLBACK git fetch and local branch diff
IF check_diff.py fails → REPORT script error; continue manual review
IF focus=security → FILTER findings to security only
IF zero changed files → REPORT F3; STOP
IF confidence < 0.4 on security finding → ESCALATE to author
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| code_exec | fetch_pr.sh, check_diff.py, git | read-only unless author approves |
| file_read | standards.md, changed source files | required |
| file_write | assets/review-output.md | review artifact |
| sub_skill_call | medium-commit-message | suggest commit message fixes |
| ask_user | Clarify PR number or focus | when inputs missing |

---

# 8. Memory Model（记忆结构）

## Skill memory (file-backed)
Store recurring findings patterns in references/learning.md with author consent.

## Session memory
Pass changed_files from S1 to S2 and diff_text from S1 to S3.

---

# 9. Evaluation（评估标准）

## L1 Task (before stable)
- Test 1: small docs PR → review with no critical findings
- Test 2: missing pr_number → ask author
- Test 3: focus=security → only security findings listed

See references/eval.md for full cases.

---

# 10. Failure Modes（失败模式）

## F1: pr-not-found
- Signal: fetch script exits 404 or unknown PR
- Recovery: ask author to verify pr_number
- Severity: block

## F2: standards-missing
- Signal: standards_file not readable
- Recovery: use built-in minimal checklist in workflow
- Severity: degrade

## F3: empty-diff
- Signal: zero changed files in PR
- Recovery: report empty PR; ask author to confirm
- Severity: block

## F4: script-failure
- Signal: check_diff.py non-zero exit
- Recovery: log stderr; continue manual review
- Severity: degrade

---

# 11. Upgrade Rules（自进化规则）

```
IF same F4 repeats → fix script or document dependency in compatibility
IF security findings frequent → expand references/standards.md
```

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on:
  - medium-commit-message
provides:
  - pr-review-report
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
parent: none
status: stable
changelog:
  - "1.0.0: initial release with scripts and standards"
```
