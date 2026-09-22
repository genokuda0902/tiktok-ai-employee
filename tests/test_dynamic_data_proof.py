import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from dynamic_data_proof import dynamic_data_filter


class DynamicDataProofTests(unittest.TestCase):
    def test_animates_click_edit_synchronized_spreadsheet_and_charts(self):
        vf = dynamic_data_filter(0, 2.5)
        self.assertIn('LIVE DATA', vf)
        self.assertIn('ROWS 5 → 1', vf)
        self.assertIn("text='TASK'", vf)
        self.assertIn("text='STATUS'", vf)
        self.assertIn("text='➤'", vf)
        self.assertIn("text='SELECT'", vf)
        self.assertIn("text='CLICK'", vf)
        self.assertIn("text='RUN'", vf)
        self.assertIn("mod(t-2.810,0.16)", vf)
        self.assertIn("text='PROCESS'", vf)
        self.assertIn("text='DONE'", vf)
        self.assertIn("text='=RESULT'", vf)
        self.assertIn("text='CHART UPDATED'", vf)
        self.assertIn("text='SYNC'", vf)
        self.assertIn("drawbox=x=360:y=1178:w=125:h=22", vf)
        self.assertIn("drawbox=x=485:y=1188:w=60:h=2", vf)
        self.assertIn("drawbox=x=543:y=1188:w=2:h=77", vf)
        self.assertIn("text='15'", vf)
        self.assertIn("text='1'", vf)
        self.assertIn("between(t,2.600,2.960)", vf)
        self.assertIn("315*0.92*min(max((t-2.960)/0.70,0),1)", vf)
        self.assertIn("315*0.66*min(max((t-3.060)/0.70,0),1)", vf)
        self.assertIn("315*0.38*min(max((t-3.160)/0.70,0),1)", vf)
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
