# cycle626 — B2:B5 four-cell selection correctness (REVIEW ONLY)

Baseline cycle625 showed all four values in the result card, but the earlier selection animation appeared to highlight only three rows. This cycle fixes the *preceding* selection scene: B2:B5 contains 120, 150, 200, 250, four rows.

GitHub contents: reusable lightweight 10-genre selection component, regression tests and isolated CI workflow. The full 20.17s 1080x1920 MP4, executed full renderer, comparison image and local 11-test log are in the ChatGPT conversation ZIP, **not in this repository**. The small GitHub component is not byte-identical to the full local renderer.

GitHub Actions isolated tests: first run 38937062882 passed 9/9 on commit 980b9d3. This README-only update may trigger another CI run.

Reference v33 MP4 (31.553s, 512x910) and user 16-panel storyboard were inspected locally. The cycle626 video is a synthetic procedural reimplementation, NOT v33 parity. Original v33 source is still missing.

No new Japanese narration; no spoken-caption alignment; smartphone playback not tested; inherited media rights not approved. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Do not merge or post. Draft PR creation was blocked by connector safety checks.
