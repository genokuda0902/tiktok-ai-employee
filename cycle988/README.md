# cycle988 — optional Japanese captions (REVIEW ONLY)

Distinct from cycle986's Calc formula magnifier and parallel cycle987 kinetic titles:
this cycle adds a selectable Japanese `mov_text` track with eight scene-timed
captions, transcribed manually from the *visible burned caption region*.
Existing H.264 video and AAC Japanese audio are **stream copied** unchanged.
The new text track is disabled by default to avoid automatic double captions.
MP4 player behavior (especially iOS/Android) remains untested.

## Actual local private MP4
- Input: cycle986 private MP4, SHA256 `8cabfb8af96a4c1373905b232d571944337aedc22d88ac56b05d1d7292590f9b`
- Output: cycle988 private review MP4, SHA256 `afc1ec9f11d69bca92c45a63342de7a306c137a66caf64522f96caf70bb15c25`
- 1080x1920, 30 fps, 691 frames, 23.033333 s, H.264/AAC 48 kHz, plus Japanese mov_text subtitle stream
- 8 text cues extracted and checked against the manifest, full video/audio decode PASS
- Video H.264 elementary-stream SHA256 `112d02dbe0ee49055fe0e4a050490ed0c1b8718fd64844fbf5544cc40a621a86` before/after identical
- Audio AAC ADTS SHA256 `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e` before/after identical
- 11 local unit tests PASS; synthetic-only CI workflow is separate from private MP4 verification
- Real MP4 and stills remain in private ChatGPT review attachments; never commit or publicly upload without rights approval

## Reproduction (only with locally authorized source)
```sh
python cycle988/caption_mux.py \
  --source /private/approved_cycle986.mp4 \
  --output /private/cycle988_review_only.mp4 \
  --manifest cycle988/captions_ai_work.json \
  --work /private/caption_work \
  --expected-sha 8cabfb8af96a4c1373905b232d571944337aedc22d88ac56b05d1d7292590f9b
python -m unittest discover -s cycle988 -p 'test_*.py' -v
```

## Important limitations
The captions are *not* an independent speech-to-text transcript. Text was
transcribed from 18 sampled frames of the existing burned captions; scene
boundaries are the source's eight 2.9-second segments. Audio energy per cue
was measured but does not prove spoken wording or word-level timing.
Independent Japanese ASR, semantic alignment, smartphone caption toggling,
reference-v33 video parity, commercial rights, employee approval, and actual
Actions billing are NOT VERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

Ten genres are declared; only ai_work is approved for real-source geometry.
All other genres fail closed until separately reviewed. No automatic TikTok
posting, paid service, merges, or private-media upload.
