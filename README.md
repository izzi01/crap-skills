# crap-skills

Blunt anti-generic brand review skills for catching homepage, landing-page, and mockup work that feels templatey, AI-generated, overpolished, or interchangeable.

## Included

### `brand-review`
A combined copy + visual critique skill for:
- faceless audience language
- mechanism-free promises
- weak proof
- gradient sludge
- fake premium glass
- anonymous SaaS card grids
- dribbblified hierarchy
- route collapse across variants

It is designed to produce:
- harsh but useful brand critique
- concrete copy and visual edits
- differentiation guidance across variants
- repo-native test ideas when the work is code-backed

### `generic-crap-review`
A focused copy-review skill for catching:
- faceless audience language
- vague claims
- presentation/meta wording
- weak proof density
- generic CTA posture

### `anti-generic-visual-review`
A focused visual-review skill for catching:
- gradient sludge
- fake premium glass
- decorative card grids
- AI-uncanny imagery
- dribbblified hierarchy
- weak visual ownability


## Repo structure

```text
skills/
  brand-review/
    SKILL.md
    references/
    evals/
  generic-crap-review/
    SKILL.md
    references/
  anti-generic-visual-review/
    SKILL.md
    references/
examples/
```

## Evaluation artifacts

This repo includes Codex-based proxy eval scaffolding and result snapshots for:
- trigger selection
- review/output quality

Current packaged snapshots:
- trigger eval: 20/20 pass
- review eval: 8/8 pass

## Usage

Read and apply:
- `skills/brand-review/SKILL.md`

Helpful supporting docs:
- `skills/brand-review/references/copy-checklist.md`
- `skills/brand-review/references/visual-checklist.md`
- `skills/brand-review/references/test-template.md`
- `skills/brand-review/references/redesign-prompts.md`

Run evals:

```bash
python skills/brand-review/evals/codex_trigger_eval.py
python skills/brand-review/evals/codex_review_eval.py
```

## Intent

This is for people who are tired of:
- generic landing page crap
- fake premium startup polish
- interchangeable variants
- brand work that looks expensive but says nothing

## Examples

See `examples/` for reusable prompt sets for all three packaged skills.
