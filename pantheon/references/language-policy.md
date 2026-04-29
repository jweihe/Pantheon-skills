# Pantheon Language Policy

Use this reference when creating localized or multilingual skill artifacts.

## Default

Match the user's language for explanations, README text, reports, and generated examples.

Keep machine-facing fields stable:

- `name` must stay lowercase ASCII hyphen-case.
- YAML keys must stay English.
- Script commands, file paths, JSON keys, and CLI flags should stay ASCII unless the target tool explicitly supports localization.

## Skill Body

For `SKILL.md`, prefer one primary language per generated skill. Use bilingual sections only when the user asks for them or the target team is multilingual.

For bilingual skill bodies:

- Put the operational rule first.
- Keep translated paragraphs adjacent, not in distant mirrored sections.
- Avoid doubling long examples; translate the explanation, not every log line.

## README And Reports

For public projects, prefer:

- `README.md` in English.
- `README.zh-CN.md` for Simplified Chinese.
- Cross-links near the top of both files.

For experiment reports, keep raw JSON keys in English and put human commentary in the requested language.

## Localization Quality Bar

A localized skill is ready only when:

- The trigger description remains precise after translation.
- The operational steps are not softened into vague advice.
- Consent, validation, and destructive-action warnings are preserved.
- The romantic voice does not obscure commands, file paths, or pass/fail criteria.
