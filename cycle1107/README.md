# cycle1107 — narration-pause scene cuts (HUMAN REVIEW ONLY)

## New change from cycle1105
Previous: 7 visual cuts had scene-safe fade-through-dark but could occur during a spoken phrase.
This cycle: detect >=0.12-second audio pauses below -32 dBFS; move the seven visual scene boundaries to nearby pause midpoints (prefer preceding pause). Piecewise retime only the picture, keep the original AAC audio packets unchanged, preserve all 8 chapter markers.

Source boundaries (frames): 0,79,174,258,340,423,503,593,675.
Output boundaries (frames): 0,94,168,247,330,412,499,575,675.

## Local real MP4 (NOT uploaded to public GitHub)
- 22.5s, 1080x1920, 30fps, 675 frames, H.264, 8 chapters, Japanese-tagged AAC 48kHz.
- Full A/V decode PASS; original and output AAC ADTS SHA256 identical.
- Median 150ms-window RMS at 7 cut points: before -13.55 dBFS, after -66.38 dBFS (52.83 dB lower).
- Maximum cut shift: 18 frames (0.6s).
- Output SHA256 and detailed QA are in the local review package.
- Visual retiming can introduce repeated/dropped frames: employee review required.

## How to reproduce (with a legitimately available source)
python cycle1107/voice_safe_cuts.py INPUT.mp4 OUTPUT.mp4
python -m unittest discover -s cycle1107/tests -p 'test_*.py' -v

## CI
Workflow tests only synthetic 22.5s media and unit tests. It does NOT include or verify the private user MP4.

## Limits
Audio amplitude pauses are not Japanese ASR, and do not prove that spoken words match burned-in subtitles. Reference v33 original, asset rights, actual smartphone playback, employee approval, TikTok performance, and Actions billing remain unverified. Ten genres can use the same timing function; only AI-work actual media has been rendered.

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
No auto-post, paid contracts, unapproved public upload, or merge.
