import importlib.util, tempfile, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("ui_safe",HERE/"ui_safe.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
CUES=[(i*27,i*27+26,word) for i,word in enumerate(mod.KEYWORDS)]
class QualityTests(unittest.TestCase):
    def test_layout(self):
        self.assertEqual(mod.FPS,30)
        self.assertLess(mod.PANEL[2],mod.RIGHT_RAIL_START)
        self.assertLess(mod.PANEL[3],mod.BOTTOM_UI_START)
    def test_keywords(self):self.assertEqual(len(mod.KEYWORDS),16)
    def test_frame_time(self):self.assertEqual(mod.stamp(30),"0:00:01.00")
    def test_build_64_events(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a.ass"
            self.assertEqual(mod.build_ass(CUES,"#52EBD0",p),64)
            self.assertEqual(p.read_text().count("Dialogue:"),64)
            self.assertIn(r"\pos(474,1462)",p.read_text())
    def test_bad_palette(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):mod.build_ass(CUES,"red",Path(d)/"a.ass")
    def test_bad_timing(self):
        with tempfile.TemporaryDirectory() as d:
            bad=CUES.copy();bad[1]=(0,10,mod.KEYWORDS[1])
            with self.assertRaises(ValueError):mod.build_ass(bad,"#52EBD0",Path(d)/"a.ass")
if __name__=="__main__":unittest.main()
