import unittest
import numpy as np
from photo_visibility import (GENRES,POLICY,SCENES,SCENE_FRAMES,
    PANEL_W,PANEL_H,PANEL_Y,PREVIOUS_PANEL_AREA,make_panel,validate)
class PhotoVisibilityTest(unittest.TestCase):
    def test_all_ten_genres(self):
        for genre in GENRES: validate(genre,POLICY)
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError): validate('other',POLICY)
    def test_reject_approval_bypass(self):
        with self.assertRaises(ValueError): validate('ai_work',{**POLICY,'publication_approved':True})
    def test_reject_auto_post(self):
        with self.assertRaises(ValueError): validate('ai_work',{**POLICY,'automatic_posting':True})
    def test_reject_rights_assertion(self):
        with self.assertRaises(ValueError): validate('ai_work',{**POLICY,'source_rights_reviewed':True})
    def test_timing(self): self.assertEqual(sum(SCENE_FRAMES),691)
    def test_scene_count(self): self.assertEqual(len(SCENES),8)
    def test_panel_footprint(self): self.assertLess(PANEL_W*PANEL_H/PREVIOUS_PANEL_AREA,.2)
    def test_panel_inside_existing_banner(self):
        self.assertGreaterEqual(PANEL_Y,1080)
        self.assertLessEqual(PANEL_Y+PANEL_H,1230)
    def test_panels_distinct(self):
        self.assertEqual(len({hash(make_panel(i).tobytes()) for i in range(8)}),8)
    def test_alpha_visible(self):
        a=make_panel(0)
        self.assertEqual(a.shape,(PANEL_H,PANEL_W,4))
        self.assertGreater(int(a[:,:,3].max()),200)
    def test_accent_varies(self):
        self.assertFalse(np.array_equal(make_panel(0,'ai_work'),make_panel(0,'romance')))
if __name__=='__main__': unittest.main()
