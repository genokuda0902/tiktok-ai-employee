import unittest
from focus_contract import ANCHORS, validate_anchors, can_publish


class FocusContractTests(unittest.TestCase):
    def test_safe_coordinates(self):
        self.assertEqual(len(ANCHORS), 8)
        self.assertTrue(validate_anchors())

    def test_unsafe_coordinates_rejected(self):
        self.assertFalse(validate_anchors(((20, 40),) * 8))

    def test_publication_defaults_to_blocked(self):
        self.assertFalse(can_publish())
        self.assertTrue(can_publish(True, True, True))


if __name__ == '__main__':
    unittest.main()
