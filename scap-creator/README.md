# scap-creator

`scap-creator` packages the workflow for creating, testing, and iterating on skills.

The name here is a lightweight repo-local packaging label for **skill capture + skill assessment + packaging**.

## What it is for

Use this workflow when you want to:
- turn an ad hoc review pattern into a reusable skill
- improve an existing skill's wording or trigger behavior
- write eval prompts for a skill
- compare outputs before and after a skill change
- reduce brittle eval grading
- package a skill for reuse in another repo

## Workflow

### 1. Capture the workflow
Write down:
- what the skill should do
- when it should trigger
- what a strong output looks like
- what failure modes it should catch
- what reference files help it stay sharp

### 2. Optionally search skills.sh for a baseline
If the problem looks reusable or common, search for existing skills before writing from scratch.

Use this step to:
- avoid reinventing an already-good skill
- inspect proven trigger wording
- inspect useful structure and references
- decide whether an external skill is good enough to adopt, adapt, or just compare against

Recommended flow:
- search skills.sh with 1-3 focused queries
- identify 1-3 high-signal candidate skills
- install or read the top candidates
- decide: **adopt**, **adapt**, **use as baseline only**, or **ignore and build greenfield**

Guardrails:
- treat external skills as input, not authority
- do not blindly copy them
- prefer the most relevant, highest-signal candidates
- record what you searched, what you selected, and why
- skip this step when the task is highly repo-specific or obviously custom

### 3. Write the skill
Create a `SKILL.md` with:
- YAML frontmatter
- pushy trigger description
- review/decision model
- explicit output format
- references the model should read when needed

### 4. Write eval prompts
Create realistic prompts that sound like real users.

At minimum, include:
- positive trigger cases
- negative trigger cases
- quality/output cases
- at least one positive control where the skill should stay balanced

### 5. Run evals
For the packaged `brand-review` skill in this repo:

```bash
python skills/brand-review/evals/codex_trigger_eval.py
python skills/brand-review/evals/codex_review_eval.py
```

When relevant, use more than one baseline:
- no skill
- the previous version of your skill
- the best external baseline skill you found via skills.sh

This gives you a stronger comparison than only asking whether the newest draft seems good in isolation.

For Anthropic's `skill-creator` tooling, use **module invocation**, not direct script execution:

```bash
cd .agents/skills/skill-creator
python -m scripts.run_eval --help
python -m scripts.run_loop --help
```

### 6. Inspect the misses
When an eval fails, separate the cause:
- skill weakness
- grader brittleness
- prompt ambiguity
- tool/runtime failure

Do not assume every failure means the skill is bad.

### 7. Tighten surgically
Prefer minimal changes:
- improve the skill wording only where it is soft or vague
- improve the grader only where it misses clear semantic equivalents
- keep eval prompts realistic

### 8. Package the skill
A reusable package should include:
- the skill
- its reference docs
- eval prompts
- eval runner scripts
- result snapshots if useful
- examples showing how to use it

## Notes from this repo's workflow

The `brand-review` package here was validated with a Codex proxy loop:
- trigger eval: 20/20 pass
- review eval: 8/8 pass

Key lesson:
- output grading for qualitative skills should use **semantic buckets**, not fragile exact phrase matching.

## Included references

- `references/eval-schemas.md`
- `references/workflow-checklist.md`
