"""Fast CI tests; actual MP4 and audio are verified in local ZIP QA."""
import unittest
from cycle776.alignment_core import align_pairs

class AlignmentCoreTests(unittest.TestCase):
    def setUp(self):
        self.cues = [
            {"start": 0.1, "end": 0.9, "text": "前半"},
            {"start": 0.9, "end": 1.9, "text": "後半"},
            {"start": 2.0, "end": 3.0, "text": "次の前半"},
            {"start": 3.0, "end": 3.9, "text": "次の後半"},
        ]
        self.blocks = [(0.3, 1.8), (2.2, 3.8)]

    def test_speech_aligned(self):
        output = align_pairs(self.cues, self.blocks)
        self.assertEqual(len(output), 4)
        self.assertAlmostEqual(output[0]["start"], 0.255)
        self.assertAlmostEqual(output[1]["end"], 1.845)
        self.assertAlmostEqual(output[2]["start"], 2.155)

    def test_content_preserved(self):
        output = align_pairs(self.cues, self.blocks)
        self.assertEqual([x["text"] for x in output],
                         [x["text"] for x in self.cues])

    def test_no_overlapping_cues(self):
        output = align_pairs(self.cues, self.blocks)
        self.assertTrue(all(a["end"] <= b["start"]
                            for a,b in zip(output,output[1:])))

    def test_bad_count_rejected(self):
        with self.assertRaises(ValueError):
            align_pairs(self.cues, self.blocks[:1])

    def test_invalid_cue_rejected(self):
        broken = [dict(x) for x in self.cues]
        broken[1]["start"] = 0.7
        with self.assertRaises(ValueError):
            align_pairs(broken, self.blocks)

if __name__ == "__main__":
    unittest.main()
