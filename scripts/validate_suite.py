#!/usr/bin/env python3
"""Dependency-free structural validation for the Open Software Studio marketplace."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / '.agents/plugins/marketplace.json'
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
MAX_ICON_BYTES = 10 * 1024
REQUIRED_INTERFACE = {'displayName', 'shortDescription', 'longDescription', 'developerName', 'category', 'capabilities', 'websiteURL', 'privacyPolicyURL', 'termsOfServiceURL', 'defaultPrompt', 'brandColor', 'composerIcon', 'logo', 'screenshots'}
OPTIONAL_INTERFACE = {'logoDark'}
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
        interface = manifest.get('interface', {})
        if not REQUIRED_INTERFACE.issubset(interface) or set(interface) - (REQUIRED_INTERFACE | OPTIONAL_INTERFACE): fail(f'{name}: interface fields')
        for asset_field in ('composerIcon', 'logo', 'logoDark'):
            if asset_field not in interface: continue
            asset = plugin / interface[asset_field].removeprefix('./')
            if not asset.is_file(): fail(f'{name}: missing {asset_field}')
            if asset.suffix.lower() != '.png' or asset.read_bytes()[:8] != PNG_SIGNATURE: fail(f'{name}: {asset_field} must be a PNG')
            if asset.stat().st_size > MAX_ICON_BYTES: fail(f'{name}: {asset_field} exceeds 10 KB')
        if manifest.get('mcpServers') != './.mcp.json': fail(f'{name}: mcpServers path')
        if manifest.get('apps') != './.app.json': fail(f'{name}: apps path')
        app_path = plugin / '.app.json'
        if not app_path.is_file(): fail(f'{name}: missing .app.json')
        app_payload = json.loads(app_path.read_text(encoding='utf-8'))
        if not isinstance(app_payload.get('apps'), dict): fail(f'{name}: invalid .app.json')
        mcp_path = plugin / '.mcp.json'
        if not mcp_path.is_file(): fail(f'{name}: missing .mcp.json')
        mcp_payload = json.loads(mcp_path.read_text(encoding='utf-8'))
        mcp_servers = mcp_payload.get('mcpServers')
        if not isinstance(mcp_servers, dict) or len(mcp_servers) != 1: fail(f'{name}: invalid .mcp.json')
        server = next(iter(mcp_servers.values()))
        if server.get('type') != 'http' or not server.get('url', '').startswith('http://127.0.0.1:8791/mcp/'): fail(f'{name}: invalid MCP endpoint')
        skills = list((plugin / 'skills').glob('*/SKILL.md'))
        if not skills: fail(f'{name}: no skills')
        for skill in skills:
            text = skill.read_text(encoding='utf-8')
            if not text.startswith('---\n') or 'name:' not in text or 'description:' not in text: fail(f'{skill}: invalid routing frontmatter')
    print(f'PASS: validated {len(entries)} manifests and {sum(1 for _ in ROOT.glob("plugins/*/skills/*/SKILL.md"))} skills')

if __name__ == '__main__': main()
