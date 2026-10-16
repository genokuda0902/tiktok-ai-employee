# cycle620: temporal caption-safe bridge (REVIEW ONLY)

Compared with cycle619's left-to-right wipe, this uses a whole-frame fade to a blank navy slate and then fades the opening frame in. It prevents captions being split at a moving boundary. Reimplementation, not recovered v33 source. Baseline footage/music rights are unapproved; no release or posting. **Does not create Japanese narration**; speech/subtitle synchronization is not verified.

```bash
python -m pip install numpy pillow
python -m unittest discover -s quality/cycle620 -p 'test_*.py' -v
python quality/cycle620/temporal_caption_bridge.py --baseline BASELINE_REVIEW_ONLY.mp4 --output cycle620_REVIEW_ONLY.mp4 --work scratch
```

Requires FFmpeg/FFprobe. Review video was rendered from cycle617 CTA original to avoid inheriting cycle619's split-text wipe, compared with cycle619. Only AI-work rendered; genre contract tests cover the actual 10 pilot categories. Baseline MP4 is not committed; it was provided in earlier cycle617 user-visible artifacts. CI checks source/tests without the unapproved MP4. No reference equivalence, voice, device playback, or rights approval implied.
