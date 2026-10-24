import unittest
from evidence_kpi import (GENRES,COLORS,DEMO,SCENE_FRAMES,START_FRAME,
                          validate_demo,panel_frame,smoothstep,W,H)

class EvidenceKpiTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(set(GENRES),set(COLORS))
    def test_fictional_values_valid(self):validate_demo(DEMO)
    def test_reject_invalid_numbers(self):
        for value in (-1,101):
            with self.assertRaises(ValueError):validate_demo([('KPI',value,70)])
    def test_reject_zero_target(self):
        with self.assertRaises(ValueError):validate_demo([('KPI',30,0)])
    def test_reject_unsupported_genre(self):
        with self.assertRaises(ValueError):panel_frame(0,'unknown')
    def test_reject_invalid_frame(self):
        with self.assertRaises(ValueError):panel_frame(SCENE_FRAMES)
    def test_animation_progress_monotone(self):
        self.assertEqual(smoothstep(-1),0)
        self.assertEqual(smoothstep(2),1)
        self.assertLess(smoothstep(.3),smoothstep(.6))
    def test_output_image_geometry(self):
        self.assertEqual(panel_frame(0).size,(W,H))
    def test_drawing_actually_changes(self):
        a=panel_frame(0).tobytes();b=panel_frame(80).tobytes()
        self.assertNotEqual(a,b)
    def test_frame_timeline(self):
        self.assertEqual((START_FRAME,START_FRAME+SCENE_FRAMES), (179,263))
        self.assertLess(START_FRAME+SCENE_FRAMES,718)
    def test_transparent_outside_panel(self):
        im=panel_frame(30)
        self.assertEqual(im.getpixel((30,300))[3],0)
        self.assertGreater(im.getpixel((500,1000))[3],0)

if __name__=='__main__':unittest.main()
