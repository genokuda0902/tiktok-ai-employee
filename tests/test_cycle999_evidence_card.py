import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'/'quality'))
from cycle999_evidence_card import SIZE,CARD,GENRES,EXAMPLE,make_card,text_fit,render
from PIL import ImageDraw,Image

class TestEvidenceCard(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRES),10)
 def test_ten_templates_render(self):
  for g in GENRES:
   im=make_card(g);self.assertEqual(im.size,SIZE)
 def test_transparent_caption_area(self):
  im=make_card()
  for x,y in ((0,0),(100,1500),(950,1500),(500,1700),(500,1900)):
   self.assertEqual(im.getpixel((x,y))[3],0)
 def test_card_opaque(self):self.assertGreater(make_card().getpixel((500,800))[3],240)
 def test_bounding_box(self):self.assertLess(CARD[3],1400)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):make_card('wrong')
 def test_invalid_content(self):
  with self.assertRaises(ValueError):make_card(content={'title':'test'})
 def test_long_text_rejected(self):
  c=dict(EXAMPLE);c['before']='あ'*91
  with self.assertRaises(ValueError):make_card(content=c)
 def test_text_fits(self):
  im=Image.new('RGB',(1000,100));d=ImageDraw.Draw(im)
  f=text_fit(d,'週次報告の「冒頭」だけ',(0,0,950,80),max_size=43)
  self.assertLessEqual(d.textbbox((0,0),'週次報告の「冒頭」だけ',font=f)[2],950)
 def test_missing_source(self):
  with self.assertRaises(FileNotFoundError):render(Path('/nonexistent.mp4'),Path('/tmp/out.mp4'))

if __name__=='__main__':unittest.main()
