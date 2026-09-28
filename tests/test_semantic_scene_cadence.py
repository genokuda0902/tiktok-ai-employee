import unittest
from video_engine.semantic_scene_cadence import build_scene_beats, render_contract

class SemanticSceneCadenceTests(unittest.TestCase):
    def test_default_covers_full_video_without_gaps(self):
        beats = build_scene_beats(12.7)
        self.assertEqual(beats[0].start, 0.0)
        self.assertEqual(beats[-1].end, 12.7)
        for a, b in zip(beats, beats[1:]):
            self.assertEqual(a.end, b.start)

    def test_hook_is_shorter_than_demo(self):
        beats = build_scene_beats(12.7)
        durations = {b.role: b.end-b.start for b in beats}
        self.assertLess(durations['hook'], durations['demo'])

    def test_invalid_delivery_fails_closed(self):
        with self.assertRaises(ValueError):
            render_contract(720, 1280)

    def test_manual_rights_checked_release_only(self):
        c = render_contract()
        self.assertTrue(c['zero_cost'])
        self.assertTrue(c['human_approval_required'])
        self.assertTrue(c['rights_check_required'])
        self.assertFalse(c['auto_post'])

if __name__ == '__main__':
    unittest.main()
