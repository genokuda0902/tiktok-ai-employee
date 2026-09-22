"""Daily two-slot enqueue. No workflow cron is enabled by this module.

Caller supplies approved plans, PostgreSQL Ledger, local date and timezone-aware
scheduled timestamps. Production execution requires a separate verified gate.
"""
from datetime import date, datetime
from src.persistent_jobs import deterministic_id


class ScheduleBlocked(RuntimeError):
    pass


def enqueue_two_slots(ledger, *, account_id, day, slots, production_enabled=False):
    if production_enabled:
        raise ScheduleBlocked('production_schedule_not_approved')
    if not isinstance(day, date) or isinstance(day, datetime):
        raise ValueError('day must be a local date')
    if len(slots) != 2:
        raise ValueError('exactly two slots required')
    seen_plans = set()
    for slot in slots:
        if slot['plan_id'] in seen_plans:
            raise ValueError('same plan cannot be scheduled twice in one day')
        seen_plans.add(slot['plan_id'])
        if not (slot['approved'] is True and slot['script_approved'] is True and slot['assets_approved'] is True):
            raise ScheduleBlocked('unapproved_plan')
        when = slot['scheduled_at']
        if when.tzinfo is None or when.date() != day:
            raise ValueError('timezone-aware scheduled_at must match day')
    return [ledger.submit(deterministic_id(account_id, day.isoformat(), index),
                          slot['plan_id'], account_id, slot['scheduled_at'])
            for index, slot in enumerate(slots, start=1)]
