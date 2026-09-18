"""Real PostgreSQL integration tests; requires TEST_DATABASE_URL and psycopg 3.
Run only against disposable PostgreSQL. Never use production DATABASE_URL.
"""
import os
import threading
import unittest
from datetime import datetime, timezone

from src.persistent_jobs import Ledger, deterministic_id


@unittest.skipUnless(os.environ.get('TEST_DATABASE_URL'), 'TEST_DATABASE_URL not configured')
class PostgreSQLIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import psycopg
        cls.psycopg = psycopg
        cls.dsn = os.environ['TEST_DATABASE_URL']
        with psycopg.connect(cls.dsn, autocommit=True) as conn:
            conn.execute('DROP TABLE IF EXISTS automation_jobs')
            Ledger(conn).initialize()

    @classmethod
    def tearDownClass(cls):
        with cls.psycopg.connect(cls.dsn, autocommit=True) as conn:
            conn.execute('DROP TABLE IF EXISTS automation_jobs')

    def setUp(self):
        self.job_id = deterministic_id('integration-account', '2026-09-18', 1)
        with self.psycopg.connect(self.dsn, autocommit=True) as conn:
            conn.execute('DELETE FROM automation_jobs')
            self.assertEqual(Ledger(conn).submit(self.job_id, 'plan-1', 'integration-account', datetime.now(timezone.utc)), 'queued')

    def test_duplicate_registration(self):
        with self.psycopg.connect(self.dsn, autocommit=True) as conn:
            self.assertEqual(Ledger(conn).submit(self.job_id, 'plan-1', 'integration-account', datetime.now(timezone.utc)), 'duplicate')
            self.assertEqual(conn.execute('SELECT count(*) FROM automation_jobs WHERE job_id=%s', (self.job_id,)).fetchone()[0], 1)

    def test_concurrent_claim_is_atomic(self):
        barrier = threading.Barrier(8)
        results = []
        lock = threading.Lock()
        def worker():
            with self.psycopg.connect(self.dsn, autocommit=True) as conn:
                barrier.wait(timeout=10)
                claim = Ledger(conn).claim(self.job_id)
                with lock:
                    results.append(claim)
        threads = [threading.Thread(target=worker) for _ in range(8)]
        for thread in threads: thread.start()
        for thread in threads: thread.join(timeout=15)
        self.assertFalse(any(thread.is_alive() for thread in threads))
        self.assertEqual(len(results), 8)
        self.assertEqual(sum(bool(result) for result in results), 1)
        with self.psycopg.connect(self.dsn, autocommit=True) as conn:
            self.assertEqual(conn.execute('SELECT attempts FROM automation_jobs WHERE job_id=%s', (self.job_id,)).fetchone()[0], 1)

    def test_expired_lease_requires_reconciliation_and_fences_stale_worker(self):
        with self.psycopg.connect(self.dsn, autocommit=True) as conn:
            ledger = Ledger(conn)
            claim = ledger.claim(self.job_id)
            conn.execute("UPDATE automation_jobs SET lease_until=now()-interval '1 second' WHERE job_id=%s", (self.job_id,))
            self.assertFalse(ledger.heartbeat(self.job_id, claim['token']))
            self.assertFalse(ledger.rendered(self.job_id, claim['token'], 'local://video.mp4', 'a'*64))
            self.assertEqual(ledger.expire(), [self.job_id])
            self.assertIsNone(ledger.claim(self.job_id))
            self.assertEqual(conn.execute('SELECT status FROM automation_jobs WHERE job_id=%s', (self.job_id,)).fetchone()[0], 'reconcile_required')

    def test_finished_job_cannot_be_claimed_twice(self):
        with self.psycopg.connect(self.dsn, autocommit=True) as conn:
            ledger = Ledger(conn)
            claim = ledger.claim(self.job_id)
            self.assertTrue(ledger.rendered(self.job_id, claim['token'], 'local://video.mp4', 'a'*64))
            self.assertIsNone(ledger.claim(self.job_id))
            self.assertEqual(ledger.submit(self.job_id, 'plan-1', 'integration-account', datetime.now(timezone.utc)), 'duplicate')

    def test_attempt_limit(self):
        with self.psycopg.connect(self.dsn, autocommit=True) as conn:
            ledger = Ledger(conn)
            conn.execute("UPDATE automation_jobs SET attempts=3 WHERE job_id=%s", (self.job_id,))
            self.assertIsNone(ledger.claim(self.job_id, max_attempts=3))
            self.assertEqual(conn.execute('SELECT attempts FROM automation_jobs WHERE job_id=%s', (self.job_id,)).fetchone()[0], 3)

    def test_qa_failure_blocks_handoff(self):
        with self.psycopg.connect(self.dsn, autocommit=True) as conn:
            ledger = Ledger(conn)
            claim = ledger.claim(self.job_id)
            self.assertTrue(ledger.rendered(self.job_id, claim['token'], 'local://video.mp4', 'a'*64))
            self.assertTrue(ledger.qa(self.job_id, False, {'passed': False, 'mock': False}))
            self.assertFalse(ledger.approve(self.job_id, human=True, rights=True, employee_authorized=True))
            self.assertEqual(conn.execute('SELECT handoff_status FROM automation_jobs WHERE job_id=%s', (self.job_id,)).fetchone()[0], 'blocked')


if __name__ == '__main__':
    unittest.main()
