import unittest
from render import scene_at
from qa import evaluate
class QualityTests(unittest.TestCase):
 def test_scene_boundaries(self):
  self.assertEqual([scene_at(t) for t in (0,2.99,3,6,9,12)], [0,0,1,2,3,3])
 def test_silent_video_rejected(self):
  m={'streams':[{'codec_type':'video','width':720,'height':1280}]}
  self.assertFalse(evaluate(m,narration_verified=True,captions_synced=True,assets_approved=True,human_approved=True)['approved'])
 def test_audio_track_is_not_proof(self):
  m={'streams':[{'codec_type':'video','width':720,'height':1280},{'codec_type':'audio'}]}
  self.assertFalse(evaluate(m,assets_approved=True,human_approved=True)['approved'])
 def test_all_evidence_required(self):
  m={'streams':[{'codec_type':'video','width':720,'height':1280},{'codec_type':'audio'}]}
  self.assertTrue(evaluate(m,narration_verified=True,captions_synced=True,assets_approved=True,human_approved=True)['approved'])
if __name__=='__main__': unittest.main()
