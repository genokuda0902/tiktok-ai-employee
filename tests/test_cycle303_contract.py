import json
from pathlib import Path
p=json.loads(Path("docs/cycle303_contract.json").read_text(encoding="utf-8"))
assert p["base_cycle"] == 302
assert p["resolution"] == [1080,1920]
assert p["improvement_axis"] == "audio_derived_cut_boundary_accents"
assert len(p["audio_derived_boundaries_seconds"]) == 5
assert p["accent"]["duration_ms"] <= 100
assert p["new_tts_generated"] is False
assert p["third_party_stock_added"] is False
assert p["auto_post"] is False
print("PASS: cycle303 audio-cut-boundary contract")
