import unittest
from quality.cycle1553_gate import Evidence, publication_ready

class TestPublicationGate(unittest.TestCase):
    def test_silent_video_is_rejected(self):
        self.assertFalse(publication_ready(Evidence(False,False,False,True,True)))

    def test_effect_sound_is_not_narration(self):
        self.assertFalse(publication_ready(Evidence(True,False,False,True,True)))

    def test_missing_human_approval_rejected(self):
        self.assertFalse(publication_ready(Evidence(True,True,True,True,False)))

    def test_all_verified_evidence_passes(self):
        self.assertTrue(publication_ready(Evidence(True,True,True,True,True)))

if __name__ == "__main__":
    unittest.main()
