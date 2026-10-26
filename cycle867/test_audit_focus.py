import unittest
from PIL import Image
from audit_focus import (DATA,TOTALS,GENRES,ROI,START,COUNT,FRAMES,
    SAFE_END_Y,POLICY,stage,ease,draw_frame,contract)

class AuditFocusTest(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_fixture_totals(self):self.assertEqual(TOTALS,(46,29))
    def test_fictional_fixture(self):self.assertTrue(POLICY['fictional_example'])
    def test_safe_region(self):self.assertEqual(ROI[1]+ROI[3],SAFE_END_Y)
    def test_frame_contract(self):self.assertEqual((START,COUNT,FRAMES),(336,86,691))
    def test_stages(self):self.assertEqual([stage(x) for x in (0,26,27,55,56,85)],[0,0,1,1,2,2])
    def test_bad_stage(self):
        with self.assertRaises(ValueError):stage(86)
    def test_ease_clamps(self):self.assertEqual((ease(-10),ease(0),ease(1),ease(5)),(0,0,1,1))
    def test_each_genre_renders_each_stage(self):
        for genre in GENRES:
            for i in (0,26,27,55,56,85):
                with self.subTest(genre=genre,i=i):
                    self.assertEqual(draw_frame(i,genre).size,(1080,1358))
    def test_no_publication(self):
        for key in ('publication_approved','external_upload','automatic_posting','source_rights_reviewed'):
            self.assertFalse(POLICY[key])
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):draw_frame(0,'bad')
    def test_reject_bad_manifest(self):
        with self.assertRaises(ValueError):contract(__file__,__file__+'.mp4',{},'ai_work')
    def test_no_overwrite(self):
        with self.assertRaises(ValueError):contract(__file__,__file__,{},'ai_work')

if __name__=='__main__':unittest.main()