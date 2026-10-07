#!/usr/bin/env python3
"""Import complete Codex-rendered workflows from an explicitly pinned gstack checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root=ROOT):
    lock = json.loads((root/'sources/gstack.lock.json').read_text())
    records = json.loads((root/'sources/gstack.files.json').read_text())
    if records['commit'] != lock['commit'] or records['roles'] != lock['roles']:
        raise ValueError('Source revision mismatch')
    expected = records['files']
    actual = {str(path.relative_to(root)): digest(path)
              for role in lock['roles'] for path in (root/role/'references/gstack').rglob('*')
              if path.is_file()}
    if actual != expected:
        raise ValueError('Imported upstream files changed; regenerate from the pinned source')
    for role, skill in lock['roles'].items():
        if not (root/role/'references/gstack/workflow.md').is_file():
            raise ValueError(f'Missing complete workflow: {skill}')
    return len(actual)


def import_source(source):
    lock = json.loads((ROOT/'sources/gstack.lock.json').read_text())
    commit = subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
    if commit != lock['commit']:
        raise ValueError('Checkout does not match pinned upstream revision')
    subprocess.run(['git','-C',str(source),'diff','--exit-code','HEAD','--'],check=True,stdout=subprocess.DEVNULL)
    records = {}
    with tempfile.TemporaryDirectory(prefix='coos-gstack-render-') as temp:
        subprocess.run(['bun',str(source/'scripts/gen-skill-docs.ts'),'--host',lock['host'],'--out-dir',temp],check=True,stdout=subprocess.DEVNULL)
        for role, skill in lock['roles'].items():
            if not re.fullmatch(r'[a-z][a-z0-9-]*(/[a-z][a-z0-9-]*)+', role) or not re.fullmatch(r'[a-z][a-z0-9-]*', skill):
                raise ValueError('Invalid source/role mapping')
            target=ROOT/role/'references/gstack'
            if not target.resolve().is_relative_to(ROOT.resolve()):
                raise ValueError('Import target escapes catalog')
            if target.exists():
                shutil.rmtree(target)
            target.mkdir(parents=True)
            # Include original role checklists/templates/specialists, then overlay Codex-rendered sections.
            for base in [source/skill, Path(temp)/'.agents/skills'/f'gstack-{skill}']:
                for path in sorted(base.rglob('*')):
                    if not path.is_file() or path.is_symlink():
                        continue
                    relative=path.relative_to(base)
                    if relative.parts[0]=='agents' or path.suffix=='.tmpl':
                        continue
                    destination=target/('workflow.md' if str(relative)=='SKILL.md' else relative)
                    destination.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copyfile(path,destination)
            shutil.copyfile(source/skill/'SKILL.md.tmpl',target/'source.tmpl')
            # Upstream source templates are retained; edit upstream or CompanyOS overlays, not snapshots.
            for path in target.rglob('*'):
                if path.is_file():
                    records[str(path.relative_to(ROOT))]=digest(path)
    (ROOT/'sources/gstack.files.json').write_text(json.dumps({'commit':commit,'roles':lock['roles'],'files':records},indent=2,sort_keys=True)+'\n')
    return verify()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check:
        print(f'Verified {verify()} pinned upstream files')
    elif args.source:
        print(f'Imported {import_source(args.source.resolve())} upstream files')
    else:
        parser.error('Pass --source CHECKOUT or --check')
