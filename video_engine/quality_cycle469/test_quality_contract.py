import unittest
from quality_contract import validate_plan
BASE={"duration":20,"publication":"NOT_APPROVED","quality":"HUMAN_REVIEW",
      "auto_post":False,"human_approval":False,"rights":"ORIGINAL_SYNTHETIC",
      "privacy":"NO_REAL_PERSONAL_DATA","narration_status":"NOT_GENERATED",
      "scenes":[{"start":0 if i==0 else (1.5+(i-1)*2.5),
                 "end":1.5+i*2.5,
                 "caption":"架空の検証動画"} for i in range(8)]}
# The final scene extends to 19 seconds; use exact 20-second contiguous timeline.
BASE["scenes"][-1]["end"]=20
class TestGate(unittest.TestCase):
    def test_valid(self): self.assertEqual(validate_plan(BASE),[])
    def test_block_auto_post(self): self.assertIn("auto_post",validate_plan({**BASE,"auto_post":True}))
    def test_block_publication(self): self.assertIn("publication",validate_plan({**BASE,"publication":"APPROVED"}))
    def test_block_fake_voice(self): self.assertIn("narration_status",validate_plan({**BASE,"narration_status":"GENERATED"}))
    def test_block_gap(self):
        s=[dict(x) for x in BASE["scenes"]];s[1]["start"]=1.7
        self.assertIn("continuity_1",validate_plan({**BASE,"scenes":s}))
    def test_block_late_hook(self):
        s=[dict(x) for x in BASE["scenes"]];s[0]["end"]=2
        self.assertIn("hook_late",validate_plan({**BASE,"scenes":s}))
if __name__=="__main__":unittest.main()
