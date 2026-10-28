# cycle928 — animated opening hero (private review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original, synthetic artwork. Reimplementation, NOT recovered v33. No automatic posting, public media, private data, merge or paid services.

## Change vs prior cycles
- cycle926 (#309): scene02 repeated-workflow explanation; cycle927 (#310): scene05 unapproved human-review gate.
- cycle928: **scene01 frames 0–86 (0–2.9s)** replaced with a high-contrast three-beat opening: identify repeated task → do not guess missing values → verify before improvement. Uses a fictional 4–6月 table and a pulsing highlight; never invents June numbers.
- All imagery drawn locally using Pillow; source narration and burned Japanese caption area y>=1460 remain in inherited private MP4. Ten genre-specific headlines and examples are configured; **only AI-work** was rendered as a full MP4.

## Reproduction with separately rights-cleared local input

```bash
python -m pip install Pillow==11.3.0
sudo apt-get install fonts-noto-cjk ffmpeg
python -m unittest discover -s cycle928/tests -v
python cycle928/src/hero_hook.py \
  --source /private/cycle926_WORKFLOW_SCENE02_JP_REVIEW_ONLY.mp4 \
  --output /private/cycle928_ANIMATED_HERO_JP_REVIEW_ONLY.mp4 \
  --workdir /private/cycle928_frames
```

## Local QA (media NOT committed)
- Input SHA256: `5d906519cc524b80035aceae41012c0f67202549129f79e0d0af9db2825c806f`
- Output SHA256: `9a05a5e6fec5c878409cac60e7769867237701ded0736240ebca65f762693b88`
- 1080x1920 H.264 30fps, 691 frames / 23.033333s, AAC 48kHz.
- Full audio/video decode PASS; ADTS audio exact SHA256 `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9` unchanged.
- 87/87 intro frames changed; other scene sampled MAE max 0.524; protected subtitle band sampled MAE max 0.301 at 1/8 size.
- 10/10 unit tests PASS. CI tests only synthetic renderer and publication gates; **not** the finished private MP4.
- Original user 16-panel storyboard is known from previous cycles; reference v33 original MP4 and complete research chats not accessible. Independent Japanese ASR, spoken-caption semantics/timing, commercial source rights, phone playback, employee approval and actual Actions billing unverified.

## Research constraints
Accessible past TikTok市場分析 / TikTok動画研究 summaries emphasize first ~1.5s hook, 15–25s, readable Japanese captions, demonstrable before/after, and manual approval. The 8-scene video still differs from the reference's 16 cinematic panels, live actors and real operation footage. PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md require approval-allowlisted imagery and prohibit robot animation and automatic posting.

This PR deliberately contains **no source or finished MP4, extracted audio, user images, screenshots or private manifests**. Keep employee posting manual after explicit approval.
