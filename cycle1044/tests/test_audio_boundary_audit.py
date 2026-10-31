import importlib.util,pathlib,unittest
p=pathlib.Path(__file__).resolve().parents[1]/'source'/'audio_boundary_audit.py'
s=importlib.util.spec_from_file_location('audit',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class AudioAuditTests(unittest.TestCase):
 def test_srt_time(self):self.assertAlmostEqual(m.seconds('00:00:02,900'),2.9)
 def test_cues(self):self.assertEqual(m.cues_from_srt('1\n00:00:00,000 --> 00:00:01,000\nこんにちは\n\n2\n00:00:01,000 --> 00:00:02,000\n世界'),[(0,1),(1,2)])
 def test_overlaps_fail(self):
  with self.assertRaisesRegex(ValueError,'overlapping'):m.cues_from_srt('1\n00:00:00,000 --> 00:00:01,500\na\n\n2\n00:00:01,000 --> 00:00:02,000\nb')
 def test_pause_parser(self):
  x=m.pauses_from_log('silence_start: 0.7\nsilence_end: 1.2 | silence_duration: 0.5',2)
  self.assertEqual(x,[(.7,1.2)])
 def test_not_semantic_pass(self):
  x=m.audit([(0,1),(1,2)],[(.8,1.2)])
  self.assertEqual(x[0]['acoustic_pause_proximity'],'NEAR_PAUSE_NOT_SEMANTIC_PROOF')
 def test_far_pause_warns(self):
  x=m.audit([(0,1),(1,2)],[(1.5,1.8)])
  self.assertEqual(x[0]['acoustic_pause_proximity'],'NEEDS_REVIEW')
if __name__=='__main__':unittest.main()
