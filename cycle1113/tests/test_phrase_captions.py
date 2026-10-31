import importlib.util,tempfile,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'code'/'phrase_captions.py'
s=importlib.util.spec_from_file_location('phrase_captions',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_genres(self):
  self.assertEqual(len(m.GENRES),10)
  for g in m.GENRES:
   with tempfile.TemporaryDirectory() as t:
    p=Path(t)/'x.ass';m.make_ass(p,[(0,2,'一','二')],[1],g);self.assertIn('二',p.read_text())
 def test_reveal(self):self.assertEqual(m.select_reveals([(0,3,'一','二')],[(1.2,1.55)]),[1.55])
 def test_fail_closed(self):
  with self.assertRaises(ValueError):m.select_reveals([(0,3,'一','二')],[])
 def test_short_pause_rejected(self):
  with self.assertRaises(ValueError):m.select_reveals([(0,3,'一','二')],[(1.2,1.3)])
 def test_bad_time(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(ValueError):m.make_ass(Path(t)/'x.ass',[(0,2,'一','二')],[0.01])
 def test_escape(self):self.assertNotIn('{',m.clean('{danger}'))
 def test_time(self):self.assertEqual(m.ass_time(1.25),'0:00:01.25')
 def test_scene_continuity(self):
  self.assertAlmostEqual(m.SCENES[-1][1],22.5)
  for a,b in zip(m.SCENES,m.SCENES[1:]):self.assertAlmostEqual(a[1],b[0],places=3)
 def test_safe_area(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'x.ass';m.make_ass(p,[(0,2,'一','二')],[1]);d=p.read_text()
   self.assertIn(r'\pos(75,1461)',d);self.assertIn(r'\pos(75,1533)',d)
   self.assertIn(r'\fad(130,0)',d)
if __name__=='__main__':unittest.main()
