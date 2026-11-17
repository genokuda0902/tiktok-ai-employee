import unittest
from color_balance import render
class ColorBalanceTests(unittest.TestCase):
    def test_rejects_excessive_saturation(self):
        with self.assertRaises(ValueError): render("missing.mp4","out.mp4",1.5)
    def test_rejects_missing_source(self):
        with self.assertRaises(FileNotFoundError): render("missing.mp4","out.mp4")
if __name__=="__main__": unittest.main()
