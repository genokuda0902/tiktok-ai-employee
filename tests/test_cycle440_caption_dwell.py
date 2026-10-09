import unittest
from video_engine.quality.caption_dwell import allocate, max_rate, visual_units

class CaptionDwellTests(unittest.TestCase):
    def test_japanese_weight(self):
        self.assertGreater(visual_units("日本語"), visual_units("ABC"))
    def test_longer_caption(self):
        beats = allocate([("短い", "こちらは長い日本語字幕です")])
        self.assertLess(beats[0].end-beats[0].start, beats[1].end-beats[1].start)
    def test_frame_boundary(self):
        beats = allocate([("あ","い"),("う","え")])
        self.assertEqual(beats[-1].end,150)
        self.assertEqual(beats[1].end,beats[2].start)
    def test_reading_rate(self):
        self.assertLessEqual(max_rate(allocate([("短い","こちらは長い日本語字幕です")])),13.5)
    def test_overlong_rejected(self):
        with self.assertRaises(ValueError):
            allocate([("あ"*29,"い"*29)])
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            allocate([("","い")])

if __name__=="__main__":
    unittest.main()
