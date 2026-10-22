import unittest
from outro_contract import GENRES, START_FRAME, END_FRAME
class TestContract(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(GENRES),10)
    def test_timing(self): self.assertEqual(END_FRAME-START_FRAME,90)
if __name__=='__main__': unittest.main()
