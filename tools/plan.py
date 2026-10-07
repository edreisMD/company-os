"""Validate a registry and coordinate bounded local engineering runs. No network writes."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import uuid
from zoneinfo import ZoneInfo

PROFILES = {'website', 'open-source', 'private-service', 'framework'}


def plan(registry, cadence, now=None):
    if cadence not in {'daily', 'weekly'}:
        raise ValueError('Unknown cadence')
    zone = ZoneInfo(registry['timezone'])
    minutes = registry['max_minutes']
    if not isinstance(minutes, int) or isinstance(minutes, bool) or not 1 <= minutes <= 45:
        raise ValueError('max_minutes must be 1..45')
    if registry['max_implementation_tasks'] != 1:
        raise ValueError('Start with one implementation task per cycle')
    if type(registry['paused']) is not bool:
        raise ValueError('paused must be boolean')
    ids = set()
    projects = []
    for project in registry['projects']:
        key = project['id']
        if not isinstance(key, str) or not key or key in ids:
            raise ValueError('Project IDs must be nonempty and unique')
        ids.add(key)
        if project['profile'] not in PROFILES or not project['default_branch']:
            raise ValueError('Unknown profile or missing default branch')
        if type(project['enabled']) is not bool:
            raise ValueError('enabled must be boolean')
        if project['enabled']:
            projects.append({'id': key, 'profile': project['profile'],
                             'repository': project.get('repository'),
                             'default_branch': project['default_branch'],
                             'blockers': project.get('blockers', []),
                             'analytics': project.get('analytics', 'unknown')})
    timestamp = now or datetime.now(timezone.utc)
    return {'date': timestamp.astimezone(zone).date().isoformat(), 'cadence': cadence,
            'paused': registry['paused'], 'max_minutes': minutes,
            'max_implementation_tasks': 0 if cadence == 'weekly' else 1,
            'merge_allowed': False, 'deploy_allowed': False,
            'projects': [] if registry['paused'] else projects}


def claim(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    token = str(uuid.uuid4())
    # Fail closed even on an expired lease: recovery requires checking the old run.
    with path.open('x') as handle:
        json.dump({'token': token, 'pid': os.getpid(),
                   'claimed_at': datetime.now(timezone.utc).isoformat(),
                   'lease_minutes': 60}, handle)
    return token


def release(path, token):
    path = Path(path)
    if json.loads(path.read_text())['token'] != token:
        raise ValueError('Lock belongs to another run')
    path.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    p = subs.add_parser('plan')
    p.add_argument('registry', type=Path)
    p.add_argument('--cadence', choices=['daily', 'weekly'], required=True)
    p = subs.add_parser('claim')
    p.add_argument('path')
    p = subs.add_parser('release')
    p.add_argument('path')
    p.add_argument('token')
    args = parser.parse_args()
    if args.command == 'plan':
        print(json.dumps(plan(json.loads(args.registry.read_text()), args.cadence), indent=2))
    elif args.command == 'claim':
        print(claim(args.path))
    else:
        release(args.path, args.token)


if __name__ == '__main__':
    main()
