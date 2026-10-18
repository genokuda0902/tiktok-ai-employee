import unittest
from caption_contract import GENRES, REVIEW_POLICY, select_burned_cues, validate_scene_captions

CUES=[(0.,2.,"フック"),(2.,4.,"課題"),(4.,6.,"結果")]
SUPPRESS={1:{"reviewed":True,"reason":"Existing scene STEP text","existing_text":"課題"}}

class ContractTests(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(GENRES),10)
    def test_timeline(self): self.assertTrue(validate_scene_captions(CUES,SUPPRESS,6))
    def test_suppress_only_reviewed(self):
        with self.assertRaises(ValueError):
            validate_scene_captions(CUES,{1:{"reviewed":False,"reason":"x","existing_text":"課題"}},6)
    def test_suppress_only_evidence(self):
        with self.assertRaises(ValueError):
            validate_scene_captions(CUES,{1:{"reviewed":True,"reason":"x","existing_text":""}},6)
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            validate_scene_captions([(0.,2.,"a"),(2.1,4.,"b")],{},4)
    def test_full_editorial_script_retained(self):
        self.assertEqual(len(CUES),3)
        self.assertEqual(len(select_burned_cues(CUES,SUPPRESS)),2)
    def test_release_gate(self):
        self.assertEqual(REVIEW_POLICY["publication"],"NOT_APPROVED")
        self.assertIn("NOT_SPEECH_SYNCED",REVIEW_POLICY["caption_sync"])
if __name__=="__main__": unittest.main()
