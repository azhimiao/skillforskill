# Skill-Core Quickstart

Build your first Agent Skill in 5 minutes.

## Prerequisites

- Python 3.10+
- Optional: `pip install pyyaml` (better frontmatter parsing)

## 1. Create a skill

```bash
python skill-core/skill.py init my-first-skill
# Windows: skill init my-first-skill
```

```
my-first-skill/
├── references/ir.md      ← design (edit)
├── references/eval.yaml  ← L1 tests
└── SKILL.md              ← generated (runtime)
```

## 2. Edit IR + tests

Edit `references/ir.md` — at minimum §1 Goal, §5 steps, §10 failures.

Edit `references/eval.yaml` for automated L1 checks.

## 3. Compile → test

```bash
python skill-core/skill.py compile my-first-skill
python skill-core/skill.py diff my-first-skill
python skill-core/skill.py validate my-first-skill
python skill-core/skill.py test my-first-skill
```

## 4. Install

```bash
# By path
python skill-core/skill.py install my-first-skill --host cursor --scope global

# By registry name
python skill-core/skill.py registry build
python skill-core/skill.py install medium-commit-message --host agents --scope global
```

| Host | Global | Project |
|------|--------|---------|
| agents | `~/.agents/skills/` | `.agents/skills/` |
| cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| claude | `~/.claude/skills/` | `.claude/skills/` |

## 5. Migrate legacy rules

```bash
python skill-core/skill.py migrate .cursor/rules/my-rule.mdc --name my-rule
python skill-core/skill.py migrate-scan --project . --out ./skills
```

Body content is preserved verbatim. Review IR and re-compile when ready.

## Examples

```bash
python skill-core/skill.py compile examples
python skill-core/skill.py test examples
python skill-core/skill.py list -v
```

| Example | Level |
|---------|-------|
| `simple-readme-writer` | Simple |
| `medium-commit-message` | Medium |
| `complex-pr-review` | Complex |

## Full CLI

```bash
skill init <name>
skill compile <path> [--json]
skill diff <path> [-v]
skill validate <path>
skill test <path>
skill registry build
skill list [--tag] [-v]
skill install <name|path> [--host cursor|claude|agents] [--scope global|project]
skill migrate <file> --name <name>
skill migrate-scan [--project .] [--out ./skills]
skill schema
skill docs          # print docs/index.html URI
```

## Documentation site

Open `docs/index.html` in a browser, or run:

```bash
python skill-core/skill.py docs
```

## CI

`.github/workflows/skills.yml` runs: registry build → compile → diff → validate → test.

## Workflow

```
edit ir.md + eval.yaml → compile → diff → validate → test → install
```
