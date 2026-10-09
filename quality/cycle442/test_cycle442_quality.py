import unittest
from quality.cycle442.voice_gate import NarrationEvidence,narration_issues,publication_allowed
from quality.cycle442.proof_layout import claims
class Cycle442QualityTests(unittest.TestCase):
    def test_source_claims(self):
        self.assertEqual(claims()['delta'],150000)
        self.assertEqual(claims()['unique'],540000)
    def test_invalid_amount(self):
        with self.assertRaises(ValueError): claims([('A',-1)])
    def test_no_speech_sfx_only(self):
        e=NarrationEvidence(None,None,(),(),False,False)
        self.assertFalse(publication_allowed(e,20,True))
        self.assertIn('JAPANESE_NARRATION_MISSING_OR_UNVERIFIED',narration_issues(e,20))
    def test_unapproved_voice(self):
        e=NarrationEvidence('v.wav','engine',('こんにちは',),((0,1),),True,False)
        self.assertIn('VOICE_RIGHTS_UNAPPROVED',narration_issues(e,20))
    def test_overlap(self):
        e=NarrationEvidence('v.wav','engine',('A','B'),((0,1),(.5,2)),True,True)
        self.assertIn('VOICE_CAPTION_TIMELINE_INVALID',narration_issues(e,20))
    def test_requires_human(self):
        e=NarrationEvidence('v.wav','engine',('こんにちは',),((0,1),),True,True)
        self.assertFalse(publication_allowed(e,20,False))
        self.assertTrue(publication_allowed(e,20,True))
if __name__=='__main__': unittest.main()
