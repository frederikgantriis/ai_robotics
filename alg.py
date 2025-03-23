"""
A Sokoban algorithm solver. 
Reads a textual map and outputs a list of directions and move types the actor should perform.
Origon (0,0) will always be at the top left, probably inside a wall.
This algorithm is extremely naive 

<<< Input
######
#@# *#
# $ .#
######

>>> Output
[
("D", "walk")
("R", "push")
("R", "push")
]
===
"""

from constants import TILES
from kueue import Queue



State = lambda actor, boxes, moves: dict(actor=actor, boxes=boxes, moves=moves)

def pos_add(pos: tuple[int, int], dir: str) -> tuple[int, int]:
    VEC = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
    return tuple(sum(x) for x in zip(pos, VEC[dir])) # type: ignore

def pretty_print(state: dict, _goals: set, _walls: set):
    actor = state["actor"]
    boxes = state["boxes"]
    walls = sorted(_walls)
    goals = sorted(_goals)



def reader(lines: list[str], mapping: dict[str, str] = TILES) -> tuple[dict, set, set]:
    actor = (-1, -1)
    boxes = set()
    goals = set()
    walls = set()

    for rowidx, line in enumerate(lines):
        for colidx, cell in enumerate(line):
            pos = (rowidx, colidx)
            val = mapping[cell]
            if val == "wall":
                walls.add(pos)
            elif val == "floor":
                pass
            elif val == "goal":
                goals.add(pos)
            elif val == "box":
                boxes.add(pos)
            elif val == "box on goal":
                boxes.add(pos)
                goals.add(pos)
            elif val == "actor on goal":
                actor = pos
                goals.add(pos)
            elif val == "actor":
                actor = pos


    return State(actor, boxes, []), goals, walls


def valid(state, dir, walls) -> tuple[bool, bool]:
    new_actor = pos_add(state["actor"], dir)

    if new_actor in walls:
        #print("Actor hit a wall")
        return False, False

    elif new_actor in state["boxes"]:
        #print(f"Hit a box at {new_actor} going {dir}")
        new_box = pos_add(new_actor, dir)
        if new_box not in walls:
            #print("Pushing box")
            return True, True
        else:
            return False, False

    return True, False



def main(init: dict, goals: set, walls: set) -> list[tuple[str, str]]:
    if init["boxes"] == goals:
        return init["moves"]

    priors = set()
    q = Queue()
    q.enqueue(init)
    while not q.is_empty():
        state = q.dequeue()

        for dir in ["left", "right", "up", "down"]:
            walk, push = valid(state, dir, walls)
            action = "push" if push else "walk" if walk else "invalid"
            if action == "invalid":
                continue
            if (state["actor"], tuple(state["boxes"]), dir) in priors:
                continue
            print((walk, push), state["actor"], dir, action)
            print(state["moves"])
            new_prior = (state["actor"], tuple(state["boxes"]), dir)
            priors.add(new_prior)

            new_actor = pos_add(state["actor"], dir)
            new_boxes = {pos_add(box, dir) for box in state["boxes"] if new_actor == box} if push else state["boxes"]
            new_moves = state["moves"] + [(dir, action)]
            new_state = State(new_actor, new_boxes, new_moves)

            if new_state["boxes"] == goals:
                return new_state["moves"]

            q.enqueue(new_state)
            #print("\n".join(map(str, sorted(priors, key= lambda x: x[0]))))
            print("="*10)

    return []



if __name__ == '__main__':
    from time import sleep
    lines = [
        "####",
        "#@ #",
        "#$ #",
        "#. #",
        "####",
    ]
    alice = """
    #######
    #.@ # #
    #$* $ #
    #   $ #
    # ..  #
    #  *  #
    #######
    """
    alice = [line.strip() for line in alice.split('\n') if line.strip()]
    print(alice)
    state, goals, walls = reader(alice)
    print(f"{state = }")
    print(f"{sorted(goals) = }")
    print(f"{sorted(walls) = }")
    sleep(5)
    solution = main(state, goals, walls)
    print(solution)
