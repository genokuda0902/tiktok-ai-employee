# Cycle571 — Verified four-bar proof (REVIEW ONLY)

Date: 2026-10-14 JST. Extra cost: JPY 0.

Baseline: cycle570, SHA256 `2495853279b5fd9cdae79d5e87bf95bb42b25a90d20eac32da81ccbc39c49625`.

Local MP4: cycle571_verified_chart_REVIEW_ONLY.mp4, SHA256 `c3dd4d0fb659a666e763a6d06caa405fe44560a9432bf624cad38ba71f9b46f6`.

Local changes: replace 14-16s chart with four explicitly labeled synthetic values 120, 150, 200, 250 and checked total 720. The source video and full renderer are **not in this PR**; see the separate user-delivered ZIP. Do not claim this PR alone reproduces the MP4.

Local tests: 14 passed. Full MP4 decode and audio decode passed; 8 subtitle intervals. Existing AAC audio preserved exactly and is instrumental only. New Japanese speech: absent. Semantic voice/caption sync: unverified. Original v33 MP4: not accessed this run. 16-panel storyboard: accessed.

CI: workflow file write was blocked. No workflow run for this branch. No PR merge, posting or approval.

To run saved tests locally: `cd quality/cycle571 && python -m unittest test_proof.py -v`.

Publication: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Only employee-approved manual posting is permitted after rights and voice QA.
