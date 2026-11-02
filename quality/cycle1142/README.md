# cycle1142 — data-lineage focus (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Not original v33 code; no auto-post, merge, paid services or public use of private media.

## Source and tests
The exact source used for the local reviewed MP4 is preserved in [source_tests.tar.xz](./source_tests.tar.xz), Git blob SHA **b729dfb6d68d57e60941870873457865ec451073**, archive SHA256 **c9ac53342860c268225bbc8b952391a6bc2b83d5933e923d01570a4fe35131e7**. Archive contains:
- quality/cycle1142/lineage_focus.py (renderer and 10-genre fail-closed manifest gate)
- quality/cycle1142/test_lineage_focus.py (13 tests, including synthetic H264/AAC smoke)
- quality/cycle1142/qa_compare.py (all 691 caption frames and outside-window drift)

Extract with \`tar -xJf quality/cycle1142/source_tests.tar.xz -C .\`. The CI extracts this exact archive before running tests; private MP4 and private manifest are not in GitHub.

## Distinct visual improvement
Cycle1140 changed opening-robot camera motion. This cycle repairs a **different spreadsheet scene regression**: during B5 selection, the inherited big callout showed C2:C4 while the real formula bar showed B2:B4. For frames 182–206 (6.067–6.900s) the label now matches B, with a B5 focus outline and \`12+16+18=46\`. Frames 207–217 show C5 focus and \`8+9+12=29\`. Ten genre IDs share the validation contract; only the AI/Excel MP4 was rendered.

## Local reproducibility
\`\`\`bash
tar -xJf quality/cycle1142/source_tests.tar.xz -C .
python quality/cycle1142/lineage_focus.py --source PRIVATE_CYCLE1140.mp4 --output PRIVATE_CYCLE1142.mp4 --manifest PRIVATE_REVIEW_MANIFEST.json --report PRIVATE_QA.json
RUN_MEDIA_SMOKE=1 PYTHONPATH=quality/cycle1142 python -m unittest discover -s quality/cycle1142 -p 'test_lineage_focus.py' -v
python quality/cycle1142/qa_compare.py --source PRIVATE_CYCLE1140.mp4 --output PRIVATE_CYCLE1142.mp4 --report PRIVATE_VISUAL_QA.json
\`\`\`

Do not commit the private source-hash manifest. See RESULT.md for exact SHA256, tests and unresolved approvals.
