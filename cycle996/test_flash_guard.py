import importlib.util
from pathlib import Path
import unittest
import numpy as np
spec = importlib.util.spec_from_file_location('flash_guard',Path(__file__).with_name('flash_guard.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class FlashGuardTests(unittest.TestCase):
    def test_ten_genre_allowlist(self):
        self.assertEqual(len(m.GENRES),10)
        self.assertNotIn('unknown',m.GENRES)

    def test_review_gate(self):
        meta={'streams':[{'codec_type':'video','width':1080,'height':1920,
                          'r_frame_rate':'30/1','nb_frames':'60'},
                         {'codec_type':'audio','sample_rate':'48000'},
                         {'codec_type':'subtitle','codec_name':'mov_text'}]}
        with self.assertRaises(ValueError):m.validate(meta,'ai_work',False,[30])
        with self.assertRaises(ValueError):m.validate(meta,'unknown',True,[30])
        with self.assertRaises(ValueError):m.validate(meta,'ai_work',True,[58])
        with self.assertRaises(ValueError):m.validate(meta,'ai_work',True,[30,30])
        self.assertEqual(m.validate(meta,'ai_work',True,[30]),60)

    def test_audio_and_caption_required(self):
        meta={'streams':[{'codec_type':'video','width':1080,'height':1920,
                          'r_frame_rate':'30/1','nb_frames':'60'}]}
        with self.assertRaises(ValueError):m.validate(meta,'ai_work',True,[30])

    def test_feather_and_caption_preservation(self):
        matte=m.mask()
        self.assertEqual(matte.shape,(855,1032,1))
        self.assertEqual(float(matte[0,100,0]),0.)
        self.assertEqual(float(matte[400,400,0]),1.)
        old=np.zeros((1920,1080,3),np.uint8)
        new=np.full((1920,1080,3),255,np.uint8)
        result=m.blend_roi(old,new,0.28,matte)
        self.assertTrue(np.array_equal(result[1450:1800],new[1450:1800]))
        self.assertEqual(int(result[700,500,0]),71)
        self.assertEqual(int(result[200,500,0]),255)

    def test_jump_reduction(self):
        matte=m.mask()
        old=np.zeros((1920,1080,3),np.uint8)
        new=np.full((1920,1080,3),255,np.uint8)
        result=m.blend_roi(old,new,m.RAMP[0],matte)
        self.assertLess(m.luma(result)-m.luma(old),m.luma(new)-m.luma(old))
        self.assertEqual(m.RAMP[-1],1.)

    def test_threshold_guard(self):
        import inspect
        self.assertIn('No qualifying flash',inspect.getsource(m.render))
        self.assertIn('review_only',inspect.getsource(m.validate))

if __name__=='__main__':unittest.main()
