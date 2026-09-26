import unittest
from video_engine.native_story_card_contract import NativeStoryCardContract, default_story_beats


class NativeStoryCardContractTests(unittest.TestCase):
    def test_default_eight_beat_story_is_valid(self):
        c = NativeStoryCardContract()
        c.validate(len(default_story_beats()), rights_approved=True)
        self.assertEqual((c.width, c.height), (1080, 1920))

    def test_too_few_cards_fail_closed(self):
        with self.assertRaises(ValueError):
            NativeStoryCardContract().validate(5, rights_approved=True)

    def test_rights_must_be_approved(self):
        with self.assertRaises(ValueError):
            NativeStoryCardContract().validate(8, rights_approved=False)

    def test_release_remains_manual_and_zero_cost(self):
        c = NativeStoryCardContract()
        self.assertTrue(c.zero_cost)
        self.assertTrue(c.human_approval_required)
        self.assertTrue(c.manual_post_only)


if __name__ == '__main__':
    unittest.main()
