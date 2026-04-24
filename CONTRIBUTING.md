# Contributing

Thanks for improving `crap-skills`.

## What belongs here

This repo is for reusable skills and workflow docs that help reviewers catch:
- generic copy
- fake premium visual treatment
- weak proof
- faceless audience language
- route collapse across variants
- vague or AI-slop brand work

## Repo layout

- `skills/brand-review/` — combined copy + visual critique skill
- `skills/generic-crap-review/` — copy-focused critique skill
- `skills/anti-generic-visual-review/` — visual-focused critique skill
- `examples/` — reusable prompt sets
- `scap-creator/` — packaged workflow docs for creating and evaluating skills

## Contribution rules

1. Keep the tone blunt, but useful.
2. Prefer concrete language over generic consultant phrasing.
3. When adding evals, write realistic prompts, not toy prompts.
4. If you tighten a grader, prefer semantic buckets over brittle exact-string checks.
5. Do not weaken a detector just because it found a real issue.

## Running the packaged evals

From repo root:

```bash
python skills/brand-review/evals/codex_trigger_eval.py
python skills/brand-review/evals/codex_review_eval.py
```

These produce:
- `skills/brand-review/evals/codex-trigger-results.json`
- `skills/brand-review/evals/codex-review-results.json`

## Working on new or modified skills

Use the `scap-creator` docs for the workflow:
1. draft the skill
2. write realistic eval prompts
3. run the eval loop
4. inspect outputs and grading
5. refine wording and grading buckets
6. rerun until the skill is sharp

## Pull requests

Good PRs usually include:
- the skill change itself
- updated examples if behavior changed
- updated evals if coverage changed
- regenerated result snapshots if relevant
- a short note explaining what became sharper and why
