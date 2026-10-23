import json, unittest, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from first_second_comparison import validate, ease, fit_cover, cover_crop, make_frame
CFG=json.loads((Path(__file__).resolve().parent/'config.json').read_text(encoding='utf-8'))
class TestHook(unittest.TestCase):
 def test_valid(self):self.assertTrue(validate(CFG))
 def test_publication_must_not_be_approved(self):
  with self.assertRaises(ValueError):validate({**CFG,'publication_approved':True})
 def test_rights_not_asserted(self):
  with self.assertRaises(ValueError):validate({**CFG,'rights_reviewed':True})
 def test_duration_guard(self):
  for dur in (.1,2.5):
   with self.assertRaises(ValueError):validate({**CFG,'hook_seconds':dur})
 def test_canvas_guard(self):
  with self.assertRaises(ValueError):validate({**CFG,'canvas':[720,1280]})
 def test_ease_bounded(self):
  self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
 def test_crop_guard(self):
  with self.assertRaises(ValueError):cover_crop(Image.new('RGB',(300,300)),[-1,0,10,10])
 def test_cover_size(self):
  self.assertEqual(fit_cover(Image.new('RGB',(300,100)),(150,200)).size,(150,200))
 def test_safe_area_and_fade(self):
  a=Image.new('RGB',(800,800),'#e2e2e2');b=Image.new('RGB',(800,800),'#242424')
  c={**CFG,'before_crop':[0,0,800,800],'after_crop':[0,0,800,800]}
  im=make_frame(c,a,b,.85)
  self.assertEqual(im.size,(1080,1920))
  self.assertEqual(im.getpixel((20,1800))[3],255)
  self.assertLess(make_frame(c,a,b,1.49).getpixel((500,500))[3],30)
 def test_portable_to_another_genre(self):
  self.assertTrue(validate({**CFG,'headline':'料理の手間、\n減らせる？','genre':'cooking'}))
if __name__=='__main__':unittest.main()
