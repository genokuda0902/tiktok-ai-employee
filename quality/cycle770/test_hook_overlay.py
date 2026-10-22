import unittest
import numpy as np
from hook_overlay import overlay_hook

class HookOverlayTests(unittest.TestCase):
    def setUp(self):
        self.frame = np.full((1920,1080,3),90,np.uint8)
        self.slides = [np.full((1135,1080,3),10,np.uint8),np.full((1135,1080,3),210,np.uint8)]
    def test_question(self):
        out=overlay_hook(self.frame,self.slides,15)
        self.assertEqual(int(out[300,500,0]),10)
        self.assertEqual(int(out[1350,500,0]),90)
        self.assertEqual(int(out[100,500,0]),90)
    def test_reveal(self):
        self.assertEqual(int(overlay_hook(self.frame,self.slides,45)[300,500,0]),210)
    def test_dissolve(self):
        self.assertEqual(int(overlay_hook(self.frame,self.slides,31)[300,500,0]),90)
    def test_after_hook(self):
        self.assertIs(overlay_hook(self.frame,self.slides,60),self.frame)
    def test_bad_slide(self):
        with self.assertRaises(ValueError):overlay_hook(self.frame,[self.slides[0]],0)

if __name__=='__main__':unittest.main()
