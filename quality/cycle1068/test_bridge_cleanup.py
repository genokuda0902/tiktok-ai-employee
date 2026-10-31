import unittest
from quality.cycle1068.bridge_cleanup import (W,H,FPS,BRIDGE_Y,BRIDGE_H,SCENES,PALETTES,CLEAN_START,render_panel,scene_at)

class BridgeTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(PALETTES),10)
        for genre in PALETTES: self.assertEqual(render_panel(0,genre).size,(W,BRIDGE_H))
    def test_subtitle_region_protected(self):
        self.assertLessEqual(BRIDGE_Y+BRIDGE_H,1460)
        self.assertEqual((W,H,FPS),(1080,1920,30))
    def test_eight_contiguous_scenes(self):
        self.assertEqual(len(SCENES),8)
        self.assertEqual(SCENES[0][0],0)
        self.assertAlmostEqual(SCENES[-1][1],23.033333)
        for i in range(7): self.assertEqual(SCENES[i][1],SCENES[i+1][0])
    def test_exact_boundaries(self):
        for i,(a,b,_) in enumerate(SCENES):
            self.assertEqual(scene_at(a),i)
            self.assertEqual(scene_at((a+b)/2),i)
    def test_bad_time(self):
        for t in (-0.1,23.1):
            with self.assertRaises(ValueError): scene_at(t)
    def test_preserve_purposeful_lower_content(self):
        self.assertEqual([i for i,y in enumerate(CLEAN_START) if y is None],[1,5,7])
        for i in (1,5,7):
            self.assertEqual(render_panel(i).getbbox(),None)
    def test_bad_genre(self):
        with self.assertRaises(ValueError): render_panel(0,'private')
    def test_bad_scene(self):
        for i in (-1,8):
            with self.assertRaises(ValueError): render_panel(i)
    def test_step_changes_visual(self):
        self.assertNotEqual(render_panel(0).tobytes(),render_panel(4).tobytes())
    def test_palettes_change_visual(self):
        self.assertNotEqual(render_panel(4,'ai_work').tobytes(),render_panel(4,'finance').tobytes())

if __name__=='__main__':unittest.main()
