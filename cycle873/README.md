# cycle873 — clean workflow scene, ten genres (REVIEW ONLY)

Reimplementation, **not** original v33. Replaces cycle872's **scene 02**, frames 89–169 (2.967–5.667 seconds), with a legible three-row work-audit graphic and sequential highlight, on the previously generated cinematic office-photo background. The previous source had a cramped browser capture and overlapping labels. No private media or user data are committed.

The genre-independent renderer accepts 10 presets: AI時短, 雑学, 料理, 美容, お金, 健康, 旅行, 商品紹介, ストーリー, 仕事術. Only AI-work has been rendered to a finished 23.033-second MP4. The existing Japanese AAC voice and lower caption strip are preserved. The code fails closed on private input/photo SHA manifest and review-only flags.

## Local reproduction with PRIVATE review assets
```bash
PYTHONPATH=cycle873 python -m unittest discover -s cycle873 -p 'test_*.py' -v
python cycle873/scene02.py --source <private-cycle872-MP4> --photo <private-generated-office-photo> --output <new-private-review-MP4> --manifest <review-only-sha-manifest.json> --report <render-report.json>
python cycle873/verify.py --old <private-cycle872-MP4> --new <new-private-review-MP4> --report <qa.json>
```

Requires Python, Pillow, FFmpeg, Noto Sans CJK; QA additionally requires cv2 and numpy. Private inputs are included only in the ChatGPT review ZIP, not GitHub. CI tests 11 portable tests and **synthetic** 1s H264/AAC, not the private 23s video. Reference 16-panel storyboard inspected directly; original v33 MP4 unavailable, original reference source code not recovered. Full TikTok市場分析/TikTok動画研究 chat transcripts unavailable; accessible research summaries consulted.

## Verified private result
Input SHA256 `5a4a88601d4618d4b6bd435cbf0c70fefabb668b488568b1573e599e72cadf4a`.
Output SHA256 `01deabc424d0cda2347f29cad5676b755182d96883c86749d698fd2a9c6864d7`.
H264 1080×1920 30fps, 691 frames, 23.033s, AAC 48kHz. Full A/V decode PASS; 81/81 target frames changed; all 691 subtitle-strip frames checked (max sampled mean delta 0.5266); outside-scene sampled max 0.4549; audio ADTS bit identical; 11 local unit tests PASS. Source voice language/pronunciation, semantic caption sync, source/publication rights, device playback, employee approval, v33 parity, retention and actual GitHub billing **unverified**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No paid services, private-media upload, auto-post, or merge.
