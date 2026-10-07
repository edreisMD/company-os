import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('importer', ROOT/'scripts/import_gstack.py')
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)


class UpstreamIntegrityTests(unittest.TestCase):
    def test_pinned_import_is_complete(self):
        self.assertGreater(importer.verify(ROOT), 0)
        lock = json.loads((ROOT/'sources/gstack.lock.json').read_text())
        for role in lock['roles']:
            self.assertIn('references/gstack/workflow.md', (ROOT/role/'SKILL.md').read_text())

    def test_changed_or_deleted_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT/'sources', root/'sources')
            lock = json.loads((ROOT/'sources/gstack.lock.json').read_text())
            for role in lock['roles']:
                shutil.copytree(ROOT/role/'references/gstack', root/role/'references/gstack')
            target = root/'engineering/planner/references/gstack/workflow.md'
            original = target.read_bytes()
            target.write_bytes(original+b'\nChanged instructions')
            with self.assertRaisesRegex(ValueError, 'changed'):
                importer.verify(root)
            target.unlink()
            with self.assertRaisesRegex(ValueError, 'changed'):
                importer.verify(root)
