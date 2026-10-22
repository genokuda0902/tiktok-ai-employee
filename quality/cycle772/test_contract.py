import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scene_contract as s

def manifest():
    return {
        "genre": "AI・仕事効率化",
        "supported_genres": list(s.GENRES),
        "review_status": "HUMAN_REVIEW",
        "quality_approved": False,
        "post_policy": "employee_manual_after_approval",
        "media_rights": "unverified_review_only",
        "source_origin": "user_provided_storyboard_review_only",
        "claim": "synthetic_comparison_only",
        "synthetic_data": True,
        "narration_cue": s.EXPECTED_CUE,
        "data": dict(s.DATA),
    }

class TestCycle772(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(s.GENRES), 10)
        self.assertEqual(len(set(s.GENRES.values())), 10)

    def test_arithmetic(self):
        self.assertEqual(sum(s.DATA.values()), 650000)
        self.assertEqual(s.DATA["4月"]-s.DATA["3月"], -20000)

    def test_valid_contract(self):
        self.assertTrue(s.validate(manifest()))

    def test_rights_and_approval_fail_closed(self):
        for key, value in [
            ("quality_approved", True), ("review_status", "APPROVED"),
            ("media_rights", "approved"), ("post_policy", "automatic"),
            ("source_origin", "unknown"),
        ]:
            with self.subTest(key=key):
                bad = {**manifest(), key: value}
                with self.assertRaises(ValueError):
                    s.validate(bad)

    def test_unsupported_claims_rejected(self):
        for key, value in [
            ("claim", "AI saves 90 percent"), ("narration_cue", "数分で完了"),
            ("synthetic_data", False),
        ]:
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    s.validate({**manifest(), key: value})

    def test_tampered_data_rejected(self):
        with self.assertRaises(ValueError):
            s.validate({**manifest(), "data": {"3月": 200000, "4月": 190000}})

    def test_timeline(self):
        self.assertEqual((s.SCENE_START, s.SCENE_END, s.SCENE_END-s.SCENE_START), (493, 604, 111))

    def test_all_genre_frames_are_portrait(self):
        for genre in s.GENRES:
            with self.subTest(genre=genre):
                frame = s.synthetic_smoke_frame(genre)
                self.assertEqual(frame.size, (1080, 1920))

    def test_caption_safe_area(self):
        self.assertTrue(s.safe_bbox((100, 200, 950, 1550)))
        self.assertFalse(s.safe_bbox((100, 200, 1070, 1550)))
        self.assertFalse(s.safe_bbox((100, 200, 950, 1800)))

if __name__ == "__main__":
    unittest.main()
