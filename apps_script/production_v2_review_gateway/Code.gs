/**
 * Owner-executed, private Drive ingress for ONE unapproved integration-test MP4.
 * Do not deploy until the owner has reviewed the Web app access setting and
 * installed a unique GATEWAY_SECRET in Script Properties (never in source).
 * Based on the PR #16 review gateway; intentionally pinned to a single digest.
 */
const DESTINATION_FOLDER_ID = '14rtOvwFKmycVO5Irq1X8QJ4-vgO2xUMk';
const EXPECTED_NAME = 'video_jp_review_0001_v1_REVIEW_ONLY.mp4';
const EXPECTED_SHA256 = '9e1cbf5fb018efa14571c39f4631d984d92fdd86b477d95bf24d17a1c81d1939';
const MAX_BYTES = 25 * 1024 * 1024;
const MAX_CLOCK_SKEW_SECONDS = 300;

function doPost(event) {
  try {
    return jsonResponse_(handleUpload_(event));
  } catch (error) {
    // No request body, HMAC, secret, or raw Drive exception is returned.
    return jsonResponse_({ok: false, error: safeErrorCode_(error)});
  }
}

function handleUpload_(event) {
  const raw = event && event.postData && event.postData.contents;
  if (!raw || raw.length > MAX_BYTES * 1.5 + 4096) throw new Error('invalid_request');
  let body;
  try { body = JSON.parse(raw); } catch (_) { throw new Error('invalid_request'); }
  const secret = PropertiesService.getScriptProperties().getProperty('GATEWAY_SECRET');
  if (!secret) throw new Error('gateway_not_configured');
  if (body.version !== 1 || body.filename !== EXPECTED_NAME ||
      body.sha256 !== EXPECTED_SHA256) throw new Error('artifact_not_allowed');
  if (typeof body.timestamp !== 'number' || !Number.isInteger(body.timestamp) ||
      Math.abs(Math.floor(Date.now() / 1000) - body.timestamp) > MAX_CLOCK_SKEW_SECONDS) {
    throw new Error('expired_request');
  }
  if (typeof body.content_b64 !== 'string' || typeof body.signature !== 'string' ||
      !/^[A-Za-z0-9+/]+={0,2}$/.test(body.content_b64) ||
      !/^[a-f0-9]{64}$/.test(body.signature)) throw new Error('invalid_request');
  const canonical = [String(body.timestamp), body.filename, body.sha256, body.content_b64].join('\n');
  const expectedSignature = bytesToHex_(Utilities.computeHmacSha256Signature(canonical, secret));
  if (!constantTimeEqual_(expectedSignature, body.signature)) throw new Error('invalid_signature');
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
    let file = matches.hasNext() ? matches.next() : null;
    if (matches.hasNext()) throw new Error('duplicate_files');
    let created = false;
    if (!file) {
      file = folder.createFile(Utilities.newBlob(bytes, 'video/mp4', EXPECTED_NAME));
      file.setDescription('UNAPPROVED REVIEW ONLY; NOT FOR POSTING');
      created = true;
    }
    if (file.getSharingAccess() !== DriveApp.Access.PRIVATE) {
      throw new Error('file_not_private');
    }
    const readback = sha256Hex_(file.getBlob().getBytes());
    if (readback !== EXPECTED_SHA256) throw new Error('readback_hash_mismatch');
    return {ok: true, created: created, file_id: file.getId(),
      readback_sha256: readback, readback_sha256_match: true,
      quality: 'QUALITY_NOT_APPROVED', posting: false};
  } finally { lock.releaseLock(); }
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
  if (typeof left !== 'string' || typeof right !== 'string' || !left.length || !right.length) return false;
  let difference = left.length ^ right.length;
  for (let i = 0; i < Math.max(left.length, right.length); i++) {
    difference |= left.charCodeAt(i % left.length) ^ right.charCodeAt(i % right.length);
  }
  return difference === 0;
}

function jsonResponse_(value) {
  return ContentService.createTextOutput(JSON.stringify(value))
    .setMimeType(ContentService.MimeType.JSON);
}

function safeErrorCode_(error) {
  const allowed = ['invalid_request', 'gateway_not_configured', 'artifact_not_allowed',
    'expired_request', 'invalid_signature', 'invalid_size', 'hash_mismatch', 'busy',
    'destination_not_private', 'duplicate_files', 'file_not_private', 'readback_hash_mismatch'];
  return allowed.indexOf(error && error.message) >= 0 ? error.message : 'internal_error';
}
