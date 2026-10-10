# Cycle483 — Japanese voice gate and prompt-storyboard experiment

Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Zero-cost, original graphics only.

Compared with cycle482: replaces a two-state static three-check card with an 18-state (six scenes × three spotlight states) example showing an ambiguous prompt and a precise goal/constraints/format prompt. Actual rendered local MP4: 1080×1920, 18s, 30fps H.264/AAC. Narration is NOT achieved: Open JTalk, Japanese dictionary, and voice model absent in the local runtime; the AAC track is synthetic SFX, not Japanese speech.

This branch contains a fail-closed native Japanese speech generator and six approval-gate tests. Run `python -m unittest discover -s experiments/cycle483 -p 'test_*.py'`. For native voice on a runner, install free Debian packages `open-jtalk open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001`; then synthesize the six scene scripts and mux into MP4 with ffmpeg, verifying alignment and listening manually.

Do not merge automatically, do not auto-post, do not claim reference-video equivalence. Employee approval is mandatory before manual publication. GitHub workflow configuration was blocked by safety checks, so CI is not confirmed.
