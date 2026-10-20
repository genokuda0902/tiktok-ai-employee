# cycle710 — 8-scene chapter rail (HUMAN REVIEW)

Change from cycle709: a new 8-segment animated chapter progress rail in the upper safe area (x=64, y=166, width=792, height=36) on all eight scenes. Existing Japanese audio and captions are preserved; speech meaning/synchronization is not verified.

## GitHub code and tests

The repository includes the reusable `src/quality/cycle710_chapter_rail.py` overlay drawing module and `tests/test_cycle710_chapter_rail.py` tests. Run:

```bash
python -m pip install Pillow
python -m unittest tests/test_cycle710_chapter_rail.py -v
```

The full ffmpeg-based MP4 renderer, QA, preview generator, input and output MP4 are in the downloadable cycle710 ZIP artifact attached to the conversation. Full renderer could not be committed due to a connector safety check; **GitHub alone is not yet sufficient to reproduce the MP4**.

Requires Python, Pillow, ffmpeg/ffprobe and a rights-cleared source MP4. Ten color palettes are supported; only the science MP4 was rendered in this cycle. Local technical QA 15/15; local unit tests 12/12. Existing audio packet bytes were preserved; no new Japanese narration was synthesized.

No paid API, automatic post, merge, or approval claim. Human review and employee approval are mandatory before any manual posting.