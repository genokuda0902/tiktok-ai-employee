"""Cycle789 subtitle contract tests: 10 genres, 16 Japanese cues, safe area."""
import tempfile
import unittest
from pathlib import Path
from cycles.cycle788.src.scene_contract import CUES
from cycles.cycle789.src import kinetic_captions as k

class KineticTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(k.GENRE_RGB), 10)

    def test_16_japanese_cues(self):
        self.assertEqual(len(k.SEGMENTS), 16)
        for cue, parts in zip(CUES, k.SEGMENTS):
            self.assertEqual(cue[2], "".join(parts))

    def test_no_overlap(self):
        self.assertTrue(all(a[1] <= b[0] for a, b in zip(CUES, CUES[1:])))

    def test_allocation_exact(self):
        for (start, end, _), parts in zip(CUES, k.SEGMENTS):
            self.assertEqual(sum(k.allocate_cs(start, end, parts)),
                             round(end * 100) - round(start * 100))

    def test_color(self):
        self.assertEqual(k.ass_color("#35E8D2"), "&H00D2E835")

    def test_ass_generation(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "captions.ass"
            text = k.render_ass(CUES, output)
            self.assertEqual(text.count("Dialogue:"), 16)
            self.assertIn("{\\kf", text)
            self.assertIn("100,180,420", text)
            self.assertEqual(text, output.read_text(encoding="utf-8"))

    def test_all_ten_render(self):
        with tempfile.TemporaryDirectory() as d:
            for genre in k.GENRE_RGB:
                text = k.render_ass(CUES, Path(d) / (genre + ".ass"), genre)
                self.assertEqual(text.count("Dialogue:"), 16)

    def test_invalid_cue(self):
        with self.assertRaises(ValueError):
            k.render_ass(CUES[:-1], "/tmp/unused.ass")

    def test_invalid_genre(self):
        with self.assertRaises(ValueError):
            k.render_ass(CUES, "/tmp/unused.ass", "unknown")

    def test_safe_bottom(self):
        self.assertLess(1920 - 420, 1920 * 0.8)

if __name__ == "__main__":
    unittest.main()
