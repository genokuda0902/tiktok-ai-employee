import unittest
import numpy as np
from cpu_light import add_glow

class TestGlow(unittest.TestCase):
    def test_caption_safe(self):
        src=np.full((1920,1080,3),15,dtype=np.uint8)
        out=add_glow(src.copy(),30)
        self.assertTrue(np.array_equal(out[1145:],src[1145:]))
    def test_visual_change(self):
        src=np.full((1920,1080,3),15,dtype=np.uint8)
        self.assertFalse(np.array_equal(add_glow(src.copy(),30),src))

if __name__=="__main__":
    unittest.main()
