"""Offline layout and policy tests. Synthetic images only."""
import tempfile, unittest
from pathlib import Path
from PIL import Image
import immersive_photo as m

class ImmersivePhotoTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.root=Path(self.tmp.name)
  self.photos=[]
  for i in range(8):
   p=self.root/f'{i}.png'
   Image.new('RGB',(450,600),(80+i*10,105,135)).save(p)
   self.photos.append(str(p))
  self.beats=[{'start':i*.95,'end':i*.95+.6,'text':'日本語の字幕'} for i in range(24)]
 def tearDown(self):self.tmp.cleanup()
 def test_ten_genres(self):self.assertEqual(len(m.ACCENTS),10)
 def test_safety_policy(self):self.assertFalse(any(m.REVIEW_ONLY.values()))
 def test_eight_photos(self):self.assertTrue(m.validate(self.photos,self.beats,'ai_work'))
 def test_wrong_photo_count(self):
  with self.assertRaises(ValueError):m.validate(self.photos[:7],self.beats,'ai_work')
 def test_bad_genre(self):
  with self.assertRaises(ValueError):m.validate(self.photos,self.beats,'bad')
 def test_bad_beats(self):
  with self.assertRaises(ValueError):m.validate(self.photos,self.beats[:23],'ai_work')
 def test_overlapping_beats(self):
  self.beats[1]['start']=.1
  with self.assertRaises(ValueError):m.validate(self.photos,self.beats,'ai_work')
 def test_card_dimensions(self):self.assertEqual(m.photo_card(self.photos[0]).size,(996,1360))
 def test_foreground_rgba(self):
  im=m.foreground(0,'ai_work')
  self.assertEqual(im.size,(1080,1920))
  self.assertEqual(im.mode,'RGBA')
  self.assertEqual(im.getpixel((500,900))[3],0)
  self.assertEqual(im.getpixel((500,100))[3],255)
 def test_caption_timing(self):
  p=self.root/'captions.ass';m.write_ass(self.beats,p)
  t=p.read_text(encoding='utf-8')
  self.assertEqual(t.count('Dialogue:'),24)
  self.assertIn('日本語の字幕',t)
 def test_area_increase(self):self.assertGreater(m.CW*m.CH/(952*844),1.65)
 def test_all_genre_layers(self):
  for genre in m.ACCENTS:self.assertEqual(m.foreground(3,genre).size,(1080,1920))

if __name__=='__main__':unittest.main()
