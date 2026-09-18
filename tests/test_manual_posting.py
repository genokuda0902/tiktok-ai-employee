"""Run: python -m unittest discover -s tests -p test_manual_posting.py"""
import hashlib
import tempfile
import unittest
from pathlib import Path
from src.manual_posting import Registry, Rejected, ADMIN_WAIT, ASSIGNED, READY, URL_WAIT, DONE

ROSTER = {
    'admin': {'approved': True, 'role': 'admin'},
    'alice': {'approved': True, 'role': 'employee'},
    'bob': {'approved': True, 'role': 'employee'},
    'pending': {'approved': False, 'role': 'employee'},
}

class PostingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.video = Path(self.tmp.name) / 'video.mp4'
        self.video.write_bytes(b'fake media fixture: registry only, not real media QA')
        self.digest = hashlib.sha256(self.video.read_bytes()).hexdigest()
        self.registry = Registry(str(Path(self.tmp.name) / 'registry.db'), ROSTER)
        self.qa = {'passed': True, 'sha256': self.digest}

    def register(self, video='v1', account='account1'):
        self.registry.register('admin', video, account, self.video, self.qa, True)

    def ready(self):
        self.register()
        self.registry.approve('admin', 'v1')
        self.registry.assign('admin', 'v1', 'alice')
        self.registry.review('alice', 'v1')

    def test_qa_failure_and_asset_rejection(self):
        for report, approval in [({'passed': False, 'sha256': self.digest}, True), (self.qa, False), ({'passed': True, 'sha256': 'wrong'}, True)]:
            with self.assertRaises(Rejected):
                self.registry.register('admin', 'v1', 'account1', self.video, report, approval)
        self.assertEqual(self.registry.history('admin'), [])

    def test_approval_and_assignment_gates(self):
        self.register()
        with self.assertRaises(Rejected):
            self.registry.assign('admin', 'v1', 'alice')
        with self.assertRaises(Rejected):
            self.registry.approve('alice', 'v1')
        self.registry.approve('admin', 'v1')
        self.registry.assign('admin', 'v1', 'alice')
        self.assertEqual(self.registry.history('admin', 'v1')[0]['status'], ASSIGNED)

    def test_unapproved_and_cross_employee_access(self):
        self.register()
        with self.assertRaises(Rejected):
            self.registry.approve('pending', 'v1')
        with self.assertRaises(Rejected):
            self.registry.assign('admin', 'v1', 'pending')
        self.registry.approve('admin', 'v1')
        self.registry.assign('admin', 'v1', 'alice')
        with self.assertRaises(Rejected):
            self.registry.review('bob', 'v1')
        self.assertEqual(self.registry.history('bob'), [])

    def test_duplicate_video_and_modified_file(self):
        self.register()
        with self.assertRaises(Rejected):
            self.register('v2')
        self.registry.approve('admin', 'v1')
        self.registry.assign('admin', 'v1', 'alice')
        self.video.write_bytes(b'changed')
        with self.assertRaises(Rejected):
            self.registry.review('alice', 'v1')

    def test_missing_url_duplicate_report_and_history(self):
        self.ready()
        with self.assertRaises(Rejected):
            self.registry.report('alice', 'v1', '', '2026-09-18T12:00:00+09:00')
        self.assertEqual(self.registry.history('admin', 'v1')[0]['status'], READY)
        url = 'https://www.tiktok.com/@example/video/123456789'
        self.registry.report('alice', 'v1', url, '2026-09-18T12:00:00+09:00')
        with self.assertRaises(Rejected):
            self.registry.report('alice', 'v1', url, '2026-09-18T12:00:00+09:00')
        self.assertEqual(self.registry.history('admin', 'v1')[0]['status'], URL_WAIT)
        with self.assertRaises(Rejected):
            self.registry.verify('admin', 'v1', False)
        self.registry.verify('admin', 'v1', True)
        self.assertEqual(self.registry.history('admin', 'v1')[0]['status'], DONE)
        self.assertTrue(any(entry['action'] == 'verify_post' for entry in self.registry.audit('admin', 'v1')))

if __name__ == '__main__':
    unittest.main()
