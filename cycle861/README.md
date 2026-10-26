# cycle861 — Editorial real-output slide prototype (HUMAN_REVIEW)

Changes relative to cycle860: rather than overlaying a Before/After prompt card onto inherited video, this cycle redesigns **all 8 scenes** as editorial 1080×1920 image slides. It shows a concrete **fictional generated email**, a one-change revision request, and a reusable prompt template. Japanese narration is inherited bit-for-bit, and 24 timed subtitles are burned into the locally rendered MP4.

The branch contains **10-genre storyboard configuration**, caption timing data, and 15 pure-Python regression tests. CI tests this contract **only**; it does not render the MP4.

The actual MP4, six previously generated photo sources, two code-drawn illustrations, full renderer, QA script and local test output are supplied separately in the ChatGPT review package. The repository intentionally contains no unapproved image or audio assets.

Local QA: 14/14 checks PASS; 1080×1920 H.264, 30fps, 691 frames, 23.033s; AAC 48kHz; 24 caption beats visually checked against the no-caption video; audio elementary stream SHA256 matches inherited source; complete video/audio decode PASS.

**Limitations:** Only AI productivity has been rendered; pronunciation and semantic subtitle alignment are not human-reviewed. Original user reference video comparison, mobile device playback, rights approval, employee approval and retention measurement are pending. No merge, paid service, or auto-post. Publication is forbidden until human approval.
