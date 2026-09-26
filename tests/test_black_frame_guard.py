import unittest

from video_engine.black_frame_guard import assert_no_long_black, parse_blackdetect


class BlackFrameGuardTests(unittest.TestCase):
    def test_clean_log_passes(self):
        assert_no_long_black('frame=600 fps=30')

    def test_short_transition_passes(self):
        log = '[blackdetect] black_start:1.0 black_end:1.3 black_duration:0.3'
        assert_no_long_black(log, max_seconds=0.5)

    def test_sustained_black_fails_closed(self):
        log = '[blackdetect] black_start:2 black_end:19.966667 black_duration:17.966667'
        with self.assertRaisesRegex(ValueError, 'long black segment'):
            assert_no_long_black(log, max_seconds=0.5)

    def test_parser_keeps_evidence(self):
        log = '[blackdetect] black_start:2 black_end:12.4 black_duration:10.4'
        segments = parse_blackdetect(log)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0].duration, 10.4)


if __name__ == '__main__':
    unittest.main()
