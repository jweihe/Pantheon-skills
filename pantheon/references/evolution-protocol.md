# Pantheon Evolution Protocol

Use this protocol when creating or changing a Codex skill.

## Evolution Contract

Pantheon may propose changes, generate drafts, and run experiments. It must not silently alter an installed skill or claim validation that was not run.

## Inputs

Collect the smallest useful set:

- The user request or repeated workflow.
- One or more concrete examples.
- Existing files, APIs, commands, or policies the skill must remember.
- The desired installation target, if known.

## Output Shape

Every generated skill should include:

- `SKILL.md` with only `name` and `description` in YAML frontmatter.
- `agents/openai.yaml` with `display_name`, `short_description`, and `default_prompt`.
- `scripts/` only for deterministic operations that would otherwise be rewritten.
- `references/` only for details that are useful but too large for the main skill body.
- `assets/` only for reusable output resources.

## Mutation Levels

Use the least powerful mutation that solves the problem:

1. **Annotation**: Add a reference note or example.
2. **Procedure patch**: Tighten or reorder steps in `SKILL.md`.
3. **Resource extraction**: Move bulky detail to `references/` or deterministic work to `scripts/`.
4. **Capability split**: Create a new skill when a responsibility becomes independently useful.
5. **Core rewrite**: Replace the workflow only when real usage shows the old one fails.

## Consent Gate

Before installing or replacing a skill, report:

- What changed.
- Why the change is worth keeping.
- What validation ran.
- What residual risk remains.

Then wait for explicit user confirmation if the target is outside the current project or replaces an existing installed skill.

## Failure Signs

Revise the skill if any of these appear:

- The description is poetic but does not trigger the right tasks.
- The body explains obvious model behavior instead of project-specific procedure.
- The skill requires reading too much context before doing simple work.
- A script writes outside its requested output directory.
- Experiments cannot distinguish success from a pleasant-looking artifact.
