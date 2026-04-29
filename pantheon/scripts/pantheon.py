#!/usr/bin/env python3
"""Pantheon: bounded evolution tools for Codex skills."""

from __future__ import annotations

import argparse
import csv
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


def run_benchmark(dataset: Path, workdir: Path) -> int:
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

    dl = sub.add_parser("download-dataset", help="Download a JSONL benchmark dataset for later benchmark runs.")
    dl.add_argument("--url", required=True)
    dl.add_argument("--out", required=True, type=Path)

    public = sub.add_parser("benchmark-public", help="Download and benchmark a supported public dataset sample.")
    public.add_argument("--name", choices=sorted(PUBLIC_DATASETS), required=True)
    public.add_argument("--limit", type=int, default=12)
    public.add_argument("--workdir", type=Path, default=Path(tempfile.gettempdir()) / "pantheon-public")
    public.add_argument("--report", type=Path)

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
        return run_benchmark(args.dataset, args.workdir)
    if args.command == "download-dataset":
        download_dataset(args.url, args.out)
        print(args.out)
        return 0
    if args.command == "benchmark-public":
        return run_public_benchmark(args.name, args.limit, args.workdir, args.report)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
