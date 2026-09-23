import unittest
from image_slide_pacing import paced_cards, zoompan_filter, micro_fade_filter


class ImageSlidePacingTests(unittest.TestCase):
    def test_ten_genre_common_card_pacing(self):
        cards = tuple({"image": f"{i:02}.png", "caption": f"caption {i}"} for i in range(10))
        result = paced_cards(cards)
        self.assertEqual(len(result), 10)
        self.assertTrue(all(c["text_baked"] for c in result))
        self.assertEqual(result[0]["motion"], "zoom_in")
        self.assertEqual(result[1]["motion"], "zoom_out")

    def test_fail_closed_on_wrong_resolution_or_missing_caption(self):
        with self.assertRaises(ValueError):
            paced_cards(({"image": "a.png", "caption": "x"},), 720, 1280)
        with self.assertRaises(ValueError):
            paced_cards(({"image": "a.png", "caption": ""},))

    def test_duration_guard(self):
        with self.assertRaises(ValueError):
            paced_cards(({"image": "a.png", "caption": "x", "duration": 0.5},))

    def test_zoompan_is_subtle_and_full_hd_vertical(self):
        self.assertIn("1.018", zoompan_filter("zoom_in"))
        self.assertIn("1080x1920", zoompan_filter("zoom_out"))

    def test_micro_fade_is_short_and_preserves_card_duration(self):
        filt = micro_fade_filter(2.0)
        self.assertIn("d=0.06", filt)
        self.assertIn("st=1.94", filt)

    def test_micro_fade_fails_closed_when_too_long(self):
        with self.assertRaises(ValueError):
            micro_fade_filter(2.0, 0.5)


if __name__ == "__main__":
    unittest.main()
