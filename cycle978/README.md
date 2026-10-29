# cycle978 — transition ghost removal, review only

## Distinct issue and fix
The previous private cycle976 MP4 shows an inherited **17 / 18** arithmetic card leaking through the transition from scene06 to scene07 (17.40–17.67 s). The result in scene06 is A=46 / B=29, so the leaked numbers are misleading. This cycle replaces only frames 522–530 (9 frames, 0.300 s) in the **upper artwork** using the clean scene07 frame 532. Original Japanese burned captions below y=1440 (visually confirmed caption panel begins below this line in this exact source) and the original AAC stream are retained. This is a transition repair, not another arithmetic card or graph redesign.

## Private local run
Run repair_transition.py with --source /path/to/approved_local_cycle976.mp4 --output /private/cycle978.mp4 --work /private/cycle978_work; then qa_transition.py with --source and --output and --report /private/qa978.json; then python -m unittest discover -s cycle978 -p 'test_*.py' -v.

The source video and extracted anchor image **must not** be committed to public GitHub. CI uses synthetic generated data only. 10 genres are enumerated but only ai_work has real-media coordinates reviewed; the other nine fail closed.

## Review and rights
The private source's ownership/commercial release rights, Japanese narration ASR/semantic subtitle alignment, mobile playback, employee signoff and actual GitHub Actions billing remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No automatic TikTok posting, no merge, no paid services.
