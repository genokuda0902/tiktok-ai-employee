import unittest
from audio_readiness import AudioEvidence, narration_ready

class AudioReadinessTest(unittest.TestCase):
    def test_cue_only_fails(self):
        self.assertFalse(narration_ready(AudioEvidence(True,False,False,True)))
    def test_no_approval_fails(self):
        self.assertFalse(narration_ready(AudioEvidence(True,True,True,False)))
    def test_all_evidence_passes(self):
        self.assertTrue(narration_ready(AudioEvidence(True,True,True,True)))

if __name__ == '__main__': unittest.main()
