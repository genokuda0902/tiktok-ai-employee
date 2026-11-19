import unittest
from render import SCENES,validate,audio_gate
class ReviewTests(unittest.TestCase):
 def test_timeline(self): validate(SCENES)
 def test_reject_no_audio(self): self.assertFalse(audio_gate({'streams':[{'codec_type':'video'}]},True,True))
 def test_reject_unverified_speech(self): self.assertFalse(audio_gate({'streams':[{'codec_type':'audio'}]},False,True))
 def test_reject_unsynced(self): self.assertFalse(audio_gate({'streams':[{'codec_type':'audio'}]},True,False))
if __name__=='__main__':unittest.main()
