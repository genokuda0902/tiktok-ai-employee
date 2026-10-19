import unittest
from genre_contract import GENRES, WIDTH, HEIGHT, FPS, CAPTION_LINES, validate_timeline

class TestCycle689(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES), 10)
        self.assertEqual(len(set(GENRES)), 10)

    def test_video_size(self):
        self.assertEqual((WIDTH, HEIGHT, FPS), (1080, 1920, 30))

    def test_japanese_lines(self):
        self.assertEqual(len(CAPTION_LINES), 8)
        self.assertTrue(all(len(parts) == 2 for parts in CAPTION_LINES))

    def test_timeline(self):
        durations = [2.1, 2.233, 2.034, 1.566, 1.334, 2.8, 1.733, 1.8]
        # Use 30fps-aligned values.
        frames = [63, 67, 61, 47, 40, 84, 52, 54]
        self.assertEqual(sum(frames), 468)
        items = []
        start = 0.0
        for i, n in enumerate(frames):
            end = start + n / FPS
            items.append({"scene": i + 1, "start": start, "end": end,
                          "spoken_text": "".join(CAPTION_LINES[i]) if i < 7 else ""})
            start = end
        self.assertTrue(validate_timeline(items))
        items[2]["spoken_text"] = "different"
        with self.assertRaises(ValueError):
            validate_timeline(items)

if __name__ == "__main__":
    unittest.main()
