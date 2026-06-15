# Skill Protocol Standard

**Version:** 2.0.0  
**Status:** Stable  
**Date:** 2026-06-15  
**Extends:** [Agent Skills Specification](https://agentskills.io/specification) (runtime layer)

---

## Abstract

This document defines **Skill Protocol v2** — a vendor-neutral standard for designing, compiling, validating, and evolving **Agent Skills**.

Agent Skills (agentskills.io) defines the **runtime format** (`SKILL.md` + optional directories). Skill Protocol defines the **authoring format** (Intermediate Representation, IR) that compiles into runtime `SKILL.md`.

Together they form a complete pipeline:

```
Author Intent → IR (this spec) → SKILL.md (agentskills.io) → Agent Host → Evaluation → Upgrade
```

---

## 1. Scope

### 1.1 In scope

- IR structure (13 normative sections)
- Runtime compilation rules (IR → `SKILL.md`)
- Portable tool identifiers
- Output profiles
- Executable step requirements (verb lint)
- Evaluation tiers (L0 / L1 / L2)
- Failure modes and upgrade rules
- Skill dependency graphs
- Directory layout and validation

### 1.2 Out of scope

- Host-specific tool APIs (see host adapter documents)
- Agent model behavior or prompting
- Marketplace distribution or signing
- UI for skill authoring

### 1.3 Conformance

| Level | Name | Requirements |
|-------|------|----------------|
| **C0** | Runtime | Valid agentskills.io `SKILL.md` |
| **C1** | Protocol | C0 + IR exists with sections 1–13 + passes compilation contract (§14) |
| **C2** | Production | C1 + L1 evaluation complete + `metadata.status: stable` |

A skill **MAY** ship at C0 without IR. A skill **SHOULD** reach C1 before team sharing. A skill **SHOULD** reach C2 before public distribution.

---

## 2. Normative language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY** in this document are to be interpreted as described in [RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119).

---

## 3. Terminology

| Term | Definition |
|------|------------|
| **Agent Skill** | A directory containing at least `SKILL.md`, conforming to agentskills.io |
| **IR** | Intermediate Representation — design-time document expressing sections §4–§16 |
| **Runtime** | Compiled `SKILL.md` loaded by an agent host |
| **Host** | Any agent product that loads Agent Skills (e.g. IDE agent, CLI agent) |
| **Portable Tool ID** | Vendor-neutral capability identifier (§11) |
| **Atom** | A sub-skill with concrete inputs, outputs, and executable steps (§7) |
| **Output Profile** | Declared shape of skill output (§6) |
| **Author** | Developer who writes or maintains the skill |

---

## 4. Architecture

### 4.1 Two layers

```
┌─────────────────────────────────────────┐
│  IR Layer (design-time)                 │
│  references/ir.md or template.skill.md  │
│  Sections §5–§16                        │
└─────────────────┬───────────────────────┘
                  │ compile
                  ▼
┌─────────────────────────────────────────┐
│  Runtime Layer (load-time)              │
│  SKILL.md (agentskills.io)              │
│  + scripts/ references/ assets/         │
└─────────────────────────────────────────┘
```

### 4.2 Progressive disclosure

| Stage | Content loaded | Token budget (recommended) |
|-------|----------------|----------------------------|
| Discovery | `name`, `description` | ~100 tokens per skill |
| Activation | Full `SKILL.md` body | < 5000 tokens |
| Execution | `references/`, `scripts/` output | On demand |

Runtime `SKILL.md` **SHOULD** stay under 500 lines. Detailed material **MUST** live in `references/`.

### 4.3 Relationship to agentskills.io

Skill Protocol **does not replace** agentskills.io. It **extends** it with:

- Authoring discipline (IR)
- Compilation mapping
- Quality gates (verb lint, failure modes, evaluation tiers)
- Portable tool IDs

All runtime skills **MUST** remain valid Agent Skills.

---

## 5. Runtime layer requirements

Runtime `SKILL.md` **MUST** conform to [agentskills.io/specification](https://agentskills.io/specification).

### 5.1 Required frontmatter

```yaml
---
name: skill-name          # MUST match directory name
description: >            # MUST: third person, WHAT + WHEN, ≤1024 chars
  ...
metadata:                 # SHOULD include protocol metadata
  version: "1.0.0"
  status: experimental    # experimental | stable | deprecated
  protocol: skill-protocol-v2
---
```

### 5.2 `name` constraints

- 1–64 characters
- Lowercase letters, digits, hyphens only (`a-z`, `0-9`, `-`)
- MUST NOT start or end with `-`
- MUST NOT contain consecutive hyphens (`--`)
- MUST equal parent directory name

### 5.3 `description` constraints

- 1–1024 characters, non-empty
- MUST describe **what** the skill does and **when** to use it
- MUST be written in third person
- SHOULD include trigger keywords authors and agents use to find the skill

**Good:**

```yaml
description: Generates conventional commit messages from staged git diffs. Use when the author asks for a commit message or before git commit.
```

**Bad:**

```yaml
description: Helps with git.
```

### 5.4 Required body sections

Runtime `SKILL.md` **MUST** include:

| Section | Content |
|---------|---------|
| Title | `# <Human-readable name>` |
| Quick Start | 3–5 imperative steps |
| Workflow | Full step-by-step execution |
| Failure Modes | ≥ 3 entries with signal and recovery |

Runtime `SKILL.md` **SHOULD** include:

| Section | Content |
|---------|---------|
| Inputs / Outputs | Condensed from IR §6–§7 |
| Tools | Portable IDs or host-mapped names |
| Verification | L0/L1 checks |
| Additional Resources | Links to `references/` (one level deep) |

### 5.5 Optional directories

```
skill-name/
├── SKILL.md          # REQUIRED
├── references/       # RECOMMENDED — IR, docs, eval rubrics
├── scripts/          # OPTIONAL — deterministic operations
└── assets/           # OPTIONAL — templates, schemas, static files
```

File references in `SKILL.md` **MUST** use relative paths with forward slashes. References **SHOULD** be one level deep from `SKILL.md`.

---

## 6. IR layer — section overview

Every skill authored under Skill Protocol **MUST** be expressible in these sections before compilation.

| § | Name | IR | Runtime mapping |
|---|------|----|-----------------|
| 0 | Frontmatter bridge | Auto-generated at compile | YAML frontmatter |
| 1 | Intent | Required | `description`, `compatibility` |
| 2 | Inputs | Required | Body § Inputs |
| 3 | Outputs | Required | Body § Outputs |
| 4 | Decomposition | Required if \|steps\| > 5 | Body § Sub-skills |
| 5 | Execution Plan | Required | Quick Start + Workflow |
| 6 | Decision Logic | Required | Workflow branches |
| 7 | Tool Binding | Required | Body § Tools |
| 8 | Memory Model | Required | `references/memory.md` if non-trivial |
| 9 | Evaluation | Required | Body § Verification |
| 10 | Failure Modes | Required (≥ 3) | Body § Failure Modes |
| 11 | Upgrade Rules | Required | Maintainer docs |
| 12 | Dependencies | Required | Skill graph metadata |
| 13 | Versioning | Required | `metadata.version`, `metadata.status` |

---

## 7. IR §1 — Intent

### 7.1 Goal

One sentence stating the outcome the skill guarantees.

### 7.2 Context

When an agent **SHOULD** activate the skill: author phrases, file types, workflow phases, upstream triggers.

### 7.3 Constraints

Authors **SHOULD** document:

| Dimension | Examples |
|-----------|----------|
| Time | single session, < 2 min, batch |
| Cost | minimal tool calls, no paid API |
| Precision | exact, best-effort, human review required |
| Tool limits | read-only, no network, shell only |

---

## 8. IR §2 — Inputs

### 8.1 Schema

Each input **MUST** define:

```yaml
- name: input_id
  type: string | path | number | boolean | enum | object
  source: author | file | env | upstream_skill
  validation: <rule>
  default: <optional>
```

### 8.2 Required vs optional

- **Required Inputs** — skill MUST NOT proceed without them; decision logic MUST ASK author
- **Optional Inputs** — MUST document defaults

---

## 9. IR §3 — Outputs

### 9.1 Output profiles

Authors **MUST** declare exactly one profile:

| Profile | Use when | Schema |
|---------|----------|--------|
| `structured` | Composable / machine-readable pipelines | §9.2 |
| `artifact` | File or code generation | §9.3 |
| `narrative` | Reviews, explanations, decisions | §9.4 |
| `hybrid` | Artifacts plus explanation | §9.3 + §9.4 |

### 9.2 Structured profile

```json
{
  "result": "",
  "steps": [],
  "confidence": 0.0,
  "errors": []
}
```

### 9.3 Artifact profile

```json
{
  "artifacts": [
    { "path": "", "type": "", "checksum": "" }
  ],
  "summary": ""
}
```

### 9.4 Narrative profile

Output **MUST** include headings:

- `# Summary`
- `# Details`
- `# Next Steps`

### 9.5 Confidence scale

| Range | Semantics | Required action |
|-------|-----------|-----------------|
| 0.0 – 0.3 | Insufficient data | MUST ask author or re-run sub-step |
| 0.4 – 0.7 | Partial | MUST deliver with explicit caveats |
| 0.8 – 1.0 | High | MAY chain to downstream skills |

---

## 10. IR §4 — Decomposition

Complex skills **MUST** decompose into atomic sub-skills S1…Sn.

### 10.1 Sub-skill schema

```yaml
id: S1
name: fetch-diff
goal: <one sentence>
inputs: [input_a, input_b]
outputs: [output_x]
primary_verb: run
depends_on: []
```

### 10.2 Atom invariant

Each sub-skill **MUST** satisfy:

```
ATOM(S) :=
  has_named_inputs(S)
  AND has_named_outputs(S)
  AND has_executable_step(S)
  AND NOT uses_abstract_verb_only(S)
```

If |S| > 5, authors **SHOULD** split into multiple top-level skills linked via §15.

---

## 11. IR §5 — Execution Plan

### 11.1 Step format

Every step **MUST** describe one observable action:

```
1. READ <source> → extract <fields>
2. RUN <command> with <args>
3. TRANSFORM <input> to <output> via <method>
4. VALIDATE <invariant>
5. GENERATE <artifact> at <path>
6. REPORT <summary>
```

### 11.2 Approved verbs

Steps **SHOULD** begin with:

`read`, `run`, `write`, `create`, `delete`, `fetch`, `parse`, `transform`, `validate`, `generate`, `compare`, `list`, `grep`, `call`, `invoke`, `deploy`, `commit`, `ask`

### 11.3 Banned standalone verbs

Steps **MUST NOT** use only:

`understand`, `analyze`, `think`, `consider`, `be aware`, `keep in mind`

**Replace with concrete actions** (see skill-core verb lint table).

---

## 12. IR §6 — Decision Logic

### 12.1 Format

```
IF <observable condition> → <concrete action>
```

### 12.2 Termination

Every branch **MUST** terminate in one of:

`CONTINUE` | `STOP` | `RETRY` | `ESCALATE` | `FALLBACK <action>`

### 12.3 Examples

```
IF required_input missing → ASK author
IF validation fails → RUN fix; IF still fails → REPORT F2 and STOP
IF confidence < 0.4 → RE-RUN S2 with expanded scope
IF file not found → SEARCH codebase; IF not found → ASK author
```

---

## 13. IR §7 — Tool Binding

Tools **MUST** be declared using **Portable Tool IDs**:

| ID | Capability |
|----|------------|
| `web_search` | Search public web |
| `web_fetch` | Fetch URL content |
| `code_exec` | Execute shell / commands |
| `file_read` | Read files |
| `file_write` | Write or patch files |
| `search_code` | Search repository |
| `sub_skill_call` | Invoke another skill |
| `subagent` | Delegate to sub-agent |
| `memory_read` | Read persisted skill notes |
| `memory_write` | Append learning notes (with author consent) |
| `ask_user` | Request clarification |

### 13.1 Tool entry schema

```yaml
- id: code_exec
  use: run tests, git operations
  constraints: no destructive commands without author approval
```

Host-specific mappings **MAY** appear in a host adapter document. IR **MUST NOT** hard-code a single vendor's tool names.

---

## 14. IR §8 — Memory Model

Two layers **MUST** be distinguished:

### 14.1 Skill memory (persistent)

Stored in files (e.g. `references/learning.md`). Written **ONLY** with author consent.

```json
{
  "patterns": [],
  "failures": [],
  "decisions": []
}
```

### 14.2 Session memory (ephemeral)

Conversation context and tool outputs from the current run. Execution plans **SHOULD** reference prior step outputs explicitly.

Skills **MUST NOT** assume cross-session episodic memory unless a real store is documented in `compatibility`.

---

## 15. IR §9 — Evaluation

### 15.1 L0 — Smoke (required before first deploy)

- [ ] Frontmatter valid (§5)
- [ ] ≥ 3 failure modes (§17)
- [ ] One happy-path walkthrough completes

### 15.2 L1 — Task (required before `stable`)

- [ ] ≥ 3 test cases with expected outputs
- [ ] Every decision branch (§12) covered by ≥ 1 test

### 15.3 L2 — Metrics (optional)

| Metric | Definition |
|--------|------------|
| `success_rate` | Runs completed without escalation / total runs |
| `accuracy` | Outputs passing validation / total runs |
| `latency_p95` | 95th percentile wall time |
| `reuse_rate` | Runs reused downstream / total runs |

Suggested targets (L2 only): `success_rate ≥ 0.8`, `accuracy ≥ 0.9`.

---

## 16. IR §10 — Failure Modes

Skills **MUST** document ≥ 3 failure modes.

### 16.1 Schema

```yaml
id: F1
name: missing-input
signal: <how to detect>
recovery: <concrete action>
severity: block | degrade
```

| Severity | Meaning |
|----------|---------|
| `block` | MUST NOT proceed |
| `degrade` | MAY proceed with reduced scope |

---

## 17. IR §11 — Upgrade Rules

Upgrade rules **SHOULD** apply only with L1 or L2 evidence:

| Signal | Action |
|--------|--------|
| `success_rate > 0.8` over ≥ 20 runs | Extract shared steps into sub-skill |
| Same failure ≥ 3 times | Split skill or add decision branch |
| `latency_p95` above budget | Compress steps; add script; move detail to references |
| Clarification rate > 30% | Refine §8 inputs; add examples to assets |
| Misfire rate > 10% | Tighten description; consider manual invocation |

### 17.1 Version bumps

| Change | Bump |
|--------|------|
| Wording, typos | PATCH |
| New optional input, new failure mode | MINOR |
| Breaking output schema, renamed sub-skills | MAJOR |

---

## 18. IR §12 — Dependencies

```yaml
depends_on:
  - other-skill
provides:
  - capability-id
```

Rules:

- Graph **MUST NOT** contain cycles
- Dependents **MUST NOT** duplicate provider logic
- Batch builds **SHOULD** create provider skills before dependents

---

## 19. IR §13 — Versioning

```yaml
version: "1.0.0"       # semver
parent: none           # or parent skill name
status: experimental   # experimental | stable | deprecated
replaced_by: null      # when deprecated
changelog:
  - "1.0.0: initial release"
```

Deprecated skills **SHOULD** remain in place with `status: deprecated` and `metadata.replaced_by` set.

---

## 20. Compilation contract

IR is **valid** when all conditions hold:

1. Sections 1–13 present (§0 generated at compile)
2. §10 atoms pass invariant (§10.2)
3. §11 passes verb lint (§11.3)
4. §12 every branch terminates (§12.2)
5. §16 ≥ 3 failure modes
6. §9 output profile declared

### 20.1 IR → runtime mapping

| IR | Runtime |
|----|---------|
| Goal + Context | `description` |
| Constraints | `compatibility` |
| §11 Execution + §12 Decision | Quick Start + Workflow |
| §8 Inputs, §9 Outputs | Inputs / Outputs section |
| §13 Tools | Tools section |
| §15 Evaluation, §16 Failures | Verification + Failure Modes |
| §19 Versioning | `metadata.version`, `metadata.status` |

Compile **SHOULD** set `metadata.protocol: skill-protocol-v2`.

---

## 21. Validation

### 21.1 Automated

Reference validator (skill-core):

```bash
python scripts/validate_skill.py ./skill-name
```

Checks: frontmatter, name/folder match, line count, failure modes, verb lint, path slashes.

### 21.2 Manual checklist

Authors **SHOULD** verify before deploy:

- [ ] `name` matches folder; valid charset
- [ ] `description`: third person, WHAT + WHEN, trigger terms
- [ ] Quick Start ≤ 5 steps; all pass verb lint
- [ ] Output profile declared and exemplified
- [ ] ≥ 3 failure modes with recovery
- [ ] `references/` used for content > 500 lines equivalent
- [ ] No vendor lock-in in IR tool section
- [ ] Dependency graph acyclic

---

## 22. Deployment

Compiled skills **MAY** install to any Agent Skills-compatible path:

| Scope | Example paths |
|-------|---------------|
| Project | `.agents/skills/<name>/`, `.cursor/skills/<name>/` |
| Personal | `~/.cursor/skills/<name>/`, `~/.claude/skills/<name>/` |
| Package | `skills/<name>/` in a skills repository |

Skills **MUST NOT** overwrite vendor-shipped built-in directories.

---

## 23. Security considerations

- Scripts in `scripts/` **SHOULD** be reviewed before execution; authors **SHOULD** document dependencies
- Skills **MUST NOT** instruct exfiltration of secrets
- `memory_write` **MUST** require author consent
- Destructive `code_exec` operations **MUST** require explicit author approval in constraints

---

## 24. Appendix A — IR template

See `skill-core/references/template.skill.md`.

## 25. Appendix B — Worked example

See `skill-core/references/example-compiled.md`.

## 26. Appendix C — Host adapters

See `skill-core/references/host-adapters.md`.

## 27. Appendix D — Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-06-15 | Initial stable release. Portable tool IDs. L0/L1/L2 eval. Extends agentskills.io. |

---

## References

1. [Agent Skills Specification](https://agentskills.io/specification)
2. [RFC 2119 — Key words for use in RFCs](https://datatracker.ietf.org/doc/html/rfc2119)
3. Skill-Core implementation: `skill-core/SKILL.md`
