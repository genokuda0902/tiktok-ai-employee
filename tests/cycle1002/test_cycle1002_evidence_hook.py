import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'/'quality'))
from cycle1002_evidence_hook import evidence_summary,parse_srt,make_badge,GENRES,render

EXAMPLE={'genre':'ai_work','classification':'synthetic_example','left_series':[12,16,18],
         'right_series':[8,9,12],'expected_left':46,'expected_right':29,'expected_difference':17}
class EvidenceTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_real_math(self): self.assertEqual(evidence_summary(EXAMPLE)['difference'],17)
    def test_bad_total_fails(self):
        with self.assertRaises(ValueError):evidence_summary(dict(EXAMPLE,expected_left=45))
    def test_bad_difference_fails(self):
        with self.assertRaises(ValueError):evidence_summary(dict(EXAMPLE,expected_difference=18))
    def test_non_synthetic_fails(self):
        with self.assertRaises(ValueError):evidence_summary(dict(EXAMPLE,classification='real_unverified'))
    def test_unknown_genre_fails(self):
        with self.assertRaises(ValueError):evidence_summary(dict(EXAMPLE,genre='unsupported'))
    def test_negative_fails(self):
        with self.assertRaises(ValueError):evidence_summary(dict(EXAMPLE,left_series=[12,-16,18]))
    def test_srt_parses(self):
        cues=parse_srt('1\n00:00:00,000 --> 00:00:01,200\n日本語字幕\n\n2\n00:00:01,200 --> 00:00:02,400\n次\n')
        self.assertEqual(len(cues),2)
        self.assertFalse(cues[0]['independent_asr_verified'])
    def test_srt_overlap_rejected(self):
        with self.assertRaises(ValueError):parse_srt('1\n00:00:00,000 --> 00:00:01,500\nA\n\n2\n00:00:01,000 --> 00:00:02,000\nB\n')
    def test_review_gate(self):
        with self.assertRaises(ValueError):render('no.mp4','out.mp4',EXAMPLE,'badge.png','report.json',False)
    def test_badge_rgba(self):
        import tempfile
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'badge.png';make_badge(EXAMPLE,p)
            im=Image.open(p)
            self.assertEqual(im.mode,'RGBA')
            self.assertEqual(im.size,(425,146))
            self.assertEqual(im.getpixel((0,0))[3],0)

if __name__=='__main__': unittest.main()
