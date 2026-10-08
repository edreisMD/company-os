#!/usr/bin/env python3
"""Validate the public role catalog against the backend's exported JSON Schema."""
import json
from pathlib import Path
import sys

import jsonschema
import yaml


def validate(root):
    root = Path(root).resolve()
    schema = json.loads((root / 'schemas/temporal.schema.json').read_text())
    agent_schema = json.loads((root / 'schemas/agent.schema.json').read_text())
    team_schema = json.loads((root / 'schemas/team.schema.json').read_text())
    result = {}
    for manifest in sorted(root.rglob('temporal.yaml')):
        if any(p.startswith('.') for p in manifest.relative_to(root).parts):
            continue
        skill = manifest.with_name('SKILL.md')
        if not manifest.resolve().is_relative_to(root) or not skill.resolve().is_relative_to(root):
            raise ValueError('Role files must stay inside catalog')
        config = yaml.safe_load(manifest.read_text())
        jsonschema.validate(config, schema)
        neutral = yaml.safe_load(manifest.with_name('agent.yaml').read_text())
        jsonschema.validate(neutral, agent_schema)
        expected_neutral = dict(config, version=1, schedule_paused=config['paused'])
        del expected_neutral['paused']
        if neutral != expected_neutral:
            raise ValueError(f'Conflicting agent/Temporal role: {manifest}')
        expected = '-'.join(manifest.parent.relative_to(root).parts)
        if config['id'] != expected or expected in result:
            raise ValueError(f'Invalid/duplicate role ID: {manifest}')
        parts = skill.read_text().split('---', 2)
        if len(parts) != 3 or parts[0].strip() or not parts[2].strip():
            raise ValueError(f'Missing skill frontmatter/body: {skill}')
        meta = yaml.safe_load(parts[1])
        if meta.get('name') != manifest.parent.name or not meta.get('description'):
            raise ValueError(f'Invalid skill name/description: {skill}')
        result[expected] = str(manifest.parent.relative_to(root))
    for skill in root.rglob('SKILL.md'):
        if skill.parent != root and not skill.with_name('temporal.yaml').is_file():
            raise ValueError(f'Role missing temporal.yaml: {skill}')
    if not result:
        raise ValueError('Empty role catalog')
    for manifest in sorted((root / 'teams').glob('*/team.yaml')):
        team = yaml.safe_load(manifest.read_text())
        jsonschema.validate(team, team_schema)
        if team['id'] != manifest.parent.name:
            raise ValueError('Team ID must match folder')
        seen = set()
        for step in team['steps']:
            if step['id'] in seen or not set(step['needs']).issubset(seen):
                raise ValueError('Team must be a unique topologically ordered graph')
            if step['kind'] == 'agent':
                if not all(step.get(key) for key in ['role', 'placement', 'contract']) or step.get('gate'):
                    raise ValueError('Incomplete agent step')
                if step['role'] not in result.values():
                    raise ValueError('Unknown team role')
            elif not step.get('gate') or any(step.get(key) for key in ['role', 'placement', 'contract']):
                raise ValueError('Incomplete decision step')
            seen.add(step['id'])
    return result


if __name__ == '__main__':
    print(json.dumps(validate(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]), indent=2))
