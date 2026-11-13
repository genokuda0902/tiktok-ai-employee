import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from quality.cycle1425_gate import publication_ready

class GateTest(unittest.TestCase):
    def test_missing_renderer_fails(self):
        self.assertFalse(publication_ready({}, '/missing/render.py'))
    def test_unapproved_fails(self):
        with TemporaryDirectory() as d:
            p=Path(d)/'render.py'; p.write_text('')
            self.assertFalse(publication_ready({'decode_passed': True}, str(p)))
    def test_all_verified(self):
        with TemporaryDirectory() as d:
            p=Path(d)/'render.py'; p.write_text('')
            self.assertTrue(publication_ready(dict.fromkeys(('japanese_narration_verified','captions_synced','assets_licensed','employee_approved','decode_passed'), True), str(p)))
