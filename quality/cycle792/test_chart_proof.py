import json,unittest
from pathlib import Path
from chart_proof import GENRES,bar_geometry,frame,validate,START,END,FPS
CFG=json.loads((Path(__file__).parent/'config.json').read_text(encoding='utf-8'))
class TestChartProof(unittest.TestCase):
    def test_ten_genres(self):
        for genre in GENRES:self.assertTrue(validate({**CFG,'genre':genre}))
    def test_total(self):self.assertEqual(sum(CFG['values_man_yen']),65)
    def test_reject_wrong_total(self):
        with self.assertRaises(ValueError):validate({**CFG,'total_man_yen':66})
    def test_reject_three_bars(self):
        with self.assertRaises(ValueError):validate({**CFG,'values_man_yen':[12,15,20]})
    def test_reject_rights(self):
        with self.assertRaises(ValueError):validate({**CFG,'rights_reviewed':True})
    def test_reject_publication(self):
        with self.assertRaises(ValueError):validate({**CFG,'publication_approved':True})
    def test_reject_non_synthetic(self):
        with self.assertRaises(ValueError):validate({**CFG,'source_data_kind':'real_records'})
    def test_geometry(self):
        b=bar_geometry(CFG,1.)
        self.assertEqual([x['value'] for x in b],[12,15,20,18])
        self.assertTrue(all(x['height']>0 for x in b))
    def test_zero_progress(self):self.assertEqual(sum(x['height'] for x in bar_geometry(CFG,0)),0)
    def test_full_frame_and_two_second_chart(self):
        im=frame(CFG,1.)
        self.assertEqual((im.mode,im.size),('RGBA',(1080,1920)))
        self.assertEqual(im.getpixel((1030,1000))[3],0)
        self.assertEqual(im.getpixel((200,700))[3],255)
        self.assertEqual(round((END-START)*FPS),60)
if __name__=='__main__':unittest.main()
