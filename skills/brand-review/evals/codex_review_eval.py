#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / '.agents' / 'skills' / 'brand-review' / 'SKILL.md'
EVALS = ROOT / '.agents' / 'skills' / 'brand-review' / 'evals' / 'review-evals.json'
OUT = ROOT / '.agents' / 'skills' / 'brand-review' / 'evals' / 'codex-review-results.json'


def read_skill_body() -> str:
    text = SKILL.read_text()
    parts = text.split('---', 2)
    return parts[2].strip() if len(parts) >= 3 else text


def run_review(skill_body: str, prompt: str) -> str:
    full_prompt = f'''Use the following skill instructions when responding. Follow the critique style and output structure faithfully, but answer the user's prompt directly. Prefer the skill's blunt callout vocabulary when the failure mode is present.\n\nSKILL INSTRUCTIONS:\n{skill_body}\n\nUSER PROMPT:\n{prompt}\n'''
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
    'audience gaps': ['audience gaps', 'faceless audience', 'speaks to no one', 'talks to nobody specific'],
    'proof gaps': ['proof gaps', 'weak proof', 'thin proof', 'no real proof', 'trust is thin'],
    'gradient sludge': ['gradient sludge', 'mesh gradient', 'gradient-heavy', 'gradient overload'],
    'fake premium glass': ['fake premium glass', 'glass card', 'glassmorphism', 'fake premium', 'premium theater'],
    'concrete copy edits': ['concrete copy edits', 'replace', 'name', 'add proof'],
    'concrete visual edits': ['concrete visual edits', 'remove', 'reduce', 'increase', 'reorder'],
    'template hero': ['template hero', 'generic hero', 'hero theater', 'default ai-startup costume'],
    'anonymous SaaS card grid': ['anonymous saas card grid', 'six cards', 'feature cemetery', 'identical cards', 'decorative card grid'],
    'weak brand-ownable cues': ['weak brand-ownable cues', 'not ownable', 'no ownable', 'borrowed trend signals'],
    'proof surfaces': ['proof surfaces', 'real proof', 'customer evidence', 'implementation detail', 'security proof', 'anchored proof'],
    'decision flow': ['decision flow', 'decision path', 'reading order', 'guides action'],
    'variant differentiation risks': ['variant differentiation risks', 'collapsing into one safe', 'interchangeable', 'mood variants'],
    'route-specific voice': ['route-specific voice', 'distinct promise', 'different core promise', 'own lane'],
    'CTA posture': ['cta posture', 'commitment model', 'book an advisory call', 'see my plan', 'talk to an advisor'],
    'visual silhouette': ['visual silhouette', 'silhouette', 'different visual shape', 'different compositional identity'],
    'what already works': ['what already works'],
    'decorative noise': ['decorative noise', 'ornamental', 'noise', 'visual theater'],
    'fake premium': ['fake premium', 'premium theater', 'cosmetically expensive'],
    'anchored proof': ['anchored proof', 'proof-bearing', 'evidence-bearing', 'operational proof'],
    'restraint': ['restraint', 'calm', 'reduce', 'strip out', 'simplify'],
    'Vitest': ['vitest'],
    'audience specificity': ['audience specificity', 'name the audience', 'explicitly name'],
    'proof density': ['proof density', 'proof signals', 'required trust/proof signals'],
    'variant differentiation': ['variant differentiation', 'route differentiation', 'route-specific'],
    'visual sameness': ['visual sameness', 'same hero', 'same card rhythm', 'same polished imagery'],
    'moodboard instead of decision flow': ['moodboard instead of decision flow', 'moodboard energy', 'style over decision'],
    'hierarchy failures': ['hierarchy failures', 'flattens priority', 'everything announces itself'],
    'copy genericness': ['copy genericness', 'category phrases', 'generic copy', 'presentation sludge'],
    'simplify hero': ['simplify hero', 'kill the hero', 'strip the hero back', 'remove the hero theater', 'rebuild the hero', 'reduce the coin-art theater', 'hero around a decision path', 'make the first screen answer', 'replace the hero promise', 'remove the hero 3d coin', 'reduce glowing metrics', 'floating charts'],
    'clarify offer': ['clarify offer', 'specific claim', 'say what it does', 'buyer-specific operating claim', 'replace the headline with the product mechanism', 'say what the product actually does', 'say that', 'who it is for, what it does, why it is better', 'product sentence', 'name the category, buyer, and job', 'name the buyer and mechanism', 'what it is, who it is for, what it helps them do'],
    'highest-leverage changes': ['highest-leverage changes'],
    'clear hierarchy': ['clear hierarchy', 'one dominant idea', 'eye lands on', 'reading order'],
}

HARSH_BUCKETS = [
    'gradient sludge', 'template hero', 'anonymous SaaS card grid', 'fake premium glass',
    'dribbblified hierarchy', 'moodboard instead of decision flow', 'audience gaps',
    'proof gaps', 'decorative noise', 'weak brand-ownable cues', 'copy genericness'
]


def bucket_hit(lower: str, concept: str) -> bool:
    variants = CONCEPT_BUCKETS.get(concept, [concept.lower()])
    return any(v.lower() in lower for v in variants)


def grade(text: str, concepts: list[str], expected_output: str) -> dict:
    lower = text.lower()
    hits = []
    misses = []
    for c in concepts:
        if bucket_hit(lower, c):
            hits.append(c)
        else:
            misses.append(c)

    harsh_hits = [c for c in HARSH_BUCKETS if bucket_hit(lower, c)]
    structured = all(section in lower for section in [
        'why it feels generic', 'what already works', 'highest-leverage changes'
    ])

    return {
        'concept_hits': hits,
        'concept_misses': misses,
        'concept_pass_rate': len(hits) / len(concepts) if concepts else 1.0,
        'harsh_hits': harsh_hits,
        'harsh_hit_count': len(harsh_hits),
        'used_expected_structure': structured,
        'looks_balanced': ('what already works' in lower),
        'passes': len(hits) >= max(2, len(concepts) - 1) and len(harsh_hits) >= 2 and structured,
        'expected_output_note': expected_output,
    }


def main():
    skill_body = read_skill_body()
    data = json.loads(EVALS.read_text())
    selected = data['evals']
    results = []
    passed = 0
    for item in selected:
        output = run_review(skill_body, item['prompt'])
        grading = grade(output, item.get('must_include_concepts', []), item.get('expected_output', ''))
        if grading['passes']:
            passed += 1
        results.append({
            'id': item['id'],
            'prompt': item['prompt'],
            'output': output,
            'grading': grading,
        })
        print(f"[{ 'PASS' if grading['passes'] else 'FAIL' }] {item['id']} concept_rate={grading['concept_pass_rate']:.2f} harsh={grading['harsh_hit_count']} structured={grading['used_expected_structure']}")
    summary = {
        'total': len(results),
        'passed': passed,
        'failed': len(results) - passed,
        'pass_rate': passed / len(results) if results else 0,
    }
    OUT.write_text(json.dumps({'skill_name': 'brand-review', 'mode': 'codex-proxy-output-eval', 'summary': summary, 'results': results}, indent=2, ensure_ascii=False))
    print(f"\nSaved results to {OUT}")
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
