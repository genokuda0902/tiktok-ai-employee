# Drive review gateway (OAuth-client-free alternative)

This standalone Apps Script receives exactly one pinned review MP4 from the
isolated GitHub Actions workflow and writes it to the pinned private My Drive
folder. It never posts to TikTok and never changes Drive sharing.

## Security model

- The deployment executes as the Drive owner.
- Requests require an HMAC-SHA256 signature using `GATEWAY_SECRET`.
- Requests expire after five minutes.
- Filename, SHA-256, size, MIME type and destination folder are pinned.
- A non-private destination, duplicate names or mismatched existing bytes fail
  closed.
- Drive bytes are read back by the owner and hashed before success is returned.
- Secrets and request bodies are never returned in errors or logs.

Apps Script's `DriveApp` requires the full Drive OAuth scope. The code limits
its actions to the fixed folder and file, but deployment authorization still
grants the script account-wide Drive access. Review the code before deployment.

## One-time deployment

1. Create a standalone Apps Script project owned by the target Drive account.
2. Replace `Code.gs` and `appsscript.json` with the files in this directory.
3. Add script property `GATEWAY_SECRET` with a newly generated random secret.
4. Deploy as a Web app: execute as the owner; access set so GitHub Actions can
   call the URL.
5. In GitHub environment `drive-review-only`, add the same secret as
   `DRIVE_REVIEW_WEBHOOK_SECRET` and the `/exec` URL as
   `DRIVE_REVIEW_WEBAPP_URL`.

The workflow prefers this gateway when both values exist. Existing Drive API
credential support remains as a rollback path.
