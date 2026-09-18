import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from src.automation_engine import Engine, validate


def request(run='run1', plan='plan1'):
    return {'run_id': run, 'account_id': 'employee1', 'plan_id': plan, 'topic': 'AI tips', 'script': 'Hello', 'generation_settings': {}}


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.engine = Engine(str(Path(self.tmp.name) / 'jobs.db'))

    def tearDown(self):
        self.engine.db.close()
        self.tmp.cleanup()

    def test_valid_and_invalid(self):
        self.assertEqual(validate(request())['run_id'], 'run1')
        with self.assertRaises(ValueError):
            validate({'run_id': 'bad'})

    def test_duplicate_run_and_plan(self):
        self.assertEqual(self.engine.submit(request()), 'queued')
        self.assertEqual(self.engine.submit(request()), 'duplicate_rejected')
        self.assertEqual(self.engine.submit(request('run2')), 'duplicate_rejected')

    def test_missing_renderer(self):
        self.engine.submit(request())
        self.assertEqual(self.engine.execute(request()), 'renderer_not_connected')

    def test_retry_cap_and_error_record(self):
        self.engine.submit(request())
        calls = []
        def broken(req):
            calls.append(1)
            raise RuntimeError('secret=do-not-log')
        self.assertEqual(self.engine.execute(request(), broken, max_attempts=2), 'failed')
        self.assertEqual(len(calls), 2)
        row = self.engine.db.execute('SELECT attempts,result FROM jobs').fetchone()
        self.assertEqual(row[0], 2)
        self.assertNotIn('do-not-log', row[1])

    def test_qa_failure_not_complete(self):
        self.engine.submit(request())
        self.assertEqual(self.engine.execute(request(), lambda _: {'video_path': '/nonexistent/video.mp4'}), 'qa_failed')
        self.assertEqual(self.engine.db.execute('SELECT status FROM jobs').fetchone()[0], 'qa_failed')

    def test_technical_pass_still_requires_human_qa(self):
        self.engine.submit(request())
        with patch('src.automation_engine.inspect_mp4', return_value={'passed': True, 'human_visual_privacy_approval': False}):
            self.assertEqual(self.engine.execute(request(), lambda _: {'video_path': '/placeholder.mp4'}), 'awaiting_human_qa')


if __name__ == '__main__':
    unittest.main()
