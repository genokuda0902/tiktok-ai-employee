import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from render_accessible_captions import CUES, GENRES, validate_cues, approval_gate, write_captions, timestamp

class CaptionQualityTests(unittest.TestCase):
    def test_10_genres(self): self.assertEqual(len(GENRES),10)
    def test_all_cues_contiguous(self): self.assertTrue(validate_cues())
    def test_short_flash_rejected(self):
        cues=list(CUES); cues[5]=(12.0,15.5,'長い字幕'); cues[6]=(15.5,16.0,'読めない');
        with self.assertRaises(ValueError):validate_cues(cues)
    def test_gap_rejected(self):
        cues=list(CUES); cues[1]=(2.2,4.0,cues[1][2]);
        with self.assertRaises(ValueError):validate_cues(cues)
    def test_uncovered_end_rejected(self):
        cues=list(CUES); cues[-1]=(18.5,19.0,cues[-1][2]);
        with self.assertRaises(ValueError):validate_cues(cues)
    def test_bad_caption_rejected(self):
        cues=list(CUES); cues[0]=(0,2,'');
        with self.assertRaises(ValueError):validate_cues(cues)
    def test_caption_files_match(self):
        with TemporaryDirectory() as td:
            s=write_captions(td)
            ass=Path(td,'captions.ass').read_text(encoding='utf-8')
            self.assertEqual(s.count(' --> '),len(CUES))
            self.assertEqual(ass.count('Dialogue: 0,'),len(CUES))
    def test_timestamp(self):self.assertEqual(timestamp(18.5),'00:00:18,500')
    def test_review_gate(self):
        d={'publication':'NOT_APPROVED','auto_post':False,'narration':'ABSENT','voice_semantic_sync':'UNVERIFIED','rights':'INHERITED_ASSETS_UNVERIFIED'}
        self.assertTrue(approval_gate(d))
        for k,v in [('publication','APPROVED'),('auto_post',True),('narration','JAPANESE'),('voice_semantic_sync','VERIFIED'),('rights','APPROVED')]:
            bad={**d,k:v}
            with self.assertRaises(ValueError):approval_gate(bad)
if __name__=='__main__':unittest.main()
