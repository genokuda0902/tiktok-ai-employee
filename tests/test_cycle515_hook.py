import json
import unittest
from pathlib import Path

class HookTests(unittest.TestCase):
    def test_review_only(self):
        m=json.loads(Path('quality/cycle515/manifest.json').read_text())
        self.assertEqual(m['publication'],'NOT_APPROVED')
        self.assertFalse(m['auto_post'])
    def test_source_exists(self):
        self.assertTrue(Path('quality/cycle515/hook_motion.py').exists())

if __name__=='__main__': unittest.main()
