"""Dependency-free external customer registry prototype. No TikTok publishing."""
from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

class AccessDenied(Exception):
    pass

class Status(str, Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    CANCELLED = 'cancelled'

@dataclass
class Customer:
    id: str
    status: Status = Status.PENDING
    accounts: set[str] = field(default_factory=set)

@dataclass(frozen=True)
class Actor:
    id: str
    customer_id: str | None
    role: str
    approved: bool

class TenantRegistry:
    def __init__(self):
        self._customers: dict[str, Customer] = {}
        self._jobs: dict[str, dict] = {}
        self._events: list[dict] = []

    def _authorize(self, actor: Actor, customer_id: str, *, admin=False):
        if not actor.approved:
            raise AccessDenied('approval required')
        if actor.role == 'platform_admin':
            return
        if actor.customer_id != customer_id or actor.role not in ('customer_admin', 'employee'):
            raise AccessDenied('cross-tenant access denied')
        if admin and actor.role != 'customer_admin':
            raise AccessDenied('customer admin required')

    def create_customer(self, actor: Actor) -> str:
        if not actor.approved or actor.role != 'platform_admin':
            raise AccessDenied('platform admin required')
        cid = str(uuid4())
        self._customers[cid] = Customer(cid)
        self._events.append({'customer_id': cid, 'action': 'created', 'actor_id': actor.id})
        return cid

    def set_status(self, actor: Actor, customer_id: str, status: Status):
        self._authorize(actor, customer_id, admin=True)
        if actor.role != 'platform_admin':
            raise AccessDenied('platform admin required')
        customer = self._customers[customer_id]
        if customer.status == Status.CANCELLED:
            raise ValueError('cancelled customer is terminal')
        customer.status = Status(status)
        self._events.append({'customer_id': customer_id, 'action': 'status_changed', 'status': status.value, 'actor_id': actor.id})

    def link_account(self, actor: Actor, customer_id: str, account_id: str):
        self._authorize(actor, customer_id, admin=True)
        customer = self._customers[customer_id]
        if customer.status != Status.ACTIVE:
            raise AccessDenied('customer not active')
        if not account_id.strip():
            raise ValueError('account id required')
        if any(account_id in c.accounts for cid, c in self._customers.items() if cid != customer_id):
            raise ValueError('account already linked to another customer')
        customer.accounts.add(account_id)
        self._events.append({'customer_id': customer_id, 'action': 'account_linked', 'actor_id': actor.id})

    def submit_job(self, actor: Actor, customer_id: str, account_id: str, cost: float = 0.0) -> str:
        self._authorize(actor, customer_id)
        customer = self._customers[customer_id]
        if customer.status != Status.ACTIVE or account_id not in customer.accounts:
            raise AccessDenied('inactive customer or unlinked account')
        if cost < 0:
            raise ValueError('negative cost')
        jid = str(uuid4())
        self._jobs[jid] = {'customer_id': customer_id, 'account_id': account_id, 'status': 'queued', 'cost': cost}
        self._events.append({'customer_id': customer_id, 'action': 'job_submitted', 'job_id': jid, 'actor_id': actor.id})
        return jid

    def get_job(self, actor: Actor, customer_id: str, job_id: str) -> dict:
        self._authorize(actor, customer_id)
        job = self._jobs[job_id]
        if job['customer_id'] != customer_id:
            raise AccessDenied('cross-tenant job access denied')
        return dict(job)

    def usage(self, actor: Actor, customer_id: str) -> dict:
        self._authorize(actor, customer_id)
        jobs = [j for j in self._jobs.values() if j['customer_id'] == customer_id]
        return {'jobs': len(jobs), 'estimated_cost': round(sum(j['cost'] for j in jobs), 6)}

    def audit(self, actor: Actor, customer_id: str) -> list[dict]:
        self._authorize(actor, customer_id, admin=True)
        return [dict(e) for e in self._events if e['customer_id'] == customer_id]
