import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
import motion_story as m

class MotionTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(m.GENRES),10)
    def test_review_only(self): self.assertFalse(any(m.REVIEW_ONLY.values()))
    def test_photo_card_shape(self):
        with TemporaryDirectory() as d:
            p=Path(d)/'p.jpg'; Image.new('RGB',(800,900),'red').save(p)
            self.assertEqual(m.photo_card(p).size,(952,844))
    def test_foreground_alpha_and_labels(self):
        with TemporaryDirectory() as d:
            p=Path(d)/'p.jpg'; Image.new('RGB',(800,900),'blue').save(p)
            im=m.foreground(p,0,m.GENRES['ai_work'])
            self.assertEqual(im.getpixel((450,700))[3],0)
            self.assertEqual(im.getpixel((200,1210))[3],255)
            self.assertEqual(im.getpixel((70,240))[3],255)
    def test_motion_presets_distinct(self):
        self.assertNotEqual(m.motion_filter(0,94),m.motion_filter(1,94))
    def test_zoom_bounded(self): self.assertLessEqual(m.ZOOM_MAX,1.05)
    def test_safety_gate(self): self.assertFalse(m.REVIEW_ONLY['automatic_posting'])
    def test_video_spec(self): self.assertEqual((m.base.W,m.base.H,m.base.FPS,m.base.FRAME_COUNT),(1080,1920,30,691))

if __name__=='__main__': unittest.main()
