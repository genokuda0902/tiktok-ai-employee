import unittest
from cycle653_proof_contract import Evidence, DATA, SCENES, validate_timeline, srt_from_timeline

class EvidenceTests(unittest.TestCase):
    def test_correct_total(self):
        self.assertTrue(Evidence(DATA, 650, 650).verified())

    def test_wrong_total(self):
        self.assertFalse(Evidence(DATA, 651, 650).verified())

    def test_caption_timeline(self):
        validate_timeline(SCENES)
        self.assertEqual(srt_from_timeline().count(' --> '), 8)

if __name__ == '__main__':
    unittest.main()
