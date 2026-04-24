# Visual Style Guide Copy Evals

This directory contains two eval sets for the `visual-style-guide-copy` skill.

## Files

### `trigger-evals.json`
Use this to test whether the skill description triggers in the right situations.
- `should_trigger: true` = the skill should activate
- `should_trigger: false` = a near miss or adjacent task that should usually use another skill or no skill

This set intentionally mixes:
- brand guideline and style guide requests
- logo/color/type/imagery/voice documentation requests
- near misses like homepage copywriting, implementation work, pure design critique, and code-only token extraction

### `review-evals.json`
Use this to test output quality after the skill triggers.
Each eval includes:
- a realistic prompt
- an `expected_output` summary
- `must_include_concepts` to help later grading

These prompts are written to test whether the skill:
- creates usable guideline structure instead of fluffy brand theater
- writes reference-friendly rules with practical examples
- handles both full-guide and section-rewrite cases
- balances discipline with readability
