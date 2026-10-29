"""Synthetic and permission tests: no user audio/video required."""
import importlib.util,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
p=Path(__file__).with_name('calc_proof.py');spec=importlib.util.spec_from_file_location('calc_proof',p)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
class CalcProofTest(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.GENRE_COLORS),10)
 def test_one_reviewed(self):self.assertEqual(m.REVIEWED_GENRES,{'ai_work'})
 def test_total_a(self):self.assertEqual(sum(x[1] for x in m.ROWS),46)
 def test_total_b(self):self.assertEqual(sum(x[2] for x in m.ROWS),29)
 def test_unique_months(self):self.assertEqual(len(set(x[0] for x in m.ROWS)),3)
 def test_frame_range(self):self.assertEqual(m.END-m.START,87)
 def test_no_publish_automation(self):self.assertNotIn('tiktok.com',p.read_text())
 def test_pdf_recalc_and_stages(self):
  with tempfile.TemporaryDirectory() as tmp:
   _,pdf,png,text=m.build_calc_export(tmp)
   self.assertTrue(pdf.is_file());self.assertIn('46',text);self.assertIn('29',text)
   ims=m.make_stages(png,tmp)
   self.assertEqual(len(ims),3)
   for im in ims:
    with Image.open(im) as image:self.assertEqual(image.size,(1080,1450))
 def test_unreviewed_genre_rejected(self):
  self.assertTrue(all(x not in m.REVIEWED_GENRES for x in m.GENRE_COLORS if x!='ai_work'))
if __name__=='__main__':unittest.main()
