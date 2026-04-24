#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / '.agents' / 'skills' / 'brand-review' / 'SKILL.md'
EVALS = ROOT / '.agents' / 'skills' / 'brand-review' / 'evals' / 'trigger-evals.json'
OUT = ROOT / '.agents' / 'skills' / 'brand-review' / 'evals' / 'codex-trigger-results.json'


def read_description() -> str:
    text = SKILL.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        raise RuntimeError('Missing YAML frontmatter')
    desc = None
    for line in lines[1:]:
        if line.strip() == '---':
            break
        if line.startswith('description:'):
            desc = line.split(':', 1)[1].strip().strip('"')
            break
    if not desc:
        raise RuntimeError('Missing description')
    return desc


def judge_prompt(query: str, description: str) -> dict:
    prompt = f'''You are evaluating skill triggering for a coding/design assistant.\n\nSkill name: brand-review\nSkill description: {description}\n\nUser prompt:\n{query}\n\nTask:\nDecide whether this prompt SHOULD trigger the brand-review skill.\nThe skill is for combined copy + visual brand critique of homepages, landing pages, mockups, screenshots, Figma directions, and variant brand directions, especially when the user wants something less generic, less AI-generated, more ownable, more specific, or wants critique across message + visual identity together.\n\nReturn JSON only with this exact shape:\n{{"should_trigger": true, "confidence": 0.0, "reason": "..."}}\n\nRules:\n- should_trigger must be true or false\n- confidence must be between 0 and 1\n- reason must be one sentence\n- If the prompt is implementation-only, grammar-only, accessibility-only, alt-text-only, token-extraction-only, or pure testing/automation without brand critique, usually return false.\n- If the prompt clearly asks for harsh critique of both copy and visuals, or brand specificity / genericness / AI-slop / ownability / variant differentiation, usually return true.'''
    cmd = [
        'codex', 'exec', '-C', str(ROOT), '--skip-git-repo-check', '--sandbox', 'read-only', '--json', prompt
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if result.returncode != 0:
        return {
            'should_trigger': False,
            'confidence': 0.0,
            'reason': f'codex error: {result.stderr.strip()[:200]}'
        }
    last = None
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
    if not last:
        return {
            'should_trigger': False,
            'confidence': 0.0,
            'reason': 'no agent output'
        }
    try:
        return json.loads(last)
    except json.JSONDecodeError:
        return {
            'should_trigger': False,
            'confidence': 0.0,
            'reason': f'non-json output: {last[:160]}'
        }


def main():
    description = read_description()
    evals = json.loads(EVALS.read_text())
    results = []
    passed = 0
    for item in evals:
        pred = judge_prompt(item['query'], description)
        ok = bool(pred.get('should_trigger')) == bool(item['should_trigger'])
        if ok:
            passed += 1
        results.append({
            'id': item['id'],
            'query': item['query'],
            'expected_should_trigger': item['should_trigger'],
            'predicted_should_trigger': pred.get('should_trigger'),
            'confidence': pred.get('confidence'),
            'reason': pred.get('reason'),
            'pass': ok,
        })
        print(f"[{ 'PASS' if ok else 'FAIL' }] {item['id']} expected={item['should_trigger']} predicted={pred.get('should_trigger')} conf={pred.get('confidence')}")
    output = {
        'skill_name': 'brand-review',
        'mode': 'codex-proxy-trigger-eval',
        'summary': {
            'total': len(results),
            'passed': passed,
            'failed': len(results) - passed,
            'accuracy': passed / len(results) if results else 0,
        },
        'results': results,
    }
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nSaved results to {OUT}")
    print(json.dumps(output['summary'], indent=2))


if __name__ == '__main__':
    main()
