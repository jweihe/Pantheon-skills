#!/usr/bin/env python3
"""Pantheon: bounded evolution tools for Codex skills."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")

PUBLIC_DATASETS = {
    "alpaca": {
        "url": "https://raw.githubusercontent.com/tatsu-lab/stanford_alpaca/main/alpaca_data.json",
        "format": "alpaca-json",
    },
    "awesome-chatgpt-prompts": {
        "url": "https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv",
        "format": "prompts-csv",
    },
}


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


MUTATION_PROFILES = {
    "archivist": {
        "title": "Archivist",
        "thesis": "Preserve the reusable memory with minimal ceremony.",
        "steps": [
            "Extract the durable workflow from the user request.",
            "Separate one-off context from repeatable procedure.",
            "Store bulky examples in references instead of the main body.",
            "Run validation before recommending installation.",
            "Summarize what memory was preserved and what still depends on humans.",
        ],
        "references": {
            "memory.md": "# Preserved Memory\n\n- Keep only details that change future behavior.\n- Prefer concrete examples over broad principles.\n",
        },
    },
    "judge": {
        "title": "Judge",
        "thesis": "Harden the skill with consent gates, failure modes, and audit checks.",
        "steps": [
            "Identify actions that could mutate files, installed skills, repositories, or external systems.",
            "Require explicit confirmation before installation, replacement, destructive edits, or remote writes.",
            "Run the audit checklist and record every failure before revising.",
            "Reject vague success claims that are not backed by a command, diff, report, or sample output.",
            "Report residual risk in the final response.",
        ],
        "references": {
            "safety.md": "# Safety Gates\n\n- Confirm before replacing installed skills.\n- Do not claim validation that did not run.\n- Keep rollback instructions with every evolution.\n",
        },
    },
    "smith": {
        "title": "Smith",
        "thesis": "Turn the workflow into tools, scripts, and repeatable artifacts.",
        "steps": [
            "Inspect existing project conventions before creating new structure.",
            "Move deterministic repeat work into scripts.",
            "Use references for rubrics, schemas, policies, and long examples.",
            "Prefer generated artifacts that can be rerun from a command.",
            "Run script syntax checks and at least one realistic smoke test.",
        ],
        "references": {
            "tooling.md": "# Tooling Rules\n\n- Scripts must write only to requested output paths.\n- Scripts should be deterministic and easy to run locally.\n",
        },
    },
    "oracle": {
        "title": "Oracle",
        "thesis": "Make the skill trigger at the right time and speak in the user's language.",
        "steps": [
            "Write a frontmatter description that names concrete trigger conditions.",
            "Match the user's language for explanations and generated examples.",
            "Keep machine-facing names, YAML keys, paths, and CLI flags stable and ASCII.",
            "Avoid poetic phrasing where commands, checks, or warnings need precision.",
            "Include a default prompt that names the skill explicitly.",
        ],
        "references": {
            "language.md": "# Language Rules\n\n- Match the user's language for prose.\n- Keep code, paths, CLI flags, and JSON keys stable.\n",
        },
    },
    "arena": {
        "title": "Arena",
        "thesis": "Optimize the skill for measurable transfer across multiple cases.",
        "steps": [
            "Define the cases the skill must handle before editing the skill.",
            "Run baseline and candidate variants on the same arena.",
            "Score trigger clarity, workflow leverage, resources, validation, and autonomy boundaries.",
            "Keep the winning variant only when it improves measurable behavior.",
            "Write a lineage report so the next evolution starts from evidence, not memory.",
        ],
        "references": {
            "arena.md": "# Arena Rubric\n\n- Compare variants on the same cases.\n- Selection requires a score delta and a qualitative reason.\n",
        },
    },
}


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-+", "-", text)
    return (text or "new-skill")[:63].strip("-") or "new-skill"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def infer_skill_name(brief: str) -> str:
    title = ""
    for line in brief.splitlines():
        clean = line.strip("# ").strip()
        if clean:
            title = clean
            break
    words = re.findall(r"[A-Za-z0-9]+", title)
    if not words:
        words = re.findall(r"[A-Za-z0-9]+", brief[:120])
    return slugify("-".join(words[:5]))


def distill_text(text: str) -> dict[str, object]:
    lowered = text.lower()
    bullets = [line.strip("-* ").strip() for line in text.splitlines() if line.strip().startswith(("-", "*"))]
    verbs = []
    for word in ("create", "build", "audit", "validate", "test", "summarize", "install", "review", "deploy"):
        if word in lowered:
            verbs.append(word)
    name = infer_skill_name(text)
    return {
        "candidate_name": name,
        "display_name": name.replace("-", " ").title(),
        "job_to_be_done": first_sentence(text),
        "repeated_steps": bullets[:12],
        "likely_scripts": infer_scripts(lowered),
        "likely_references": infer_references(lowered),
        "validation_plan": [
            "Run Pantheon audit on the generated skill.",
            "Exercise the skill on one realistic case in a temporary directory.",
            "Record failures before recommending installation.",
        ],
        "risk_flags": infer_risks(lowered),
        "detected_action_words": verbs,
    }


def first_sentence(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("-", "*")):
            continue
        clean_line = line.strip("# ").strip()
        if clean_line.lower().startswith("experiment case:"):
            continue
        lines.append(clean_line)
    clean = " ".join(lines) or " ".join(line.strip("-#* ").strip() for line in text.splitlines() if line.strip())
    match = re.search(r"(.{20,220}?)(?:[.!?。]|$)", clean)
    return match.group(1).strip() if match else clean[:220]


def infer_scripts(lowered: str) -> list[str]:
    scripts = []
    if any(word in lowered for word in ("validate", "audit", "check", "test")):
        scripts.append("validation or audit helper")
    if any(word in lowered for word in ("generate", "scaffold", "create")):
        scripts.append("scaffolding helper")
    if any(word in lowered for word in ("convert", "parse", "extract", "transform")):
        scripts.append("parser or transformer")
    return scripts


def infer_references(lowered: str) -> list[str]:
    refs = []
    if any(word in lowered for word in ("policy", "rules", "guideline", "checklist")):
        refs.append("checklist or policy reference")
    if any(word in lowered for word in ("examples", "cases", "experiment")):
        refs.append("examples and experiment rubric")
    if any(word in lowered for word in ("api", "schema", "database")):
        refs.append("API or schema reference")
    return refs


def infer_risks(lowered: str) -> list[str]:
    risks = []
    if "self" in lowered or "evolve" in lowered or "自进化" in lowered:
        risks.append("self-modification must be reviewable and consent-based")
    if "install" in lowered or "replace" in lowered:
        risks.append("installation or replacement needs explicit user confirmation")
    if "delete" in lowered or "destructive" in lowered:
        risks.append("destructive operations need strong approval gates")
    return risks


def make_skill_files(brief: str, out_dir: Path, name: str | None = None) -> Path:
    spec = distill_text(brief)
    skill_name = slugify(name or str(spec["candidate_name"]))
    skill_dir = out_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=False)
    (skill_dir / "agents").mkdir()
    (skill_dir / "references").mkdir()
    description = (
        f"Use when Codex needs to {spec['job_to_be_done'].rstrip('.')} "
        "and turn the workflow into repeatable, validated procedural knowledge."
    )
    skill_md = f"""---
