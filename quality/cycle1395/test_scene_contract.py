"""Reusable fail-closed QA for review-only vertical MP4s."""
import json
import subprocess
import unittest


def inspect(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def publication_ready(metadata, captions_verified=False, rights_approved=False, human_approved=False):
    streams=metadata['streams']
    video=next((s for s in streams if s.get('codec_type')=='video'), None)
    audio=any(s.get('codec_type')=='audio' for s in streams)
    return bool(video and video.get('width')==1080 and video.get('height')==1920 and audio and captions_verified and rights_approved and human_approved)


class GateTests(unittest.TestCase):
    def test_silent_video_blocked(self):
        self.assertFalse(publication_ready({'streams':[{'codec_type':'video','width':1080,'height':1920}]}))

    def test_unapproved_video_blocked(self):
        self.assertFalse(publication_ready({'streams':[{'codec_type':'video','width':1080,'height':1920},{'codec_type':'audio'}]}, True, True, False))

    def test_approved_video_allowed(self):
        self.assertTrue(publication_ready({'streams':[{'codec_type':'video','width':1080,'height':1920},{'codec_type':'audio'}]}, True, True, True))


if __name__=='__main__':
    unittest.main()
