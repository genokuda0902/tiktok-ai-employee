import unittest
from audio_chapter_audit import CHAPTER_EDGES,validate_edges

class ChapterAudioTest(unittest.TestCase):
    def test_eight_chapters_cover_video(self):
        self.assertEqual(len(CHAPTER_EDGES)-1,8)
        validate_edges(CHAPTER_EDGES,23.033333)
    def test_reject_missing_end(self):
        with self.assertRaises(ValueError):validate_edges(CHAPTER_EDGES[:-1],23.033333)
    def test_reject_reversed(self):
        with self.assertRaises(ValueError):validate_edges([0,2,1,3],3)
    def test_reject_nan(self):
        with self.assertRaises(ValueError):validate_edges([0,float('nan'),3],3)
