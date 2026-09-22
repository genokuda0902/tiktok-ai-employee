import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from dynamic_data_proof import dynamic_data_filter


class DynamicDataProofTests(unittest.TestCase):
    def test_animates_rows_counter_and_multiple_bars(self):
        vf = dynamic_data_filter(0, 2.5)
        self.assertIn('LIVE DATA', vf)
        self.assertIn('ROWS 5 → 1', vf)
        self.assertIn("text='15'", vf)
        self.assertIn("text='1'", vf)
        self.assertIn("between(t,2.500,2.820)", vf)
        self.assertIn("360*0.92*min(max((t-2.500)/0.70,0),1)", vf)
        self.assertIn("360*0.66*min(max((t-2.600)/0.70,0),1)", vf)
        self.assertIn("360*0.38*min(max((t-2.700)/0.70,0),1)", vf)
        self.assertIn('UPDATED', vf)

    def test_varies_across_scenes(self):
        filters = [dynamic_data_filter(i, 2.0) for i in range(5)]
        self.assertEqual(len(set(filters)), 5)

    def test_never_uses_personal_or_external_asset_data(self):
        vf = dynamic_data_filter(1, 0.0)
        self.assertNotIn('http', vf.lower())
        self.assertNotIn('@', vf)


if __name__ == '__main__':
    unittest.main()
