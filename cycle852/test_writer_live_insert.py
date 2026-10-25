import unittest
import tempfile
from pathlib import Path
import numpy as np
from writer_live_insert import GENRES, POLICY, PANEL, WINDOW, beat, composite, panel_image, validate

class WriterCutawayTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_fail_closed(self):
        self.assertTrue(POLICY['review_only']);self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['automatic_posting']);self.assertFalse(POLICY['external_upload'])
    def test_beat_boundaries(self):
        self.assertEqual([beat(i,81) for i in (0,26,27,53,54,80)],[0,0,1,1,2,2])
    def test_invalid_beat(self):
        with self.assertRaises(ValueError): beat(81,81)
    def test_panel_dimensions(self): self.assertEqual((PANEL[2]-PANEL[0],PANEL[3]-PANEL[1]),(908,758))
    def test_scene7_only(self): self.assertEqual(WINDOW,(507,588))
    def test_protect_subtitle_region(self):
        f=np.full((1920,1080,3),23,np.uint8)
        g=np.full((900,1440,3),215,np.uint8)
        out=composite(f,g,20,81,'ai_work')
        self.assertTrue(np.array_equal(f[1300:1850],out[1300:1850]))
        self.assertTrue(np.array_equal(f[:420],out[:420]))
        self.assertGreater(np.mean(np.abs(out[476:1234,86:994].astype(int)-23)),2)
    def test_gui_too_small(self):
        with self.assertRaises(ValueError): panel_image(np.zeros((300,500,3),np.uint8),0,81,'ai_work')
    def test_each_genre_renders(self):
        g=np.full((900,1440,3),220,np.uint8)
        for genre in GENRES:
            self.assertEqual(panel_image(g,30,81,genre).shape,(758,908,3))
    def test_invalid_genre(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError): validate('x','y',str(Path(t)/'out.mp4'),{},'unknown',(0,1))
    def test_missing_inputs(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(FileNotFoundError): validate('x','y',str(Path(t)/'out.mp4'),{},'ai_work',(0,1))

if __name__=='__main__':unittest.main()