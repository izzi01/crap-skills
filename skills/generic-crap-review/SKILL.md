---
name: generic-crap-review
description: "Detect and fix generic landing-page, homepage, hero, and marketing copy that sounds vague, interchangeable, overclaimed, internally conceptual, or not grounded in a real audience. Use this whenever the user asks to review homepage copy, make a page less generic, sharpen positioning, audit variants like K/K1/K2/K3, critique CTA/hero sections, or turn subjective 'this feels bland' feedback into concrete edits and repo-native tests. Also use when writing or tightening anti-generic content checks in Vitest or similar test suites."
---

# Generic Crap Review

Turn fuzzy feedback like "this sounds generic" into a concrete review and rewrite process.

This skill is for landing pages and homepage variants that look polished but say very little. Its job is to find where copy could belong to almost any brand, then replace that with audience reality, proof, and route-specific voice.

## When to use

Use this skill when the user wants to:
- review a homepage, hero, CTA, or landing page for bland marketing language
- make copy less generic, less agency-ish, less presentation-like, or less corporate
- compare multiple page variants and ensure they do not collapse into one safe voice
- check whether a page names a real audience, real pain, real mechanism, and real proof
- convert quality concerns into automated tests, especially in Vitest

## What generic crap looks like

Treat copy as suspect when it does one or more of these:

1. **Talks to nobody specific**
   - says "you" or "khách hàng" or "người dùng" without naming the actual audience
   - ignores stakeholders like phụ huynh, học viên, founder, operator, buyer, recruiter

2. **Claims value without mechanism**
   - "giải pháp toàn diện"
   - "đồng hành trên hành trình"
   - "nâng tầm"
   - "world-class"
   - "premium solution"

3. **Sounds like internal concept language**
   - talks about the design concept instead of the user's situation
   - uses meta labels like "immersive", "hybrid", "framework", "branch", "outcome", "backbone" as if they are customer-facing benefits

4. **Uses aspiration without proof**
   - promises results but gives no process, credential, artifact, channel, or milestone
   - no names, no numbers, no stages, no operators, no evidence surfaces

5. **Erases page-level differentiation**
   - variants all use the same safe hero and CTA language
   - no distinct posture, audience angle, or conversion behavior per route

## Review method

For each page or variant, inspect in this order.

### 1. Audience reality
Ask:
- Who exactly is this page for?
- Does the page name that audience in their own language?
- Is there more than one audience that matters?
- Does the copy acknowledge their real worries, not just the brand's offer?

If the audience is implied but not named, rewrite it.

### 2. Problem reality
Ask:
- What specific stuck moment is the reader in?
- What confusion, risk, delay, or fear do they have?
- Would the intended reader say "yes, that's my situation"?

Prefer concrete tension over motivational fluff.

### 3. Mechanism clarity
Ask:
- How does this business actually help?
- What steps, process, or operating model produce the promise?
- Can the user see what happens after they click?

If the page promises a result, it should usually show the mechanism that gets there.

### 4. Proof surfaces
Look for concrete proof such as:
- credentials
- team or teacher specificity
- hotline, Zalo, email, consult channel
- certificates, visa, hồ sơ, school/program artifacts
- before/after states
- counts, milestones, levels, SLAs, turnaround windows

If proof is absent, add it or reduce the claim.

### 5. Route-specific voice
When reviewing multiple variants, ask:
- Why does this variant exist?
- What is its distinct stance or conversion style?
- Which lines must belong only to this version?

Each route should preserve at least 2-3 distinctive signals.

## Rewrite rules

When editing, prefer these moves.

### Replace vague claim with audience-specific truth
- Bad: "Chúng tôi đồng hành cùng bạn trên hành trình chinh phục tương lai."
- Better: "CAP giúp học viên mất gốc và phụ huynh đang mơ hồ về hướng đi nhìn ra lộ trình học tiếng Pháp, chứng chỉ, và hồ sơ du học phù hợp với tình huống hiện tại."

### Replace brand puffery with operational detail
- Bad: "Giải pháp toàn diện cho mục tiêu của bạn"
- Better: "Kiểm tra trình độ, xếp lớp phù hợp, lên lộ trình học và tư vấn bước tiếp theo cho hồ sơ du học."

### Replace concept-meta wording with client wording
- Bad: "Immersive hybrid branch with stronger visual storytelling"
- Better: "Phiên bản này dùng hình ảnh lớn hơn để tạo niềm tin nhanh hơn, nhưng vẫn giữ trọng tâm ở lộ trình, giảng viên, và bước liên hệ rõ ràng."

### Replace empty CTA with concrete next step
- Bad: "Liên hệ ngay"
- Better: "Chat Zalo với CAP để hỏi nhanh về trình độ hiện tại và lộ trình nên đi trước."

## Anti-generic checklist

Before calling copy good enough, confirm:
- The page names the real audience explicitly.
- The page names at least one real pain or confusion.
- The page explains how the service works.
- The page contains proof surfaces, not just promises.
- The CTA reflects real user behavior.
- Variant pages have distinct voices.
- Internal design/presentation language is removed.

## Converting judgment into tests

When the repo has a test runner, prefer encoding the critique as tests.

### Good test categories
1. **Audience specificity**
   - require audience terms to appear
2. **Domain specificity**
   - require route-specific vocabulary
3. **Proof density**
   - require operational/proof signals
4. **Banned filler**
   - ban known generic phrases
5. **Variant differentiation**
   - require distinct phrases per route

### Vitest pattern
Use simple source-reading tests for static pages.

```ts
import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';

const source = readFileSync('src/pages/variant-k1.astro', 'utf8');

test('names the real audience', () => {
  expect(source.includes('phụ huynh')).toBe(true);
});
```

Keep detectors honest:
- do not relax a failing test just because it found a real issue
- if a test finds a true weakness, fix the page
- failure messages should explain what kind of genericness was detected

## Suggested workflow

1. Read the page source.
2. List generic phrases, missing audiences, weak proof, and meta language.
3. Propose concrete rewrites.
4. Apply edits.
5. Add or update repo-native tests.
6. Run only the focused tests first.
7. Report exact pass/fail evidence without pretending success.

## Output format

When reporting findings, use this structure:

### Generic-crap review
- **Audience gaps:** ...
- **Generic phrases:** ...
- **Proof gaps:** ...
- **Meta/internal language to remove:** ...
- **Variant differentiation risks:** ...

### Recommended edits
- ...

### Verification
- focused tests run
- result
- exact failing or passing evidence

## Reference files

If you need examples or a reusable checklist, read:
- `references/checklist.md`
- `references/test-template.md`
