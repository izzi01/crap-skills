# Eval Schemas

This is a compact packaging of the most useful schema ideas from the original skill-creator workflow.

## `evals.json`

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "review-01",
      "prompt": "Realistic user prompt",
      "expected_output": "What a good answer should do",
      "must_include_concepts": ["audience gaps", "proof gaps"],
      "files": []
    }
  ]
}
```

### Fields
- `skill_name`: must match the skill package
- `evals[].id`: stable eval identifier
- `evals[].prompt`: realistic user request
- `evals[].expected_output`: human-readable success description
- `evals[].must_include_concepts`: concepts or semantic buckets the grader should look for
- `evals[].files`: optional input files

## Result snapshot shape

```json
{
  "skill_name": "example-skill",
  "mode": "codex-proxy-output-eval",
  "summary": {
    "total": 8,
    "passed": 8,
    "failed": 0,
    "pass_rate": 1.0
  },
  "results": [
    {
      "id": "review-01",
      "prompt": "...",
      "output": "...",
      "grading": {
        "concept_hits": ["audience gaps"],
        "concept_misses": [],
        "concept_pass_rate": 1.0,
        "harsh_hit_count": 4,
        "used_expected_structure": true,
        "passes": true
      }
    }
  ]
}
```

## Practical grading guidance

For qualitative skills:
- prefer semantic buckets
- avoid exact phrase dependence when synonyms mean the same thing
- still keep some structure checks so the skill does not drift
- distinguish between concept misses and runtime failures
