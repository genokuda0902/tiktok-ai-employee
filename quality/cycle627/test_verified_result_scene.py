import unittest
from verified_result_scene import contract, display_state, frame_text, GENRES, FRAMES, draw_frame
class TestResultProof(unittest.TestCase):
    def test_ten_genres(self):
        for g in GENRES:self.assertEqual(contract(genre=g)['total'],720)
    def test_four_inputs(self):
        with self.assertRaises(ValueError):contract(values=(120,150,200))
    def test_negative_input(self):
        with self.assertRaises(ValueError):contract(values=(120,-1,200,250))
    def test_bad_genre(self):
        with self.assertRaises(ValueError):contract(genre='unknown')
    def test_rights_fail_closed(self):
        with self.assertRaises(ValueError):contract(rights='PUBLIC')
    def test_publication_fail_closed(self):
        with self.assertRaises(ValueError):contract(publication='APPROVED')
    def test_no_intermediate_wrong_total(self):
        data=contract()
        for i in range(FRAMES):
            s=frame_text(i,data)
            self.assertNotIn('420',s)
            if i<23:self.assertNotIn('720',s)
            else:self.assertIn('720',s)
    def test_state_boundaries(self):
        self.assertEqual(display_state(22),'calculating')
        self.assertEqual(display_state(23),'verified')
    def test_formula(self):self.assertEqual(contract()['formula'],'=SUM(B2:B5)')
    def test_frame_render(self):self.assertEqual(draw_frame(30,contract()).size,(540,960))
    def test_data_is_synthetic(self):self.assertFalse(contract()['actual_excel_recording'])
    def test_no_new_voice_claim(self):self.assertFalse(contract()['new_japanese_voice'])
if __name__=='__main__':unittest.main()
