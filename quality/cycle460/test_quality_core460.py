import unittest
from dataclasses import dataclass
from quality_core460 import validate_beats, validate_evidence, publication_gate

@dataclass
class Beat:
    start: float
    end: float
    caption: str

class QualityTests(unittest.TestCase):
    def test_timeline(self):
        self.assertTrue(validate_beats([Beat(0,1.5,'導入'),Beat(1.5,20,'説明')]))
    def test_late_hook(self):
        with self.assertRaises(ValueError):
            validate_beats([Beat(0,2,'導入'),Beat(2,20,'説明')])
    def test_evidence(self):
        self.assertTrue(validate_evidence([('R1','A',12),('R3','A',9),('R5','A',14)],['R1','R3','R5'],35))
    def test_wrong_total(self):
        with self.assertRaises(ValueError):
            validate_evidence([('R1','A',12)],['R1'],35)
    def test_review_only(self):
        m={'rights':'SYNTHETIC_ORIGINAL','publication':'NOT_APPROVED','auto_post':False,'japanese_narration_verified':False,'caption_voice_sync_verified':False}
        self.assertEqual(publication_gate(m),'REVIEW_ONLY_NO_JAPANESE_VOICE')

if __name__=='__main__':
    unittest.main()
