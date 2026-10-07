#!/usr/bin/env python3
"""Review committed role edits using governance from an explicitly trusted base."""
import argparse
import json
from pathlib import Path, PurePosixPath
import subprocess

import yaml


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.DEVNULL)


def read(repo, revision, path):
    try:
        return git(repo, 'show', f'{revision}:{path}').decode()
    except subprocess.CalledProcessError:
        return None


def check(repo, base, head, actor):
    # Resolve refs before constructing object paths or diff arguments.
    base = git(repo, 'rev-parse', '--verify', f'{base}^{{commit}}').decode().strip()
    head = git(repo, 'rev-parse', '--verify', f'{head}^{{commit}}').decode().strip()
    policy = yaml.safe_load(read(repo, base, 'governance.yaml'))
    if policy['version'] != 1 or actor not in policy['owners']:
        raise ValueError('Unknown governance version or actor')
    departments = policy['owners'][actor]['editable_departments']
    owner_paths = {owner.replace('-', '/') for owner in policy['owners']}
    changed = git(repo, 'diff', '--name-only', '-z', '--no-renames', base, head).decode().split('\0')
    changed = [p for p in changed if p]
    if not changed:
        raise ValueError('No organization changes')
    role_paths = set()
    for path in changed:
        parts = PurePosixPath(path).parts
        if len(parts) < 3 or parts[0] not in departments or any(p.startswith('.') for p in parts):
            raise ValueError(f'Outside actor scope: {path}')
        role = None
        for length in range(len(parts) - 1, 1, -1):
            candidate = '/'.join(parts[:length])
            if any(read(repo, revision, f'{candidate}/temporal.yaml') is not None for revision in (base, head)):
                role = candidate
                break
        if role is None:
            raise ValueError(f'Not a role folder: {path}')
        if path.startswith(actor.replace('-', '/') + '/') or (actor != 'executive-ceo' and any(path.startswith(owner + '/') for owner in owner_paths)):
            raise ValueError(f'Cannot edit own role or another manager: {path}')
        role_paths.add(role)
        mode = git(repo, 'ls-tree', head, '--', path).decode().split(' ', 1)[0]
        if mode and mode not in {'100644', '100755'}:
            raise ValueError(f'Only regular role files allowed: {path}')
    for role in role_paths:
        before = read(repo, base, f'{role}/temporal.yaml')
        after = read(repo, head, f'{role}/temporal.yaml')
        old = yaml.safe_load(before) if before else None
        new = yaml.safe_load(after) if after else None
        if old is None and new is None:
            raise ValueError(f'Not a role folder: {role}')
        if new is None:
            if role in owner_paths:
                raise ValueError('Removing a manager requires a governance change')
            if not old.get('paused', True):
                raise ValueError('Retirement requires a prior merged pause and drain verification')
            if read(repo, head, f'{role}/SKILL.md') is not None:
                raise ValueError('Partial role deletion')
            continue
        if read(repo, head, f'{role}/SKILL.md') is None:
            raise ValueError('Missing SKILL.md')
        if old is None and not new.get('paused', True):
            raise ValueError('New roles must start paused')
        if old:
            for key, default in [('workspace', 'project'), ('sandbox', 'read-only'), ('timeout_seconds', 2700), ('session', 'new')]:
                if new.get(key, default) != old.get(key, default):
                    raise ValueError(f'Execution setting requires separate review: {key}')
            if old.get('paused', True) and not new.get('paused', True):
                raise ValueError('Activation is outside role-editing authority')
    files = git(repo, 'ls-tree', '-r', '--name-only', head).decode().splitlines()
    for department in departments:
        count = sum(p.startswith(department + '/') and p.endswith('/temporal.yaml') for p in files)
        if count > policy['max_roles_per_department']:
            raise ValueError(f'Department role budget exceeded: {department}')
    return {'actor': actor, 'base': base, 'head': head, 'roles': sorted(role_paths)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', default='HEAD')
    parser.add_argument('--actor', required=True)
    args = parser.parse_args()
    print(json.dumps(check(args.repo, args.base, args.head, args.actor), indent=2))
