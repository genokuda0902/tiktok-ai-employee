"""Offline deterministic tests for cycle1003 focus ring."""
import unittest
import cv2
import numpy as np
from tools.quality.cycle1003_tracked_focus import (
    GENRES, ROI, CAPTION_TOP, detect_active_tab, add_focus, render,
)

class FocusTests(unittest.TestCase):
    def setUp(self):
        self.frame=np.zeros((1920,1080,3),dtype=np.uint8)
        cv2.rectangle(self.frame,(345,577),(570,620),(220,215,35),-1)

    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)

    def test_detect(self):
        self.assertAlmostEqual(detect_active_tab(self.frame)[0],345,delta=3)

    def test_no_tab(self):
        self.assertIsNone(detect_active_tab(np.zeros_like(self.frame)))

    def test_small_frame(self):
        with self.assertRaises(ValueError):
            detect_active_tab(np.zeros((200,200,3),dtype=np.uint8))

    def test_all_genres(self):
        for genre in GENRES:
            with self.subTest(genre=genre):
                self.assertEqual(add_focus(self.frame.copy(),(345,577,226,44),genre).shape,self.frame.shape)

    def test_bad_genre(self):
        with self.assertRaises(ValueError):
            add_focus(self.frame.copy(),(345,577,226,44),'invalid')

    def test_caption_preserved(self):
        result=add_focus(self.frame.copy(),(345,577,226,44))
        self.assertTrue(np.array_equal(result[CAPTION_TOP:],self.frame[CAPTION_TOP:]))

    def test_headline_preserved(self):
        result=add_focus(self.frame.copy(),(345,577,226,44))
        self.assertTrue(np.array_equal(result[:350],self.frame[:350]))

    def test_focus_visible(self):
        result=add_focus(self.frame.copy(),(345,577,226,44))
        self.assertGreater(np.count_nonzero(result[550:645,300:610]!=self.frame[550:645,300:610]),100)

    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            render('/missing/input.mp4','/tmp/never.mp4')

    def test_bad_timing(self):
        with self.assertRaises(ValueError):
            render(__file__,'/tmp/never.mp4',start=5,end=3)

    def test_roi_above_captions(self):
        self.assertLess(ROI[3],CAPTION_TOP)

    def test_noop(self):
        self.assertTrue(np.array_equal(add_focus(self.frame.copy(),None),self.frame))

if __name__=='__main__':
    unittest.main()