name: {skill_name}
description: {description}
---

# {str(spec["display_name"])}

## Purpose

Capture the repeated workflow from the source brief and execute it with less rediscovery next time.

## Workflow

1. Inspect the current task and identify which parts match the source workflow.
2. Reuse the checklist in `references/checklist.md`.
3. Prefer existing project conventions and local tools.
4. Run the validation steps before claiming the work is complete.
5. Report changed files, checks run, and remaining risk.

## Validation

Use the checklist in `references/checklist.md`. Add task-specific tests when the change touches shared behavior or user-facing workflows.
"""
    checklist = "# Checklist\n\n"
    repeated = spec["repeated_steps"] or ["State the reusable workflow.", "Run at least one verification step."]
    checklist += "\n".join(f"- {item}" for item in repeated)
    checklist += "\n\n## Validation Plan\n\n"
    checklist += "\n".join(f"- {item}" for item in spec["validation_plan"])
    checklist += "\n"
    openai_yaml = f'''interface:
  display_name: "{str(spec["display_name"])}"
  short_description: "Reusable workflow captured as a Codex skill"
  default_prompt: "Use ${skill_name} to apply the captured workflow to this task."
'''
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (skill_dir / "references" / "checklist.md").write_text(checklist, encoding="utf-8")
    (skill_dir / "agents" / "openai.yaml").write_text(openai_yaml, encoding="utf-8")
    return skill_dir


def make_mutated_skill(brief: str, out_dir: Path, mutation: str, name: str | None = None) -> Path:
    if mutation not in MUTATION_PROFILES:
        raise ValueError(f"unknown mutation profile: {mutation}")
    profile = MUTATION_PROFILES[mutation]
    spec = distill_text(brief)
    base_name = slugify(name or str(spec["candidate_name"]))
    skill_name = slugify(f"{base_name}-{mutation}")
    skill_dir = out_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=False)
    (skill_dir / "agents").mkdir()
    (skill_dir / "references").mkdir()
    display = f"{str(spec['display_name'])} {profile['title']}"
    description = (
        f"Use when Codex needs to {spec['job_to_be_done'].rstrip('.')} with the {profile['title']} mutation: "
        "a reviewable, validated, consent-based workflow that can be tested before installation or replacement."
    )
    steps = "\n".join(f"{index}. {step}" for index, step in enumerate(profile["steps"], 1))
    risk_lines = spec["risk_flags"] or ["Confirm before installing, replacing, deleting, pushing, or mutating durable state."]
    risks = "\n".join(f"- {risk}" for risk in risk_lines)
    skill_md = f"""---
name: {skill_name}
description: {description}
---

# {display}

## Mutation Thesis

{profile["thesis"]}

## Workflow

{steps}

## Validation

1. Run a local audit of the generated or edited skill.
2. Test the workflow on at least one realistic case outside the original prompt.
3. Compare the result against a simpler baseline when a benchmark exists.
4. Record the commands, reports, and residual risk before recommending installation.

## Consent Gates

{risks}

## Lineage Notes

