"""
Utility functions for the sokoban algorithm
"""

State = lambda actor, boxes, moves: {"actor": actor, "boxes": boxes, "moves": moves}

def pos_add(pos: tuple[int, int], direction: str) -> tuple[int, int]:
    VEC = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
    return tuple(sum(x) for x in zip(pos, VEC[direction])) # type: ignore

def valid(state, direction, walls) -> tuple[bool, bool]:
    new_actor = pos_add(state["actor"], direction)

    if new_actor in walls:
        return False, False

    if new_actor in state["boxes"]:
        new_box = pos_add(new_actor, direction)
        if new_box not in walls:
            return True, True
        return False, False

    return True, False
