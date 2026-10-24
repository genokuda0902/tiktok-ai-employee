"""Cycle814: safe zone, genre coverage, ffprobe contracts; no paid APIs."""
import unittest
from editorial_contract import (
    GENRE_ACCENTS, CAPTIONS, SCENE_COUNT, CAPTION_SAFE_ZONE,
    MIN_BOTTOM_UI_CLEARANCE, HEIGHT, check_scene_contract, validate_probe,
)

class EditorialContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS), 10)
        self.assertEqual(len(set(GENRE_ACCENTS.values())), 10)

    def test_eight_caption_scenes(self):
        self.assertEqual(len(CAPTIONS), SCENE_COUNT)
        self.assertTrue(check_scene_contract(list(range(8))))

    def test_bottom_safe_zone(self):
        self.assertLessEqual(CAPTION_SAFE_ZONE[3], HEIGHT-MIN_BOTTOM_UI_CLEARANCE)

    def test_bad_scene_count_rejected(self):
        with self.assertRaises(AssertionError):
            check_scene_contract(list(range(7)))

    def test_video_probe(self):
        streams=[
            dict(codec_type="video",width=1080,height=1920,codec_name="h264",r_frame_rate="30/1"),
            dict(codec_type="audio",codec_name="aac",sample_rate="48000")
        ]
        self.assertTrue(all(validate_probe({"streams":streams}).values()))
        streams[0]["width"]=720
        self.assertFalse(validate_probe({"streams":streams})["1080x1920"])

if __name__ == "__main__":
    unittest.main()
