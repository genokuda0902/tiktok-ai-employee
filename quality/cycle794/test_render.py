import unittest
from render import build_filter, DEFAULT_FRAMES, GENRE_THEMES
class RenderTests(unittest.TestCase):
    def test_frame_count(self): self.assertEqual(sum(DEFAULT_FRAMES),429)
    def test_genres(self): self.assertEqual(len(GENRE_THEMES),10)
    def test_transitions(self): self.assertEqual(build_filter(DEFAULT_FRAMES).count("xfade="),7)
    def test_artwork_only(self):
        graph=build_filter(DEFAULT_FRAMES)
        self.assertIn("crop=900:620:90:560",graph)
        self.assertIn("overlay=90:560",graph)
    def test_invalid_short_scene(self):
        with self.assertRaises(AssertionError): build_filter([3,2],6)
    def test_total_frame_trim(self):
        self.assertIn("trim=end_frame=429",build_filter(DEFAULT_FRAMES))
if __name__=="__main__": unittest.main()
