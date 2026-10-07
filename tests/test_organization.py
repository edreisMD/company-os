import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

spec = importlib.util.spec_from_file_location('scope', Path(__file__).resolve().parents[1] / 'scripts/check_org_change.py')
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)


class OrganizationScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Test')
        source = Path(__file__).resolve().parents[1]
        (self.root/'governance.yaml').write_text((source/'governance.yaml').read_text())
        for role in ['engineering/manager', 'engineering/developer', 'sales/manager', 'sales/seo', 'executive/ceo']:
            self.role(role)
        self.base = self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args]).decode().strip()

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')
        return self.git('rev-parse', 'HEAD')

    def role(self, name, paused=True):
        folder = self.root/name
        folder.mkdir(parents=True, exist_ok=True)
        (folder/'SKILL.md').write_text('---\nname: '+folder.name+'\ndescription: Test\n---\nInstructions')
        (folder/'temporal.yaml').write_text(yaml.safe_dump({'version':2,'id':name.replace('/','-'),'paused':paused,'trigger':{'type':'manual'}}))

    def check(self, actor='engineering-manager'):
        return scope.check(self.root, self.base, self.commit(), actor)

    def test_manager_can_add_nested_subordinate(self):
        self.role('engineering/frontend/accessibility')
        self.assertEqual(self.check()['roles'], ['engineering/frontend/accessibility'])

    def test_self_and_other_department_are_rejected(self):
        for role in ['engineering/manager', 'sales/seo']:
            with self.subTest(role=role):
                self.git('reset', '--hard', self.base)
                (self.root/role/'SKILL.md').write_text('changed')
                with self.assertRaises(ValueError):
                    self.check()

    def test_ceo_can_edit_subordinate_manager(self):
        (self.root/'engineering/manager/SKILL.md').write_text('changed')
        self.assertEqual(self.check('executive-ceo')['roles'], ['engineering/manager'])

    def test_candidate_cannot_expand_base_authority(self):
        (self.root/'governance.yaml').write_text('owners: {}')
        with self.assertRaisesRegex(ValueError, 'scope'):
            self.check()

    def test_activation_is_rejected(self):
        self.role('engineering/developer', paused=False)
        with self.assertRaisesRegex(ValueError, 'Activation'):
            self.check()

    def test_new_active_role_is_rejected(self):
        self.role('engineering/new', paused=False)
        with self.assertRaisesRegex(ValueError, 'start paused'):
            self.check()

    def test_execution_settings_are_protected(self):
        path = self.root/'engineering/developer/temporal.yaml'
        data = yaml.safe_load(path.read_text()); data['sandbox'] = 'workspace-write'
        path.write_text(yaml.safe_dump(data))
        with self.assertRaisesRegex(ValueError, 'Execution setting'):
            self.check()

    def test_symlink_is_rejected(self):
        (self.root/'engineering/developer/escape').symlink_to('/tmp')
        with self.assertRaisesRegex(ValueError, 'regular'):
            self.check()

    def test_role_budget(self):
        for number in range(11):
            self.role(f'engineering/role-{number}')
        with self.assertRaisesRegex(ValueError, 'budget'):
            self.check()