- Parent memory: {spec["job_to_be_done"]}
- Mutation: {mutation}
- Keep this skill only if it improves measured behavior or reduces future rediscovery.
"""
    checklist = "# Checklist\n\n"
    repeated = spec["repeated_steps"] or ["State the reusable workflow.", "Run at least one verification step."]
    checklist += "\n".join(f"- {item}" for item in repeated)
    checklist += "\n\n## Mutation Checks\n\n"
    checklist += "\n".join(f"- {step}" for step in profile["steps"])
    checklist += "\n"
    openai_yaml = f'''interface:
  display_name: "{display}"
  short_description: "Mutation-tested Codex skill candidate"
  default_prompt: "Use ${skill_name} to apply this mutation-tested workflow."
'''
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (skill_dir / "references" / "checklist.md").write_text(checklist, encoding="utf-8")
    for ref_name, ref_body in profile["references"].items():
        (skill_dir / "references" / ref_name).write_text(ref_body, encoding="utf-8")
    (skill_dir / "agents" / "openai.yaml").write_text(openai_yaml, encoding="utf-8")
    return skill_dir


def make_ascended_skill(brief: str, out_dir: Path, winners: list[dict[str, object]], name: str | None = None) -> Path:
    spec = distill_text(brief)
    skill_name = slugify(name or f"{spec['candidate_name']}-ascended")
    skill_dir = out_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=False)
    (skill_dir / "agents").mkdir()
    (skill_dir / "references").mkdir()
    winner_names = [str(winner["mutation"]) for winner in winners]
    inherited_steps: list[str] = []
    for winner in winners:
        profile = MUTATION_PROFILES[str(winner["mutation"])]
        inherited_steps.extend(profile["steps"][:3])
    deduped_steps = list(dict.fromkeys(inherited_steps))
    steps = "\n".join(f"{index}. {step}" for index, step in enumerate(deduped_steps[:8], 1))
    description = (
        f"Use when Codex needs to {spec['job_to_be_done'].rstrip('.')} through an evolved skill that inherits "
        f"the strongest measured traits from {', '.join(winner_names)} and keeps validation, lineage, and consent gates."
    )
    skill_md = f"""---
name: {skill_name}
description: {description}
---

# {str(spec["display_name"])} Ascended

## Evolution Thesis

This skill is not a first draft. It is the merged survivor of a small mutation arena. It should preserve the strongest measured behavior while keeping the work reviewable.

## Workflow

{steps}

## Validation

1. Run `pantheon.py audit` on the skill before installation.
2. Run the arena cases again when changing the workflow.
3. Compare the new score against the lineage report.
4. Keep rollback notes when replacing an installed skill.

## Consent Gates

- Confirm before installing or replacing a skill.
- Confirm before destructive file edits, remote writes, or repository state changes.
- Do not claim an evolution improved the skill unless the lineage report shows the measured delta.

## Lineage

Inherited mutations: {", ".join(winner_names)}
"""
    lineage = "# Lineage\n\n"
    lineage += "\n".join(f"- {winner['mutation']}: score {winner['score']}" for winner in winners)
    lineage += "\n"
    openai_yaml = f'''interface:
  display_name: "{str(spec["display_name"])} Ascended"
  short_description: "Arena-selected evolved Codex skill"
  default_prompt: "Use ${skill_name} to apply the arena-selected workflow."
'''
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (skill_dir / "references" / "lineage.md").write_text(lineage, encoding="utf-8")
    (skill_dir / "agents" / "openai.yaml").write_text(openai_yaml, encoding="utf-8")
    return skill_dir


def make_baseline_skill(brief: str, out_dir: Path, name: str | None = None) -> Path:
    skill_name = slugify(name or infer_skill_name(brief) + "-baseline")
    skill_dir = out_dir / skill_name
    skill_dir.mkdir(parents=True, exist_ok=False)
    (skill_dir / "agents").mkdir()
    skill_md = f"""---
name: {skill_name}
description: Helps with {first_sentence(brief)}
---

# {skill_name.replace("-", " ").title()}

