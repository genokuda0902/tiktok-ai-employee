# cycle974 — cross-scene numeric verification (private review only)

**Improvement over cycle972:** the scene 05 source-data chart gives A=12+16+18=46 and B=8+9+12=29, but inherited scene 06 showed an unrelated 17→18 comparison. Scene 06 now demonstrates an explicitly *fictional* AI draft of 45, then checks the actual upstream scene 05 arithmetic 12+16+18=46, and finally corrects 45→46. This avoids a misleading unsupported numeric jump. The script imports `cycle972/chart_reveal.py` to derive totals, so upstream changes cannot silently diverge.

The demonstration is fictional and is **not** a real ChatGPT or Excel operation. No private footage, audio or generated MP4 is uploaded to public GitHub. Original AAC is copied without modification; original burned Japanese captions below y=1240 are kept from source frames. Source code is an original reimplementation, not recovered v33 source.

## Local reproduction

```bash
python -m unittest discover -s cycle974 -p 'test_*.py' -v
python cycle974/verification_reveal.py --source /private/cycle972.mp4 --output /private/cycle974.mp4 --report /private/cycle974_report.json
ffmpeg -v error -i /private/cycle974.mp4 -f null -
```

10 genre accent palettes are defined; only `ai_work` is reviewed, the other nine fail closed. The GitHub Actions workflow uses only synthetic input, does not assert Japanese ASR, rights, actual smartphone playback, employee approval, production readiness, or paid-resource billing. Publication is not approved; employees must approve and manually post.
