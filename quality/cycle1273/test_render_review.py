from pathlib import Path
import ast
SOURCE=Path(__file__).with_name("render_review.py")
def test_syntax(): ast.parse(SOURCE.read_text(encoding="utf8"))
def test_no_auto_post(): assert "tiktok.upload" not in SOURCE.read_text(encoding="utf8").lower()
def test_review_only(): assert "REVIEW ONLY" in SOURCE.read_text(encoding="utf8")
