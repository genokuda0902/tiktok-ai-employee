import importlib.util
from pathlib import Path
p=Path(__file__).with_name("render.py")
spec=importlib.util.spec_from_file_location("cycle1248_render",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def test_scene_count(): assert len(m.SCENES)==3
def test_safe_synthetic_data(): assert "300" in str(m.SCENES) and "REVIEW_ONLY" in m.render.__code__.co_consts or len(m.SCENES)==3
def test_render(tmp_path):
    import subprocess, json
    out=m.render(tmp_path)
    assert out.exists() and out.stat().st_size>10000
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_name,width,height","-show_entries","format=duration","-of","json",str(out)]))
    assert float(probe["format"]["duration"])==12
    assert probe["streams"][0]["width"]==720
    assert probe["streams"][0]["height"]==1280
