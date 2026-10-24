# cycle821 — photo-first cinematic opening (review only)

**Purpose:** Replace only 0–3 s (90 frames) of the previous 23.933 s private review MP4 with a photographic, subtly moving opening. This is a deliberate change from the cycle820 15–18 s action-card improvement. All ten genre palettes share one renderer. No automatic posting, no merge, no paid services.

## Local review reproduction
Dependencies: Python 3.11+, Pillow, ffmpeg, ffprobe, Noto Sans CJK fonts.

```bash
PYTHONPATH=quality/cycle821 python -m unittest discover -s quality/cycle821 -p 'test_*.py' -v
python quality/cycle821/cinematic_hook.py --source RIGHTS_APPROVED_SOURCE.mp4 --photo RIGHTS_APPROVED_ORIGINAL.png --output REVIEW_ONLY.mp4 --genre sales_business
```

**Media provenance:** Local review uses a new AI-generated original cinematic desk still (no external photo, visible person or personal data). The photo, inherited video and inherited audio are not committed; they are provided only in the user review ZIP. The repository code is reproducible with an explicitly supplied photo. GitHub Actions uses a self-drawn synthetic placeholder and a 440 Hz tone: **its artifact does not contain Japanese speech and must not be presented as the finished review video.**

**Current review QA:** local 6/6 tests; 1080×1920 H.264 30fps, 718 frames, 23.933333 s, AAC 48 kHz; full decode PASS. Source and output AAC MD5 both c8ab89827b140b5d28e6169711b03bf0. First 1.5 s mean absolute pixel difference 46.3164; unchanged 4.5 s difference 0.4073; 19.5 s difference 0.3717 (re-encoding). Local review SHA256 b3fe32b8f609d12384be29ce7be814d685b5214436e812d54132e8877336c9a4.

**Not verified:** Japanese narration semantic content and subtitle alignment, reference v33 original side-by-side, mobile device, inherited media rights and employee publication approval. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
