# cycle626 — four-row selection correctness (REVIEW ONLY)

Previous cycle625 fixed the fourth chart row being hidden. This cycle fixes a different issue: the preceding B2:B5 selection animation visually highlighted only three cells in the prior version.

Changes: a four-row geometry contract, progressive highlight, sample values 120/150/200/250, tests for all ten genre IDs, rights/publication fail-closed metadata. The GitHub module is a small reusable component. The full local video renderer, MP4, QA logs, and exact run command are provided in the cycle626 conversation ZIP, **not committed here**. Do not claim the small module reproduces the entire MP4.

Baseline: cycle625, 1080x1920, 605 frames, 20.17 s. New segment: frames 315..389 (10.5–13.0 s). Original AAC audio reused. Japanese narration absent, spoken-caption sync not achieved.

Rights: synthetic visuals only for new segment; inherited content not approved. Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Do not merge, post, or claim v33 parity without human review.
