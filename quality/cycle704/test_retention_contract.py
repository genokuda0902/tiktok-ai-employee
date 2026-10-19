import unittest
from retention_contract import *

class Cycle704RetentionTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)
    def test_continuous_beats(self):
        b = beats()
        self.assertEqual(b[0].start, 0)
        self.assertEqual(b[-1].end, 20)
        self.assertTrue(all(a.end == z.start for a, z in zip(b, b[1:])))
    def test_verified_hook_visible_immediately(self):
        for t in (0, .1, .5, .95):
            self.assertEqual(proof_hook(t)["value"], 6000)
            self.assertTrue(proof_hook(t)["visible"])
    def test_false_number_rejected(self):
        with self.assertRaises(ValueError): proof_hook(.1, 7000)
    def test_bad_time_rejected(self):
        for t in (-1, float("nan"), 20):
            with self.assertRaises(ValueError): proof_hook(t)
    def test_sumif(self):
        self.assertEqual(verified_sumif(), 6000)
        self.assertEqual(verified_sumif([("A", 3), ("B", 4), ("A", 2)], "A"), 5)
    def test_negative_rejected(self):
        with self.assertRaises(ValueError): verified_sumif([("青", -10)])
    def test_safe_caption(self):
        self.assertTrue(safe_caption((34, 708, 460, 758)))
        self.assertFalse(safe_caption((0, 800, 530, 930)))
    def test_bgm_is_not_narration(self):
        self.assertEqual(narration_status(1, False), "BGM_ONLY_NOT_JA")
        self.assertEqual(narration_status(0, True), "BGM_ONLY_NOT_JA")
    def test_fail_closed(self):
        self.assertEqual(release_gate(True, True, False, False, False, False),
                         "PUBLICATION_NOT_APPROVED")
        self.assertEqual(release_gate(True, True, True, True, True, True),
                         "MANUAL_POST_REVIEWED")
        self.assertEqual(release_gate(True, False, True, True, True, True),
                         "PUBLICATION_NOT_APPROVED")

if __name__ == "__main__":
    unittest.main()
