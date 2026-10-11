import unittest
from quality.cycle486.quality_gate import Scene, validate_scenes, publication_gate
S = [Scene('ai_work',0,1.5,'手入力はもう終わり？'),
     Scene('ai_work',1.5,3.5,'元データを確認')]
class TestQualityGate(unittest.TestCase):
    def test_scenes(self): self.assertEqual(validate_scenes(S,20.17)['scene_count'],2)
    def test_bad_rights(self):
        with self.assertRaises(ValueError): validate_scenes([Scene('ai_work',0,1,'test','UNKNOWN')],20)
    def test_overlap(self):
        with self.assertRaises(ValueError): validate_scenes([Scene('ai_work',0,2,'a'),Scene('ai_work',1,3,'b')],20)
    def test_bad_duration(self):
        with self.assertRaises(ValueError): validate_scenes(S,float('nan'))
    def test_missing_caption(self):
        with self.assertRaises(ValueError): validate_scenes([Scene('ai_work',0,1,'')],20)
    def test_bad_genre(self):
        with self.assertRaises(ValueError): validate_scenes(S,20,{'sports'})
    def gate(self,**kw):
        p=dict(audio_codec='aac',japanese_voice_verified=False,
               captions_transcript_verified=False,semantic_sync_verified=False,
               human_approved=False,rights_approved=False,auto_post=False)
        p.update(kw); return publication_gate(**p)
    def test_fail_without_voice(self): self.assertEqual(self.gate()['publication'],'NOT_APPROVED')
    def test_pass_with_evidence(self):
        self.assertEqual(self.gate(japanese_voice_verified=True,captions_transcript_verified=True,
                                   semantic_sync_verified=True,human_approved=True,
                                   rights_approved=True)['publication'],'APPROVED_FOR_MANUAL_POST')
    def test_fail_without_sync(self):
        self.assertEqual(self.gate(japanese_voice_verified=True,captions_transcript_verified=True,
                                   human_approved=True,rights_approved=True)['publication'],'NOT_APPROVED')
    def test_fail_wrong_codec(self):
        self.assertEqual(self.gate(audio_codec='mp3',japanese_voice_verified=True,
                                   captions_transcript_verified=True,semantic_sync_verified=True,
                                   human_approved=True,rights_approved=True)['publication'],'NOT_APPROVED')
    def test_auto_post_rejected(self):
        with self.assertRaises(ValueError): self.gate(auto_post=True)
if __name__ == '__main__': unittest.main()
