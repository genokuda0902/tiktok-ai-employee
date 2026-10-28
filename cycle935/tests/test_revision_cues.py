import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from revision_cues import *

class CueTests(unittest.TestCase):
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_all_genres_render(self):
        for g in GENRES: self.assertEqual(draw_frame(18,g).size,CANVAS)
    def test_unknown_genre_fails_closed(self):
        with self.assertRaises(ValueError): draw_frame(12,'unsupported')
    def test_exact_frame_count(self): self.assertEqual(FRAME_COUNT,round((END-START)*FPS))
    def test_stage_order(self): self.assertEqual([stage_for_frame(n) for n in (0,28,29,57,58,86)],[0,0,1,1,2,2])
    def test_outside_scene_fails_closed(self):
        for n in (-1,87):
            with self.assertRaises(ValueError): stage_for_frame(n)
    def test_alpha_bounded(self):
        self.assertTrue(all(0<=alpha_for_frame(n)<=1 for n in range(FRAME_COUNT)))
    def test_visual_content(self): self.assertIsNotNone(draw_frame(17).getbbox())
    def test_transparent_first_frame(self): self.assertIsNone(draw_frame(0).getbbox())
    def test_caption_region_safe(self): self.assertLess(POSITION_Y+CANVAS[1],SAFE_CAPTION_START_Y)
    def test_no_external_assets(self): self.assertTrue(all(len(x)==3 for x in STEPS))

if __name__=='__main__': unittest.main()
