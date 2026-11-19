import unittest
from quality.cycle1559_evidence_gate import Evidence, evaluate

class TestGate(unittest.TestCase):
    def base(self, **overrides):
        values=dict(width=720,height=1280,duration=20,video_decodes=True,
                    audio_stream=True,japanese_voice_verified=True,
                    captions_synchronized=True,assets_approved=True,
                    employee_approved=True)
        values.update(overrides)
        return Evidence(**values)

    def test_effect_only_audio_fails(self):
        result=evaluate(self.base(japanese_voice_verified=False))
        self.assertFalse(result["posting_allowed"])
        self.assertIn("japanese_narration_unverified",result["issues"])

    def test_no_employee_approval_fails(self):
        self.assertFalse(evaluate(self.base(employee_approved=False))["posting_allowed"])

    def test_all_evidence_passes(self):
        self.assertTrue(evaluate(self.base())["posting_allowed"])

    def test_no_audio_fails(self):
        self.assertIn("audio_missing",evaluate(self.base(audio_stream=False))["issues"])

if __name__ == "__main__": unittest.main()
