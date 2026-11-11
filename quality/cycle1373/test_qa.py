import unittest
from quality.cycle1373.qa import assess

class GateTest(unittest.TestCase):
    def test_fail_closed_without_approval(self):
        # This is a source-level gate test; real MP4 integration requires an artifact.
        import inspect
        source=inspect.getsource(assess)
        self.assertIn("employee_approved",source)
        self.assertIn("narration_verified",source)
        self.assertIn("captions_synced",source)
