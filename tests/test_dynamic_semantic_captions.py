import unittest
from video_engine.dynamic_semantic_captions import CaptionCue, render_policy, validate_cues

class DynamicSemanticCaptionTests(unittest.TestCase):
    def _cues(self):
        beats = ("hook", "problem", "solution", "demo", "result", "cta")
        return [CaptionCue(b, i * 2.0, (i + 1) * 2.0, f"字幕{i+1}") for i, b in enumerate(beats)]

    def test_valid_six_beat_caption_track(self):
        validate_cues(self._cues())

    def test_wrong_geometry_fails_closed(self):
        with self.assertRaises(ValueError):
            validate_cues(self._cues(), 720, 1280)

    def test_empty_text_fails_closed(self):
        cues = self._cues()
        cues[2] = CaptionCue("solution", 4.0, 6.0, " ")
        with self.assertRaises(ValueError):
            validate_cues(cues)

    def test_policy_keeps_manual_release(self):
        p = render_policy()
        self.assertTrue(p["zero_cost"])
        self.assertTrue(p["caption_layer_separate_from_image"])
        self.assertTrue(p["human_quality_review_required"])
        self.assertFalse(p["auto_post"])

if __name__ == "__main__":
    unittest.main()
