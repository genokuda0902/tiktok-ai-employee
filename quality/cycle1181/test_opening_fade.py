import unittest
from opening_fade import command

class OpeningFadeTests(unittest.TestCase):
    def test_audio_is_copied(self):
        args = command("input.mp4", "output.mp4")
        self.assertEqual(args[args.index("-c:a")+1], "copy")
    def test_fade_duration(self):
        self.assertIn("fade=t=in:st=0:d=0.30", command("a.mp4", "b.mp4"))
    def test_no_source_overwrite(self):
        with self.assertRaises(ValueError):
            command("a.mp4", "./a.mp4")
    def test_reject_invalid_duration(self):
        with self.assertRaises(ValueError):
            command("a.mp4", "b.mp4", 2.0)

if __name__ == "__main__":
    unittest.main()
