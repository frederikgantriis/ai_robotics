"""
A Sokoban algorithm solver. 
Reads a textual level and outputs a list of directions and move types the actor should perform.
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
from utils import pos_add, valid, State
from prettyprint import replay



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
            if (state["actor"], tuple(state["boxes"]), dir) in priors or action == "invalid":
                continue
            new_prior = (state["actor"], tuple(state["boxes"]), dir)
            priors.add(new_prior)

            new_actor = pos_add(state["actor"], dir)
            new_boxes = {pos_add(box, dir) if new_actor == box else box 
                            for box in state["boxes"]} if push else state["boxes"]
            new_moves = state["moves"] + [(dir, action)]
            new_state = State(new_actor, new_boxes, new_moves)

            if new_state["boxes"] == goals:
                return new_state["moves"]

            q.enqueue(new_state)

    return []

if __name__ == '__main__':
    from time import sleep
    claire = """
    #######
    #.@ # #
    #$* $ #
    #   $ #
    # ..  #
    #  *  #
    #######
    """
    alice = """
    #######
    #.    #
    #$* # #
    #.  $*#
    # .$  #
    #@ *  #
    #######
    """
    sophia = """
    #######
    #     #
    #@$.# #
    #*$  .#
    # $$  #
    # . . #
    #######
    """


    split = lambda s: [line.strip() for line in s.split('\n') if line.strip()]
    level = split(sophia)
    state, goals, walls = reader(level)
    print("Starting search...")
    solution = main(state, goals, walls)
    print("Found solution!")
    replay(state, goals, walls, solution)
    print(solution)
