import unittest
from src.cycle1233_chapter_progress import chapter_at, progress, ffmpeg_filter

class ChapterProgressTest(unittest.TestCase):
    def test_chapter_boundaries(self):
        self.assertEqual([chapter_at(t) for t in (0,7,16)],["導入","確認ポイント","まとめ"])
    def test_progress_clamps(self):
        self.assertEqual(progress(30,23),1)
        self.assertEqual(progress(-1,23),0)
    def test_invalid_duration(self):
        with self.assertRaises(ValueError): progress(1,0)
    def test_filter_has_three_chapters(self):
        self.assertIn("確認ポイント",ffmpeg_filter())
if __name__ == "__main__": unittest.main()
