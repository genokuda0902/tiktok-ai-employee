from quality.cycle462.mascot_contract import POSES, Pose, mascot_pose, safe_for_caption

def test_reuse_three_scenes():
    assert set(POSES)=={'hook','result','cta'}

def test_not_in_caption():
    assert all(safe_for_caption(p) for p in POSES.values())

def test_unknown_scene():
    assert mascot_pose('formula',8) is None

def test_motion_bounded():
    for kind in POSES:
        for t in [0,1,2,4,8,13,19.8]:
            p=mascot_pose(kind,t)
            assert abs(p.center_y-POSES[kind].center_y)<=7
            assert safe_for_caption(p)

def test_pose_is_immutable():
    assert Pose(1,2,3).size==3
