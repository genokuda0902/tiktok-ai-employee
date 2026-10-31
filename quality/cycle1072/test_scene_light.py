import unittest
from quality.cycle1072.scene_light import W,H,FPS,NFRAMES,START,END,OVERLAY_Y,OVERLAY_H,PALETTES,frame_overlay

class SceneLightTest(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
    def test_format(self):self.assertEqual((W,H,FPS,NFRAMES),(1080,1920,30,691))
    def test_hook_only(self):self.assertEqual((START,END),(0,87))
    def test_caption_safe(self):self.assertLess(OVERLAY_Y+OVERLAY_H,1350)
    def test_title_safe(self):self.assertGreaterEqual(OVERLAY_Y,380)
    def test_rgba_size(self):self.assertEqual(frame_overlay(30).size,(W,OVERLAY_H))
    def test_dynamic(self):self.assertNotEqual(frame_overlay(0).tobytes(),frame_overlay(45).tobytes())
    def test_genre_color(self):self.assertNotEqual(frame_overlay(45,'finance').tobytes(),frame_overlay(45,'ai_work').tobytes())
    def test_nonopaque(self):self.assertLess(frame_overlay(30).getchannel('A').getextrema()[1],255)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):frame_overlay(30,'bad')
    def test_invalid_frame(self):
        for x in (-1,END):
            with self.assertRaises(ValueError):frame_overlay(x)
if __name__=='__main__':unittest.main()
