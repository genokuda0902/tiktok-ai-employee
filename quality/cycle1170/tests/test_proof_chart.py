import unittest
from unittest.mock import patch
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import proof_chart as p

class ChartTests(unittest.TestCase):
    def setUp(self):
        self.m={'genre':'ai','roi':[54,806,940,240],'time':[14.5,16.9],
                'fictional_data':{'A':[12,16,18],'B':[8,9,12]}}
    def test_truth(self):self.assertEqual(p.numbers(self.m),(46,29,75))
    def test_ten_genres(self):self.assertEqual(len(p.GENRE_COLORS),10)
    def test_bad_missing_data(self):
        self.m['fictional_data']['A']=[12,16]
        with self.assertRaises(ValueError):p.numbers(self.m)
    def test_negative_data(self):
        self.m['fictional_data']['B']=[8,-9,12]
        with self.assertRaises(ValueError):p.numbers(self.m)
    def test_zero_total(self):
        self.m['fictional_data']={'A':[0,0,0],'B':[0,0,0]}
        with self.assertRaises(ValueError):p.numbers(self.m)
    def test_graph_uses_proportional_bar(self):
        s=p.graph(self.m)
        self.assertIn('w=610',s)
        self.assertIn('w=385',s)
        self.assertIn('合計 75',s)
    def test_invalid_policy_fails_closed(self):
        from unittest.mock import patch
        m=dict(self.m,policy='PUBLICATION_APPROVED',asset_approval='review_only_no_publication',manual_post_only=True)
        with self.assertRaises(ValueError):p.validate(m,'unused.mp4')
    def test_missing_roi_approval_fails_closed(self):
        m=dict(self.m,policy=p.POLICY,asset_approval='review_only_no_publication',manual_post_only=True)
        with patch.object(p,'digest',return_value='actual'):
            with self.assertRaises(ValueError):p.validate(m,'unused.mp4')
    def test_bad_genre_fails_closed(self):
        m=dict(self.m,policy=p.POLICY,asset_approval='review_only_no_publication',manual_post_only=True,roi_reviewed=True,source_sha256='wrong',genre='unknown')
        with patch.object(p,'digest',return_value='actual'):
            with self.assertRaises(ValueError):p.validate(m,'unused.mp4')
    def test_bad_source_digest_fails_closed(self):
        m=dict(self.m,policy=p.POLICY,asset_approval='review_only_no_publication',manual_post_only=True,roi_reviewed=True,source_sha256='wrong')
        with patch.object(p,'digest',return_value='actual'):
            with self.assertRaises(ValueError):p.validate(m,'unused.mp4')
    def test_no_caption_overlay(self):
        self.assertLess(self.m['roi'][1]+self.m['roi'][3],p.CAPTION_TOP)

if __name__=='__main__':unittest.main()
