"""Unit tests for zero-cost cycle651 slideshow motion."""
import unittest
from tiktok_quality.cycle651_motion import (
    FPS, BOUNDS, GENRES, frame_counts, zoom_expr,
    VOICE_NEWLY_GENERATED, SPOKEN_CAPTION_SEMANTIC_MATCH_VERIFIED,
    PUBLICATION_APPROVED,
)

class Cycle651MotionTest(unittest.TestCase):
    def test_10_genres(self):
        self.assertEqual(len(GENRES), 10)

    def test_eight_scenes_and_468_frames(self):
        self.assertEqual(len(frame_counts()), 8)
        self.assertEqual(sum(frame_counts()), 468)

    def test_duration(self):
        self.assertEqual(sum(frame_counts()) / FPS, 15.6)

    def test_motion_alternates(self):
        self.assertIn("z='1+", zoom_expr(0, 63))
        self.assertIn("z='1.075-", zoom_expr(1, 67))

    def test_vertical_output(self):
        self.assertIn("s=1080x1920:fps=30", zoom_expr(0, 63))

    def test_no_false_voice_or_publication_approval(self):
        self.assertFalse(VOICE_NEWLY_GENERATED)
        self.assertFalse(SPOKEN_CAPTION_SEMANTIC_MATCH_VERIFIED)
        self.assertFalse(PUBLICATION_APPROVED)

if __name__ == "__main__":
    unittest.main()
