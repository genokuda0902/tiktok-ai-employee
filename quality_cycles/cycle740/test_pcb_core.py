"""Local deterministic tests for the reusable concept board."""
from pathlib import Path
import importlib.util
import hashlib

def board_generator():
    path = Path(__file__).with_name("pcb_art_core.py")
    spec = importlib.util.spec_from_file_location("pcb_art_core", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_pcb

def test_board_dimensions():
    assert board_generator()().size == (1280, 820)

def test_board_is_repeatable():
    draw = board_generator()
    first = hashlib.sha256(draw(seed=740).tobytes()).digest()
    second = hashlib.sha256(draw(seed=740).tobytes()).digest()
    assert first == second

def test_board_has_color_detail():
    assert len(set(board_generator()().getdata())) > 200
