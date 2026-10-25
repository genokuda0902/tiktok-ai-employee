# cycle844 — 24 narration-beat progress pulses (review only)

New vs cycle843: an animated progress line grows during each of 24 Japanese spoken subtitle beats, then resets. All eight photo scenes, eight kinetic example cards, seven photo dissolves, original burned captions and Japanese AAC audio are preserved. No new native-resolution photos were generated.

Run from this directory:
```
python -m unittest -v test_caption_pulse.py
python caption_pulse.py --source /path/to/cycle843.mp4 --output /path/to/cycle844.mp4 --beats caption_beats.json --manifest manifest.review.json --genre ai_work
```
Requires FFmpeg with libass. No paid API or posting. Input media is not committed: photo/voice/model rights and employee approval remain unverified. The ten genres share the same engine and have different accent colors. This overlay is only compatible with the reviewed cycle843 geometry (1080x1920). CI tests the source code, **not** the MP4. Local MP4 full decode, frame count, 24 animated beats and exact AAC bitstream identity are verified separately. Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
