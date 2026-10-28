# cycle924 — clean report preview (REVIEW ONLY)

New change relative to cycle923 PR #305 (prompt UI) and PR #306 (scene wipes): the scene03 chart had stacked labels and did not clearly illustrate the Japanese caption about preparing a completed example. Frames 174–260 are replaced with an original, fictional, high-contrast report preview in three timed beats. Only upper editorial region y<=1390 is drawn. Inherited burned subtitles and Japanese AAC are retained; this does not independently verify spoken Japanese.

Run on a PRIVATE approved local source:
python -m pip install pillow opencv-python-headless numpy
python cycle924/src/clear_scene03.py --source /PRIVATE/previous_REVIEW_ONLY.mp4 --output /PRIVATE/cycle924_CLEAR_REPORT_REVIEW_ONLY.mp4 --report /PRIVATE/manifest924.json --genre ai_work
PYTHONPATH=cycle924/src python -m unittest discover -s cycle924/tests -p 'test_*.py' -v

10 original fictional genre presets. Only ai_work rendered into a full MP4. Do NOT commit source MP4, audio, reference media, user images, or unapproved assets to this public repository. CI tests synthetic frames and review-only safety, not the private finished MP4. No merge or posting. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

Local full MP4 SHA256: df244e6656910a54c4edf2575da370d732642e15450d084993fe5ec8089fc99b. Full A/V decode PASS, AAC ADTS stream unchanged, 87/87 changed frames, 15 local tests PASS. Reference v33 MP4, independent ASR, phone playback, rights clearance and employee approval unverified.
