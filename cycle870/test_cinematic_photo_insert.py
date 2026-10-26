import tempfile
import unittest
from pathlib import Path
from PIL import Image
from cinematic_photo_insert import (GENRES, REVIEW_POLICY, SCENE_FRAMES,
    SCENE_START, INSERT_TOP, INSERT_BOTTOM, ease, photo_base, draw_insert_frame,
    assert_copy_fits, font, sha256, ImageDraw)

class PhotoInsertTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.photo=Image.new('RGB',(941,1672),(34,68,110))

    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            for f in (0,20,35,50,77):
                im=draw_insert_frame(self.photo,f,genre)
                self.assertEqual(im.size,(1080,1358))

    def test_review_gate_fail_closed(self):
        self.assertTrue(REVIEW_POLICY['review_only'])
        self.assertFalse(REVIEW_POLICY['publication_approved'])
        self.assertFalse(REVIEW_POLICY['automatic_posting'])
        self.assertFalse(REVIEW_POLICY['external_upload'])
        self.assertFalse(REVIEW_POLICY['source_rights_reviewed'])

    def test_invalid_genre(self):
        with self.assertRaises(ValueError):draw_insert_frame(self.photo,0,'unsafe')

    def test_invalid_frames(self):
        for i in (-1,SCENE_FRAMES):
            with self.assertRaises(ValueError):draw_insert_frame(self.photo,i)

    def test_scene_is_not_caption_strip(self):
        self.assertEqual((SCENE_START,SCENE_FRAMES),(510,78))
        self.assertEqual((INSERT_TOP,INSERT_BOTTOM),(132,1490))
        self.assertGreater(1920-INSERT_BOTTOM,300)

    def test_image_resolution_gate(self):
        with self.assertRaises(ValueError):photo_base(Image.new('RGB',(640,480)))
        self.assertEqual(photo_base(self.photo).size,self.photo.size)

    def test_motion_easing(self):
        self.assertEqual(ease(-1),0)
        self.assertEqual(ease(0),0)
        self.assertEqual(ease(1),1)
        self.assertEqual(ease(2),1)
        self.assertLess(ease(.25),ease(.75))

    def test_frame_changes(self):
        a=draw_insert_frame(self.photo,0)
        b=draw_insert_frame(self.photo,77)
        self.assertNotEqual(a.tobytes(),b.tobytes())

    def test_label_width_guard(self):
        d=ImageDraw.Draw(Image.new('RGB',(1080,200)))
        with self.assertRaises(ValueError):assert_copy_fits(d,'あ'*50,54,95,995)

    def test_private_hash(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'a.txt';p.write_text('private')
            self.assertEqual(len(sha256(p)),64)

    def test_no_source_photo_in_repo(self):
        self.assertNotIn('pexels',str(GENRES))

    def test_font(self):
        self.assertGreater(font(54).size,0)

if __name__=='__main__':unittest.main()