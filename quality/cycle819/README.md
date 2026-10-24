# cycle819 — Japanese narration in CI (draft, no publication)

This is a stacked change based on cycle818 PR #130, **not a merge**.

## Improvement over cycle818
The CI fixture no longer uses a 440 Hz beep. The new workflow uses the
offline **Open JTalk** engine to synthesize Japanese narration for all 8
scenes, while reusing the original Pillow-generated synthetic images,
24 caption-highlight states, and final animated CTA from cycle818.

The offline NIT ATR503 M001 voice is licensed **CC BY 3.0**; attribution
is included in the artifact. See the upstream voice distribution:
https://sourceforge.net/projects/open-jtalk/files/HTS%20voice/hts_voice_nitech_jp_atr503_m001-1.05/

The separate **local** cycle819 review video inherits the existing
Japanese narration and images and adds a readable animated opening hook.
It is not uploaded to this public repository because inherited image
rights and employee approval are still pending.

## Review gates
- Original CI graphics; no unapproved AI portraits uploaded.
- 1080x1920 H.264 / AAC; full video decode and caption checks.
- Speech pacing may be mechanically adjusted to fit the fixed storyboard.
- Human evaluation of Japanese naturalness, exact caption alignment, and
  mobile playback remains outstanding.
- 10 genre accent presets are inherited from cycle817; 10 fully authored
  scripts and voiceovers are **not** yet implemented.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
- No merge, posting, billing change, paid API, or external upload.

If the GitHub runner cannot install the Ubuntu voice package or the TTS
is too slow, inspect Actions logs and repair package setup/tempo handling
before adding new visual effects.
