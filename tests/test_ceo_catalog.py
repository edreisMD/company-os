import importlib.util
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog_validator', ROOT/'scripts/validate.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CeoCatalogTests(unittest.TestCase):
    def test_neutral_roles_keep_temporal_execution_fields(self):
        result = catalog.validate(ROOT)
        self.assertEqual(len(result), 15)
        for folder in result.values():
            legacy = yaml.safe_load((ROOT/folder/'temporal.yaml').read_text())
            agent = yaml.safe_load((ROOT/folder/'agent.yaml').read_text())
            self.assertTrue(agent['schedule_paused'])
            self.assertEqual(agent['trigger'], legacy['trigger'])

    def test_small_teams_preserve_each_founder_gate_and_candidate_owner(self):
        for manifest in (ROOT/'teams').glob('*/team.yaml'):
            team = yaml.safe_load(manifest.read_text())
            self.assertEqual({step.get('gate') for step in team['steps'] if step['kind']=='decision'}, {'plan','release','publication'})
            isolated = [step for step in team['steps'] if step.get('placement') == 'isolated']
            self.assertEqual(len(isolated), 1)
            self.assertEqual(isolated[0]['contract'], 'candidate')
            for step in team['steps']:
                if step.get('contract') in {'review','qa'}:
                    agent = yaml.safe_load((ROOT/step['role']/'agent.yaml').read_text())
                    self.assertEqual(agent['sandbox'], 'read-only')


if __name__ == '__main__':
    unittest.main()
