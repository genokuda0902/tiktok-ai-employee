# cycle1016 — two image-first storyboard inserts / REVIEW ONLY

Date: 2026-10-30 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Verified difference from cycle1014
- Prior cycle1014 added a 48-bar waveform driven by AAC soundtrack. This cycle adds two *original, procedurally illustrated* short central-panel storyboard inserts, at **3.90–5.10s** (repetitive task inventory) and **18.08–19.28s** (reusable instruction template). Animated rows and subtle fade/slide. Labels explicitly state that the graphics are examples, not real screen captures.
- These are **2 additional visual beats within 8 existing scenes**, not 10 new full scenes. They preserve original title area, burned Japanese captions and bottom audio visualization. The original human/robot and Calc footage is not replaced outside the two central inserts.
- Common declarative insert layout and 10 genre IDs. **Only the exact SHA-pinned local AI-work source is permitted for real rendering**; other 9 genres fail closed until approved material is supplied. Synthetic CI bypass requires a named <=3.1s synthetic fixture.

## Private local video and verification
- Input cycle1014 MP4 SHA256 `b27da279d11e07d3c59a4da32038b51b3a61f25c132fa4ac75ca484efa5d2362`.
- Output `cycle1016_TWO_STORYBOARD_INSERTS_JP_REVIEW_ONLY.mp4` SHA256 `ba2b8937fd6343a12f5dd09fcfcef590d800fef73347b52662792ea72e5fa163`.
- H.264 1080x1920 30fps, 691 frames, 23.033333s; Japanese-tagged AAC 48kHz. Full video/audio decode PASS.
- AAC ADTS bitstream SHA256 identical before/after: `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e`.
- Caption ROI y1490–1700 sampled at frames 60,133,200,450,560,650: mean pixel differences 0.333,0.448,0.352,0.349,0.346,0.388 /255. Central insert region frame133: 49.543/255, frame560: 111.88/255. These are samples, not exhaustive subtitle QA.
- 10 local unit tests PASS. GitHub Actions validates tests and a synthetic 2s fixture, **not** the private completed MP4.
- The private MP4 is shared only in the ChatGPT conversation, never committed or uploaded to public GitHub.

## Research and reference
- Consulted accessible summaries of `TikTok市場分析` (completed result in first seconds, measurable engagement, 24h/72h/7d KPI) and `TikTok動画研究` (before/after, meaningful cuts, real UI, readable Japanese captions, manual human approval). Full task/chat transcripts not accessible.
- Directly viewed user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` from Library: 16 panels/~36s, cinematic robot/human imagery, real UI, Before/After, CTA. Original reference v33 MP4 inaccessible. This cycle's 8 scenes/23s and simple vector inserts do **not** match cinematic reference quality.
- Verified main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, open PRs including #416 and parallel #415, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, and `src/build_daily.py` (still silent `-an`).

## Reproduce (private approved local source only)
```bash
python -m pip install Pillow==11.3.0
python -m unittest discover -s cycle1016/tests -p 'test_*.py' -v
python cycle1016/source/insert_storyboard.py --source /private/cycle1014.mp4 --output /private/cycle1016.mp4 --report /private/qa1016.json --review-only
```

## Still unverified / next priority
- **Independent Japanese ASR and speech-caption semantic/timing comparison remain undone**: local environment has no approved offline Japanese model. AAC data identity only proves audio preservation.
- Original/reference v33 MP4 direct comparison, source-media publication rights, real smartphone playback, employee approval, TikTok performance, actual Actions charges unverified.
- Next: secure a lawful offline Japanese ASR model, compare all 8 captions to speech, then increase genuinely distinct rights-cleared footage. No merge, auto-post, paid service, or external private-media upload.
