from pathlib import Path
import importlib.util
p=Path(__file__).with_name("verified_result_overlay.py")
s=importlib.util.spec_from_file_location("verify",p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
assert len(m.GENRES)==10
assert sum(m.VALUES)==650000
assert m.WINDOWS=={"intro":(0,96),"chart":(300,384)}
for g in m.GENRES:
 for scene in m.WINDOWS:
  assert m.overlay(scene,g).size==(1080,1920)
print("cycle770: 10 genres and verified sum passed")
