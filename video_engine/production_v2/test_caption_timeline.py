import unittest

from video_engine.production_v2.caption_timeline import build_caption_timeline


GENRES = [
    "ai_work", "beauty", "psychology", "money", "sales",
    "career", "health", "science", "travel_food", "product_comparison",
]


class CaptionTimelineContractTest(unittest.TestCase):
    def test_ten_genres_share_measured_timeline_contract(self):
        for genre in GENRES:
            scenes = [
                {"genre": genre, "caption": "結論を先に見せます"},
                {"genre": genre, "caption": "理由を一つだけ説明します"},
                {"genre": genre, "caption": "最後に次の行動を示します"},
            ]
            timeline = build_caption_timeline(scenes, [1.2, 2.0, 1.4])
            self.assertEqual(timeline[0]["start"], 0.0)
            self.assertEqual(timeline[-1]["end"], 4.6)
            self.assertTrue(all(x["text"] for x in timeline))

    def test_fail_closed_on_count_mismatch(self):
        with self.assertRaises(ValueError):
            build_caption_timeline([{"caption": "a"}], [1.0, 1.0])

    def test_fail_closed_on_duration_bounds(self):
        with self.assertRaises(ValueError):
            build_caption_timeline([{"caption": "a"}], [0.2])
        with self.assertRaises(ValueError):
            build_caption_timeline([{"caption": "a"}], [5.5])

    def test_fail_closed_on_missing_caption_and_narration(self):
        with self.assertRaises(ValueError):
            build_caption_timeline([{}], [1.0])


if __name__ == "__main__":
    unittest.main()
