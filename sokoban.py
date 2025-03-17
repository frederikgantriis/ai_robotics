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
("D", walk)
("R", push)
("R", push)
]
===
"""
from constants import TILES, L, R, F, B


type pos = tuple[int, int]
type move = tuple[int, str] # L | R | F | B, walk | push
type moves = list[move]

type walls = set[pos]
type goals = set[pos]
type boxes = set[pos]

# Example state: { actor = (1,0), boxes = {(2,0)}, moves = [((0,0), walk), ((1,0), push)] }
# Callable[[pos, list[pos], list[tuple[pos, move]]], dict]
# (actor, boxes, moves) -> state
type State = dict[str, pos|boxes|moves]
state = lambda a, b, m: dict(actor=a, boxes=b, moves=m)


def play(s: State, ws: walls, gs: goals) -> moves:

    if s["boxes"] == gs: # All boxes are on goals
        return s["moves"]


    return [
        (F, "push"),
        (L, "walk")
    ]


def reader(map: list[str], *, mapping: dict[str, str] = TILES) -> tuple[State, walls, goals]:

    ws: walls = set()
    bs: boxes = set()
    gs: goals = set()
    actor: None|pos = None

    for rowidx, row in enumerate(map):
        for colidx, tile in enumerate(row):
            curr = (rowidx, colidx)
            t = mapping.get(tile, "")

            if t == "wall": 
                ws.add(curr)
            elif t == "floor": 
                pass
            elif t == "box": 
                bs.add(curr)
            elif t == "goal": 
                gs.add(curr)
            elif t == "actor": 
                actor = curr
            elif t == "box on goal": 
                gs.add(curr)
                bs.add(curr)
            else: 
                print(f"Unknown {tile = }")


    print(actor)
    return state(actor, bs, []), ws, gs


if __name__ == "__main__":
    n = int(input())
    m= []
    for _ in range(n):
        m.append(input())

    print(reader(m))
    play(*reader(m))


