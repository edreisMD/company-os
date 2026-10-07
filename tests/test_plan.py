from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from plan import plan, claim, release

class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((Path(__file__).resolve().parents[1] / 'templates/project-registry.example.json').read_text())

    def test_local_date_and_no_release_authority(self):
        result = plan(self.registry, 'daily', datetime(2026, 10, 7, 1, tzinfo=timezone.utc))
        self.assertEqual(result['date'], '2026-10-06')
        self.assertFalse(result['merge_allowed'])
        self.assertFalse(result['deploy_allowed'])

    def test_pause_excludes_all_projects(self):
        self.registry['paused'] = True
        self.assertEqual(plan(self.registry, 'daily')['projects'], [])

    def test_weekly_never_starts_implementation(self):
        self.assertEqual(plan(self.registry, 'weekly')['max_implementation_tasks'], 0)

    def test_duplicate_project_rejected(self):
        self.registry['projects'].append(deepcopy(self.registry['projects'][0]))
        with self.assertRaises(ValueError): plan(self.registry, 'daily')

    def test_disabled_project_excluded(self):
        self.registry['projects'][0]['enabled'] = False
        self.assertEqual(plan(self.registry, 'daily')['projects'], [])

    def test_unknown_metrics_preserved(self):
        self.assertEqual(plan(self.registry, 'daily')['projects'][0]['analytics'], 'missing')

    def test_excessive_budget_rejected(self):
        self.registry['max_minutes'] = 61
        with self.assertRaises(ValueError): plan(self.registry, 'daily')

    def test_atomic_claim_and_ownership(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'lock.json'
            token = claim(path)
            with self.assertRaises(FileExistsError): claim(path)
            with self.assertRaises(ValueError): release(path, 'someone-else')
            self.assertTrue(path.exists())
            release(path, token)
            self.assertFalse(path.exists())
            next_token = claim(path)
            self.assertNotEqual(token, next_token)
            release(path, next_token)

if __name__ == '__main__': unittest.main()
