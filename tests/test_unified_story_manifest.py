import unittest
from video_engine.unified_story_manifest import StoryCut, StoryManifest, release_contract


def cut(i=0, caption="10分が1分に"):
    return StoryCut(
        image_prompt=f"approved public-safe vertical office scene {i}",
        image_copy="10分 → 1分",
        narration="AIなら10分が1分に短縮できます",
        caption=caption,
        duration=2.0,
    )


class UnifiedStoryManifestTests(unittest.TestCase):
    def test_valid_eight_cut_story(self):
        m = StoryManifest("ai-work", [cut(i) for i in range(8)])
        self.assertEqual(m.duration, 16.0)

    def test_caption_must_come_from_narration(self):
        cuts = [cut(i) for i in range(8)]
        cuts[3] = cut(3, caption="音声にない文章")
        with self.assertRaisesRegex(ValueError, "caption drifts"):
            StoryManifest("ai-work", cuts).validate()

    def test_requires_8_to_12_cuts(self):
        with self.assertRaises(ValueError):
            StoryManifest("ai-work", [cut(i) for i in range(7)]).validate()

    def test_portrait_and_manual_release_are_mandatory(self):
        with self.assertRaises(ValueError):
            StoryManifest("ai-work", [cut(i) for i in range(8)], width=720, height=1280).validate()
        with self.assertRaises(ValueError):
            StoryManifest("ai-work", [cut(i) for i in range(8)], manual_post_only=False).validate()

    def test_release_contract_is_zero_cost_and_no_auto_post(self):
        c = release_contract()
        self.assertTrue(c["zero_cost"])
        self.assertTrue(c["single_source_manifest"])
        self.assertTrue(c["human_approval_required"])
        self.assertFalse(c["auto_post"])


if __name__ == "__main__":
    unittest.main()
