# cycle904 — review-only microcamera and audio-signal QA

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Reimplementation, NOT recovered v33 source. No merge, posting, paid services or public private-media upload.

## Distinct change vs cycle903
cycle903: two-line Japanese caption focus. cycle904: bounded 1.002–1.022x camera drift only in upper y0–1300, preserving the lower HUD and burned-in subtitles. Added objective 20ms PCM signal audit (RMS, peak, near clipping, eight scene-level RMS values) and eight private audio clips for later human/ASR transcription. This is NOT independent Japanese ASR or speech/caption semantic alignment. The same safe renderer validates ten genre identifiers; only ai_work was rendered.

## Local private MP4 verification
Source cycle903 SHA256: 19896d68b73de12195269c6a9e9dfdd020db440fa7708fdffc11cd3c142fea72
Output cycle904 SHA256: 29ecff18efa6b515f6732c1cc3e644520b22930fc528b7c8352f6ed8fe5a992b

- H.264 1080x1920, 30fps, 691 frames, 23.033333s; AAC 48kHz; full A/V decode PASS.
- AAC ADTS SHA256 identical: 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9.
- 690/691 frames changed in upper-region quarter-resolution pixel MAE >1, average 9.748. Caption band y1492–1840 max quarter-res MAE 0.446, from codec recompression.
- Audio peak normalized 0.60254, near-clipped fraction 0. No claim of intelligibility or pronunciation.
- 14 local unit tests PASS. GitHub CI tests source and synthetic one-second A/V only, NOT the private Japanese MP4.

## Reproduction
Use a PRIVATE manifest with genre=ai_work, publication_approved=false, employee_approval=false, contains_private_data=false, asset_rights_approved=false, upload_media_to_github=false, source_sha256=<local review MP4 SHA256>.

python cycle904/cinematic_motion_audit.py --source /PRIVATE/previous.mp4 --output /PRIVATE/new_review.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/verification.json --clips-dir /PRIVATE/review_audio

python -m unittest discover -s cycle904 -p 'test_*.py' -v

Do not commit manifest, source/finished video, extracted frames, audio clips or reference media.

## Research and remaining gates
Consulted accessible summaries of TikTok市場分析 and TikTok動画研究; full original chats inaccessible. Directly inspected user-provided ChatGPT×Excel時短術16コマ絵コンテ.png (16 panels / 36s). Original v33 MP4 inaccessible. Read main 18e084c, open PRs including #275/#276, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md and src/build_daily.py (still silent -an). This eight-scene synthetic video does not match the reference's cinematic people, robot or actual software operation.

Independent Japanese transcription, voice-caption meaning and timing, rights, smartphone playback, employee approval and Actions billing remain unverified. Next: independently transcribe/review the eight audio clips, validate caption timing, clear media rights, then expand approved image-first scenes. Publication remains blocked.
