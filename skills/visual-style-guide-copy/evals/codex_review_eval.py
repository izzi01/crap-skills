#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / 'skills' / 'visual-style-guide-copy' / 'SKILL.md'
EVALS = ROOT / 'skills' / 'visual-style-guide-copy' / 'evals' / 'review-evals.json'
OUT = ROOT / 'skills' / 'visual-style-guide-copy' / 'evals' / 'codex-review-results.json'


def read_skill_body() -> str:
    text = SKILL.read_text()
    parts = text.split('---', 2)
    return parts[2].strip() if len(parts) >= 3 else text


def run_review(skill_body: str, prompt: str) -> str:
    full_prompt = f'''Use the following skill instructions when responding. Follow the skill structure faithfully, but answer the user's prompt directly.\n\nSKILL INSTRUCTIONS:\n{skill_body}\n\nUSER PROMPT:\n{prompt}\n'''
    cmd = ['codex', 'exec', '-C', str(ROOT), '--skip-git-repo-check', '--sandbox', 'read-only', '--json', full_prompt]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        return f'ERROR: {result.stderr.strip()[:400]}'
    last = ''
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get('type') == 'item.completed':
            item = event.get('item', {})
            if item.get('type') == 'agent_message':
                last = item.get('text', '')
    return last


CONCEPT_BUCKETS = {
    'structure': ['purpose', 'who this guide is for', 'brand foundations', 'logo guidelines', 'color palette'],
    'logo': ['logo'],
    'color': ['color', 'palette'],
    'typography': ['typography', 'typeface', 'type hierarchy'],
    'imagery': ['imagery', 'photography', 'illustration'],
    "do/don't": ["do / don't", "do/don't", 'incorrect usage'],
    'practical guidance': ['practical', 'usable', 'reference-friendly', 'apply'],
    'rules': ['rules', 'guidelines', 'usage'],
    'rationale': ['why', 'rationale', 'matters because'],
    'examples': ['example', 'examples'],
    'less fluff': ['less fluffy', 'not marketing', 'not decorative brand theater', 'practical'],
    'section rewrite': ['style guide rewrite', 'rewritten section', 'only rewrite'],
    'actionable': ['actionable', 'clearer', 'more usable'],
    'concrete': ['concrete', 'specific'],
    'voice': ['voice'],
    'tone': ['tone'],
    'aligned with visual system': ['aligned with the visual system', 'inside a broader guide', 'fit inside'],
    'guide section': ['section'],
    'what already works': ['what already works'],
    'focused improvements': ['focused improvements', 'better structure', 'improvements'],
    'balance': ['what already works', 'do not invent fake problems', 'already pretty solid'],
    'clarity': ['clarity', 'clear'],
    'usability': ['usable', 'use', 'practical'],
}


def bucket_hit(lower: str, concept: str) -> bool:
    variants = CONCEPT_BUCKETS.get(concept, [concept.lower()])
    return any(v.lower() in lower for v in variants)


def grade(text: str, concepts: list[str], expected_output: str) -> dict:
    lower = text.lower()
    hits, misses = [], []
    for c in concepts:
        if bucket_hit(lower, c):
            hits.append(c)
        else:
            misses.append(c)
    structured = any(h in lower for h in ['purpose', 'who this guide is for', 'brand foundations', 'style guide rewrite'])
    return {
        'concept_hits': hits,
        'concept_misses': misses,
        'concept_pass_rate': len(hits) / len(concepts) if concepts else 1.0,
        'used_expected_structure': structured,
        'looks_balanced': ('what already works' in lower) or ('better structure' in lower),
        'passes': len(hits) >= max(3, len(concepts) - 1) and structured,
        'expected_output_note': expected_output,
    }


def main():
    skill_body = read_skill_body()
    data = json.loads(EVALS.read_text())
    results = []
    passed = 0
    for item in data['evals']:
        output = run_review(skill_body, item['prompt'])
        grading = grade(output, item.get('must_include_concepts', []), item.get('expected_output', ''))
        if grading['passes']:
            passed += 1
        results.append({'id': item['id'], 'prompt': item['prompt'], 'output': output, 'grading': grading})
        print(f"[{'PASS' if grading['passes'] else 'FAIL'}] {item['id']} concept_rate={grading['concept_pass_rate']:.2f} structured={grading['used_expected_structure']}")
    summary = {'total': len(results), 'passed': passed, 'failed': len(results) - passed, 'pass_rate': passed / len(results) if results else 0}
    OUT.write_text(json.dumps({'skill_name': 'visual-style-guide-copy', 'mode': 'codex-proxy-output-eval', 'summary': summary, 'results': results}, indent=2, ensure_ascii=False))
    print(f"\nSaved results to {OUT}")
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
