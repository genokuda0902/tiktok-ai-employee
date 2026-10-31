import unittest
from quality.cycle1066.habit_story import (W,H,COUNT,START,PALETTES,STEPS,
    ease,stage,render_frame,background,parse_srt)

class HabitStoryTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES),10)
        for genre in PALETTES:
            self.assertEqual(render_frame(0,genre).size,(W,H))
    def test_frame_limits(self):
        self.assertEqual((START,COUNT),(609,82))
        for i in (-1,82):
            with self.assertRaises(ValueError): stage(i)
    def test_three_stages(self):
        self.assertEqual([stage(i) for i in (0,27,28,55,56,81)],[0,0,1,1,2,2])
        self.assertEqual(len(STEPS),3)
    def test_ease(self):
        self.assertEqual(ease(-1),0)
        self.assertEqual(ease(2),1)
        self.assertAlmostEqual(ease(0.5),0.5)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError): render_frame(0,'unknown')
    def test_animated_frame_difference(self):
        base=background(PALETTES['ai_work'])
        self.assertNotEqual(render_frame(0,base=base).tobytes(),render_frame(81,base=base).tobytes())
    def test_caption_parser(self):
        s='1\n00:00:00,000 --> 00:00:02,900\n日本語の字幕\n\n2\n00:00:02,900 --> 00:00:05,800\n次の字幕\n'
        items=parse_srt(s)
        self.assertEqual(len(items),2)
        self.assertEqual(items[1][1],2.9)
        self.assertEqual(items[0][3],'日本語の字幕')

if __name__=='__main__': unittest.main()
