# Cycle577: cross-scene evidence consistency (review only)

The cycle576 comparison scene showed A1:A4 and incomplete/incorrect arithmetic, despite selecting B2:B5 earlier. Cycle577 corrects all four cell labels, SUM range, and 120+150+200+250=720. It does not claim the original reference v33 quality.

Local reproduction (requires separately supplied SHA-locked cycle576 MP4; inherited rights unverified):
\`\`\`sh
pip install pillow
python -m unittest discover -s quality/cycle577 -p 'test_*.py' -v
python quality/cycle577/proof_consistency.py --source cycle576_kinetic_earcons_REVIEW_ONLY.mp4 --output cycle577_proof_consistency_REVIEW_ONLY.mp4
\`\`\`
FFmpeg and NotoSansCJK font required. The original cycle576 MP4 is not committed because rights have not been approved. No new Japanese narration; BGM and subtitle track inherited. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge or posting.
