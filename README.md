# Pantheon / 万神殿

Pantheon is a Codex skill for creating and evolving other Codex skills.

The idea is borrowed from the emotional center of *Pantheon*: memory becomes useful only when it survives transformation without losing accountability. In this project, a skill is treated as an uploaded working memory: a repeatable procedure extracted from hard-won work, tested before it is trusted, and never silently rewritten.

## What It Does

- Distills messy briefs or past workflows into skill proposals.
- Scaffolds valid Codex skill directories.
- Audits skills for trigger clarity, context size, missing validation, placeholder text, and unsafe autonomy.
- Runs experiments that generate a skill in a temporary directory and validate it.
- Benchmarks Pantheon-generated skills against a naive baseline.
- Downloads supported public datasets and transforms them into skill-creation benchmark cases.

## Structure

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
│   └── experiment-rubric.md
├── reports/
│   ├── alpaca-12.json
│   └── prompts-12.json
└── scripts/pantheon.py
```

## Quick Start

Run from the repository root:

```bash
python3 pantheon/scripts/pantheon.py audit pantheon
python3 pantheon/scripts/pantheon.py distill --input pantheon/experiments/skill-forge-basic.md
python3 pantheon/scripts/pantheon.py experiment --case pantheon/experiments/skill-forge-basic.md --workdir /tmp/pantheon-exp
python3 pantheon/scripts/pantheon.py benchmark --dataset pantheon/experiments/pantheon-benchmark.jsonl --workdir /tmp/pantheon-bench
```

To run public dataset samples:

```bash
python3 pantheon/scripts/pantheon.py benchmark-public --name alpaca --limit 12 --report pantheon/reports/alpaca-12.json
python3 pantheon/scripts/pantheon.py benchmark-public --name awesome-chatgpt-prompts --limit 12 --report pantheon/reports/prompts-12.json
```

Supported public adapters:

- `alpaca`: Stanford Alpaca instruction data from `tatsu-lab/stanford_alpaca`
- `awesome-chatgpt-prompts`: prompt-role data from `f/awesome-chatgpt-prompts`

## Experiment Design

The benchmark compares two generators on the same briefs:

- **Baseline**: creates a minimal generic skill.
- **Pantheon**: creates a skill with workflow, references, validation, and bounded-autonomy expectations.

Each generated skill is scored from 0 to 10:

- Trigger clarity
- Workflow leverage
- Resource fit
- Validation integrity
- Bounded autonomy

These scores are engineering evidence, not a scientific claim. They are useful because they can fail, can be repeated, and can expose weak skill designs before installation.

## Current Local Results

Built-in benchmark:

```text
cases: 4
baseline_avg: 2.0 / 10
pantheon_avg: 8.25 / 10
```

Public benchmark samples:

```text
Stanford Alpaca sample, 12 cases:
baseline_avg: 1.0 / 10
pantheon_avg: 8.0 / 10
report: pantheon/reports/alpaca-12.json

awesome-chatgpt-prompts sample, 12 cases:
baseline_avg: 1.75 / 10
pantheon_avg: 8.0 / 10
report: pantheon/reports/prompts-12.json
```

Validation:

```text
Pantheon audit: 10 passed, 0 failed
Codex quick_validate: Skill is valid
Skill-forge experiment: 9 passed, 0 failed
```

Public dataset reports are written under `pantheon/reports/`. They include per-case scores and audit failures for both baseline and Pantheon generations.

## Installation As A Codex Skill

For local discovery, copy or symlink the `pantheon` directory into your Codex skills directory:

```bash
ln -s "$PWD/pantheon" "${CODEX_HOME:-$HOME/.codex}/skills/pantheon"
```

Then invoke it in a prompt:

```text
Use $pantheon to turn this repeated workflow into a validated Codex skill.
```

## Safety Model

Pantheon is intentionally not a silent self-modifier.

It may:

- Propose evolutions.
- Generate patches.
- Run audits and benchmarks.
- Produce installable skill drafts.

It must not:

- Replace installed skills without confirmation.
- Claim validation that did not run.
- Hide destructive changes behind poetic language.
- Treat benchmark scores as proof of universal quality.

The romantic claim is simple: keep the human memory, but make it operational.
