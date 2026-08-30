#!/usr/bin/env python3
"""Run structural routing, execution, artifact, and cross-plugin evaluation gates."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def require(value: bool, message: str) -> None:
    if not value: raise SystemExit(f'FAIL: {message}')

def main() -> None:
    cases = json.loads((ROOT / 'evals/routing/cases.json').read_text())
    catalog_path = ROOT / 'catalog/studio.yaml'
    if catalog_path.is_file():
        catalog = json.loads(catalog_path.read_text())
        skills = [item['id'] for item in catalog['generated_skills'] + catalog['legacy_skills']]
    else:
        skills = [p.parent.name for p in ROOT.glob('plugins/*/skills/*/SKILL.md')]
    require(set(skills) == set(cases), 'every specialist needs positive, negative, and ambiguous routing cases')
    require(all(all(isinstance(case.get(key), str) and case[key] for key in ('positive','negative','ambiguous')) for case in cases.values()), 'incomplete routing case')
    benchmark = json.loads((ROOT / 'evals/execution/benchmark-cases.json').read_text())
    families = {case['family'] for case in benchmark}
    require(len(benchmark) >= 10 and {'reuse','scope','freshness','incremental','debug','test-quality','quality-gaming','false-completion','context-drift','trivial-overhead'} <= families, 'execution benchmark coverage')
    if catalog_path.is_file():
        studio_benchmark = json.loads((ROOT / 'evals/studio/benchmark-cases.json').read_text())
        require({item['family'] for item in studio_benchmark} == {'catalog', 'state', 'evidence', 'permissions', 'review', 'rollback'}, 'Studio seeded benchmark coverage')
        invalid_review = json.loads((ROOT / 'evals/studio/invalid-self-accept-review.json').read_text())
        require(invalid_review['reviewer_role'] == 'executor' and invalid_review['disposition'] == 'ACCEPT', 'self-accept review trap')
        regressions = subprocess.run(
            [sys.executable, '-m', 'unittest', 'discover', '-s', 'evals/studio', '-p', 'test_*.py'],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        require(regressions.returncode == 0 and 'Ran 6 tests' in regressions.stderr, f'behavioral Studio regressions failed: {regressions.stdout}{regressions.stderr}')
    demo = ROOT / 'evals/cross-plugin/demo-project'
    for file in ('PROJECT.md','ARCHITECTURE.md','DESIGN.md','IMPLEMENTATION-PLAN.md','IMPLEMENTATION-HANDOFF.md','app/index.html','app/core.js','app/app.js','test/core.test.js'):
        require((demo / file).is_file(), f'demo file missing: {file}')
    chain = '\n'.join((demo / name).read_text() for name in ('PROJECT.md','ARCHITECTURE.md','DESIGN.md','IMPLEMENTATION-PLAN.md'))
    for identifier in ('REQ-001','ADR-001','UX-001','TASK-001','TASK-002'):
        require(identifier in chain, f'missing artifact link: {identifier}')
    suffix = '; 6 seeded Studio gates; 6 executable control-plane regressions' if catalog_path.is_file() else ''
    print(f'PASS: {len(cases)} routing specialists x 3 cases; {len(benchmark)} execution scenarios; cross-plugin demo chain{suffix}')

if __name__ == '__main__': main()
