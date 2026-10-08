import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from video_engine.production_v2.sound import mix

class SoundTests(unittest.TestCase):
    def test_three_roles_and_rights_are_required(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)
            for name,hz in (('voice',440),('bgm',120),('sfx',800)):
                subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',f'sine=frequency={hz}:duration=2','-c:a','pcm_s16le',str(p/f'{name}.wav')],check=True)
            rights={role:{'source':'local test generator','rights_status':'TEST_ONLY'} for role in ('VOICE','BGM','SFX')}
            with self.assertRaises(ValueError):mix(p/'voice.wav',p/'bgm.wav',p/'sfx.wav',p/'mix.wav',2,{})
            mix(p/'voice.wav',p/'bgm.wav',p/'sfx.wav',p/'mix.wav',2,rights)
            probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(p/'mix.wav')]))
            self.assertLess(abs(float(probe['format']['duration'])-2),0.05)
            self.assertEqual(json.loads((p/'mix.json').read_text())['approval'],'HUMAN_REVIEW')
if __name__=='__main__':unittest.main()
