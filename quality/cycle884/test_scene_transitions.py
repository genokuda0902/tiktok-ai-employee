import unittest
from scene_transitions import (
    FRAME_COUNT, GENRES, SCENE_BOUNDS, DISSOLVE_FRAMES,
    plan, smoothstep, transition_alpha, source_gate, validate_caption_layout
)

class TransitionTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        for g in GENRES:
            self.assertEqual(sum(s.frames for s in plan(g)), FRAME_COUNT)
    def test_no_unknown_genre(self):
        with self.assertRaises(ValueError): plan('made_up')
    def test_seven_scene_transitions(self):
        self.assertEqual(sum(s.kind == 'dissolve' for s in plan()), 7 * DISSOLVE_FRAMES)
    def test_frame_exact(self):
        self.assertEqual(sum(s.frames for s in plan()), 691)
    def test_scene_boundaries(self):
        self.assertEqual(SCENE_BOUNDS[0], 0)
        self.assertEqual(SCENE_BOUNDS[-1], FRAME_COUNT)
        self.assertEqual(len(SCENE_BOUNDS), 9)
    def test_ease_monotonic(self):
        values = [transition_alpha(i) for i in range(1, DISSOLVE_FRAMES + 1)]
        self.assertEqual(values, sorted(values))
        self.assertTrue(0 < values[0] < values[-1] < 1)
    def test_ease_endpoints(self):
        self.assertEqual(smoothstep(0), 0)
        self.assertEqual(smoothstep(1), 1)
    def test_ease_invalid(self):
        for v in [-0.1, 1.1]:
            with self.assertRaises(ValueError): smoothstep(v)
    def test_invalid_dissolve(self):
        for v in [0, 1, 9, 100]:
            with self.assertRaises(ValueError): plan(dissolve=v)
    def test_safe_source_review(self):
        self.assertFalse(source_gate(provenance='prior-cycle locally authored slides and mock Chromium UI')['publication_approved'])
    def test_reject_unknown_source(self):
        with self.assertRaises(ValueError): source_gate(provenance='downloaded influencer video')
    def test_reject_personal_data(self):
        with self.assertRaises(ValueError): source_gate(provenance='prior-cycle locally authored slides and mock Chromium UI', personal_data=True)
    def test_reject_external(self):
        with self.assertRaises(ValueError): source_gate(provenance='prior-cycle locally authored slides and mock Chromium UI', external_network=True)
    def test_reject_approval_without_rights(self):
        with self.assertRaises(ValueError): source_gate(provenance='prior-cycle locally authored slides and mock Chromium UI', publication_approved=True)
    def test_caption_safe(self):
        self.assertTrue(validate_caption_layout(80, 1470, 920, 190))
    def test_caption_unsafe(self):
        with self.assertRaises(ValueError): validate_caption_layout(80, 1700, 920, 190)

if __name__ == '__main__': unittest.main()
