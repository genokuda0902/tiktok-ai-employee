"""Zero-cost, stdlib-only checks for the cycle730 scene contract."""
import unittest
from scene_contract import (
    W, H, FPS, START_FRAME, END_FRAME, TOTAL_FRAMES,
    GENRES, MONTHS, SALES, CAPTION_BOX, visible_rows,
    validate, publication_allowed,
)

class ContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for name in GENRES:
            self.assertTrue(validate(name))

    def test_timing(self):
        self.assertEqual((W, H, FPS), (1080, 1920, 30))
        self.assertEqual((START_FRAME, END_FRAME, TOTAL_FRAMES), (96, 195, 819))

    def test_progress(self):
        self.assertEqual(visible_rows(0), 1)
        self.assertEqual(visible_rows(90), 4)
        with self.assertRaises(ValueError):
            visible_rows(99)

    def test_fictional_proof(self):
        self.assertEqual(sum(SALES), 65)
        self.assertEqual(len(MONTHS), 4)

    def test_publication_fail_closed(self):
        self.assertFalse(publication_allowed({}))
        good = dict.fromkeys(("rights", "privacy", "narration", "captions", "phone", "employee"), True)
        good["mode"] = "MANUAL_ONLY"
        self.assertTrue(publication_allowed(good))
        for field in ("rights", "privacy", "narration", "captions", "phone", "employee"):
            bad = dict(good); bad[field] = False
            self.assertFalse(publication_allowed(bad))

if __name__ == "__main__":
    unittest.main()
