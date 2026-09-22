import unittest
from datetime import date, datetime, timezone
from src.daily_schedule import enqueue_two_slots, ScheduleBlocked


class FakeLedger:
    def __init__(self): self.ids = set()
    def submit(self, job_id, plan_id, account_id, scheduled_at):
        if job_id in self.ids: return 'duplicate'
        self.ids.add(job_id)
        return 'queued'


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.ledger = FakeLedger()
        self.day = date(2026, 9, 18)
        self.slots = [dict(plan_id=f'plan-{n}', approved=True, script_approved=True,
                           assets_approved=True,
                           scheduled_at=datetime(2026, 9, 18, 9+n, tzinfo=timezone.utc))
                      for n in (1, 2)]

    def test_two_slots_are_idempotent(self):
        args = dict(account_id='acct', day=self.day, slots=self.slots)
        self.assertEqual(enqueue_two_slots(self.ledger, **args), ['queued', 'queued'])
        self.assertEqual(enqueue_two_slots(self.ledger, **args), ['duplicate', 'duplicate'])

    def test_same_plan_in_one_day_rejected(self):
        self.slots[1]['plan_id'] = self.slots[0]['plan_id']
        with self.assertRaises(ValueError):
            enqueue_two_slots(self.ledger, account_id='acct', day=self.day, slots=self.slots)
        self.assertEqual(len(self.ledger.ids), 0)

    def test_unapproved_plan_rejected(self):
        self.slots[1]['assets_approved'] = False
        with self.assertRaises(ScheduleBlocked):
            enqueue_two_slots(self.ledger, account_id='acct', day=self.day, slots=self.slots)
        self.assertEqual(len(self.ledger.ids), 0)

    def test_production_activation_is_blocked(self):
        with self.assertRaises(ScheduleBlocked):
            enqueue_two_slots(self.ledger, account_id='acct', day=self.day, slots=self.slots, production_enabled=True)


if __name__ == '__main__': unittest.main()
