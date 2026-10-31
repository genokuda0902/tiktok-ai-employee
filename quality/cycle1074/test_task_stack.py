import unittest
from quality.cycle1074.task_stack import W,H,FPS,START,END,X,Y,OW,OH,PALETTES,frame_overlay,ease

class TaskStackTest(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
    def test_format(self):self.assertEqual((W,H,FPS),(1080,1920,30))
    def test_scene_two_only(self):self.assertEqual((START,END),(87,174))
    def test_title_safe(self):self.assertGreaterEqual(X,600)
    def test_caption_safe(self):self.assertLess(Y+OH,465)
    def test_canvas_safe(self):self.assertLessEqual(X+OW,W)
    def test_image_size(self):self.assertEqual(frame_overlay(130).size,(OW,OH))
    def test_dynamic(self):self.assertNotEqual(frame_overlay(100).tobytes(),frame_overlay(150).tobytes())
    def test_genre_palette(self):self.assertNotEqual(frame_overlay(135,'finance').tobytes(),frame_overlay(135,'ai_work').tobytes())
    def test_transparency(self):self.assertEqual(frame_overlay(135).getpixel((0,0))[3],0)
    def test_early_late_fade(self):self.assertLess(frame_overlay(87).getchannel('A').getextrema()[1],frame_overlay(120).getchannel('A').getextrema()[1])
    def test_ease_clamps(self):self.assertEqual((ease(-1),ease(2)),(0,1))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):frame_overlay(100,'not_a_genre')
    def test_invalid_frames(self):
        for f in (-1,86,174):
            with self.assertRaises(ValueError):frame_overlay(f)
if __name__=='__main__':unittest.main()
