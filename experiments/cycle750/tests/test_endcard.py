"""CI-safe tests: no user footage or audio required."""
from pathlib import Path
import importlib.util
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/(name+".py"))
    m=importlib.util.module_from_spec(spec)
    import sys
    sys.modules[name]=m
    spec.loader.exec_module(m)
    return m
class QualityTests(unittest.TestCase):
    def test_canvas(self):
        m=module("endcard");self.assertEqual((m.W,m.H),(1080,1920))
    def test_stages(self):
        m=module("endcard")
        with tempfile.TemporaryDirectory() as d:
            for i in range(3):
                p=m.draw(m.SCIENCE,i,Path(d)/f"{i}.png")
                self.assertGreater(p.stat().st_size,50000)
    def test_invalid_stage(self):
        m=module("endcard")
        with self.assertRaises(ValueError):m.draw(m.SCIENCE,5,"bad.png")
    def test_frame_cues(self):
        m=module("render")
        self.assertEqual(m.SPLITS,(378,395,405,429))
        self.assertEqual(m.FRAMES,429)
    def test_japanese_captions(self):
        m=module("endcard")
        self.assertEqual(m.SCIENCE.captions,("保存して、","あとで試そう。"))
    def test_genres(self):
        import json
        gs=json.loads((ROOT/"genres.json").read_text())["genres"]
        self.assertEqual(len(gs),10)
        self.assertEqual(len(set(gs)),10)
if __name__=="__main__":unittest.main()
