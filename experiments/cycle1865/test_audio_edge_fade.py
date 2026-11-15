import unittest
from audio_edge_fade import render

class TestAudioEdgeFade(unittest.TestCase):
    def test_callable(self):
        self.assertTrue(callable(render))

    def test_default_duration(self):
        self.assertEqual(render.__defaults__, (0.25,))

if __name__ == "__main__":
    unittest.main()
