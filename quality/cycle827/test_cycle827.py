"""Offline regression tests for speech-aware Japanese subtitles."""
import unittest
from pathlib import Path
import speech827

class SpeechAwareTests(unittest.TestCase):
    def test_eight_scenes_and_24_caption_states(self):
        self.assertEqual(len(speech827.PHRASES),8)
        self.assertEqual(sum(speech827.FRAMES),775)
        self.assertTrue(all(''.join(x)==s for x,s in zip(speech827.PHRASES,speech827.SPEECH)))
    def test_speech_quantile_skips_pause(self):
        self.assertAlmostEqual(speech827.active_quantile([(0.2,0.7),(1.2,1.7)],0.5),0.7)
        self.assertAlmostEqual(speech827.active_quantile([(0.2,0.7),(1.2,1.7)],0.75),1.45)
    def test_speech_aware_not_equal_thirds(self):
        bounds,ok,_=speech827.align_scene(0,3.3,
            ['AIで仕事を','早くするなら、','最初の一歩が大事。'],
            [(0,0.27),(1.55,1.88),(2.81,3.3)])
        self.assertTrue(ok)
        self.assertTrue(0.26<=bounds[0]<=0.28)
        self.assertTrue(all(bounds[i]<bounds[i+1] for i in range(3)))
        self.assertGreater(abs(bounds[1]-1.1),0.05)
    def test_silence_fallback_is_not_misreported_as_aligned(self):
        bounds,ok,_=speech827.align_scene(0,3,['a','b','c'],[(0,3)])
        self.assertFalse(ok)
        self.assertEqual(bounds,[0,1,2,3])
    def test_ass_time_rounding(self):
        self.assertEqual(speech827.timestamp(25.83333),'0:00:25.83')
        self.assertEqual(speech827.timestamp(3.705),'0:00:03.71')
    def test_shadow_fields_prevent_black_smudges(self):
        self.assertIn('0,0,1,5,1,5,65,65,0,1',Path(speech827.__file__).read_text())
    def test_no_network_or_posting(self):
        code=Path(speech827.__file__).read_text()
        self.assertNotIn('requests.post(',code)
        self.assertNotIn('tiktok.com/upload',code)
        self.assertIn('not_forced_alignment',code)

if __name__=='__main__':unittest.main()
