import unittest

from video_engine.scene_entry_punch import build_entry_punches, render_contract


class SceneEntryPunchTests(unittest.TestCase):
    def test_six_semantic_boundaries_are_supported(self):
        punches = build_entry_punches((0.0, 1.524, 3.302, 5.461, 8.255, 10.795), 12.7)
        self.assertEqual(len(punches), 6)
        self.assertLessEqual(max(p.scale_from for p in punches), 1.025)

    def test_bad_timeline_fails_closed(self):
        with self.assertRaises(ValueError):
            build_entry_punches((0.0, 3.0, 2.0), 12.7)
        with self.assertRaises(ValueError):
            build_entry_punches((0.2, 3.0), 12.7)

    def test_release_policy_stays_manual(self):
        c = render_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["rights_check_required"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])
        self.assertTrue(c["preserve_narration"])
        self.assertTrue(c["preserve_caption_copy"])

    def test_wrong_geometry_rejected(self):
        with self.assertRaises(ValueError):
            render_contract(720, 1280)


if __name__ == "__main__":
    unittest.main()
