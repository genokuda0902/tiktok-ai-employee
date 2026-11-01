import sys,unittest
from pathlib import Path
from dataclasses import replace
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from calculation_trace import Proof,DEMO,GENRES,validate,phase_for,annotate,font_path

class ProofTest(unittest.TestCase):
    def test_sum(self):self.assertTrue(validate(DEMO,675))
    def test_reject_incorrect_sum(self):
        with self.assertRaises(ValueError):validate(replace(DEMO,result=45),675)
    def test_reject_caption_overlap(self):
        with self.assertRaises(ValueError):validate(replace(DEMO,result_cell=(50,1150,300,1180)),675)
    def test_reject_bad_timing(self):
        with self.assertRaises(ValueError):validate(replace(DEMO,first_frame=215),675)
    def test_reject_mismatch(self):
        with self.assertRaises(ValueError):validate(replace(DEMO,values=(9,14)),675)
    def test_reject_negative(self):
        with self.assertRaises(ValueError):validate(replace(DEMO,values=(-9,14,21),result=26),675)
    def test_before_after_unchanged(self):
        self.assertIsNone(phase_for(180,DEMO));self.assertIsNone(phase_for(218,DEMO))
    def test_all_stages(self):
        stages={phase_for(i,DEMO)[0] for i in range(181,218)}
        self.assertEqual(stages,{0,1,2,3})
    def test_10_genres(self):self.assertEqual(len(set(GENRES)),10)
    def test_caption_pixel_exact(self):
        src=np.zeros((1920,1080,3),dtype=np.uint8);src[1160:]=[17,32,48]
        dst=annotate(src,214,DEMO,font_path())
        self.assertTrue(np.array_equal(dst[1160:],src[1160:]))
        self.assertTrue(np.any(dst[1060:1151]!=src[1060:1151]))
    def test_no_modification_outside_window(self):
        src=np.zeros((1920,1080,3),dtype=np.uint8)
        self.assertTrue(np.array_equal(annotate(src,170,DEMO,font_path()),src))
    def test_caption_bound(self):
        self.assertLess(max(box[3] for box in (*DEMO.cells,DEMO.result_cell,DEMO.status_box)),DEMO.caption_top)

if __name__=='__main__':unittest.main()
