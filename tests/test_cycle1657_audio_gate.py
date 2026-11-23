import unittest
from quality.cycle1657_audio_gate import ready

class GateTest(unittest.TestCase):
    def setUp(self):
        self.good = {"video_present": True, "vertical_1080p": True, "audio_stream_present": True}
        self.flags = dict(japanese_speech_verified=True, sync_verified=True, rights_approved=True, employee_approved=True)

    def test_all_approved(self):
        self.assertTrue(ready(self.good, **self.flags))

    def test_silent_video_rejected(self):
        self.assertFalse(ready({**self.good, "audio_stream_present": False}, **self.flags))

    def test_missing_speech_review_rejected(self):
        self.assertFalse(ready(self.good, **{**self.flags, "japanese_speech_verified": False}))

    def test_missing_rights_rejected(self):
        self.assertFalse(ready(self.good, **{**self.flags, "rights_approved": False}))

    def test_missing_employee_approval_rejected(self):
        self.assertFalse(ready(self.good, **{**self.flags, "employee_approved": False}))

if __name__ == "__main__":
    unittest.main()
