import unittest,sys,tempfile,wave,struct,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import caption_focus as m

class CaptionFocusTests(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_policy(self):
  self.assertFalse(m.POLICY['automatic_posting'])
  self.assertFalse(m.POLICY['public_media_upload'])
  self.assertFalse(m.POLICY['paid_service'])
  self.assertFalse(m.POLICY['publication_approved'])
 def test_scenes(self):
  self.assertEqual(sum(b-a+1 for a,b in m.SCENES),691)
  self.assertEqual(m.SCENES[0][0],0)
  self.assertEqual(m.SCENES[-1][1],690)
 def test_switch_center(self):
  self.assertTrue(36<=m.choose_switch_frame([],0,88)<=57)
 def test_switch_favors_pause(self):
  levels=[0.4]*200
  for i in range(72,82):levels[i]=0.0
  self.assertTrue(40<=m.choose_switch_frame(levels,0,88)<=52)
 def test_manifest_valid(self):
  d={'genre':'ai_work','publication_approved':False,'employee_approval':False,
     'contains_private_data':False,'source_sha256':'a'*64,
     'captions':[['一行目です','二行目です'] for _ in range(8)]}
  self.assertEqual(len(m.validate_manifest(d)),8)
 def test_manifest_private_fail(self):
  d={'genre':'ai_work','publication_approved':False,'employee_approval':False,
     'contains_private_data':True,'source_sha256':'a'*64,
     'captions':[['a','b'] for _ in range(8)]}
  with self.assertRaises(ValueError):m.validate_manifest(d)
 def test_manifest_genre_fail(self):
  d={'genre':'other','publication_approved':False,'employee_approval':False,
     'contains_private_data':False,'source_sha256':'a'*64,
     'captions':[['a','b'] for _ in range(8)]}
  with self.assertRaises(ValueError):m.validate_manifest(d)
 def test_manifest_missing_sha_fail(self):
  d={'genre':'ai_work','publication_approved':False,'employee_approval':False,
     'contains_private_data':False,'source_sha256':'abc',
     'captions':[['a','b'] for _ in range(8)]}
  with self.assertRaises(ValueError):m.validate_manifest(d)
 def test_release_gate(self):
  with self.assertRaises(PermissionError):m.release_gate({'spoken_japanese_semantics_verified':False})
 def test_release_gate_even_if_asr(self):
  with self.assertRaises(PermissionError):m.release_gate({'spoken_japanese_semantics_verified':True},independent_asr='dummy')
 def test_panel(self):
  if not Path(m.FONT).exists():self.skipTest('font unavailable')
  im=m.render_panel('AIで仕事を早くするなら、','最初の一歩が大事。',0)
  self.assertEqual(im.size,(1080,226))
 def test_overflow_fail(self):
  if not Path(m.FONT).exists():self.skipTest('font unavailable')
  with self.assertRaises(ValueError):m.render_panel('日本語'*20,'普通',0)
 def test_rms(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'a.wav'
   with wave.open(str(p),'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000)
    w.writeframes(struct.pack('<320h',*([0]*320)))
   self.assertEqual(m.read_rms(p),[0.0])
 def test_no_source_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'same.mp4';p.write_bytes(b'x')
   with self.assertRaises(ValueError):m.build(p,p,'nonexistent')

if __name__=='__main__':unittest.main()
