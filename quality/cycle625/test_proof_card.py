import unittest
from proof_card import validate,layout,frame,ALLOWED
class ProofCardTests(unittest.TestCase):
    def test_all_ten_genres(self):
        for genre in ALLOWED:self.assertEqual(validate([120,150,200,250],['1月','2月','3月','4月'],genre),720)
    def test_all_four_rows_visible_in_safe_area(self):
        x=layout(); self.assertEqual(len(x['row_y']),4)
        self.assertTrue(all(100<=y<y+x['row_height']<855 for y in x['row_y']))
    def test_sum_uses_fourth_row(self):
        self.assertEqual(validate([120,150,200,250],['1月','2月','3月','4月'],'ai_work'),720)
        self.assertEqual(validate([120,150,200,0],['1月','2月','3月','4月'],'ai_work'),470)
    def test_reject_bad_values(self):
        with self.assertRaises(ValueError):validate([1,2,3],['1','2','3'],'ai_work')
        with self.assertRaises(ValueError):validate([1,2,3,-1],['1','2','3','4'],'ai_work')
        with self.assertRaises(ValueError):validate([1,2,3,4],['1','2','3','4'],'unapproved')
    def test_frame_dimensions(self):
        self.assertEqual(frame(3).size,(540,960))
if __name__=='__main__':unittest.main()
