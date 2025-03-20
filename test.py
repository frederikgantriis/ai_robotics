from alg import reader

def test_actor_on_box():
    lines = [
        "+"
    ]

    state, _, _ = reader(lines)

    actor = state.get("actor", tuple())
    boxes = state.get("boxes", set())

    assert actor
    assert actor == (0,0)

    assert len(boxes) == 1
    assert {(0,0)} == boxes


def test_box_on_goal():
    lines = [
        "*"
    ]

    state, goals, _ = reader(lines)

    boxes = state.get("boxes", set())

    assert len(boxes) == 1
    assert {(0,0)} == boxes

    assert len(goals) == 1
    assert {(0,0)} == goals


def test_reader_small():
    lines = [
        "#@$."
    ]

    state, goals, walls = reader(lines)

    actor = state.get("actor", tuple())
    boxes = state.get("boxes", set())
    moves = state.get("moves", [1])


    assert actor
    assert actor == (0,1)

    assert len(boxes) == 1
    assert {(0,2)} == boxes

    assert len(moves) == 0

    assert len(goals) == 1
    assert {(0,3)} == goals

    assert len(walls) == 1
    assert {(0,0)} == walls

def test_reader_big():
    lines = [
        "#####",
        "#.$ #",
        "#.$ #",
        "#@  #",
        "#####"
    ]

    state, goals, walls = reader(lines)


    actor = state.get("actor", False)
    boxes = state.get("boxes", [])
    moves = state.get("moves", [1])


    assert actor
    assert actor == (3,1)

    assert len(boxes) == 2
    assert {(1,1), (2,1)} == boxes

    assert len(moves) == 0

    assert len(goals) == 2
    assert {(1,2), (2,2)} == goals

    assert len(walls) == 16
    assert {
        (0,0),(0,1),(0,2),(0,3),(0,4),
        (1,0),                  (4,1),
        (2,0),                  (4,2),
        (3,0),                  (4,3),
        (4,0),(4,1),(4,2),(4,3),(4,4),
    } == walls
    
    