Use this skill to help with the task described by the brief.
"""
    openai_yaml = f'''interface:
  display_name: "{skill_name.replace("-", " ").title()}"
  short_description: "Basic generated skill"
  default_prompt: "Use ${skill_name} for this task."
'''
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (skill_dir / "agents" / "openai.yaml").write_text(openai_yaml, encoding="utf-8")
    return skill_dir


def audit_skill(skill_dir: Path) -> list[Check]:
    checks: list[Check] = []
    skill_md = skill_dir / "SKILL.md"
    checks.append(Check("skill-dir-exists", skill_dir.is_dir(), str(skill_dir)))
    checks.append(Check("skill-md-exists", skill_md.is_file(), "required"))
    if not skill_md.is_file():
        return checks

    text = read_text(skill_md)
    frontmatter, body = parse_frontmatter(text)
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    checks.append(Check("frontmatter-name", bool(NAME_RE.match(name)), name or "missing"))
    checks.append(Check("frontmatter-description", len(description) >= 80 and "TODO" not in description, description[:120] or "missing"))
    checks.append(Check("frontmatter-only-name-description", set(frontmatter.keys()) == {"name", "description"}, ",".join(frontmatter.keys())))
    checks.append(Check("body-under-500-lines", len(body.splitlines()) <= 500, f"{len(body.splitlines())} lines"))
    checks.append(Check("no-todo-placeholders", "TODO" not in text and "[TODO" not in text, "placeholder scan"))

    openai = skill_dir / "agents" / "openai.yaml"
    if openai.exists():
        openai_text = read_text(openai)
        checks.append(Check("openai-default-prompt-mentions-skill", f"${name}" in openai_text, f"expects ${name}"))
    else:
        checks.append(Check("openai-yaml-exists", False, "agents/openai.yaml missing"))

    for script in sorted((skill_dir / "scripts").glob("*.py")) if (skill_dir / "scripts").is_dir() else []:
        try:
            compile(read_text(script), str(script), "exec")
            checks.append(Check(f"script-compiles:{script.name}", True, "ok"))
        except SyntaxError as exc:
            checks.append(Check(f"script-compiles:{script.name}", False, f"{exc.msg} at line {exc.lineno}"))

    readmes = list(skill_dir.glob("README*"))
    checks.append(Check("no-skill-readme-clutter", not readmes, ", ".join(p.name for p in readmes) or "ok"))
    return checks


def print_checks(checks: list[Check]) -> int:
    failed = [check for check in checks if not check.ok]
    for check in checks:
        status = "PASS" if check.ok else "FAIL"
        print(f"{status} {check.name}: {check.detail}")
    print(json.dumps({"passed": len(checks) - len(failed), "failed": len(failed)}, ensure_ascii=False))
    return 1 if failed else 0


def run_experiment(case_file: Path, workdir: Path) -> int:
    workdir.mkdir(parents=True, exist_ok=True)
    brief = read_text(case_file)
    exp_dir = Path(tempfile.mkdtemp(prefix="pantheon-", dir=str(workdir)))
    skill_dir = make_skill_files(brief, exp_dir)
    checks = audit_skill(skill_dir)
    report = {
        "case": str(case_file),
        "generated_skill": str(skill_dir),
        "checks": [check.__dict__ for check in checks],
        "score_hint": sum(1 for check in checks if check.ok),
    }
    report_path = exp_dir / "experiment-report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated: {skill_dir}")
    print(f"Report: {report_path}")
    return print_checks(checks)


def score_skill(skill_dir: Path) -> dict[str, object]:
    skill_md = read_text(skill_dir / "SKILL.md")
    frontmatter, body = parse_frontmatter(skill_md)
    description = frontmatter.get("description", "")
    refs = list((skill_dir / "references").glob("*")) if (skill_dir / "references").is_dir() else []
    scripts = list((skill_dir / "scripts").glob("*")) if (skill_dir / "scripts").is_dir() else []
    checks = audit_skill(skill_dir)

    categories = {
        "trigger_clarity": int(len(description) >= 80) + int(any(word in description.lower() for word in ("when", "use", "needs", "wants"))),
        "workflow_leverage": int("## Workflow" in body) + int(len(re.findall(r"^\d+\. ", body, flags=re.M)) >= 3),
        "resource_fit": int(bool(refs or scripts)) + int("references/" in body or "scripts/" in body),
        "validation_integrity": int("validation" in skill_md.lower()) + int(any(check.name.startswith("script-compiles") or check.name == "frontmatter-description" for check in checks)),
        "bounded_autonomy": int(any(word in skill_md.lower() for word in ("confirm", "consent", "approval", "review"))) + int("install" in skill_md.lower() or "destructive" in skill_md.lower()),
    }
    capped = {key: min(value, 2) for key, value in categories.items()}
    return {
        "skill": str(skill_dir),
        "score": sum(capped.values()),
        "categories": capped,
        "audit_failed": [check.name for check in checks if not check.ok],
    }


def load_jsonl(path: Path) -> list[dict[str, str]]:
    cases = []
    for i, line in enumerate(read_text(path).splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if "brief" not in item:
            raise ValueError(f"{path}:{i} missing 'brief'")
        cases.append(item)
    return cases


def run_benchmark(dataset: Path, workdir: Path, report_out: Path | None = None) -> int:
    cases = load_jsonl(dataset)
    if not cases:
        raise ValueError("dataset is empty")
    workdir.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="pantheon-benchmark-", dir=str(workdir)))
    rows = []
    for index, case in enumerate(cases, 1):
        case_dir = root / f"case-{index:02d}"
        baseline_dir = case_dir / "baseline"
        pantheon_dir = case_dir / "pantheon"
        baseline_dir.mkdir(parents=True)
        pantheon_dir.mkdir(parents=True)
        base_skill = make_baseline_skill(case["brief"], baseline_dir, f"{case.get('id', 'case')}-baseline")
        pan_skill = make_skill_files(case["brief"], pantheon_dir, f"{case.get('id', 'case')}-pantheon")
        rows.append({
            "id": case.get("id", f"case-{index}"),
            "baseline": score_skill(base_skill),
            "pantheon": score_skill(pan_skill),
        })
    summary = {
        "dataset": str(dataset),
        "workdir": str(root),
        "cases": len(rows),
        "baseline_avg": round(sum(row["baseline"]["score"] for row in rows) / len(rows), 2),
        "pantheon_avg": round(sum(row["pantheon"]["score"] for row in rows) / len(rows), 2),
        "rows": rows,
    }
    report = root / "benchmark-report.json"
    report.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Report: {report}")
    if report_out:
        report_out.parent.mkdir(parents=True, exist_ok=True)
        report_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Saved report: {report_out}")
    print(json.dumps({k: summary[k] for k in ("cases", "baseline_avg", "pantheon_avg")}, ensure_ascii=False))
    for row in rows:
        print(f"{row['id']}: baseline={row['baseline']['score']} pantheon={row['pantheon']['score']}")
    return 0 if summary["pantheon_avg"] > summary["baseline_avg"] else 1


def download_dataset(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    out.write_bytes(data)


def convert_public_dataset(raw_path: Path, dataset_format: str, out_path: Path, limit: int) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    if dataset_format == "alpaca-json":
        data = json.loads(read_text(raw_path))
        for index, item in enumerate(data[:limit], 1):
            instruction = str(item.get("instruction", "")).strip()
            input_text = str(item.get("input", "")).strip()
            if not instruction:
                continue
            brief = (
                "Create a Codex skill for a recurring instruction-following workflow. "
                f"The workflow request is: {instruction}"
            )
            if input_text:
                brief += f" Context example: {input_text}"
            brief += (
                " The skill should capture reusable steps, validation checks, and boundaries "
                "instead of copying a one-off answer."
            )
            rows.append({"id": f"alpaca-{index:04d}", "brief": brief})
    elif dataset_format == "prompts-csv":
        with raw_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for index, item in enumerate(reader, 1):
                if len(rows) >= limit:
                    break
                act = str(item.get("act", "")).strip()
                prompt = str(item.get("prompt", "")).strip()
                if not prompt:
                    continue
                brief = (
                    f"Create a Codex skill for the recurring role or workflow '{act}'. "
                    f"Source prompt: {prompt[:1000]} "
                    "The skill should turn the prompt into operational procedure, include validation, "
                    "and avoid pretending to be a human expert."
                )
                rows.append({"id": f"prompt-{index:04d}", "brief": brief})
    else:
        raise ValueError(f"unsupported public dataset format: {dataset_format}")

    with out_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def run_public_benchmark(name: str, limit: int, workdir: Path, report: Path | None) -> int:
    if name not in PUBLIC_DATASETS:
        choices = ", ".join(sorted(PUBLIC_DATASETS))
        raise ValueError(f"unknown dataset '{name}'. choices: {choices}")
    workdir.mkdir(parents=True, exist_ok=True)
    meta = PUBLIC_DATASETS[name]
    raw_path = workdir / f"{name}.raw"
    dataset_path = workdir / f"{name}.jsonl"
    download_dataset(str(meta["url"]), raw_path)
    count = convert_public_dataset(raw_path, str(meta["format"]), dataset_path, limit)
    print(f"Downloaded: {meta['url']}")
    print(f"Converted: {dataset_path} ({count} cases)")
    exit_code = run_benchmark(dataset_path, workdir / "runs")
    latest_reports = sorted((workdir / "runs").glob("pantheon-benchmark-*/benchmark-report.json"))
    if report and latest_reports:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(read_text(latest_reports[-1]), encoding="utf-8")
        print(f"Saved report: {report}")
    return exit_code


def report_label(path: Path, data: dict[str, object]) -> str:
    name = path.stem
    if "alpaca" in name:
        return "Stanford Alpaca"
    if "prompt" in name:
        return "awesome-chatgpt-prompts"
    if "builtin" in name:
        return "Built-in skill forge"
    dataset = str(data.get("dataset", ""))
    if "pantheon-benchmark" in dataset:
        return "Built-in skill forge"
    return name.replace("-", " ").title()


def load_report(path: Path) -> dict[str, object]:
    data = json.loads(read_text(path))
    for key in ("cases", "baseline_avg", "pantheon_avg"):
        if key not in data:
            raise ValueError(f"{path} missing {key}")
    return data


def generate_results_svg(report_paths: list[Path], out: Path, title: str = "Pantheon Benchmark Results") -> None:
    reports = [(report_label(path, load_report(path)), load_report(path)) for path in report_paths]
    if not reports:
        raise ValueError("at least one report is required")

    width = 1200
    height = 680
    chart_left = 108
    chart_right = 1092
    chart_top = 190
    chart_bottom = 500
    chart_height = chart_bottom - chart_top
    group_width = (chart_right - chart_left) / len(reports)
    bar_width = 48
    gap = 20
    max_score = 10
    total_cases = sum(int(data["cases"]) for _, data in reports)
    baseline_avg = sum(float(data["baseline_avg"]) * int(data["cases"]) for _, data in reports) / total_cases
    pantheon_avg = sum(float(data["pantheon_avg"]) * int(data["cases"]) for _, data in reports) / total_cases
    lift = pantheon_avg / baseline_avg if baseline_avg else 0

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">',
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#17151f"/>',
        '<stop offset="55%" stop-color="#222034"/>',
        '<stop offset="100%" stop-color="#30264a"/>',
        "</linearGradient>",
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">',
        '<feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#000" flood-opacity="0.25"/>',
        "</filter>",
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="34" fill="url(#bg)"/>',
        '<circle cx="1040" cy="100" r="82" fill="#f5c86a" opacity="0.10"/>',
        '<circle cx="132" cy="586" r="96" fill="#0969da" opacity="0.10"/>',
        f'<text x="64" y="76" fill="#f8f7ff" font-family="Inter, Arial, sans-serif" font-size="36" font-weight="850">{html.escape(title)}</text>',
        '<text x="64" y="112" fill="#c9c6d8" font-family="Inter, Arial, sans-serif" font-size="16">Naive templates vs Pantheon-generated skills across built-in and public benchmark samples.</text>',
    ]

    metric_x = 720
    metrics = [
        ("Cases", str(total_cases)),
        ("Pantheon avg", f"{pantheon_avg:.2f}/10"),
        ("Lift", f"{lift:.1f}x"),
    ]
    for i, (label, value) in enumerate(metrics):
        x = metric_x + i * 142
        parts.extend([
            f'<rect x="{x}" y="50" width="126" height="76" rx="18" fill="#ffffff" opacity="0.08" filter="url(#shadow)"/>',
            f'<text x="{x + 18}" y="79" fill="#c9c6d8" font-family="Inter, Arial, sans-serif" font-size="13">{label}</text>',
            f'<text x="{x + 18}" y="108" fill="#f5c86a" font-family="Inter, Arial, sans-serif" font-size="25" font-weight="850">{value}</text>',
        ])

    parts.append(f'<line x1="{chart_left}" y1="{chart_bottom}" x2="{chart_right}" y2="{chart_bottom}" stroke="#ffffff" stroke-opacity="0.22"/>')
    for score in range(0, 11, 2):
        y = chart_bottom - (score / max_score) * chart_height
        parts.append(f'<line x1="{chart_left}" y1="{y:.1f}" x2="{chart_right}" y2="{y:.1f}" stroke="#ffffff" stroke-opacity="0.08"/>')
        parts.append(f'<text x="{chart_left - 28}" y="{y + 5:.1f}" text-anchor="end" fill="#aaa6bd" font-family="Inter, Arial, sans-serif" font-size="12">{score}</text>')

    for index, (label, data) in enumerate(reports):
        center = chart_left + group_width * index + group_width / 2
        baseline = float(data["baseline_avg"])
        pantheon = float(data["pantheon_avg"])
        base_h = baseline / max_score * chart_height
        pan_h = pantheon / max_score * chart_height
        base_x = center - bar_width - gap / 2
        pan_x = center + gap / 2
        base_y = chart_bottom - base_h
        pan_y = chart_bottom - pan_h
        label_lines = split_label(label)
        parts.extend([
            f'<rect x="{base_x}" y="{base_y:.1f}" width="{bar_width}" height="{base_h:.1f}" rx="10" fill="#7d7894"/>',
            f'<rect x="{pan_x}" y="{pan_y:.1f}" width="{bar_width}" height="{pan_h:.1f}" rx="10" fill="#f5c86a"/>',
            f'<text x="{base_x + bar_width / 2}" y="{base_y - 10:.1f}" text-anchor="middle" fill="#d8d5e6" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="700">{baseline:.2f}</text>',
            f'<text x="{pan_x + bar_width / 2}" y="{pan_y - 10:.1f}" text-anchor="middle" fill="#f5c86a" font-family="Inter, Arial, sans-serif" font-size="14" font-weight="800">{pantheon:.2f}</text>',
        ])
        for line_index, line in enumerate(label_lines):
            parts.append(f'<text x="{center}" y="{chart_bottom + 36 + line_index * 18}" text-anchor="middle" fill="#f8f7ff" font-family="Inter, Arial, sans-serif" font-size="14">{html.escape(line)}</text>')
        parts.append(f'<text x="{center}" y="{chart_bottom + 92}" text-anchor="middle" fill="#9a96ad" font-family="Inter, Arial, sans-serif" font-size="12">{int(data["cases"])} cases</text>')

    parts.extend([
        '<rect x="760" y="590" width="16" height="16" rx="4" fill="#7d7894"/>',
        '<text x="784" y="603" fill="#c9c6d8" font-family="Inter, Arial, sans-serif" font-size="14">Naive baseline</text>',
        '<rect x="920" y="590" width="16" height="16" rx="4" fill="#f5c86a"/>',
        '<text x="944" y="603" fill="#c9c6d8" font-family="Inter, Arial, sans-serif" font-size="14">Pantheon</text>',
        '<text x="64" y="620" fill="#9a96ad" font-family="Inter, Arial, sans-serif" font-size="13">Repeatable audit scores, not a universal quality claim.</text>',
        "</svg>",
    ])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts), encoding="utf-8")


def split_label(label: str) -> list[str]:
    words = label.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > 18 and current:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines[:3]


def run_evolution(brief_path: Path, workdir: Path, out_report: Path | None, out_svg: Path | None, variants: int) -> int:
    brief = read_text(brief_path)
    workdir.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="pantheon-evolve-", dir=str(workdir)))
    baseline_dir = root / "baseline"
    variants_dir = root / "variants"
    ascended_dir = root / "ascended"
    baseline_dir.mkdir()
    variants_dir.mkdir()
    ascended_dir.mkdir()

    baseline = make_skill_files(brief, baseline_dir, "generation-0-seed")
    baseline_score = score_skill(baseline)
    mutation_names = list(MUTATION_PROFILES)[: max(1, min(variants, len(MUTATION_PROFILES)))]
    candidates = []
    for mutation in mutation_names:
        skill = make_mutated_skill(brief, variants_dir, mutation, "generation-1")
        scored = score_skill(skill)
        candidates.append({
            "mutation": mutation,
            "skill": str(skill),
            "score": scored["score"],
            "categories": scored["categories"],
            "audit_failed": scored["audit_failed"],
        })
    candidates.sort(key=lambda item: (int(item["score"]), str(item["mutation"])), reverse=True)
    winners = candidates[:2]
    ascended = make_ascended_skill(brief, ascended_dir, winners, "generation-2-ascended")
    ascended_score = score_skill(ascended)
    report = {
        "brief": str(brief_path),
        "workdir": str(root),
        "thesis": "Skills improve by digital evolution: fork variants, run an arena, select winners, merge traits, preserve lineage.",
        "generation_0": {
            "kind": "seed",
            "skill": str(baseline),
            "score": baseline_score["score"],
            "categories": baseline_score["categories"],
        },
        "generation_1": candidates,
        "selection": {
            "winners": [{"mutation": winner["mutation"], "score": winner["score"], "skill": winner["skill"]} for winner in winners],
            "rule": "Select the top two audited variants by score, then merge their strongest procedural traits.",
        },
        "generation_2": {
            "kind": "ascended",
            "skill": str(ascended),
            "score": ascended_score["score"],
            "categories": ascended_score["categories"],
            "audit_failed": ascended_score["audit_failed"],
        },
    }
    report_path = out_report or (root / "evolution-report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Evolution report: {report_path}")
    if out_svg:
        generate_evolution_svg(report, out_svg)
        print(f"Evolution chart: {out_svg}")
    print(json.dumps({
        "seed_score": baseline_score["score"],
        "best_variant": winners[0]["mutation"],
        "best_variant_score": winners[0]["score"],
        "ascended_score": ascended_score["score"],
    }, ensure_ascii=False))
    return 0 if int(ascended_score["score"]) >= int(baseline_score["score"]) else 1


def generate_evolution_svg(report: dict[str, object], out: Path) -> None:
    width = 1200
    height = 680
    gen0 = report["generation_0"]  # type: ignore[index]
    gen1 = report["generation_1"]  # type: ignore[index]
    gen2 = report["generation_2"]  # type: ignore[index]
    candidates = list(gen1)  # type: ignore[arg-type]
    max_score = 10
    seed_score = int(gen0["score"])  # type: ignore[index]
    asc_score = int(gen2["score"])  # type: ignore[index]
    best = max(candidates, key=lambda item: int(item["score"]))

    chart_top = 220
    chart_bottom = 510
    chart_height = chart_bottom - chart_top

    def bar_h(score: int) -> float:
        return score / max_score * chart_height

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Pantheon skill evolution lineage">',
        "<defs>",
        '<linearGradient id="evoBg" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0%" stop-color="#111018"/>',
        '<stop offset="50%" stop-color="#211f33"/>',
        '<stop offset="100%" stop-color="#34264f"/>',
        "</linearGradient>",
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L8,3 z" fill="#f5c86a"/></marker>',
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="34" fill="url(#evoBg)"/>',
        '<text x="64" y="72" fill="#f8f7ff" font-family="Inter, Arial, sans-serif" font-size="36" font-weight="850">Skill Evolution Arena</text>',
        '<text x="64" y="108" fill="#c9c6d8" font-family="Inter, Arial, sans-serif" font-size="16">Fork variants, score them, select winners, merge traits, preserve lineage.</text>',
        '<text x="82" y="164" fill="#f5c86a" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="800">Generation 0</text>',
        '<text x="392" y="164" fill="#f5c86a" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="800">Generation 1: Mutations</text>',
        '<text x="960" y="164" fill="#f5c86a" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="800">Generation 2</text>',
        f'<line x1="72" y1="{chart_bottom}" x2="1128" y2="{chart_bottom}" stroke="#ffffff" stroke-opacity="0.18"/>',
    ]
    seed_h = bar_h(seed_score)
    parts.extend([
        '<rect x="82" y="196" width="180" height="350" rx="26" fill="#ffffff" opacity="0.08"/>',
        '<text x="172" y="238" text-anchor="middle" fill="#f8f7ff" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="800">Seed Skill</text>',
        f'<rect x="144" y="{chart_bottom - seed_h:.1f}" width="56" height="{seed_h:.1f}" rx="12" fill="#7d7894"/>',
        f'<text x="172" y="{chart_bottom - seed_h - 12:.1f}" text-anchor="middle" fill="#d8d5e6" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="800">{seed_score}/10</text>',
        '<text x="172" y="574" text-anchor="middle" fill="#aaa6bd" font-family="Inter, Arial, sans-serif" font-size="13">initial draft</text>',
    ])
    start_x = 342
    for index, candidate in enumerate(candidates):
        x = start_x + index * 112
        score = int(candidate["score"])
        h = bar_h(score)
        color = "#f5c86a" if candidate is best else "#0969da"
        mutation = str(candidate["mutation"]).title()
        parts.extend([
            f'<rect x="{x}" y="196" width="86" height="350" rx="20" fill="#ffffff" opacity="0.07"/>',
            f'<rect x="{x + 22}" y="{chart_bottom - h:.1f}" width="42" height="{h:.1f}" rx="10" fill="{color}"/>',
            f'<text x="{x + 43}" y="{chart_bottom - h - 10:.1f}" text-anchor="middle" fill="{color}" font-family="Inter, Arial, sans-serif" font-size="15" font-weight="800">{score}</text>',
            f'<text x="{x + 43}" y="574" text-anchor="middle" fill="#f8f7ff" font-family="Inter, Arial, sans-serif" font-size="13">{html.escape(mutation)}</text>',
        ])
    asc_h = bar_h(asc_score)
    parts.extend([
        '<rect x="954" y="196" width="184" height="350" rx="28" fill="#f5c86a" opacity="0.14" stroke="#f5c86a" stroke-opacity="0.58"/>',
        '<text x="1046" y="238" text-anchor="middle" fill="#f8f7ff" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="850">Ascended</text>',
        f'<rect x="1018" y="{chart_bottom - asc_h:.1f}" width="56" height="{asc_h:.1f}" rx="12" fill="#f5c86a"/>',
        f'<text x="1046" y="{chart_bottom - asc_h - 12:.1f}" text-anchor="middle" fill="#f5c86a" font-family="Inter, Arial, sans-serif" font-size="18" font-weight="850">{asc_score}/10</text>',
        '<text x="1046" y="574" text-anchor="middle" fill="#f8f7ff" font-family="Inter, Arial, sans-serif" font-size="13">merged survivor</text>',
    ])
    parts.extend([
        '<line x1="276" y1="350" x2="320" y2="350" stroke="#f5c86a" stroke-width="4" marker-end="url(#arrow)" opacity="0.9"/>',
        '<line x1="906" y1="350" x2="942" y2="350" stroke="#f5c86a" stroke-width="4" marker-end="url(#arrow)" opacity="0.9"/>',
        '<text x="64" y="626" fill="#c9c6d8" font-family="Inter, Arial, sans-serif" font-size="15">Selection rule: top audited variants are merged into the ascended skill.</text>',
        '<text x="64" y="652" fill="#9a96ad" font-family="Inter, Arial, sans-serif" font-size="13">Bounded evolution means fork, score, select, merge, and record lineage before replacing anything durable.</text>',
        "</svg>",
    ])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(parts), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bounded evolution tools for Codex skills.")
    sub = parser.add_subparsers(dest="command", required=True)

    distill = sub.add_parser("distill", help="Distill a brief or transcript into a skill proposal.")
    distill.add_argument("--input", required=True, type=Path)

    scaffold = sub.add_parser("scaffold", help="Create a draft skill from a brief.")
    scaffold.add_argument("--brief", required=True, type=Path)
    scaffold.add_argument("--out", required=True, type=Path)
    scaffold.add_argument("--name")

    audit = sub.add_parser("audit", help="Audit a skill directory.")
    audit.add_argument("skill_dir", type=Path)

    exp = sub.add_parser("experiment", help="Run a scaffold-and-audit experiment.")
    exp.add_argument("--case", required=True, type=Path)
    exp.add_argument("--workdir", type=Path, default=Path(tempfile.gettempdir()) / "pantheon-experiments")

    bench = sub.add_parser("benchmark", help="Compare naive skill generation against Pantheon generation.")
    bench.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parents[1] / "experiments" / "pantheon-benchmark.jsonl")
    bench.add_argument("--workdir", type=Path, default=Path(tempfile.gettempdir()) / "pantheon-benchmarks")
    bench.add_argument("--report", type=Path)

    dl = sub.add_parser("download-dataset", help="Download a JSONL benchmark dataset for later benchmark runs.")
    dl.add_argument("--url", required=True)
    dl.add_argument("--out", required=True, type=Path)

    public = sub.add_parser("benchmark-public", help="Download and benchmark a supported public dataset sample.")
    public.add_argument("--name", choices=sorted(PUBLIC_DATASETS), required=True)
    public.add_argument("--limit", type=int, default=12)
    public.add_argument("--workdir", type=Path, default=Path(tempfile.gettempdir()) / "pantheon-public")
    public.add_argument("--report", type=Path)

    plot = sub.add_parser("plot-reports", help="Render benchmark reports into a GitHub-friendly SVG chart.")
    plot.add_argument("--report", action="append", required=True, type=Path)
    plot.add_argument("--out", required=True, type=Path)
    plot.add_argument("--title", default="Pantheon Benchmark Results")

    evolve = sub.add_parser("evolve", help="Fork skill variants, score them in an arena, merge winners, and write lineage.")
    evolve.add_argument("--brief", required=True, type=Path)
    evolve.add_argument("--workdir", type=Path, default=Path(tempfile.gettempdir()) / "pantheon-evolution")
    evolve.add_argument("--report", type=Path)
    evolve.add_argument("--svg", type=Path)
    evolve.add_argument("--variants", type=int, default=5)

    args = parser.parse_args(argv)
    if args.command == "distill":
        print(json.dumps(distill_text(read_text(args.input)), indent=2, ensure_ascii=False))
        return 0
    if args.command == "scaffold":
        skill_dir = make_skill_files(read_text(args.brief), args.out, args.name)
        print(skill_dir)
        return 0
    if args.command == "audit":
        return print_checks(audit_skill(args.skill_dir))
    if args.command == "experiment":
        return run_experiment(args.case, args.workdir)
    if args.command == "benchmark":
        return run_benchmark(args.dataset, args.workdir, args.report)
    if args.command == "download-dataset":
        download_dataset(args.url, args.out)
        print(args.out)
        return 0
    if args.command == "benchmark-public":
        return run_public_benchmark(args.name, args.limit, args.workdir, args.report)
    if args.command == "plot-reports":
        generate_results_svg(args.report, args.out, args.title)
        print(args.out)
        return 0
    if args.command == "evolve":
        return run_evolution(args.brief, args.workdir, args.report, args.svg, args.variants)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
