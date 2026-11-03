import tempfile
import unittest
from pathlib import Path
from src.cycle1195_hook_hierarchy import filtergraph, render

class HookHierarchyTest(unittest.TestCase):
    def test_top_panel_and_safe_lower_area(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"font.ttc";f.touch()
            graph=filtergraph(str(f))
            self.assertIn("y=160",graph)
            self.assertIn("h=230",graph)
            self.assertNotIn("y=1400",graph)
    def test_reject_punctuation(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"font.ttc";f.touch()
            with self.assertRaises(ValueError):filtergraph(str(f),hook="bad:hook")
    def test_reject_missing_source(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"font.ttc";f.touch()
            with self.assertRaises(FileNotFoundError):render("missing.mp4","out.mp4",str(f),"AI","HOOK")
if __name__=="__main__":unittest.main()
