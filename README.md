<p align="center">
  <img src="pantheon/assets/pantheon-mark.svg" width="120" alt="Pantheon mark">
</p>

<h1 align="center">Pantheon / 万神殿</h1>

<p align="center">
  <strong>A bounded self-evolving Codex skill system that turns human workflows into validated, reusable AI memory.</strong>
</p>

<p align="center">
  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/English-README-17151f?style=for-the-badge"></a>
  <a href="README.zh-CN.md"><img alt="中文" src="https://img.shields.io/badge/%E4%B8%AD%E6%96%87-%E6%96%87%E6%A1%A3-f5c86a?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="pantheon/SKILL.md"><img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-17151f?style=flat-square"></a>
  <a href="pantheon/references/evolution-protocol.md"><img alt="Self Evolving" src="https://img.shields.io/badge/Self--Evolving-Bounded-f5c86a?style=flat-square"></a>
  <a href="pantheon/reports/alpaca-12.json"><img alt="Alpaca" src="https://img.shields.io/badge/Alpaca-8.0%2F10-2ea043?style=flat-square"></a>
  <a href="pantheon/reports/prompts-12.json"><img alt="Prompts" src="https://img.shields.io/badge/Prompts-8.0%2F10-2ea043?style=flat-square"></a>
  <a href="pantheon/references/language-policy.md"><img alt="Multilingual" src="https://img.shields.io/badge/Docs-Multilingual-0969da?style=flat-square"></a>
</p>

---

<table>
  <tr>
    <td><strong>Distill</strong><br>Turn messy work into durable procedures.</td>
    <td><strong>Forge</strong><br>Generate valid, installable Codex skills.</td>
    <td><strong>Judge</strong><br>Audit, benchmark, and preserve consent gates.</td>
  </tr>
</table>

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

<p align="center">
  <img alt="Flow" src="https://img.shields.io/badge/messy%20task-distill-17151f?style=for-the-badge">
  <img alt="Flow" src="https://img.shields.io/badge/workflow-forge-f5c86a?style=for-the-badge">
  <img alt="Flow" src="https://img.shields.io/badge/skill-audit-0969da?style=for-the-badge">
  <img alt="Flow" src="https://img.shields.io/badge/memory-install-2ea043?style=for-the-badge">
</p>

## What Pantheon Does

<table>
  <tr>
    <th>Module</th>
    <th>Capability</th>
    <th>What it means</th>
  </tr>
  <tr>
    <td><img alt="Distill" src="https://img.shields.io/badge/01-Distill-17151f"></td>
    <td>Workflow extraction</td>
    <td>Turn messy briefs, transcripts, or repeated work into skill proposals.</td>
  </tr>
  <tr>
    <td><img alt="Scaffold" src="https://img.shields.io/badge/02-Scaffold-f5c86a"></td>
    <td>Skill generation</td>
    <td>Generate valid Codex skill directories with references, scripts, and metadata.</td>
  </tr>
  <tr>
    <td><img alt="Audit" src="https://img.shields.io/badge/03-Audit-0969da"></td>
    <td>Quality gates</td>
    <td>Check trigger clarity, placeholders, context size, validation, and autonomy boundaries.</td>
  </tr>
  <tr>
    <td><img alt="Experiment" src="https://img.shields.io/badge/04-Experiment-8250df"></td>
    <td>Proof loop</td>
    <td>Generate skills in temp dirs and verify them before trust.</td>
  </tr>
  <tr>
    <td><img alt="Benchmark" src="https://img.shields.io/badge/05-Benchmark-2ea043"></td>
    <td>Measured comparison</td>
    <td>Compare Pantheon output against a naive baseline on built-in and public datasets.</td>
  </tr>
  <tr>
    <td><img alt="Language" src="https://img.shields.io/badge/06-Language-c6538c"></td>
    <td>Multilingual output</td>
    <td>Produce docs and skill guidance in the user's preferred language.</td>
  </tr>
</table>

## Results

Pantheon includes repeatable benchmark reports, not just screenshots and vibes.

<table>
  <tr>
    <th>Benchmark</th>
    <th>Cases</th>
    <th>Baseline Avg</th>
    <th>Pantheon Avg</th>
    <th>Lift</th>
  </tr>
  <tr>
    <td>Built-in skill forge cases</td>
    <td align="right">4</td>
    <td align="right">2.00 / 10</td>
    <td align="right"><strong>8.25 / 10</strong></td>
    <td><img alt="4.1x" src="https://img.shields.io/badge/lift-4.1x-2ea043"></td>
  </tr>
  <tr>
    <td>Stanford Alpaca sample</td>
    <td align="right">12</td>
    <td align="right">1.00 / 10</td>
    <td align="right"><strong>8.00 / 10</strong></td>
    <td><img alt="8.0x" src="https://img.shields.io/badge/lift-8.0x-2ea043"></td>
  </tr>
  <tr>
    <td>awesome-chatgpt-prompts sample</td>
    <td align="right">12</td>
    <td align="right">1.75 / 10</td>
    <td align="right"><strong>8.00 / 10</strong></td>
    <td><img alt="4.6x" src="https://img.shields.io/badge/lift-4.6x-2ea043"></td>
  </tr>
</table>

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
