import copy
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from quality.cycle1092 import stable_total_guard as g
M=json.loads((Path(__file__).parent/'manifest.json').read_text())

class TruthGuardTests(unittest.TestCase):
    def test_ten_genres_and_safe_box(self):
        for genre in g.PALETTES:
            m=dict(M,genre=genre)
            self.assertEqual(g.validate(m),75)
            self.assertEqual(g.card(40,m).size,(294,218))
            self.assertLess(g.BOX[1]+g.BOX[3],g.CAPTION_START_Y)

    def test_no_false_intermediate_total(self):
        for i in range(91):
            self.assertIn(g.displayed_total(i,M),(None,75))
        self.assertIsNone(g.displayed_total(29,M))
        self.assertEqual(g.displayed_total(30,M),75)

    def test_values_are_computed_not_hardcoded(self):
        m=copy.deepcopy(M);m['values']={'営業A':11,'営業B':22}
        self.assertEqual(g.validate(m),33)
        self.assertEqual(g.displayed_total(50,m),33)

    def test_private_and_rights_fail_closed(self):
        for k,v in [('synthetic',False),('review_only',False),
                    ('rights_status','approved'),('contains_private_data',True)]:
            with self.subTest(k=k):
                with self.assertRaises(ValueError):g.validate(dict(M,**{k:v}))

    def test_invalid_data_fails(self):
        for v in [-1,True,1000,1.5]:
            m=copy.deepcopy(M);m['values']['営業A']=v
            with self.assertRaises(ValueError):g.validate(m)
        with self.assertRaises(ValueError):g.validate(dict(M,reveal_frame=91))
        with self.assertRaises(ValueError):g.displayed_total(-1,M)

    def test_sha_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'x';p.write_bytes(b'test')
            self.assertEqual(len(g.sha256(p)),64)
            with self.assertRaises(ValueError):g.render(p,p.with_name('out.mp4'),'0'*64,M)

if __name__=='__main__':unittest.main()
