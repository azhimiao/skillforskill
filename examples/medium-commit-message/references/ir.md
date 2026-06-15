medium-commit-message

---

# 0. Compilation Target

```yaml
deploy_to: examples/medium-commit-message/
host: any
invocation: auto
output_profile: narrative
```

---

# 1. Intent（意图）

## Goal
Generate conventional commit messages from staged git diffs.

## Context
Author asks for a commit message, help writing a commit, or review before git commit.

## Constraints
- 时间：under 30 seconds
- 成本：read-only git commands only
- 精度：exact conventional commit format
- 工具限制：code_exec for git only, no push

---

# 2. Inputs（输入定义）

## Required Inputs
- repo_path: path — git repository — validation: contains .git

## Optional Inputs
- scope: string — commit scope override — default: inferred from diff paths

---

# 3. Outputs（输出定义）

**Profile:** narrative

Present `# Suggested commit message` and `# Rationale`.

---

# 4. Skill Decomposition（能力拆解）

## S1: read-staged-diff
- Goal: Retrieve staged diff text
- Inputs: repo_path
- Outputs: diff_text, file_list
- Primary verb: run

## S2: classify-change
- Goal: Determine commit type and scope
- Inputs: diff_text
- Outputs: type, scope
- Primary verb: parse

## S3: compose-message
- Goal: Format conventional commit message
- Inputs: type, scope, diff_text
- Outputs: commit_message
- Primary verb: generate

---

# 5. Execution Plan（执行流程）

1. RUN `git status` and `git diff --staged` in repo_path
2. PARSE diff into changed files and change summary
3. CLASSIFY type as feat, fix, docs, test, refactor, or chore
4. GENERATE subject line max 72 chars in conventional format
5. VALIDATE imperative mood and optional body explaining why

---

# 6. Decision Logic（决策系统）

```
IF no staged changes → ASK author to git add; STOP
IF not a git repo → REPORT F2; STOP
IF diff lines > 500 → SUMMARIZE by directory; ASK author for focus
IF type unclear → default chore; note in Rationale
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| code_exec | git status, git diff --staged | read-only git |
| ask_user | Stage files or narrow large diffs | when blocked |

---

# 8. Memory Model（记忆结构）

## Session memory
Pass diff_text from step 1 to steps 3 and 4.

---

# 9. Evaluation（评估标准）

## L1 Task (before stable)
- Test 1: staged feat diff → feat(scope): subject
- Test 2: empty staged → ask to stage
- Test 3: docs-only diff → docs: subject

---

# 10. Failure Modes（失败模式）

## F1: no-staged-changes
- Signal: git diff --staged empty
- Recovery: ask author to run git add
- Severity: block

## F2: not-git-repo
- Signal: git command fails with not a repository
- Recovery: report path; suggest git init
- Severity: block

## F3: diff-too-large
- Signal: diff exceeds 500 lines
- Recovery: summarize by directory; ask focus area
- Severity: degrade

---

# 11. Upgrade Rules（自进化规则）

```
IF success_rate high → extract classify rules to references/conventional-commits.md
```

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on: []
provides:
  - conventional-commit-message
```

---

# 13. Versioning（版本系统）

```yaml
version: "1.0.0"
parent: none
status: stable
changelog:
  - "1.0.0: initial release"
```
