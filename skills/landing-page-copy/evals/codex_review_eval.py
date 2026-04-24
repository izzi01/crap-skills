#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / 'skills' / 'landing-page-copy' / 'SKILL.md'
EVALS = ROOT / 'skills' / 'landing-page-copy' / 'evals' / 'review-evals.json'
OUT = ROOT / 'skills' / 'landing-page-copy' / 'evals' / 'codex-review-results.json'


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
    'audience': ['audience', 'for parents', 'for students', 'for finance teams', 'for operators', 'who it is for'],
    'offer': ['offer', 'what it does', 'what the service does', 'what the product does'],
    'proof': ['proof', 'trust', 'evidence', 'testimonial', 'numbers', 'credibility'],
    'how it works': ['how it works', '3-step', 'three-step', 'process', 'steps'],
    'CTA': ['cta', 'call to action', 'book', 'get your', 'see how it works', 'next step'],
    'problem': ['problem', 'pain', 'stakes', 'friction'],
    'mechanism': ['mechanism', 'how it works', 'workflow', 'process', 'operating model'],
    'CTA posture': ['cta posture', 'commitment', 'low-friction', 'medium-friction', 'high-friction', 'book a', 'see a', 'get your'],
    'specificity': ['specific', 'specificity', 'clearly', 'named audience', 'named buyer'],
    'trust': ['trust', 'proof', 'credibility', 'evidence'],
    'no hype': ['no hype', 'believable', 'avoid hype', 'without hype', 'not fake-premium'],
    'low-friction': ['low-friction'],
    'medium-friction': ['medium-friction'],
    'high-friction': ['high-friction'],
    'consistency': ['consistent', 'consistency', 'same core message', 'keep the message'],
    'what already works': ['what already works', "preserve the existing structure", "what's already working", 'preserve'],
    'focused improvements': ['focused improvements', 'best rewrite moves', 'improve carefully', 'highest-leverage', 'i’ll focus on', 'focus on:', 'tightening the hero', 'sharpening cta language', 'making proof and process sections feel more concrete'],
    'clarity': ['clarity', 'clearer', 'clear', 'tightening', 'sharpening', 'specific language'],
    'balance': ['what already works', 'balanced', 'careful', 'not a total rewrite', 'no total rewrite', 'preserve the existing structure', 'flagging only the copy that genuinely needs work'],
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
    structured = any(h in lower for h in ['positioning snapshot', 'what is weak now', 'hero', 'rewritten copy'])
    return {
        'concept_hits': hits,
        'concept_misses': misses,
        'concept_pass_rate': len(hits) / len(concepts) if concepts else 1.0,
        'used_expected_structure': structured,
        'looks_balanced': ('what already works' in lower) or ('best rewrite moves' in lower),
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
    OUT.write_text(json.dumps({'skill_name': 'landing-page-copy', 'mode': 'codex-proxy-output-eval', 'summary': summary, 'results': results}, indent=2, ensure_ascii=False))
    print(f"\nSaved results to {OUT}")
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
