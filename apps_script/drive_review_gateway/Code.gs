/**
 * Private review-video ingress for GitHub Actions.
 *
 * Deploy as a Web app that executes as the owner. The endpoint is reachable by
 * GitHub Actions, but every request must carry a short-lived HMAC signature.
 * It writes only the pinned review MP4 to the pinned private Drive folder.
 */
const DESTINATION_FOLDER_ID = '14rtOvwFKmycVO5Irq1X8QJ4-vgO2xUMk';
const EXPECTED_NAME = 'pi5_review_20s_REVIEW_ONLY.mp4';
const EXPECTED_SHA256 = 'd8b3c0736dbf29cbf528ccca19acdd7172175b73ec00e7d23a9b3b4f5933838f';
const MAX_BYTES = 25 * 1024 * 1024;
const MAX_CLOCK_SKEW_SECONDS = 300;

function doPost(event) {
  try {
    return jsonResponse_(handleUpload_(event));
  } catch (error) {
    // Never return request bodies, signatures, secrets, or Drive exception text.
    return jsonResponse_({ok: false, error: safeErrorCode_(error)});
  }
}

function handleUpload_(event) {
  const raw = event && event.postData && event.postData.contents;
  if (!raw) throw new Error('invalid_request');

  const body = JSON.parse(raw);
  const secret = PropertiesService.getScriptProperties().getProperty('GATEWAY_SECRET');
  if (!secret) throw new Error('gateway_not_configured');
  if (body.version !== 1) throw new Error('unsupported_version');
  if (body.filename !== EXPECTED_NAME || body.sha256 !== EXPECTED_SHA256) {
    throw new Error('artifact_not_allowed');
  }

  const timestamp = Number(body.timestamp);
  const now = Math.floor(Date.now() / 1000);
  if (!Number.isFinite(timestamp) || Math.abs(now - timestamp) > MAX_CLOCK_SKEW_SECONDS) {
    throw new Error('expired_request');
  }
  if (typeof body.content_b64 !== 'string' || typeof body.signature !== 'string') {
    throw new Error('invalid_request');
  }

  const canonical = [String(timestamp), body.filename, body.sha256, body.content_b64].join('\n');
  const expectedSignature = bytesToHex_(
    Utilities.computeHmacSha256Signature(canonical, secret)
  );
  if (!constantTimeEqual_(expectedSignature, body.signature.toLowerCase())) {
    throw new Error('invalid_signature');
  }

  const bytes = Utilities.base64Decode(body.content_b64);
  if (!bytes.length || bytes.length > MAX_BYTES) throw new Error('invalid_size');
  if (sha256Hex_(bytes) !== EXPECTED_SHA256) throw new Error('hash_mismatch');

  const lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) throw new Error('busy');
  try {
    const folder = DriveApp.getFolderById(DESTINATION_FOLDER_ID);
    if (folder.getSharingAccess() !== DriveApp.Access.PRIVATE) {
      throw new Error('destination_not_private');
    }

    const matches = folder.getFilesByName(EXPECTED_NAME);
    let file = null;
    if (matches.hasNext()) file = matches.next();
    if (matches.hasNext()) throw new Error('duplicate_files');

    let created = false;
    if (file) {
      if (sha256Hex_(file.getBlob().getBytes()) !== EXPECTED_SHA256) {
        throw new Error('existing_file_mismatch');
      }
    } else {
      const blob = Utilities.newBlob(bytes, 'video/mp4', EXPECTED_NAME);
      file = folder.createFile(blob);
      file.setDescription('UNAPPROVED REVIEW ONLY; NOT FOR POSTING');
      created = true;
    }

    // Authenticated owner-side readback from Drive after create/idempotent lookup.
    const readback = sha256Hex_(file.getBlob().getBytes());
    if (readback !== EXPECTED_SHA256) throw new Error('readback_hash_mismatch');
    return {
      ok: true,
      created: created,
      file_id: file.getId(),
      readback_sha256: readback,
      readback_sha256_match: true,
      quality: 'UNAPPROVED_REVIEW_ONLY',
      posting: false
    };
  } finally {
    lock.releaseLock();
  }
}

function sha256Hex_(bytes) {
  return bytesToHex_(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, bytes));
}

function bytesToHex_(bytes) {
  return bytes.map(function(value) {
    return ('0' + ((value < 0 ? value + 256 : value) & 255).toString(16)).slice(-2);
  }).join('');
}

function constantTimeEqual_(left, right) {
  if (typeof left !== 'string' || typeof right !== 'string') return false;
  let difference = left.length ^ right.length;
  const length = Math.max(left.length, right.length);
  for (let index = 0; index < length; index += 1) {
    difference |= (left.charCodeAt(index % left.length) || 0) ^
      (right.charCodeAt(index % right.length) || 0);
  }
  return difference === 0;
}

function jsonResponse_(value) {
  return ContentService.createTextOutput(JSON.stringify(value))
    .setMimeType(ContentService.MimeType.JSON);
}

function safeErrorCode_(error) {
  const allowed = [
    'invalid_request', 'gateway_not_configured', 'unsupported_version',
    'artifact_not_allowed', 'expired_request', 'invalid_signature',
    'invalid_size', 'hash_mismatch', 'busy', 'destination_not_private',
    'duplicate_files', 'existing_file_mismatch', 'readback_hash_mismatch'
  ];
  return allowed.indexOf(error && error.message) >= 0 ? error.message : 'internal_error';
}
