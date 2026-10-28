# cycle926 — 3-stage scene02 task clarity (review only)

Distinct from cycle925's outro CTA (#308) and cycle924's scene03 report (#307). Fixes **scene02's cropped spreadsheet number** and the mismatch with the inherited spoken/captioned message "まず、繰り返している作業を書き出そう。". Replaces only scene02 frames 87–173 (2.9–5.8s) with three original, fictional workflow cards (choose a repeated task → split steps → improve one step). Existing Japanese subtitles at y>=1460 and inherited AAC narration are not modified at source-frame level.

## Reproduction (requires separately approved local private source MP4)

```bash
python -m pip install Pillow==11.3.0
sudo apt-get install fonts-noto-cjk ffmpeg
python cycle926/src/scene02_workflow_clarity.py \
  --source /private/cycle924_CLEAR_REPORT_REVIEW_ONLY.mp4 \
  --output /private/cycle926_WORKFLOW_SCENE02_JP_REVIEW_ONLY.mp4 \
  --workdir /private/cycle926_render
python -m unittest discover -s cycle926/tests -p 'test_*.py' -v
```

Never upload the source MP4, original v33 video, inherited audio, or user assets to public GitHub. The artwork is an **illustrative mock-up**, not real app footage. No publication, posting, merge, or paid-service actions.

## Verified local output (not in repository)

- File: `cycle926_WORKFLOW_SCENE02_JP_REVIEW_ONLY.mp4`; SHA256 `5d906519cc524b80035aceae41012c0f67202549129f79e0d0af9db2825c806f`.
- Source cycle924 SHA256 `dfd16c88c6b1f680c15f84d875690f366e9e034c34e1d73e77eb18132cb7324b`.
- H.264 1080×1920 30fps 691 frames 23.033333s; AAC 48kHz. Full A/V decode PASS.
- Audio ADTS SHA256 unchanged: `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- Changed scene02 87/87 frames; protected subtitle-region maximum 1/8 sampled MAE 0.497; outside-scene maximum 1/8 sampled MAE 0.782.
- Local 15 tests PASS. Ten fictional genre presets, only AI-work MP4 actually rendered.
- User's 16-panel storyboard directly inspected; original v33 MP4, full research chats, independent Japanese ASR, subtitle meaning/timing, rights clearance, smartphone playback, employee approval, actual Actions billing not verified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. CI only validates source and synthetic graphics, never private finished MP4.
