import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'code' / 'diagram_clarity.py'
spec = importlib.util.spec_from_file_location('diagram_clarity', MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class DiagramClarityTests(unittest.TestCase):
    def setUp(self):
        self.meta = {'streams': [
            {'codec_type': 'video', 'width': 1080, 'height': 1920,
             'r_frame_rate': '30/1', 'nb_frames': '60'},
            {'codec_type': 'audio', 'codec_name': 'aac'}]}

    def test_all_ten_genres(self):
        self.assertEqual(len(mod.GENRES), 10)
        for genre in mod.GENRES:
            self.assertEqual(mod.validate(self.meta, genre, mod.DEFAULT_ROI), 60)
            self.assertIn('unsharp', mod.filter_graph(genre, mod.DEFAULT_ROI))

    def test_rejects_caption_overlap(self):
        for roi in [(60, 800, 960, 800), (60, 1340, 960, 100),
                    (60, 390, 960, 960), (61, 390, 960, 930)]:
            with self.subTest(roi=roi), self.assertRaises(ValueError):
                mod.validate(self.meta, 'ai', roi)

    def test_rejects_wrong_video(self):
        bad = json.loads(json.dumps(self.meta))
        bad['streams'][0]['width'] = 720
        with self.assertRaises(ValueError):
            mod.validate(bad, 'ai', mod.DEFAULT_ROI)

    def test_rejects_no_audio(self):
        with self.assertRaises(ValueError):
            mod.validate({'streams': [self.meta['streams'][0]]}, 'ai', mod.DEFAULT_ROI)

    def test_rejects_unknown_genre(self):
        with self.assertRaises(ValueError):
            mod.validate(self.meta, 'fake', mod.DEFAULT_ROI)

    def test_filter_has_no_subtitle_processing(self):
        f = mod.filter_graph('ai', mod.DEFAULT_ROI)
        self.assertNotIn('drawtext', f)
        self.assertNotIn('subtitles', f)
        self.assertIn('overlay=60:390', f)

    def test_synthetic_render_and_audio_copy(self):
        with tempfile.TemporaryDirectory() as td:
            source, target = Path(td) / 'src.mp4', Path(td) / 'dst.mp4'
            subprocess.run(['ffmpeg', '-nostdin', '-y', '-hide_banner', '-loglevel', 'error',
                            '-f', 'lavfi', '-i', 'testsrc2=size=1080x1920:rate=30:duration=1',
                            '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=1',
                            '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'ultrafast',
                            '-crf', '28', '-c:a', 'aac', '-metadata:s:a:0', 'language=jpn',
                            '-shortest', str(source)], check=True)
            report = mod.render(source, target)
            self.assertEqual(report['frames'], 30)
            self.assertEqual(int(next(s for s in mod.probe(target)['streams']
                                      if s['codec_type'] == 'video')['nb_frames']), 30)
            for p in (source, target):
                subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(p),
                                '-f', 'null', '-'], check=True, capture_output=True)
            def audio_hash(p):
                import hashlib
                raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(p),
                                      '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', 'pipe:1'],
                                     check=True, capture_output=True).stdout
                return hashlib.sha256(raw).hexdigest()
            self.assertEqual(audio_hash(source), audio_hash(target))


if __name__ == '__main__':
    unittest.main()
