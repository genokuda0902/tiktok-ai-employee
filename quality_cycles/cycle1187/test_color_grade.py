import unittest
from color_grade import command

class TestColorGrade(unittest.TestCase):
    def test_filter(self):
        self.assertIn("eq=contrast=1.025:saturation=1.035", command("a.mp4","b.mp4"))
    def test_audio_preserved(self):
        c=command("a.mp4","b.mp4")
        self.assertEqual(c[c.index("-c:a")+1], "copy")
    def test_no_overwrite_input(self):
        with self.assertRaises(ValueError):
            command("a.mp4","a.mp4")
if __name__ == "__main__":
    unittest.main()
