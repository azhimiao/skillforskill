simple-readme-writer

---

# 0. Compilation Target

```yaml
deploy_to: examples/simple-readme-writer/
host: any
invocation: auto
output_profile: narrative
```

---

# 1. Intent（意图）

## Goal
Generate a concise README section for a given project topic.

## Context
Author asks for README text, documentation section, or project intro paragraph.

## Constraints
- 时间：single session, under 2 min
- 成本：minimal tool calls, no network required
- 精度：best-effort, author review before commit
- 工具限制：file_read optional, no code_exec required

---

# 2. Inputs（输入定义）

## Required Inputs
- topic: string — what the README section covers — validation: non-empty
- audience: string — who will read it — validation: non-empty

## Optional Inputs
- tone: enum — default: professional
- max_words: number — default: 200

---

# 3. Outputs（输出定义）

**Profile:** narrative

Required headings: `# Summary`, `# Details`, `# Next Steps`

---

# 4. Skill Decomposition（能力拆解）

## S1: gather-context
- Goal: Collect topic and audience from author
- Inputs: topic, audience
- Outputs: brief_brief
- Primary verb: ask

## S2: draft-section
- Goal: Write README section markdown
- Inputs: brief_brief, tone, max_words
- Outputs: readme_section
- Primary verb: generate

---

# 5. Execution Plan（执行流程）

1. ASK author for topic and audience if missing
2. LIST required README elements: title, overview, usage hint
3. GENERATE markdown section within max_words
4. VALIDATE section has title and at least one paragraph
5. REPORT draft with `# Summary`, `# Details`, `# Next Steps`

---

# 6. Decision Logic（决策系统）

```
IF topic missing → ASK author for topic; STOP until provided
IF audience missing → ASK author for audience; STOP until provided
IF max_words exceeded → TRIM section; REPORT word count
IF author requests revision → REGENERATE with new tone
```

---

# 7. Tool / API Binding（工具绑定）

| Portable ID | Use | Constraints |
|-------------|-----|-------------|
| ask_user | Clarify topic and audience | required when inputs missing |
| file_read | Read existing README for context | optional |

---

# 8. Memory Model（记忆结构）

## Session memory
Carry topic, audience, and tone from step 1 to step 3.

---

# 9. Evaluation（评估标准）

## L0 Smoke
- [ ] Happy path completes with topic + audience

## L1 Task (before stable)
- Test 1: topic=CLI tool, audience=developers → README section with title and usage
- Test 2: missing topic → ask author
- Test 3: max_words=50 → output under 60 words

---

# 10. Failure Modes（失败模式）

## F1: missing-topic
- Signal: topic empty after input phase
- Recovery: ask author for topic
- Severity: block

## F2: vague-audience
- Signal: audience is "everyone" or empty
- Recovery: ask author to narrow audience
- Severity: degrade

## F3: empty-output
- Signal: generated section has no paragraph
- Recovery: regenerate with explicit overview requirement
- Severity: block

---

# 11. Upgrade Rules（自进化规则）

```
IF ambiguity high → add examples to assets/readme-samples.md
IF latency high → compress Quick Start to 3 steps
```

---

# 12. Skill Graph Dependencies（依赖）

```yaml
depends_on: []
provides:
  - readme-section-draft
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
