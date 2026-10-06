"""Server boundary. Never accept an employee ID as a caller credential.

Google ID tokens are verified cryptographically using google-auth; the `sub` claim,
not the mutable email, is the identity key. This is a library, not an HTTP app.
The hosting app must protect cookies/CSRF, TLS, and all file download routes.
"""
import re
from .core import Denied


class GoogleVerifier:
    def __init__(self, client_id, hosted_domain=None):
        if not client_id:
            raise ValueError('GOOGLE_OAUTH_CLIENT_ID required')
        self.client_id = client_id
        self.hosted_domain = hosted_domain

    def verify(self, token):
        if not isinstance(token, str) or not token:
            raise Denied('authentication required')
        try:
            from google.auth.transport import requests
            from google.oauth2 import id_token
            claims = id_token.verify_oauth2_token(token, requests.Request(), self.client_id)
        except Exception as exc:
            raise Denied('invalid Google ID token') from exc
        if claims.get('iss') not in ('accounts.google.com', 'https://accounts.google.com'):
            raise Denied('invalid issuer')
        if claims.get('email_verified') is not True:
            raise Denied('unverified email')
        if self.hosted_domain and claims.get('hd') != self.hosted_domain:
            raise Denied('outside organization')
        subject = claims.get('sub')
        if not isinstance(subject, str) or not re.fullmatch(r'[0-9]{1,255}', subject):
            raise Denied('invalid subject')
        return subject


class AuthenticatedService:
    """Each operation verifies caller token and resolves current DB status again."""
    def __init__(self, registry, verifier):
        self.registry = registry
        self.verifier = verifier

    def _actor(self, token):
        return self.registry.resolve_identity(self.verifier.verify(token))

    def history(self, token, employee_id=None):
        return self.registry.history(self._actor(token), employee_id)

    def video(self, token, job_id):
        return self.registry.job_for_employee(self._actor(token), job_id)

    def request(self, token, account_id):
        return self.registry.request(self._actor(token), account_id)

    def review(self, token, job_id, decision, post_url=None):
        return self.registry.review(self._actor(token), job_id, decision, post_url)

    def decide(self, token, employee_id, decision):
        return self.registry.decide(self._actor(token), employee_id, decision)

    def change_role(self, token, employee_id, role):
        return self.registry.change_role(self._actor(token), employee_id, role)

    def link_account(self, token, employee_id, account_id, handle):
        return self.registry.link_account(self._actor(token), employee_id, account_id, handle)

    def assign_identity(self, token, employee_id, google_token):
        """Admin-controlled binding; verified Google subject cannot be self-asserted."""
        admin = self._actor(token)
        self.registry._admin(admin)
        subject = self.verifier.verify(google_token)
        with self.registry.db:
            self.registry.bind_identity(employee_id, subject)
            self.registry._audit(admin, 'identity.linked', employee_id)

    def posting_context(self, token, job_id):
        """For team ④: no bearer token or direct download URL returned."""
        row = self.video(token, job_id)
        return {'job_id': row[0], 'employee_id': row[1], 'account_id': row[2],
                'status': row[3], 'manual_post_only': True}
