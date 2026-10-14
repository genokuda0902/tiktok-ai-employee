import unittest, tempfile, wave, math, struct
from pathlib import Path
from narration_gate import check_wav
class TestVoiceGate(unittest.TestCase):
    def test_missing_voice_fails(self):
        with self.assertRaisesRegex(ValueError,'NO_JAPANESE_VOICE_FILE'):check_wav('/does/not/exist.wav')
    def test_silent_voice_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'silent.wav'
            with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(b'\0\0'*24000)
            with self.assertRaisesRegex(ValueError,'VOICE_SILENT'):check_wav(p)
    def test_tone_signal_is_not_ja_verified(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'tone.wav'
            with wave.open(str(p),'wb') as w:
                w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000)
                w.writeframes(b''.join(struct.pack('<h',int(4000*math.sin(i*.1))) for i in range(24000)))
            r=check_wav(p)
            self.assertEqual(r['speech_language'],'UNVERIFIED')
if __name__=='__main__':unittest.main()