# Cycle480 — provenance-backed motion proof (review only)

This iteration improves the **source → prompt → table → comparison** demonstration with real cell-level intermediate states, rather than merely zooming static slides. The local 18s synthetic MP4 is **SFX ONLY**, not Japanese narration, and is **NOT_APPROVED**.

Reproduction is possible from the local QA bundle (includes `build_cycle480.py`, original synthetic input, exact command, MP4, test and probe logs). No confidential images, reference video frames or customer information are used. The original v33 source remains unrecovered.

The repository change is a **genre-neutral provenance guard** and tests. Run:

```sh
python -m unittest quality.cycle480.test_source_provenance -v
```

No automatic posting. No merge. No quality approval. Caption timing is scene-based, **not voice aligned**. Human review and licensed narration remain required. Previous cycle479: static-card-style 18s with no narration; cycle480: per-cell reveal, highlighted unknown fields, source-linked rows.
