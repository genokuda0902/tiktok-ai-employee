import unittest
from cycle626_selection_scene import GENRES,ROW_HEIGHT,ROW_TOP,selection_rect,selected_rows,validate,frame,FRAMES
class QualityTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:self.assertEqual(validate(genre=g)['sum'],720)
    def test_four_rows(self):
        x0,y0,x1,y1=selection_rect()
        self.assertEqual(y1-y0,4*ROW_HEIGHT)
        self.assertEqual(y0,ROW_TOP)
    def test_fourth_row_selected(self):
        self.assertEqual(selected_rows(0),0)
        self.assertEqual(selected_rows(1.3),4)
        self.assertEqual(selected_rows(2.4),4)
    def test_sum(self):
        self.assertEqual(validate()['sum'],720)
    def test_bad_genre(self):
        with self.assertRaises(ValueError):validate(genre='unknown')
    def test_bad_rights(self):
        with self.assertRaises(ValueError):validate(rights='UNKNOWN')
    def test_bad_values(self):
        with self.assertRaises(ValueError):validate(values=(120,150,200))
    def test_render(self):
        self.assertEqual(frame(FRAMES-1).size,(540,960))
    def test_publication_gate(self):
        v=validate()
        self.assertEqual(v['publication'],'NOT_APPROVED')
        self.assertFalse(v['new_japanese_voice'])
if __name__=='__main__':unittest.main()
