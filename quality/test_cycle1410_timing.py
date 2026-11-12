import unittest
from cycle1410_timing import TypingCue, visible_text, publishable

class TimingTests(unittest.TestCase):
    def test_typing_progress(self):
        cue = TypingCue("=SUM(B2:B4)", 1.0, 2.0)
        self.assertEqual(visible_text(cue, 0.5), "")
        self.assertEqual(visible_text(cue, 2.0), "=SUM(")
        self.assertEqual(visible_text(cue, 3.0), "=SUM(B2:B4)")
    def test_bad_timing(self):
        with self.assertRaises(ValueError):
            visible_text(TypingCue("x", 0, 0), 1)
    def test_publication_fail_closed(self):
        self.assertFalse(publishable(japanese_voice_verified=False,speech_sync_verified=False,rights_approved=True,employee_approved=False))

if __name__ == "__main__":
    unittest.main()
