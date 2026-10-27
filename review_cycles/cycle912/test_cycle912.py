import importlib.util
import pathlib
import tempfile
import unittest

P=pathlib.Path(__file__).with_name('legible_calc_focus.py')
spec=importlib.util.spec_from_file_location('cycle912_focus',P)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ReviewOnlyTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.addCleanup(self.tmp.cleanup)
  d=pathlib.Path(self.tmp.name)
  self.source=d/'input.mp4';self.source.write_bytes(b'fake local review input')
  self.caps=[d/f'cap{i}.png' for i in range(3)]
  for c in self.caps:c.write_bytes(b'fictional screenshot')
  self.out=d/'cycle912_FOCUS_REVIEW_ONLY.mp4'
  self.sha=m.sha256(self.source)
 def valid(self,**kwargs):
  opts=dict(source=self.source,output=self.out,captures=self.caps,expected_sha=self.sha,genre='ai_work')
  opts.update(kwargs)
  return m.check_policy(**opts)
 def test_valid(self):self.assertIsNone(self.valid())
 def test_source_sha(self):
  with self.assertRaisesRegex(ValueError,'SHA'):self.valid(expected_sha='0'*64)
 def test_same_path(self):
  with self.assertRaisesRegex(ValueError,'overwrite'):self.valid(output=self.source)
 def test_reject_public_output(self):
  with self.assertRaisesRegex(ValueError,'REVIEW_ONLY'):self.valid(output=self.out.with_name('PUBLIC.mp4'))
 def test_reject_unlisted_genre(self):
  with self.assertRaisesRegex(ValueError,'allowlisted'):self.valid(genre='unknown')
 def test_reject_missing_capture(self):
  with self.assertRaisesRegex(ValueError,'three'):self.valid(captures=self.caps[:2])
 def test_reject_missing_file(self):
  with self.assertRaisesRegex(ValueError,'three'):self.valid(captures=self.caps[:2]+[pathlib.Path('/nonexistent.png')])
 def test_reject_unapproved_policy(self):
  with self.assertRaisesRegex(ValueError,'policy'):m.check_policy(self.source,self.out,self.caps,self.sha,'ai_work',policy='PUBLISH')
 def test_ten_genres(self):self.assertEqual(len(m.GENRE_ACCENTS),10)
 def test_three_stages(self):self.assertEqual([m.stage_for_frame(x) for x in (0,28,29,57,58,86)],[0,0,1,1,2,2])
 def test_frame_bounds(self):
  for x in (-1,87):
   with self.assertRaises(ValueError):m.stage_for_frame(x)
 def test_caption_safe(self):self.assertLess(m.OVERLAY_Y+m.OVERLAY_H,m.CAPTION_SAFE_Y)
 def test_87_frames(self):self.assertEqual(m.END_FRAME-m.START_FRAME,87)
 def test_policy(self):self.assertIn('PUBLICATION_NOT_APPROVED',m.POLICY)
 def test_pure_sha(self):self.assertEqual(self.sha,m.sha256(self.source))

if __name__=='__main__':unittest.main()
