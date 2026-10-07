import unittest

def validate(scenes, timeline, total):
    if len(timeline) != len(scenes):
        raise ValueError("scene count mismatch")
    cursor = 0.0
    for scene, item in zip(scenes, timeline):
        if item["scene_id"] != scene["scene_id"]:
            raise ValueError("scene mismatch")
        if abs(float(item["start"]) - cursor) > 0.02:
            raise ValueError("timeline gap")
        if float(item["end"]) <= float(item["start"]):
            raise ValueError("non-positive caption")
        if item["text"] != scene["caption"]:
            raise ValueError("caption mismatch")
        cursor = float(item["end"])
    if abs(cursor - total) > 0.05:
        raise ValueError("duration mismatch")
    return True

class MeasuredCaptionContract(unittest.TestCase):
    def test_ten_genres_share_contract(self):
        genres=["ai_work","beauty","relationship","money","sales","career","health","trivia","travel","product_compare"]
        for genre in genres:
            scenes=[{"scene_id":"s1","caption":genre+" A"},{"scene_id":"s2","caption":genre+" B"}]
            timeline=[{"scene_id":"s1","start":0.0,"end":1.2,"text":genre+" A"},{"scene_id":"s2","start":1.2,"end":2.5,"text":genre+" B"}]
            self.assertTrue(validate(scenes,timeline,2.5))
    def test_gap_fails_closed(self):
        scenes=[{"scene_id":"s1","caption":"A"},{"scene_id":"s2","caption":"B"}]
        timeline=[{"scene_id":"s1","start":0.0,"end":1.0,"text":"A"},{"scene_id":"s2","start":1.2,"end":2.0,"text":"B"}]
        with self.assertRaises(ValueError): validate(scenes,timeline,2.0)

if __name__=="__main__":
    unittest.main()
