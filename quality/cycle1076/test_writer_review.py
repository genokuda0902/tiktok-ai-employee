import unittest
from quality.cycle1076.writer_review import W,H,FPS,START,END,X,Y,OW,OH,PALETTES,CHECK_Y,frame_overlay,ease

class WriterReviewTest(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
    def test_output_format(self):self.assertEqual((W,H,FPS),(1080,1920,30))
    def test_scene_seven_only(self):self.assertEqual((START,END),(520,609))
    def test_safe_gutter_not_text(self):self.assertLessEqual(X+OW,150)
    def test_safe_from_captions(self):self.assertLess(Y+OH,1280)
    def test_canvas_bounds(self):self.assertLessEqual(X+OW,W)
    def test_three_rows(self):self.assertEqual(len(CHECK_Y),3)
    def test_image_size(self):self.assertEqual(frame_overlay(565).size,(OW,OH))
    def test_dynamic(self):self.assertNotEqual(frame_overlay(540).tobytes(),frame_overlay(590).tobytes())
    def test_ten_genre_differ(self):
        self.assertEqual(len({frame_overlay(590,g).tobytes() for g in PALETTES}),10)
    def test_no_text_pixels(self):
        # The rendered overlay itself has no pixels beyond the left screenshot gutter.
        self.assertEqual(frame_overlay(580).size[0],60)
    def test_stage_one_precedes_three(self):
        im=frame_overlay(540)
        self.assertGreater(im.getpixel((28,CHECK_Y[0]))[3],im.getpixel((28,CHECK_Y[2]))[3])
    def test_all_three_complete(self):
        im=frame_overlay(598)
        self.assertTrue(all(im.getpixel((28,y))[3]>0 for y in CHECK_Y))
    def test_start_fade(self):self.assertEqual(frame_overlay(START).getchannel('A').getextrema()[1],0)
    def test_end_fade(self):self.assertEqual(frame_overlay(END-1).getchannel('A').getextrema()[1],0)
    def test_ease_clamps(self):self.assertEqual((ease(-2),ease(3)),(0,1))
    def test_bad_genre(self):
        with self.assertRaises(ValueError):frame_overlay(570,'fake')
    def test_bad_frames(self):
        for f in (0,519,609,691):
            with self.assertRaises(ValueError):frame_overlay(f)

if __name__=='__main__':unittest.main()
