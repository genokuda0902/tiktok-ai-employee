import json
from pathlib import Path
p=json.loads(Path(__file__).with_name("contract.json").read_text())
assert p["base_cycle"]==301
assert p["resolution"]==[1080,1920]
assert p["improvement_axis"]=="adaptive_rms_audio_driven_scene_emphasis"
assert 3 <= len(p["analyzer"]["derived_emphasis_windows"]) <= 6
assert p["micro_zoom"] <= 1.01
assert p["new_tts_generated"] is False
assert p["third_party_stock_added"] is False
assert p["auto_post"] is False
print("PASS: cycle302 adaptive RMS audio-sync contract")
