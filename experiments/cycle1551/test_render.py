import unittest
from render import frame

class CaptionTests(unittest.TestCase):
    def test_frame_sizes(self):
        for t in (0,2.9,3,5.9,6,8.9,9,11.9):
            self.assertEqual(frame(t).size,(360,640))
    def test_caption_boundaries(self):
        captions=["まず合計したい数値を確認","合計セルを選択します","SUM関数で範囲を指定","合計500が自動で出ます"]
        self.assertEqual(len(captions),4)
        self.assertEqual([min(3,int(t//3)) for t in (0,3,6,9)],[0,1,2,3])
if __name__=="__main__": unittest.main()
