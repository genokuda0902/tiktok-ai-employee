"""Unit tests for cycle478 scene contract (stdlib only)."""
import unittest
from scene_contract import validate, release_errors

def safe_plan():
    scenes = [
        {"start":0,"end":1.5,"kind":"hook","caption":"冒頭"},
        {"start":1.5,"end":4.5,"kind":"notes","caption":"メモ"},
        {"start":4.5,"end":7.5,"kind":"prompt","caption":"指示"},
        {"start":7.5,"end":11.5,"kind":"table","caption":"表"},
        {"start":11.5,"end":15.5,"kind":"compare","caption":"比較"},
        {"start":15.5,"end":18,"kind":"cta","caption":"保存"},
    ]
    return {"scenes":scenes,"duration":18,"rights":"ORIGINAL_SYNTHETIC",
            "privacy":"NO_PERSONAL_DATA","publication":"NOT_APPROVED",
            "human_approval":False,"auto_post":False,"reference_equivalence":False,
            "narration_status":"NOT_GENERATED",
            "subtitle_provenance":"SCRIPT_TIMED_NOT_SPEECH_ALIGNED"}

class TestContract(unittest.TestCase):
    def test_safe_preview(self):
        self.assertEqual(validate(safe_plan()), [])
    def test_voice_is_not_assumed_from_aac(self):
        self.assertTrue(any("narration" in x for x in release_errors(safe_plan())))
    def test_script_subtitles_are_not_voice_sync(self):
        self.assertTrue(any("sync" in x for x in release_errors(safe_plan())))
    def test_publication_not_approved(self):
        self.assertTrue(any("human approval" in x for x in release_errors(safe_plan())))
    def test_no_autopost(self):
        p=safe_plan();p["auto_post"]=True
        self.assertTrue(validate(p))
    def test_hook_limit(self):
        p=safe_plan();p["scenes"][0]["end"]=2
        self.assertTrue(any("hook" in x for x in validate(p)))
    def test_missing_caption(self):
        p=safe_plan();p["scenes"][1]["caption"]=""
        self.assertTrue(validate(p))
    def test_gap(self):
        p=safe_plan();p["scenes"][1]["start"]=1.7
        self.assertTrue(validate(p))
    def test_unapproved_asset(self):
        p=safe_plan();p["rights"]="UNKNOWN"
        self.assertTrue(validate(p))
    def test_wrong_duration(self):
        p=safe_plan();p["duration"]=20
        self.assertTrue(validate(p))

if __name__=="__main__":
    unittest.main()
