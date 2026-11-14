import unittest
from qa import Review, scene_beat, can_publish

class QualityTest(unittest.TestCase):
    def test_scene_beat_boundaries(self):
        self.assertEqual(scene_beat(0), (0, 0))
        self.assertEqual(scene_beat(5.5), (1, 1))
        self.assertEqual(scene_beat(11.9), (2, 3))
    def test_reject_missing_voice(self):
        self.assertFalse(can_publish(Review(12, (0,4,8), False, False, True, True)))
    def test_reject_missing_approval(self):
        self.assertFalse(can_publish(Review(12, (0,4,8), True, True, True, False)))
    def test_approved_gate_only(self):
        self.assertTrue(can_publish(Review(12, (0,4,8), True, True, True, True)))
    def test_bad_timeline(self):
        with self.assertRaises(ValueError): scene_beat(12)
        self.assertFalse(can_publish(Review(12, (4,0,8), True, True, True, True)))

if __name__ == "__main__":
    unittest.main()
