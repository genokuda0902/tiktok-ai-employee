import unittest
import numpy as np
from audio_caption_audit import analyze_pcm
class AudioCueTest(unittest.TestCase):
 def test_eight_cues(self):
  sr=16000
  x=np.sin(2*np.pi*220*np.arange(8*sr)/sr).astype('float32')*0.1
  result=analyze_pcm(x,sr,list(range(9)))
  self.assertEqual(len(result),8)
  self.assertTrue(all(x['nonzero_signal'] for x in result))
 def test_silence_is_not_claimed_as_speech(self):
  result=analyze_pcm(np.zeros(16000,dtype='float32'),16000,[0,1])
  self.assertFalse(result[0]['nonzero_signal'])
 def test_invalid_cuts(self):
  with self.assertRaises(ValueError):analyze_pcm(np.zeros(1000),16000,[0,1,1])
if __name__=='__main__':unittest.main()
