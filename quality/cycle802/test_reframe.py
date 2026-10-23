"""Synthetic-only tests: never load user footage in CI."""
import copy,json,tempfile,unittest
from pathlib import Path
from reframe import W,H,FPS,load_config,build_filter
CFG=Path(__file__).with_name("config.json")
class ReframeTests(unittest.TestCase):
    def setUp(self): self.cfg=json.loads(CFG.read_text(encoding="utf-8"))
    def validate_bad(self,bad):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"bad.json";f.write_text(json.dumps(bad))
            with self.assertRaises(ValueError):load_config(f)
    def test_valid(self): self.assertEqual(load_config(CFG)["shift_px"],136)
    def test_ten_genres(self): self.assertEqual(len(set(self.cfg["genres"])),10)
    def test_geometry(self): self.assertEqual((W,H,FPS),(1080,1920,30))
    def test_left_safe(self):
        self.assertGreaterEqual(min(s["important_content_x"][0] for s in self.cfg["windows"])+136,180)
    def test_right_safe(self):
        self.assertLessEqual(max(s["important_content_x"][1] for s in self.cfg["windows"])+136,920)
    def test_right_overflow_fails(self):
        bad=copy.deepcopy(self.cfg);bad["windows"][0]["important_content_x"]=[60,900];self.validate_bad(bad)
    def test_unapproved_modes_fail(self):
        for key in ("rights_reviewed","employee_approved","publication_approved"):
            bad=copy.deepcopy(self.cfg);bad[key]=True;self.validate_bad(bad)
    def test_wrong_genre_count_fails(self):
        bad=copy.deepcopy(self.cfg);bad["genres"].pop();self.validate_bad(bad)
    def test_invalid_shift_fails(self):
        for value in (-2,137,182):
            bad=copy.deepcopy(self.cfg);bad["shift_px"]=value;self.validate_bad(bad)
    def test_overlapping_scenes_fail(self):
        bad=copy.deepcopy(self.cfg);bad["windows"][1]["start"]=3.0;self.validate_bad(bad)
    def test_middle_scenes_untouched(self):
        filt=build_filter(self.cfg)
        self.assertIn("between(t,0",filt)
        self.assertIn("between(t,20.8",filt)
        self.assertNotIn("between(t,3.2,20.8)",filt)
    def test_edge_replication(self):
        filt=build_filter(self.cfg)
        self.assertIn("crop=2:1920:0:0",filt)
        self.assertIn("scale=136:1920",filt)
    def test_zero_shift(self):
        bad=copy.deepcopy(self.cfg);bad["shift_px"]=0
        self.assertEqual(build_filter(bad),"[0:v]null[v]")
if __name__=="__main__": unittest.main()
