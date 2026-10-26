import tempfile
import unittest
from pathlib import Path
from PIL import Image
from audio_caption_audit import (CUES,POLICY,analyze,trim_last_cue,validate_cues,meter_png)

class AudioCaptionTests(unittest.TestCase):
    def test_8_cues(self): self.assertTrue(validate_cues(CUES,23.04))
    def test_10_genres(self):
        for i in range(10):
            cues=((.1,.9),(.99,1.9)) if i%2 else ((.2,1.7),)
            self.assertTrue(validate_cues(cues,2.0))
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):validate_cues(((0,1),(.5,1.5)),2)
    def test_short_rejected(self):
        with self.assertRaises(ValueError):validate_cues(((0,.1),),2)
    def test_no_activity_rejected(self):
        with self.assertRaises(ValueError):analyze([-140.]*60,((0,1),))
    def test_last_tail_trim(self):
        e=[-15.]*65+[-140.]*25
        cues=((0,3),)
        rows=analyze(e,cues)
        updated=trim_last_cue(cues,rows)
        self.assertLess(updated[-1][1],3)
        self.assertGreater(updated[-1][1],2.1)
    def test_no_trim_when_aligned(self):
        cues=((0,2),)
        rows=analyze([-15.]*60,cues)
        self.assertEqual(trim_last_cue(cues,rows),cues)
    def test_meter_opaque_only_when_caption_visible(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'m.png';meter_png(p,[-12.]*90,0,((.3,2),))
            self.assertEqual(Image.open(p).getpixel((10,10))[3],0)
            meter_png(p,[-12.]*90,15,((.3,2),))
            self.assertGreater(Image.open(p).getpixel((10,10))[3],0)
    def test_publication_guard(self):
        self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['external_upload'])
        self.assertFalse(POLICY['automatic_posting'])
        self.assertFalse(POLICY['source_rights_reviewed'])

if __name__=='__main__':unittest.main()
