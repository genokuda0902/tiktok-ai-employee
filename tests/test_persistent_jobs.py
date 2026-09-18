import unittest
from datetime import datetime, timezone
from src.persistent_jobs import deterministic_id, Ledger


class PersistentJobTests(unittest.TestCase):
    def test_same_slot_same_id(self):
        self.assertEqual(deterministic_id('account', '2026-09-18', 1), deterministic_id('account', '2026-09-18', 1))

    def test_different_slots_different_id(self):
        self.assertNotEqual(deterministic_id('account', '2026-09-18', 1), deterministic_id('account', '2026-09-18', 2))

    def test_invalid_slot(self):
        with self.assertRaises(ValueError):
            deterministic_id('account', '2026-09-18', 3)

    def test_naive_time_rejected_before_db(self):
        class NoConnection:
            def transaction(self):
                raise AssertionError('database must not be touched')
        with self.assertRaises(ValueError):
            Ledger(NoConnection()).submit('job', 'plan', 'account', datetime(2026, 9, 18))

    def test_missing_approval_never_touches_db(self):
        class NoConnection:
            def transaction(self):
                raise AssertionError('database must not be touched')
        self.assertFalse(Ledger(NoConnection()).approve('job', human=True, rights=False, employee_authorized=True))

    def test_mock_qa_rejected_before_db(self):
        class NoConnection:
            def transaction(self):
                raise AssertionError('database must not be touched')
        with self.assertRaises(ValueError):
            Ledger(NoConnection()).qa('job', True, {'mock': True})


if __name__ == '__main__':
    unittest.main()
