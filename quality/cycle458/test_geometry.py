import unittest
from quality_contract import check_caption_box

class TestGeometry(unittest.TestCase):
    def test_inside(self):
        self.assertTrue(check_caption_box())
