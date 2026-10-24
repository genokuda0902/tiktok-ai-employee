import unittest
from safe_area import (
    WIDTH, HEIGHT, FPS, CAPTION_BOX, GENRES, PALETTE,
    SENTENCE_CHUNKS, validate_caption_box, allocate_frames,
    validate_genre, review_gate, AUTO_POST,
)

class SafeAreaTests(unittest.TestCase):
    def test_format(self):
        self.assertEqual((WIDTH, HEIGHT, FPS), (1080, 1920, 30))
    def test_safe_zone(self):
        self.assertTrue(validate_caption_box())
        self.assertFalse(validate_caption_box((60, 1500, 1020, 1700)))
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(set(GENRES), set(PALETTE))
        for genre in GENRES:
            self.assertTrue(validate_genre(genre).startswith("#"))
    def test_scene_chunks(self):
        self.assertEqual(len(SENTENCE_CHUNKS), 8)
        self.assertTrue(all(len(x) == 3 for x in SENTENCE_CHUNKS))
    def test_frame_conservation(self):
        for total in (80, 90, 99, 105, 112, 130):
            for chunks in SENTENCE_CHUNKS:
                got = allocate_frames(total, chunks)
                self.assertEqual(sum(got), total)
                self.assertTrue(all(n >= 5 for n in got))
    def test_too_short(self):
        with self.assertRaises(ValueError):
            allocate_frames(10, ("a", "b", "c"))
    def test_human_gate(self):
        self.assertFalse(AUTO_POST)
        self.assertFalse(review_gate())
        self.assertFalse(review_gate(True, True, True))

if __name__ == "__main__":
    unittest.main()
