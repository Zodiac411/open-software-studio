#!/usr/bin/env python3
"""Dependency-free structural validation for the Open Software Studio marketplace."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / '.agents/plugins/marketplace.json'
REQUIRED_INTERFACE = {'displayName', 'shortDescription', 'longDescription', 'developerName', 'category', 'capabilities', 'websiteURL', 'privacyPolicyURL', 'termsOfServiceURL', 'defaultPrompt', 'brandColor', 'composerIcon', 'logo', 'screenshots'}
CODEX_ONLY = {'web-app-builder', 'execution-guard'}

def fail(message: str) -> None:
    raise SystemExit(f'FAIL: {message}')

def main() -> None:
    marketplace = json.loads(MARKETPLACE.read_text(encoding='utf-8'))
    if marketplace.get('name') != 'open-software-studio': fail('marketplace name')
    entries = marketplace.get('plugins', [])
    if len(entries) != 7: fail('expected seven marketplace entries')
    names = {entry.get('name') for entry in entries}
    if len(names) != 7: fail('duplicate marketplace names')
    for entry in entries:
        name = entry['name']
        policy = entry.get('policy', {})
        if set(('installation', 'authentication')) - set(policy): fail(f'{name}: missing policy')
        products = set(policy.get('products', []))
        if (name in CODEX_ONLY) != (products == {'CODEX'}): fail(f'{name}: incorrect product gate')
        plugin = ROOT / 'plugins' / name
        manifest_path = plugin / '.codex-plugin/plugin.json'
        if not manifest_path.is_file(): fail(f'{name}: missing manifest')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        if manifest.get('name') != name or manifest.get('version') != '0.1.0': fail(f'{name}: identity')
        if manifest.get('skills') != './skills/': fail(f'{name}: skills path')
        if set(manifest.get('interface', {})) != REQUIRED_INTERFACE: fail(f'{name}: interface fields')
        for asset_field in ('composerIcon', 'logo'):
            asset = plugin / manifest['interface'][asset_field].removeprefix('./')
            if not asset.is_file(): fail(f'{name}: missing {asset_field}')
        if any(key in manifest for key in ('apps', 'mcpServers', 'hooks')): fail(f'{name}: unexpected integration surface')
        skills = list((plugin / 'skills').glob('*/SKILL.md'))
        if not skills: fail(f'{name}: no skills')
        for skill in skills:
            text = skill.read_text(encoding='utf-8')
            if not text.startswith('---\n') or 'name:' not in text or 'description:' not in text: fail(f'{skill}: invalid routing frontmatter')
    print(f'PASS: validated {len(entries)} manifests and {sum(1 for _ in ROOT.glob("plugins/*/skills/*/SKILL.md"))} skills')

if __name__ == '__main__': main()
