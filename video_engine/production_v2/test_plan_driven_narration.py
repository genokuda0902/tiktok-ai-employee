import unittest
from video_engine.production_v2.aivis_narration import _scene_lines

class PlanDrivenNarrationTests(unittest.TestCase):
    def test_scene_narration_and_caption_are_semantic_source(self):
        rows=_scene_lines({"scenes":[{"id":"s1","narration":"結果を先に見せます","caption":"結果を先に"}]})
        self.assertEqual(rows[0][1],"結果を先に見せます")
        self.assertEqual(rows[0][2],"結果を先に")

    def test_legacy_message_fallback(self):
        rows=_scene_lines({"scenes":[{"id":"s1","message":"旧形式"}]})
        self.assertEqual(rows[0][1:3],("旧形式","旧形式"))

    def test_empty_plan_fails_closed(self):
        with self.assertRaises(RuntimeError): _scene_lines({"scenes":[]})

    def test_missing_semantic_source_fails_closed(self):
        with self.assertRaises(RuntimeError): _scene_lines({"scenes":[{"id":"s1","caption":"字幕のみ"}]})

    def test_ten_genres_share_contract(self):
        genres=["ai","beauty","psychology","money","sales","career","health","science","travel_food","product_compare"]
        for genre in genres:
            rows=_scene_lines({"genre":genre,"scenes":[{"id":"hook","narration":f"{genre}の結果","caption":"結果"}]})
            self.assertEqual(rows[0][0]["id"],"hook")

if __name__=="__main__": unittest.main()
