# cycle1176 — readable approval disclosure

**Review only. No assets or private media committed.** This is a reimplementation, not recovered original v33 code.

Input: an existing H264 1080×1920 30fps + AAC 48kHz video, with a *manually reviewed* disclosure at x=38..1042/y=1290..1432 during 14.45–17.45 seconds. Never apply these coordinates blindly to a different video. Subtitle region starts at y=1480.

Dependencies: Python 3.11+, Pillow 10–11, FFmpeg/FFprobe, NotoSansCJK-Regular.ttc (fonts-noto-cjk). No paid service.

Create local manifest (source video stays local):
```python
import hashlib,json
source="INPUT_REVIEW_ONLY.mp4"
m={"policy":"HUMAN_REVIEW/PUBLICATION_NOT_APPROVED",
   "asset_approval":"review_only_no_publication","manual_post_only":True,
   "disclosure_roi_reviewed":True,"genre":"ai",
   "source_sha256":hashlib.sha256(open(source,"rb").read()).hexdigest(),
   "start":14.45,"end":17.45}
open("manifest.json","w").write(json.dumps(m))
```

Run:
```bash
python quality/cycle1176/review_disclosure.py \
  --source INPUT_REVIEW_ONLY.mp4 --output OUTPUT_REVIEW_ONLY.mp4 \
  --manifest manifest.json --report qa.json --overlay overlay.png
python -m unittest discover -s quality/cycle1176/tests -p 'test_*.py' -v
```

The 10 genre identifiers share the same disclosure policy; all source media, timings and panel geometry must be reviewed per video. This script preserves the existing AAC bitstream, does not transcribe Japanese speech, and does not approve publication.

CI renders only a short synthetic clip, not the actual local MP4. See RESULT.md for local full-length validation and limitations.
