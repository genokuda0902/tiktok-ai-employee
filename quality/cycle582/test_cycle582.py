import unittest
from hook import Hook, DEFAULT, GENRES, render_frame, SIZE
from qa_gate import QAResult

class HookTests(unittest.TestCase):
    def test_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            self.assertTrue(Hook(genre,'問い','答え','ラベル','サンプル',True).validate())
    def test_claim_must_be_verified(self):
        with self.assertRaises(ValueError):
            Hook('sales','問い','売上10倍','ラベル','架空').validate()
    def test_frame_bounds(self):
        self.assertEqual(render_frame(DEFAULT,0).size,SIZE)
        self.assertEqual(render_frame(DEFAULT,59).size,SIZE)
        with self.assertRaises(ValueError): render_frame(DEFAULT,60)
    def test_label_validation(self):
        with self.assertRaises(ValueError):
            Hook('ai_productivity','x'*33,'答え','ラベル','架空',True).validate()

class QATests(unittest.TestCase):
    def test_fail_closed_without_narration(self):
        q=QAResult('ai_productivity',20,((0,2,'手計算の前に、合計720を確認'),),False,False,False,False)
        d=q.evaluate()
        self.assertIn('JAPANESE_NARRATION_ABSENT',d['blockers'])
        self.assertEqual(d['publication'],'NOT_APPROVED')
    def test_caption_overlap_rejected(self):
        with self.assertRaises(ValueError):
            QAResult('sales',20,((0,2,'a'),(1,3,'b')),True,True,True,True).evaluate()
    def test_caption_too_long_rejected(self):
        with self.assertRaises(ValueError):
            QAResult('science',20,((0,2,'a'*46),),True,True,True,True).evaluate()
    def test_caption_beyond_video_rejected(self):
        with self.assertRaises(ValueError):
            QAResult('career',20,((19,21,'text'),),True,True,True,True).evaluate()

if __name__ == '__main__': unittest.main()
