"""Offline CI tests for cycle812 narrative-matched 10-genre contract."""
import unittest
import scene_spec as s
class StoryboardTests(unittest.TestCase):
    def test_dimensions(self): self.assertEqual((s.WIDTH,s.HEIGHT,s.FPS),(1080,1920,30))
    def test_ten_genres(self): self.assertEqual(len(set(s.GENRES)),10)
    def test_eight_semantic_scenes(self): self.assertEqual(len(s.SCENE_TYPES),8)
    def test_24_subtitle_phases(self): self.assertEqual(sum(map(len,s.CHUNKS)),24)
    def test_tiktok_safe_area(self):
        self.assertLess(s.SAFE_CAPTION_RECT[2],s.RIGHT_UI_RESERVED_X)
        self.assertLess(s.SAFE_CAPTION_RECT[3],s.BOTTOM_UI_RESERVED_Y)
    def test_frame_allocation(self):
        for n in range(20,120):
            self.assertEqual(sum(s.allocate_frames(n,s.CHUNKS[0])),n)
    def test_no_automatic_posting(self):
        self.assertFalse(s.POSTING_ENABLED)
        self.assertFalse(s.EMPLOYEE_APPROVED)
    def test_full_validation(self): self.assertTrue(s.validate())
if __name__ == "__main__": unittest.main()
