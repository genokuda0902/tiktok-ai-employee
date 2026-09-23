import unittest
from video_engine.semantic_timeline import Scene, build_timeline, posting_policy

class SemanticTimelineTest(unittest.TestCase):
    def test_one_semantic_unit_owns_image_voice_caption(self):
        scenes = [
            Scene("a.jpg", "最初の一言", "最初の一言", 2.4),
            Scene("b.jpg", "次の説明", "次の説明", 2.1),
        ]
        tl = build_timeline(scenes)
        self.assertEqual(tl[0]["start"], 0.0)
        self.assertEqual(tl[0]["end"], tl[1]["start"])
        self.assertEqual(tl[-1]["end"], 4.5)
        self.assertTrue(all(x["image"] and x["narration"] and x["caption"] for x in tl))

    def test_missing_semantic_component_fails_closed(self):
        with self.assertRaises(ValueError):
            build_timeline([Scene("a.jpg", "", "字幕", 2.0)])

    def test_manual_post_policy(self):
        p = posting_policy()
        self.assertTrue(p["zero_cost"])
        self.assertTrue(p["human_approval_required"])
        self.assertFalse(p["auto_post"])

if __name__ == "__main__":
    unittest.main()
