import unittest
from media_gate import approved_for_posting

class GateTests(unittest.TestCase):
 def test_silent_audio_not_approved(self):
  self.assertFalse(approved_for_posting({'audio_stream':True}))
 def test_all_approvals_required(self):
  data=dict(japanese_narration_verified=True,timed_captions_verified=True,assets_rights_approved=True,employee_approved=True)
  self.assertTrue(approved_for_posting(data))
  data['employee_approved']=False
  self.assertFalse(approved_for_posting(data))

if __name__=='__main__': unittest.main()
