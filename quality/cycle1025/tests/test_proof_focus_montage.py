import importlib.util
from pathlib import Path
import unittest
import numpy as np

SCRIPT=Path(__file__).resolve().parents[1]/'code'/'proof_focus_montage.py'
spec=importlib.util.spec_from_file_location('proof_focus_montage',SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class MontageTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(m.GENRE_IDS),10)

    def test_all_eight_chapters(self):
        self.assertEqual([m.chapter_at(t) for t in [0,3,6,9,12,15,17,20]],list(range(1,9)))

    def test_six_new_visual_beats(self):
        self.assertEqual(len(m.FOCUS),6)
        self.assertFalse(m.detail_active(.5,1))
        for c in m.FOCUS:
            start,end=m.CHAPTERS[c-1:c+1]
            self.assertFalse(m.detail_active(start+.1,c))
            self.assertTrue(m.detail_active(start+(end-start)*.75,c))

    def test_protect_subtitles_and_header(self):
        image=np.zeros((1920,1080,3),np.uint8)
        image[:155]=71;image[1435:]=131
        rng=np.random.default_rng(7)
        image[155:1435]=rng.integers(0,255,size=(1280,1080,3),dtype=np.uint8)
        result=m.focus_content(image,2)
        self.assertTrue(np.array_equal(result[:155],image[:155]))
        self.assertTrue(np.array_equal(result[1435:],image[1435:]))
        self.assertGreater(np.mean(np.abs(result[300:1000].astype('float')-image[300:1000].astype('float'))),5)

    def test_focal_points_safe(self):
        for x,y in m.FOCUS.values():
            self.assertTrue(.3<=x<=.7 and .3<=y<=.7)

if __name__=='__main__':unittest.main()
