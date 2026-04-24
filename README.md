# crap-skills

> Blunt anti-generic skills for people who are tired of fake-premium landing pages, faceless copy, and brand work that looks expensive but says nothing.

`crap-skills` packages reusable review skills for homepage, landing-page, mockup, and brand-direction critique.

## Included skills

### `brand-review`
Combined copy + visual critique for:
- faceless audience language
- mechanism-free promises
- weak proof
- gradient sludge
- fake premium glass
- anonymous SaaS card grids
- dribbblified hierarchy
- route collapse across variants

Produces:
- harsh but useful critique
- concrete copy edits
- concrete visual edits
- variant differentiation guidance
- repo-native test ideas when the work is code-backed

### `generic-crap-review`
Copy-focused critique for:
- vague claims
- presentation/meta wording
- generic CTA posture
- weak proof density
- faceless audience language

### `anti-generic-visual-review`
Visual-focused critique for:
- gradient sludge
- fake premium glass
- decorative card grids
- AI-uncanny imagery
- weak visual ownability
- dribbblified hierarchy

### `landing-page-copy`
Externally grounded landing-page/homepage copy skill synthesized from baseline skills for conversion structure and research-first copy discipline.

### `visual-style-guide-copy`
Externally grounded skill for writing brand-guideline and visual-style-guide copy that is structured, practical, and usable by real teams.

## Why this repo exists

A lot of review feedback is too vague to be useful:
- “make it more premium”
- “this feels AI-generated”
- “can we make it feel stronger?”
- “it looks polished but something is off”

This repo turns that hand-wavy discomfort into:
- named failure modes
- repeatable critique structure
- concrete edits
- reusable eval prompts
- packaging guidance for future skills

## Quick start

Read the main skill:
- `skills/brand-review/SKILL.md`

Then use supporting references:
- `skills/brand-review/references/copy-checklist.md`
- `skills/brand-review/references/visual-checklist.md`
- `skills/brand-review/references/test-template.md`
- `skills/brand-review/references/redesign-prompts.md`

## Examples

See `examples/` for reusable prompt sets, including:
- education landing page sludge
- AI startup template hero
- variant collapse
- strong copy / weak surface
- strong surface / weak copy
- repo-native Vitest angle

## Eval status

Packaged Codex proxy snapshots:
- trigger eval: **20/20 pass**
- review eval: **8/8 pass**

Run them from repo root:

```bash
python skills/brand-review/evals/codex_trigger_eval.py
python skills/brand-review/evals/codex_review_eval.py
```

## Skill-building workflow

This repo also packages a reusable skill creation/eval workflow under:
- `scap-creator/`

Use it for:
- writing new skills
- building eval prompts
- distinguishing skill weakness from grader brittleness
- packaging skills for reuse

Start here:
- `scap-creator/README.md`
- `scap-creator/references/workflow-checklist.md`
- `scap-creator/references/eval-schemas.md`

## Repo structure

```text
skills/
  brand-review/
  generic-crap-review/
  anti-generic-visual-review/
  landing-page-copy/
  visual-style-guide-copy/
examples/
scap-creator/
CONTRIBUTING.md
```

## Contributing

See `CONTRIBUTING.md`.

## Intent

This is for people who are tired of:
- generic landing page crap
- fake premium startup polish
- interchangeable variants
- consultant-filler copy
- visual moodboards pretending to be product clarity
