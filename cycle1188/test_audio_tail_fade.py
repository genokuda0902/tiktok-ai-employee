import unittest
from cycle1188.audio_tail_fade import fade_start

class FadeTest(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(fade_start(23.033333),22.683)
    def test_short(self):
        self.assertEqual(fade_start(0.5,0.2),0.3)
    def test_invalid(self):
        for d,f in [(0,0.35),(1,0),(0.2,0.35)]:
            with self.assertRaises(ValueError):
                fade_start(d,f)

if __name__ == "__main__":
    unittest.main()
