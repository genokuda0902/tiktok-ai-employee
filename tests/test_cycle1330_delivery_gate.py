import unittest
from quality.cycle1330_delivery_gate import validate

class DeliveryGateTests(unittest.TestCase):
    def test_silent_rejected(self):
        data={"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"12"}}
        self.assertIn("missing narration/audio stream",validate(data))
    def test_complete_accepted(self):
        data={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12"}}
        self.assertEqual([],validate(data))
    def test_low_resolution_rejected(self):
        data={"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}],"format":{"duration":"12"}}
        self.assertIn("below 1080x1920",validate(data))
if __name__=="__main__": unittest.main()
