import unittest
from qa_contract import Scene, validate_plan, evaluate_release, verify_spreadsheet, GENRES
SCENES=[Scene(i*2.5,(i+1)*2.5,"短い字幕") for i in range(8)]
class TestQuality(unittest.TestCase):
    def test_genres(self):
        for genre in GENRES:
            self.assertTrue(validate_plan(SCENES,genre=genre))
    def test_timeline(self):
        bad=list(SCENES);bad[3]=Scene(8,10,"caption")
        with self.assertRaises(ValueError):validate_plan(bad)
    def test_caption(self):
        bad=list(SCENES);bad[0]=Scene(0,2.5,"あ"*37)
        with self.assertRaises(ValueError):validate_plan(bad)
    def test_voice_gate(self):
        self.assertIn("narration_japanese",evaluate_release({"mp4_decode":True}))
    def test_human_gate(self):
        keys=("mp4_decode","vertical_1080x1920","narration_japanese","captions_semantic_sync","assets_rights_approved","human_content_approved","employee_manual_post_only")
        qa=dict.fromkeys(keys,True)
        self.assertEqual(evaluate_release(qa),[])
        qa["human_content_approved"]=False
        self.assertIn("human_content_approved",evaluate_release(qa))
    def test_sum(self):
        self.assertTrue(verify_spreadsheet([120,150,200,180],"=SUM(B2:B5)",650,[120,150,200,180]))
    def test_wrong_sum(self):
        with self.assertRaises(ValueError):verify_spreadsheet([120,150,200,180],"=SUM(B2:B5)",640,[120,150,200,180])
    def test_wrong_chart(self):
        with self.assertRaises(ValueError):verify_spreadsheet([120,150,200,180],"=SUM(B2:B5)",650,[120,150,180,200])
if __name__=="__main__":unittest.main()
