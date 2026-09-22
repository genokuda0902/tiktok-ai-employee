import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from dynamic_data_proof import dynamic_data_filter


class DynamicDataProofTests(unittest.TestCase):
    def test_contains_table_counter_and_animated_chart(self):
        vf = dynamic_data_filter(0, 2.5)
        self.assertIn('DATA CHANGE', vf)
        self.assertIn('ROWS 5 → 1', vf)
        self.assertIn("15 → 1", vf)
        self.assertIn("700*min(max((t-2.500)/0.75,0),1)", vf)
        self.assertIn("enable='gte(t,3.250)'", vf)

    def test_varies_across_scenes(self):
        filters = [dynamic_data_filter(i, 2.0) for i in range(5)]
        self.assertEqual(len(set(filters)), 5)


if __name__ == '__main__':
    unittest.main()
