import copy, json, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"video_engine"/"quality"))
from cycle778_hook import *
META=json.loads((Path(__file__).resolve().parents[1]/"video_engine"/"quality"/"cycle778_manifest.json").read_text())
class Cycle778Test(unittest.TestCase):
    def test_genres(self):self.assertEqual(len(GENRES),10)
    def test_manifest(self):self.assertTrue(validate(META))
    def test_total(self):self.assertEqual(sum(MONTHS),650000)
    def test_invalid_total(self):
        m=copy.deepcopy(META);m["total_yen"]=650001
        with self.assertRaises(ValueError):validate(m)
    def test_rights(self):
        m=copy.deepcopy(META);m["audio_rights"]="approved"
        with self.assertRaises(ValueError):validate(m)
    def test_publication(self):
        m=copy.deepcopy(META);m["publication_approved"]=True
        with self.assertRaises(ValueError):validate(m)
    def test_manual_only(self):
        m=copy.deepcopy(META);m["manual_post_only"]=False
        with self.assertRaises(ValueError):validate(m)
    def test_performance_claim(self):
        m=copy.deepcopy(META);m["performance_claim"]="10分→1分"
        with self.assertRaises(ValueError):validate(m)
    def test_all_genres(self):
        for g in GENRES:
            m=copy.deepcopy(META);m["genre"]=g
            self.assertTrue(validate(m))
    def test_safe_area(self):
        self.assertTrue(safe_box((67,325,643,565)))
        self.assertTrue(safe_box((107,1370,825,1519)))
        self.assertFalse(safe_box((67,1700,800,1800)))
    def test_timing(self):self.assertEqual((W,H,FPS),(1080,1920,30))
    def test_easing(self):self.assertEqual((ease(-1),ease(0),ease(1),ease(2)),(0,0,1,1))
    def test_frame(self):self.assertEqual(draw_frame(30).size,(1080,1920))
    def test_all_genre_frames(self):
        for g in GENRES:self.assertEqual(draw_frame(30,genre=g).size,(1080,1920))
    def test_outside(self):
        with self.assertRaises(ValueError):draw_frame(96)
if __name__=="__main__":unittest.main()
