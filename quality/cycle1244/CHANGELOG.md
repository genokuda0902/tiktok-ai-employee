# cycle1244

Previous cycle1243: timed captions on an existing silent clip; input not reproducible from repository.

This cycle: independent original synthetic spreadsheet story renderer, 15 seconds, 720x1280, silent, Japanese on-screen explanatory text, three distinct stages. This is a reimplementation, not original v33. Local demo was rendered using a closely related but not byte-identical local script; repository renderer itself and repository test have not been run. Local tests: 2 pass, full MP4 decode pass. No voice, no synchronized subtitles, no approval for publication. Requires Pillow, ffmpeg and Noto CJK fonts. Run: python quality/cycle1244/render_story.py output.mp4 ; python -m unittest discover -s quality/cycle1244 -p 'test_*.py'.
