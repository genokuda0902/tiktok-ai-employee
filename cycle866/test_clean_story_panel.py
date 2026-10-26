import unittest
from unittest.mock import patch
from pathlib import Path
from PIL import Image
from clean_story_panel import (DATA, GENRES, BOXES, ROI, START, COUNT,
    FRAMES, POLICY, draw_frame, layout_ok, text_fits, intersects, ease, contract,
    sha256, font)

class CleanStoryPanelTest(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_geometry(self): self.assertTrue(layout_ok())
    def test_caption_safe(self): self.assertLessEqual(ROI[1]+ROI[3],1490)
    def test_81_frames(self): self.assertEqual((START,COUNT,FRAMES),(170,81,691))
    def test_data_consistent(self):
        self.assertEqual([sum(v) for v in zip(*DATA.values())],[46,29])
    def test_maximum(self): self.assertEqual(max(DATA, key=lambda k: DATA[k][0]),'6月')
    def test_nonoverlap_detection(self): self.assertTrue(intersects((0,0,10,10),(9,9,20,20)))
    def test_touch_is_not_overlap(self): self.assertFalse(intersects((0,0,10,10),(10,10,20,20)))
    def test_ease_clamped(self): self.assertEqual([ease(-3),ease(0),ease(1),ease(8)],[0,0,1,1])
    def test_fails_closed_policy(self):
        self.assertFalse(POLICY['publication_approved'])
        self.assertFalse(POLICY['external_upload'])
        self.assertFalse(POLICY['source_rights_reviewed'])
    def test_all_genre_ends(self):
        for genre in GENRES:
            for i in (0,40,80):
                with self.subTest(genre=genre,i=i):
                    self.assertEqual(draw_frame(i,genre).size,(1080,1120))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError): draw_frame(0,'unapproved')
    def test_invalid_frame(self):
        with self.assertRaises(ValueError): draw_frame(81)
    def test_no_overwrite(self):
        with self.assertRaises(ValueError): contract(__file__,__file__,{},'ai_work')
    def test_no_fake_rights(self):
        with self.assertRaises(ValueError): contract(__file__,__file__+'.mp4',POLICY,'ai_work')
    def test_text_clip_detection(self):
        im=Image.new('RGB',(1080,1120));d=__import__('PIL.ImageDraw',fromlist=['ImageDraw']).Draw(im)
        self.assertFalse(text_fits(d,(1000,1000),'long caption',font(80),BOXES['summary']))

if __name__=='__main__': unittest.main()