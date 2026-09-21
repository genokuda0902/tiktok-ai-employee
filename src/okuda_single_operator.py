"""Single-operator pilot authorization boundary; NOT a login implementation.

Call only after a trusted server-side identity provider has authenticated the
request. Never derive authenticated_user_id from a browser form, query parameter,
or user-supplied email. Production deployment requires an identity provider.
"""
from dataclasses import dataclass
from .manual_posting_flow import Principal, Forbidden


@dataclass(frozen=True)
class TrustedIdentity:
    subject: str
    authenticated: bool
    issuer_verified: bool


def owner_principal(identity: TrustedIdentity, *, configured_owner_subject: str) -> Principal:
    """Deny all users except the configured, issuer-verified owner."""
    if not configured_owner_subject or not identity.subject:
        raise Forbidden('Owner identity is not configured')
    if not identity.authenticated or not identity.issuer_verified:
        raise Forbidden('Verified authentication required')
    if identity.subject != configured_owner_subject:
        raise Forbidden('Pilot restricted to configured owner')
    return Principal(user_id=identity.subject, role='admin', authenticated=True,
                     approved=True, active=True)
