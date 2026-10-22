import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('result_reveal', ROOT/'src/result_reveal.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ResultRevealTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=ROOT/'input/cycle774_baseline.mp4'
        cls.manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))

    def test_ten_genres(self): self.assertEqual(len(m.GENRE_COLORS),10)
    def test_source_hash(self): self.assertTrue(m.validate(self.manifest,self.source))
    def test_data_sum(self): self.assertEqual(sum(v for _,v in m.DATA),650000)
    def test_frames(self): self.assertEqual(m.END-m.START,84)
    def test_duration(self): self.assertEqual(m.TOTAL_FRAMES,819)
    def test_safe_reveal(self): self.assertEqual(m.chart_layout()[2][2],200000)
    def test_bad_sum_fails(self):
        x=copy.deepcopy(self.manifest);x['total_yen']=650001
        with self.assertRaises(ValueError):m.validate(x,self.source)
    def test_bad_audio_rights_fails(self):
        x=copy.deepcopy(self.manifest);x['audio_rights']='approved'
        with self.assertRaises(ValueError):m.validate(x,self.source)
    def test_unapproved_image_fails(self):
        x=copy.deepcopy(self.manifest);x['asset_provenance']='unknown'
        with self.assertRaises(ValueError):m.validate(x,self.source)
    def test_auto_post_fails(self):
        x=copy.deepcopy(self.manifest);x['publish_mode']='auto'
        with self.assertRaises(ValueError):m.validate(x,self.source)
    def test_approval_fails(self):
        x=copy.deepcopy(self.manifest);x['quality_approved']=True
        with self.assertRaises(ValueError):m.validate(x,self.source)
    def test_unverified_time_claim_fails(self):
        x=copy.deepcopy(self.manifest);x['time_saved_claim']='90%'
        with self.assertRaises(ValueError):m.validate(x,self.source)
    def test_wrong_source_fails(self):
        x=copy.deepcopy(self.manifest);x['source_sha256']='0'*64
        with self.assertRaises(ValueError):m.validate(x,self.source)
    def test_each_genre_frame(self):
        for genre in m.GENRE_COLORS:
            im=m.draw_static(m.GENRE_COLORS[genre]);fr=m.draw_frame(im,60,genre)
            self.assertEqual(fr.size,(1080,1920))
    def test_invalid_frame(self):
        with self.assertRaises(ValueError):m.draw_frame(m.draw_static('#20C7BB'),84,'AI・仕事効率化')

if __name__=='__main__':unittest.main()
