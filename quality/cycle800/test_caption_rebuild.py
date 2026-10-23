import json,unittest
import numpy as np
from pathlib import Path
from caption_rebuild import GENRES, CAP_Y,CAP_H, WIDTH, HEIGHT, contrast_ratio,validate_cues,make_caption,apply_overlay
CUES=json.loads((Path(__file__).parent/'captions_science_review.json').read_text())
class CaptionTests(unittest.TestCase):
    def test_10_genres(self):self.assertEqual(len(GENRES),10)
    def test_cues(self):self.assertTrue(validate_cues(CUES,429));self.assertEqual(len(CUES),16)
    def test_bad_order(self):
        with self.assertRaises(ValueError):validate_cues([CUES[1],CUES[0]],429)
    def test_bad_accent(self):
        c=dict(CUES[0],accent='見当たらない')
        with self.assertRaises(ValueError):validate_cues([c],429)
    def test_safe_region(self):self.assertLess(CAP_Y+CAP_H,1800)
    def test_contrast(self):
        self.assertGreater(contrast_ratio('#FFFFFF','#031522'),12)
        for c in GENRES.values():self.assertGreater(contrast_ratio(c,'#031522'),8)
    def test_image(self):
        for genre in GENRES:
            im=make_caption(CUES[0],genre)
            self.assertEqual(im.shape,(CAP_H,WIDTH,4))
            self.assertGreater(im[:,:,3].sum(),0)
    def test_preserve_outside(self):
        frame=np.full((HEIGHT,WIDTH,3),20,dtype='uint8')
        before=frame.copy();apply_overlay(frame,make_caption(CUES[0],'science'),255)
        self.assertTrue(np.array_equal(frame[:CAP_Y],before[:CAP_Y]))
        self.assertTrue(np.array_equal(frame[CAP_Y+CAP_H:],before[CAP_Y+CAP_H:]))
        self.assertGreater(np.abs(frame[CAP_Y:CAP_Y+CAP_H].astype('int16')-before[CAP_Y:CAP_Y+CAP_H]).sum(),0)
if __name__=='__main__':unittest.main()
