import json
import unittest
from pathlib import Path
from caption_pulse import GENRES, POLICY, TRACK_Y, TRACK_H, validate, generate_ass, ass_time

ROOT = Path(__file__).parent
BEATS = json.loads((ROOT / "caption_beats.json").read_text())
MANIFEST = json.loads((ROOT / "manifest.review.json").read_text())

class CaptionPulseTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            self.assertIn("Dialogue: 1", generate_ass(BEATS, genre, MANIFEST))
    def test_review_only_fails_closed(self):
        for key, value in POLICY.items():
            wrong = dict(MANIFEST)
            wrong[key] = not value
            with self.assertRaises(ValueError):
                validate(BEATS, "ai_work", wrong)
    def test_24_beats_48_events(self):
        self.assertEqual(generate_ass(BEATS, "ai_work", MANIFEST).count("Dialogue: "), 48)
    def test_overlap_rejected(self):
        wrong = [dict(b) for b in BEATS]
        wrong[1]["start"] = 0.1
        with self.assertRaises(ValueError):
            validate(wrong, "ai_work", MANIFEST)
    def test_bad_count_rejected(self):
        with self.assertRaises(ValueError):
            validate(BEATS[:-1], "ai_work", MANIFEST)
    def test_safe_region(self):
        self.assertGreaterEqual(TRACK_Y, 1320)
        self.assertLess(TRACK_Y + TRACK_H, 1365)
    def test_clock(self):
        self.assertEqual(ass_time(1.23), "0:00:01.23")
    def test_each_beat_has_animation(self):
        text = generate_ass(BEATS, "ai_work", MANIFEST)
        self.assertEqual(text.count("\\fscx1\\t"), 24)
        self.assertEqual(text.count("\\fscx100"), 24)

if __name__ == "__main__":
    unittest.main()
