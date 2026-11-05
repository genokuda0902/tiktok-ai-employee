from pathlib import Path
def test_story_has_three_stages():
 text=Path("tools/cycle1242_synthetic_story.py").read_text()
 assert all(x in text for x in ["BEFORE","ACTION","AFTER"])
def test_story_is_synthetic():
 text=Path("tools/cycle1242_synthetic_story.py").read_text()
 assert "Image.new" in text and "IMG_5805" not in text
