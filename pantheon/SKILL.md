---
name: pantheon
description: Create, evolve, audit, and validate Codex skills from repeated workflows or hard-won project experience. Use when the user wants a new skill, wants a self-improving skill system, wants to turn conversations or repository work into reusable procedural knowledge, or wants experiments that prove a skill is practical before installation.
---

# Pantheon

Pantheon is a bounded evolution system for Codex skills. Treat each skill as an uploaded working memory: not a personality to imitate, but a tested procedure that can survive outside the original conversation.

## Core Rule

Never silently mutate installed skills. Propose, patch, audit, test, and ask for confirmation before installing or replacing a skill.

## Workflow

1. **Observe the mortal task**
   - Identify the repeated workflow, brittle decision, tool ritual, or domain knowledge that should outlive the current conversation.
   - Prefer concrete examples over broad ambition.
   - If the request is vague, create the smallest useful skill and list the assumptions.

2. **Name the god**
   - Use a lowercase hyphenated machine name under 64 characters.
   - Use a human-facing display name only in `agents/openai.yaml`.
   - Avoid names that describe vibes only; the trigger description must say what work the skill performs.

3. **Choose the body**
   - Put essential procedure in `SKILL.md`.
   - Put detailed policies, rubrics, schemas, and examples in `references/`.
   - Put deterministic repeatable operations in `scripts/`.
   - Put templates, icons, or reusable output assets in `assets/`.

4. **Forge the skill**
   - Use `scripts/pantheon.py scaffold` when a draft is enough.
   - Manually refine the generated `SKILL.md`; Codex is expected to improve the draft.
   - Keep the body concise and operational. Remove lore that does not change behavior.

5. **Judge the skill**
   - Run `scripts/pantheon.py audit <skill-dir>`.
   - If the skill is nontrivial, run `scripts/pantheon.py experiment --case <case-file>`.
   - Fix failures before suggesting installation.

6. **Evolve with consent**
   - For an existing skill, produce a short change plan before editing.
   - Preserve working behavior unless the user explicitly wants a redesign.
   - Keep a clear diff and verification result.

## Deity Roles

Use these roles as a thinking frame, not as extra agents unless the user explicitly asks for subagents.

- **Archivist**: Extract durable knowledge from a messy task.
- **Smith**: Convert knowledge into `SKILL.md`, scripts, references, and assets.
- **Oracle**: Write trigger descriptions and default prompts that invoke the skill at the right time.
- **Judge**: Audit for overreach, missing validation, context bloat, unsafe autonomy, and untestable claims.
- **Ember**: Preserve the romantic purpose: the skill should feel like a memory made useful, not a generic template.

## Commands

From the Pantheon skill directory:

```bash
python3 scripts/pantheon.py distill --input path/to/notes.md
python3 scripts/pantheon.py scaffold --brief path/to/brief.md --out /tmp/skills
python3 scripts/pantheon.py audit path/to/skill
python3 scripts/pantheon.py experiment --case experiments/skill-forge-basic.md --workdir /tmp/pantheon-exp
python3 scripts/pantheon.py benchmark --dataset experiments/pantheon-benchmark.jsonl --workdir /tmp/pantheon-bench
python3 scripts/pantheon.py download-dataset --url https://example.com/skills.jsonl --out /tmp/skills.jsonl
python3 scripts/pantheon.py benchmark-public --name alpaca --limit 12 --report reports/alpaca-12.json
python3 scripts/pantheon.py benchmark-public --name awesome-chatgpt-prompts --limit 12 --report reports/prompts-12.json
```

Read `references/evolution-protocol.md` before evolving an installed skill. Read `references/experiment-rubric.md` before claiming the skill has been proven useful.
Read `references/language-policy.md` when the user asks for Chinese, bilingual, localized, or non-English skill output.

## Experiments

Use the built-in benchmark for a fast proof loop. It compares a naive baseline generator against Pantheon generation on JSONL briefs and scores trigger clarity, workflow leverage, resource fit, validation integrity, and bounded autonomy.

Use `benchmark-public` for public dataset samples. Current adapters support Stanford Alpaca and awesome-chatgpt-prompts; both are transformed into skill-creation briefs before scoring.

Treat benchmark scores as engineering evidence, not truth. Include qualitative notes from the generated artifacts before claiming impact.

## Quality Bar

A Pantheon-created skill is ready only when:

- Its frontmatter description contains the actual trigger conditions.
- Its workflow is shorter than the task it replaces.
- Its reusable resources are justified by repeat use or deterministic reliability.
- Its validation checks can fail for real defects.
- Its autonomy is bounded by user review before installation or destructive edits.
- Its language carries the project's myth without obscuring the engineering contract.
