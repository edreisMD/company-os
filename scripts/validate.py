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
    result = {}
    for manifest in sorted(root.rglob('temporal.yaml')):
        if any(p.startswith('.') for p in manifest.relative_to(root).parts):
            continue
        skill = manifest.with_name('SKILL.md')
        if not manifest.resolve().is_relative_to(root) or not skill.resolve().is_relative_to(root):
            raise ValueError('Role files must stay inside catalog')
        config = yaml.safe_load(manifest.read_text())
        jsonschema.validate(config, schema)
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
    return result


if __name__ == '__main__':
    print(json.dumps(validate(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]), indent=2))
