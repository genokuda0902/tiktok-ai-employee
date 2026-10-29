import importlib.util, pathlib, unittest
P=pathlib.Path(__file__).resolve().parents[1]/"code"/"filled_example.py"
S=importlib.util.spec_from_file_location("filled_example",P)
m=importlib.util.module_from_spec(S);S.loader.exec_module(m)
class TestFilledExample(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(m.COLORS),10)
 def test_unreviewed_fails_closed(self):
  for g in m.COLORS:
   if g!="ai_work":
    with self.assertRaises(PermissionError): m.overlay(1,g)
 def test_unknown(self):
  with self.assertRaises(ValueError): m.overlay(1,"unknown")
 def test_bad_index(self):
  with self.assertRaises(ValueError): m.overlay(4)
 def test_three_states(self):
  self.assertNotEqual(m.overlay(0).tobytes(),m.overlay(1).tobytes())
  self.assertNotEqual(m.overlay(1).tobytes(),m.overlay(2).tobytes())
 def test_safe_area(self):
  for i in range(3):
   x0,y0,x1,y1=m.overlay(i).getchannel("A").getbbox()
   a,b,c,d=m.SAFE
   self.assertGreaterEqual(x0,a);self.assertGreaterEqual(y0,b)
   self.assertLessEqual(x1,c);self.assertLessEqual(y1,d)
 def test_no_fake_real_stats(self):
  self.assertEqual(len(m.ROWS),3)
  self.assertTrue(all(x and y for x,y in m.ROWS))
 def test_codec_gate(self):
  with self.assertRaises(ValueError):
   m.validate({"streams":[{"codec_type":"video","codec_name":"h264","width":720,"height":1280,"r_frame_rate":"30/1"}]})
if __name__=="__main__": unittest.main()
