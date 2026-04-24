# Brand Review Evals

This directory contains two eval sets for the `brand-review` skill.

## Files

### `trigger-evals.json`
Use this to test whether the skill description triggers in the right situations.
- `should_trigger: true` = the skill should activate
- `should_trigger: false` = a near miss or adjacent task that should usually use another skill or no skill

This set intentionally mixes:
- homepage and landing-page critiques
- screenshot / Figma / code-backed brand review prompts
- near misses like accessibility-only, implementation-only, grammar-only, and test-only tasks

### `review-evals.json`
Use this to test output quality after the skill triggers.
Each eval includes:
- a realistic prompt
- an `expected_output` summary
- `must_include_concepts` to help later grading

These prompts are written to test the tone you asked for:
- harsh on gradient sludge and fake premium visuals
- harsh on faceless audience language and mechanism-free copy
- still able to acknowledge what works when the design is actually strong

## Suggested next step

If you want, the next move is to:
1. run description-trigger evaluation against `trigger-evals.json`
2. run qualitative skill-output evaluation against `review-evals.json`
3. add grading assertions for the `must_include_concepts`
4. optimize the skill description if trigger accuracy is weak
