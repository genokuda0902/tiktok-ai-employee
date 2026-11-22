import unittest
from audio_gate import publishable

class GateTests(unittest.TestCase):
    def setUp(self):
        self.good = dict(video=True,width=1080,height=1920,audio_stream=True,
                         japanese_narration_verified=True,caption_sync_verified=True,
                         assets_approved=True,employee_approved=True)
    def test_good(self): self.assertTrue(publishable(self.good))
    def test_silent(self): self.assertFalse(publishable({**self.good,"audio_stream":False}))
    def test_unknown_language(self): self.assertFalse(publishable({**self.good,"japanese_narration_verified":False}))
    def test_unsynced(self): self.assertFalse(publishable({**self.good,"caption_sync_verified":False}))
    def test_unapproved(self): self.assertFalse(publishable({**self.good,"employee_approved":False}))
if __name__ == "__main__": unittest.main()
