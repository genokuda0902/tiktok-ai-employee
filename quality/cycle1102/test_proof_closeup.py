import unittest
from proof_closeup import CROP,DEST,GENRES,SAFE_Y,validate,START,END
GOOD={'genre':'ai_work','synthetic_scenario':True,'review_only':True,'rights_status':'unverified','contains_private_data':False}
class TestProofCloseup(unittest.TestCase):
    def test_ten_genres(self):
        for g in GENRES:self.assertTrue(validate({**GOOD,'genre':g}))
    def test_unsupported_genre(self):
        with self.assertRaises(ValueError):validate({**GOOD,'genre':'unknown'})
    def test_no_private_data(self):
        with self.assertRaises(ValueError):validate({**GOOD,'contains_private_data':True})
    def test_rights_unverified_only(self):
        with self.assertRaises(ValueError):validate({**GOOD,'rights_status':'approved'})
    def test_review_only(self):
        with self.assertRaises(ValueError):validate({**GOOD,'review_only':False})
    def test_synthetic_only(self):
        with self.assertRaises(ValueError):validate({**GOOD,'synthetic_scenario':False})
    def test_exact_manifest(self):
        with self.assertRaises(ValueError):validate({**GOOD,'extra':'yes'})
    def test_geometry(self):
        self.assertLess(DEST[1]+DEST[3],SAFE_Y)
        self.assertLess(CROP[1]+CROP[3],SAFE_Y)
        self.assertLessEqual(DEST[0]+DEST[2],1080)
    def test_scene_window(self):
        self.assertAlmostEqual(END-START,1.3)
if __name__=='__main__':unittest.main()
