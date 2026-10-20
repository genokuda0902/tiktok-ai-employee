"""Unit tests for cycle722 motion contract (no source video required)."""
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import cycle722_motion as m
from PIL import Image

class MotionContract(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRES),10)
        self.assertEqual(len(set(m.GENRES)),10)
    def test_review_only(self):
        self.assertFalse(m.PUBLISH_ALLOWED)
    def test_motion_windows(self):
        self.assertEqual(m.SCENES["hook"],(0.0,3.2))
        self.assertEqual(m.SCENES["graph"],(9.8,12.8))
    def test_motion_filter_is_time_bounded(self):
        g=m.filter_graph()
        self.assertIn("between(t,0,2.0)",g)
        self.assertIn("between(t,9.8,12.75)",g)
        self.assertIn("eval=frame",g)
        self.assertIn("format=yuv420p",g)
    def test_overlay_assets(self):
        a,b=m.overlays()
        with Image.open(a) as i:self.assertEqual(i.size,(842,258))
        with Image.open(b) as i:self.assertEqual(i.size,(860,405))
    def test_no_brand_or_private_files(self):
        self.assertFalse(any(x in m.filter_graph() for x in ("IMG_5805","tiktok.com","https://")))
    def test_input_not_silently_assumed(self):
        self.assertIn("cycle721",str(m.PREVIOUS))
        self.assertTrue(str(m.OUTPUT).endswith(".mp4"))

if __name__=="__main__":unittest.main(verbosity=2)
