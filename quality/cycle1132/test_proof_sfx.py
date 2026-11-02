import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import subprocess

import numpy as np

from proof_sfx import (POLICY, GENRES, cue, make_sfx_wav, probe, render, sha256, validate_manifest, video_stream_hash)


class CueTests(unittest.TestCase):
    def setUp(self):
        self.events = [{'time': 0.3, 'type': 'tap'}, {'time': 1.0, 'type': 'confirm'}]
        self.base = {'policy': POLICY, 'asset_approval': 'private_review_only',
                     'source_sha256': 'a' * 64, 'genre': 'ai', 'events': self.events}

    def test_genre_contract(self):
        self.assertEqual(len(GENRES), 10)
        for genre in GENRES:
            m = dict(self.base, genre=genre)
            self.assertEqual(validate_manifest(m, 'a' * 64, 2.1), self.events)

    def test_fail_closed_source_and_rights(self):
        for change in ({'asset_approval': 'public'}, {'source_sha256': 'b' * 64}, {'policy': 'APPROVED'}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                validate_manifest(dict(self.base, **change), 'a' * 64, 2.1)

    def test_bad_event_rejected(self):
        for events in ([{'time': -1, 'type': 'tap'}], [{'time': 0.5, 'type': 'music'}],
                       [{'time': 0.3, 'type': 'tap'}, {'time': 0.4, 'type': 'reuse'}]):
            with self.subTest(events=events), self.assertRaises(ValueError):
                validate_manifest(dict(self.base, events=events), 'a' * 64, 2.1)

    def test_cue_is_original_quiet_short_nonmusic(self):
        for kind in ('tap', 'confirm', 'reuse'):
            x = cue(kind)
            self.assertLessEqual(np.max(np.abs(x)), 0.03901)
            self.assertLess(len(x), 0.31 * 48000)
            self.assertGreater(np.max(np.abs(x)), 0.037)

    def test_wav_stereo_and_peak(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'sfx.wav'
            peak = make_sfx_wav(self.events, 2.1, p)
            self.assertLessEqual(peak, 0.041)
            self.assertGreater(p.stat().st_size, 10000)

    def test_synthetic_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            source, output = td / 'synthetic.mp4', td / 'review.mp4'
            manifest, report = td / 'private.json', td / 'qa.json'
            subprocess.run(['ffmpeg', '-hide_banner', '-v', 'error', '-f', 'lavfi', '-i',
                            'color=c=#101f35:s=270x480:r=30:d=2.1', '-f', 'lavfi', '-i',
                            'sine=frequency=320:sample_rate=48000:duration=2.1',
                            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                            '-metadata:s:a:0', 'language=jpn', '-shortest', str(source)], check=True)
            m = dict(self.base, source_sha256=sha256(source))
            manifest.write_text(json.dumps(m), encoding='utf8')
            qa = render(source, output, manifest, report)
            self.assertEqual(qa['full_av_decode'], 'PASS')
            self.assertEqual(video_stream_hash(source), video_stream_hash(output))
            self.assertEqual(probe(output)['frames'], 63)
            self.assertLess(qa['output_audio_peak_dbfs'], -1.0)
            self.assertTrue(report.exists())


if __name__ == '__main__':
    unittest.main()
