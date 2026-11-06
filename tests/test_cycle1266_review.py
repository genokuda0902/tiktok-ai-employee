import unittest
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("renderer",Path(__file__).resolve().parents[1]/"tools"/"cycle1266_review.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class SceneContract(unittest.TestCase):
    def test_three_distinct_scenes(self):
        self.assertEqual(len(m.SCENES),3)
        self.assertEqual(len({x[1] for x in m.SCENES}),3)
    def test_no_sensitive_assets(self):
        self.assertNotIn("IMG_5805",str(m.SCENES))
    def test_review_only_label(self):
        self.assertIn("REVIEW ONLY",m.render.__code__.co_consts.__str__())
if __name__=="__main__":unittest.main()
