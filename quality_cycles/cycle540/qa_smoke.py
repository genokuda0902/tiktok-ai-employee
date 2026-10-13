"""Cycle540 QA smoke checks."""
import visual_recipe as recipe

def run():
    assert len(recipe.GENRES) == 10
    assert len(recipe.SCENE_VISUALS) == 8
    assert len(set(recipe.SCENE_VISUALS[2:])) == 6
    assert recipe.scene_at(3.52) == 2
    assert recipe.scene_at(11.18) == 7
    assert recipe.validate_layout()
    assert recipe.assert_review_only()
    print("cycle540: 7 checks passed")

if __name__ == "__main__":
    run()
