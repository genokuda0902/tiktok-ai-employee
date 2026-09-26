import unittest
from video_engine.audio_edge_guard import build_edge_filter

class AudioEdgeGuardTests(unittest.TestCase):
    def test_default_filter(self):
        f = build_edge_filter(12.233)
        self.assertIn("afade=t=in:st=0:d=0.020", f)
        self.assertIn("afade=t=out:st=12.153:d=0.080", f)
    def test_rejects_nonpositive_duration(self):
        with self.assertRaises(ValueError): build_edge_filter(0)
    def test_rejects_excessive_fades(self):
        with self.assertRaises(ValueError): build_edge_filter(1, fade_in_s=.2)
        with self.assertRaises(ValueError): build_edge_filter(1, fade_out_s=.2)
    def test_rejects_fade_longer_than_clip(self):
        with self.assertRaises(ValueError): build_edge_filter(.05, fade_out_s=.08)

if __name__ == '__main__': unittest.main()
