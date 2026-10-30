# cycle989 — original scene-transition sound cues (HUMAN_REVIEW)

This experiment improves the **sound design** of the existing eight-scene Japanese image-slide video. It adds seven deterministic, self-synthesized 185ms airy transition cues at scene boundaries (frames 87, 174, 261, 348, 435, 522, 609 at 30fps). The original narration is mixed without changing the video bitstream. No external music, sound sample, cloud API, credentials, paid services, or automated posting.

## Source and scope
- Previous review MP4: cycle987_KINETIC_HEADLINES_JP_HUMAN_REVIEW.mp4 (available only in the user conversation, **not** checked into this public repository).
- Source dimensions: 1080x1920, H.264, 30fps, 691 frames, 23.033s; Japanese AAC 48kHz mono.
- Script is genre-independent and accepts arbitrary scene boundary frame numbers through its Python API. Ten genre layouts **are not** all approved or rendered.
- Source assets' commercial rights, v33 original, smartphone playback, and staff approval remain unverified.

## Reproduce locally
```sh
python experiments/cycle989/transition_audio.py input.mp4 output_review.mp4 --report render989.json
python -m unittest discover -s experiments/cycle989/tests -v
ffmpeg -v error -i output_review.mp4 -f null -
```

## Local measured results
- 7/7 unit tests passed; full MP4 video/audio decode passed.
- Source and output video packet SHA-256: `9eeb5b064061167ab2b07336747ae5b3094d91a1f1498e1d021f3eba2eb0e4ec` (identical).
- Original integrated loudness: -16.25 LUFS, true peak -1.57 dBTP.
- Output integrated loudness: -16.26 LUFS, true peak -1.58 dBTP.
- Source narration/captions retained; **independent Japanese ASR semantic and word-level timing validation not yet performed**.
- CI uses synthetic audio/video and does not validate the real MP4, the Japanese voice, or source rights.

## Delta from cycle987
- cycle987: animated headline reveal on all eight scenes (visual only).
- cycle989: new original subtle transition audio at seven scene boundaries (audio only); source visual and burned-in captions are bitstream identical.
- No merge, posting, paid contract, or user account operation.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED** — staff must approve and manually post. This is not a claim of parity with reference v33 or production quality.
