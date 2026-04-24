# Workflow Checklist

## Baseline search (optional)
- [ ] Did we search skills.sh if the problem looked reusable/common?
- [ ] Did we check 1-3 high-signal candidates instead of blindly taking the first result?
- [ ] Did we decide adopt / adapt / baseline-only / ignore?
- [ ] Did we record why we used or rejected each candidate?

## Skill draft
- [ ] Clear name
- [ ] Trigger description says when to use it
- [ ] Core model or review framework is explicit
- [ ] Output structure is explicit
- [ ] Reference files are linked

## Eval design
- [ ] If relevant, do we have a comparison against an external baseline skill as well as no-skill or prior-skill baselines?
- [ ] Trigger-positive prompts
- [ ] Trigger-negative prompts
- [ ] Output-quality prompts
- [ ] Positive control prompt
- [ ] Expected outputs are described clearly
- [ ] Must-include concepts reflect meaning, not only exact wording

## Review of failures
- [ ] Is the miss a skill problem?
- [ ] Is the miss a grader problem?
- [ ] Is the prompt unrealistic or underspecified?
- [ ] Is the failure just a runtime/tooling issue?

## Packaging
- [ ] README explains intent
- [ ] Examples exist
- [ ] Eval scripts are runnable
- [ ] Result snapshots are current
- [ ] Contribution guidance exists
