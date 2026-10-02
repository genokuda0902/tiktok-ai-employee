def validate_asset_schema(data):
    assert data["format"]["width"] == 1080
    assert data["format"]["height"] == 1920
    assert len(data["scenes"]) == 8
    for s in data["scenes"]:
        a=s["asset"]
        assert a["source"] == "newly_generated_cycle255_image"
        assert a["rights"].startswith("AI-generated")
        assert a["human_review_required"] is True
        assert s["publication_allowed"] is False
    return True
