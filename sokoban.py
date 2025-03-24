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



def reader(lines: list[str], *, mapping: dict[str, str] = TILES) -> tuple[dict, set, set]:
    """
    Helper function translating a list of strings into a sokoban map

    Arguments:
        lines: list of strings to map
        *:
        mapping: dictionary mapping characters such as '#' to their meaning e.g. 'wall'

    Returns:
        tuple[dict,set,set]:
        Initial state of the game <br>
        Set of coordinates for all goals on the map <br>
        Set of coordinates for all walls on the map
    """
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


def sokoban(
        init: dict,
        goals: set[tuple[int, int]],
        walls: set[tuple[int, int]],
    ) -> list[tuple[str, str]]:
    """
    Main function for sokoban algorithm, calculates a solution for a sokoban game

    Arguments:
        init: Initial state of the sokoban game
        goals: Set of coordinates for all goals
        walls: Set of coordinates for all walls

    Returns:
        list[tuple[direction,action]]:
        List of moves to perform in order to solve the level, \
            empty if level is unsolvable or solved by default
    """
    if init["boxes"] == goals:
        return init["moves"]

    priors = set()
    q = Queue()
    q.enqueue(init)
    while not q.is_empty():
        state = q.dequeue()

        for direction in ["left", "right", "up", "down"]:
            walk, push = valid(state, direction, walls)
            action = "push" if push else "walk" if walk else "invalid"
            if (state["actor"], tuple(state["boxes"]), direction) in priors or action == "invalid":
                continue
            new_prior = (state["actor"], tuple(state["boxes"]), direction)
            priors.add(new_prior)

            new_actor = pos_add(state["actor"], direction)
            new_boxes = {pos_add(box, direction) if new_actor == box else box
                            for box in state["boxes"]} if push else state["boxes"]
            new_moves = state["moves"] + [(direction, action)]
            new_state = State(new_actor, new_boxes, new_moves)

            if new_state["boxes"] == goals:
                return new_state["moves"]

            q.enqueue(new_state)

    return []

if __name__ == '__main__':
    CLAIRE = """
    #######
    #.@ # #
    #$* $ #
    #   $ #
    # ..  #
    #  *  #
    #######
    """
    ALICE = """
    #######
    #.    #
    #$* # #
    #.  $*#
    # .$  #
    #@ *  #
    #######
    """
    SOPHIA = """
    #######
    #     #
    #@$.# #
    #*$  .#
    # $$  #
    # . . #
    #######
    """
    COMP = """
    #######
    #@   .#
    # $   # 
    #.$   #
    # $  .#
    #######
    """

    split = lambda s: [line.strip() for line in s.split('\n') if line.strip()]
    level = split(COMP)
    init_state, init_goals, init_walls = reader(level)

    print("Starting search...")
    solution = sokoban(init_state, init_goals, init_walls)

    print("Found solution!")
    replay(init_state, init_goals, init_walls, solution)
    print(solution)
