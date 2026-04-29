<p align="center">
  <img src="pantheon/assets/pantheon-mark.svg" width="120" alt="Pantheon mark">
</p>

<h1 align="center">Pantheon / 万神殿</h1>

<p align="center">
  <strong>A bounded self-evolving Codex skill system that turns human workflows into validated, reusable AI memory.</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">中文文档</a>
  ·
  <a href="pantheon/SKILL.md">Skill</a>
  ·
  <a href="pantheon/reports/alpaca-12.json">Alpaca Report</a>
  ·
  <a href="pantheon/reports/prompts-12.json">Prompts Report</a>
</p>

<p align="center">
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-17151f?style=for-the-badge">
  <img alt="Self Evolving" src="https://img.shields.io/badge/Self--Evolving-Bounded-f5c86a?style=for-the-badge">
  <img alt="Validation" src="https://img.shields.io/badge/Validation-10%2F10-brightgreen?style=for-the-badge">
  <img alt="Language" src="https://img.shields.io/badge/Language-Multilingual-blue?style=for-the-badge">
</p>

---

## The Pitch

Most AI workflows die in chat history.

Pantheon turns them into **skills**: small, installable packets of operational memory that can be audited, tested, benchmarked, localized, and evolved with consent.

It is inspired by the emotional premise of *Pantheon*: what if memory could survive transformation? Here, the answer is practical. A workflow becomes a skill only after it gains structure, validation, and boundaries.

> Not an agent swarm. Not a prompt dump. Not silent self-modification.
>
> Pantheon is a ritual for turning useful work into durable AI capability.

## Why It Matters

AI agents repeat themselves constantly:

- rediscovering the same project conventions
- forgetting the same validation steps
- rewriting the same boilerplate
- losing hard-won debugging knowledge
- producing "helpful" instructions that cannot be tested

Pantheon gives those lessons a body.

```text
messy task -> distilled workflow -> generated skill -> audit -> benchmark -> installable memory
```

## What Pantheon Does

| Capability | What it means |
| --- | --- |
| Distill | Turn messy briefs, transcripts, or repeated work into skill proposals |
| Scaffold | Generate valid Codex skill directories |
| Audit | Check trigger clarity, placeholder text, context size, validation, and autonomy boundaries |
| Experiment | Generate skills in temp dirs and verify them before trust |
| Benchmark | Compare Pantheon output against a naive baseline |
| Public datasets | Run samples from Stanford Alpaca and awesome-chatgpt-prompts |
| Multilingual | Produce docs and skill guidance in the user's preferred language |

## Results

Pantheon includes repeatable benchmark reports, not just screenshots and vibes.

| Benchmark | Cases | Baseline Avg | Pantheon Avg |
| --- | ---: | ---: | ---: |
| Built-in skill forge cases | 4 | 2.00 / 10 | 8.25 / 10 |
| Stanford Alpaca sample | 12 | 1.00 / 10 | 8.00 / 10 |
| awesome-chatgpt-prompts sample | 12 | 1.75 / 10 | 8.00 / 10 |

Validation:

```text
Pantheon audit: 10 passed, 0 failed
Codex quick_validate: Skill is valid
Skill-forge experiment: 9 passed, 0 failed
```

Reports:

- [pantheon/reports/alpaca-12.json](pantheon/reports/alpaca-12.json)
- [pantheon/reports/prompts-12.json](pantheon/reports/prompts-12.json)

These scores are engineering evidence, not a universal quality claim. The point is that the system has a proof loop: generate, audit, fail, revise, benchmark.

## Quick Start

```bash
python3 pantheon/scripts/pantheon.py audit pantheon
python3 pantheon/scripts/pantheon.py distill --input pantheon/experiments/skill-forge-basic.md
python3 pantheon/scripts/pantheon.py experiment --case pantheon/experiments/skill-forge-basic.md --workdir /tmp/pantheon-exp
python3 pantheon/scripts/pantheon.py benchmark --dataset pantheon/experiments/pantheon-benchmark.jsonl --workdir /tmp/pantheon-bench
```

Run public dataset samples:

```bash
python3 pantheon/scripts/pantheon.py benchmark-public --name alpaca --limit 12 --report pantheon/reports/alpaca-12.json
python3 pantheon/scripts/pantheon.py benchmark-public --name awesome-chatgpt-prompts --limit 12 --report pantheon/reports/prompts-12.json
```

## Use It As A Codex Skill

Install locally by symlinking the skill directory:

```bash
ln -s "$PWD/pantheon" "${CODEX_HOME:-$HOME/.codex}/skills/pantheon"
```

Then invoke it:

```text
Use $pantheon to turn this repeated workflow into a validated Codex skill.
```

Chinese works too:

```text
使用 $pantheon，把这个重复工作流沉淀成一个经过验证的 Codex skill。
```

## Project Layout

```text
pantheon/
├── SKILL.md
├── agents/openai.yaml
├── assets/pantheon-mark.svg
├── experiments/
│   ├── pantheon-benchmark.jsonl
│   └── skill-forge-basic.md
├── references/
│   ├── evolution-protocol.md
│   ├── experiment-rubric.md
│   └── language-policy.md
├── reports/
│   ├── alpaca-12.json
│   └── prompts-12.json
└── scripts/pantheon.py
```

## The Safety Model

Pantheon is designed to evolve skills without pretending that autonomy is free.

It may:

- propose evolutions
- generate patches
- run audits and benchmarks
- produce installable skill drafts

It must not:

- replace installed skills without confirmation
- claim validation that did not run
- hide destructive changes behind mythic language
- treat benchmark scores as proof of universal quality

## Roadmap

- Larger public benchmark adapters
- Human preference review for generated skill drafts
- Cross-language skill quality checks
- Regression tests for skill evolution
- A gallery of generated "deity" skills for common agent workflows

## The Manifesto

Every team has invisible rituals.

The commands people remember. The checks they run before shipping. The weird bug they only fixed once. The review comment that taught them how the system really works.

Pantheon is a place to preserve those rituals without freezing them. Skills can evolve, but only under witness. Memory can become executable, but it must remain accountable.

Keep the human memory.

Make it operational.
