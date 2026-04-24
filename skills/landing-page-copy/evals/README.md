# Landing Page Copy Evals

This directory contains two eval sets for the `landing-page-copy` skill.

## Files

### `trigger-evals.json`
Use this to test whether the skill description triggers in the right situations.
- `should_trigger: true` = the skill should activate
- `should_trigger: false` = a near miss or adjacent task that should usually use another skill or no skill

This set intentionally mixes:
- landing page and homepage copy requests
- hero/CTA/FAQ/proof rewrite requests
- near misses like design-only critique, grammar-only proofreading, implementation-only, and visual token extraction

### `review-evals.json`
Use this to test output quality after the skill triggers.
Each eval includes:
- a realistic prompt
- an `expected_output` summary
- `must_include_concepts` to help later grading

These prompts are written to test whether the skill:
- writes with clearer audience and offer specificity
- explains mechanism instead of leaning on puffery
- uses proof and CTA posture appropriately
- avoids generic startup or consultant filler
- can improve existing copy without flattening what already works
