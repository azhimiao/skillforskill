---
name: simple-readme-writer
description: >-
  Generate a concise README section for a given project topic. Use when author asks for
  README text, documentation section, or project intro paragraph.
metadata:
  version: "1.0.0"
  status: stable
  protocol: skill-protocol-v2
compatibility: minimal tool calls, no network required; file_read optional, no code_exec required
---

# Simple Readme Writer

## Quick Start

1. ASK author for topic and audience if missing
2. LIST required README elements: title, overview, usage hint
3. GENERATE markdown section within max_words
4. VALIDATE section has title and at least one paragraph
5. REPORT draft with `# Summary`, `# Details`, `# Next Steps`

## Workflow

### Step 1
ASK author for topic and audience if missing

### Step 2
LIST required README elements: title, overview, usage hint

### Step 3
GENERATE markdown section within max_words

### Step 4
VALIDATE section has title and at least one paragraph

### Step 5
REPORT draft with `# Summary`, `# Details`, `# Next Steps`

### Decision logic

```
IF topic missing → ASK author for topic; STOP until provided
IF audience missing → ASK author for audience; STOP until provided
IF max_words exceeded → TRIM section; REPORT word count
IF author requests revision → REGENERATE with new tone
```

## Inputs

**Required**

- topic: string — what the README section covers — validation: non-empty
- audience: string — who will read it — validation: non-empty

**Optional**

- tone: enum — default: professional
- max_words: number — default: 200

## Outputs

Profile: `narrative`

Deliver with headings: `# Summary`, `# Details`, `# Next Steps`.

## Tools

| ID | Use | Constraints |
|----|-----|-------------|
| ask_user | Clarify topic and audience | required when inputs missing |
| file_read | Read existing README for context | optional |

## Sub-skills

- **S1 gather-context** — Collect topic and audience from author
- **S2 draft-section** — Write README section markdown

## Failure Modes

| ID | Signal | Recovery |
|----|--------|----------|
| F1 | topic empty after input phase | ask author for topic |
| F2 | audience is "everyone" or empty | ask author to narrow audience |
| F3 | generated section has no paragraph | regenerate with explicit overview requirement |

## Verification

| Test | Expected |
|------|----------|
| Test 1: topic=CLI tool, audience=developers | README section with title and usage |
| Test 2: missing topic | ask author |
| Test 3: max_words=50 | output under 60 words |

## Additional Resources

- [IR source](references/ir.md)
