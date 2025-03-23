"""
Utility functions for the sokoban algorithm
"""

State = lambda actor, boxes, moves: dict(actor=actor, boxes=boxes, moves=moves)

def pos_add(pos: tuple[int, int], dir: str) -> tuple[int, int]:
    VEC = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
    return tuple(sum(x) for x in zip(pos, VEC[dir])) # type: ignore

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
