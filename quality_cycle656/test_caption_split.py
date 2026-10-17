import unittest
from quality_cycle656.aspect_caption import split_caption

class CaptionTests(unittest.TestCase):
    def test_split(self):
        text = '小さくても、パソコンとして動きます。'
        a, b = split_caption(text)
        self.assertEqual(a+b, text)
