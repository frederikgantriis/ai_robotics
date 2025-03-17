"""
A Sokoban algorithm solver. 
Reads a textual map and outputs a list of coordinates and move types the actor should perform.
Origon (0,0) will always be at the bottom left.
This algorithm is extremely naive 

<<< Input
######
#@# *#
# $ .#
######

>>> Output
[
((0,0), walk)
((1,0), push)
((2,0), push)

l
d
r
u

]
===
"""


type pos = tuple[int, int]
type move = tuple[pos, str] # walk | push
type moves = list[move]

type walls = set[pos]
type goals = set[pos]
type boxes = set[pos]

# Example state: { actor = (1,0), boxes = {(2,0)}, moves = [((0,0), walk), ((1,0), push)] }
# Callable[[pos, list[pos], list[tuple[pos, move]]], dict]
# (actor, boxes, moves) -> state
type State = dict[str, pos|boxes|moves]
state = lambda a, b, m: dict(actor=a, boxes=b, moves=m)


def reader(str, mapping=TILES) -> tuple[State, walls, goals]:
    
