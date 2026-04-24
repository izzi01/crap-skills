# Brand Review Test Template

```ts
import { describe, expect, test } from 'vitest';
import { readFileSync } from 'node:fs';

const source = readFileSync('src/pages/variant-k1.astro', 'utf8');

const bannedGenericPhrases = [
  'tốt nhất',
  'đẳng cấp',
  'đột phá',
  'nâng tầm',
  'giải pháp toàn diện',
  'world-class',
  'best-in-class',
  'premium solution',
];

const audienceSignals = ['phụ huynh', 'học viên'];
const proofSignals = ['hồ sơ', 'chứng chỉ', 'Zalo', 'hotline', 'đội ngũ'];
const distinctSignals = ['route-only phrase 1', 'route-only phrase 2'];

function countMatches(text: string, terms: string[]) {
  return terms.filter((term) => text.includes(term));
}

describe('brand review detector', () => {
  test('names the real audience', () => {
    const missing = audienceSignals.filter((term) => !source.includes(term));
    expect(missing, `Missing audience signals: ${missing.join(', ')}`).toEqual([]);
  });

  test('includes proof signals', () => {
    const matches = countMatches(source, proofSignals);
    expect(matches.length, `Expected stronger proof density. Only found: ${matches.join(', ')}`).toBeGreaterThanOrEqual(3);
  });

  test('avoids banned filler', () => {
    const leftovers = bannedGenericPhrases.filter((term) => source.includes(term));
    expect(leftovers, `Replace generic filler: ${leftovers.join(', ')}`).toEqual([]);
  });

  test('keeps route-specific voice', () => {
    const missing = distinctSignals.filter((term) => !source.includes(term));
    expect(missing, `Missing distinct route signals: ${missing.join(', ')}`).toEqual([]);
  });
});
```

Adapt the signals to the domain. Prefer hard-to-fake terms tied to real audience, real proof, and real route differentiation.
