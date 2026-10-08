import unittest
from dataclasses import replace
from video_engine.quality.beat_reveal_contract import Beat, validate_beats

class BeatRevealContractTests(unittest.TestCase):
    def setUp(self):
        self.beats = [Beat(f'scene{i//2}', i%2, i*1.25, (i+1)*1.25, '日本語の字幕', f's{i:02}.png') for i in range(16)]
        self.m = {'auto_post':False,'publication':'NOT_APPROVED','rights':'ORIGINAL_VECTOR_ONLY','personal_data':False,'resolution':[1080,1920],'human_review_required':True,'narration':'ABSENT'}
    def test_storyboard_passes_but_voice_fails(self):
        r=validate_beats(self.beats,self.m)
        self.assertEqual(r['technical_storyboard'],'PASS')
        self.assertEqual(r['japanese_narration'],'FAIL')
    def test_wrong_resolution(self):
        with self.assertRaises(ValueError):validate_beats(self.beats,{**self.m,'resolution':[540,960]})
    def test_unapproved_rights(self):
        with self.assertRaises(ValueError):validate_beats(self.beats,{**self.m,'rights':'UNKNOWN'})
    def test_auto_post(self):
        with self.assertRaises(ValueError):validate_beats(self.beats,{**self.m,'auto_post':True})
    def test_premature_approval(self):
        with self.assertRaises(ValueError):validate_beats(self.beats,{**self.m,'publication':'APPROVED'})
    def test_privacy(self):
        with self.assertRaises(ValueError):validate_beats(self.beats,{**self.m,'personal_data':True})
    def test_non_contiguous_timeline(self):
        b=self.beats.copy();b[2]=replace(b[2],start=5)
        with self.assertRaises(ValueError):validate_beats(b,self.m)
    def test_missing_second_beat(self):
        with self.assertRaises(ValueError):validate_beats(self.beats[:-1],self.m)
    def test_stage_mismatch(self):
        b=self.beats.copy();b[1]=replace(b[1],stage=0)
        with self.assertRaises(ValueError):validate_beats(b,self.m)
    def test_forged_tts_without_provenance(self):
        with self.assertRaises(ValueError):validate_beats(self.beats,{**self.m,'narration':'VERIFIED_JAPANESE_TTS'})
    def test_approved_tts_still_not_publishable(self):
        r=validate_beats(self.beats,{**self.m,'narration':'VERIFIED_JAPANESE_TTS','voice_provenance':'self-generated','voice_listening_approved':True})
        self.assertEqual(r['publication'],'NOT_APPROVED')
    def test_no_human_review(self):
        with self.assertRaises(ValueError):validate_beats(self.beats,{**self.m,'human_review_required':False})

if __name__=='__main__':unittest.main()
