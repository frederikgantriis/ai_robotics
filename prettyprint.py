"""
Silly pretty printing of sokoban algorithm
"""
from constants import TILES
from utils import pos_add, State

def pretty_print(state: dict, _goals: set, _walls: set, *, animate: bool = False):
    """
    Arguments:
        state: The dictionary of the state to print <br> \
        {actor: (int, int), boxes: set((int, int)), ...}

        _goals: The set of coordinates for all goals <br> \
        set((int, int), (int, int), ...)

        _walls: The set of coordinates for all walls <br> \
        set((int, int), (int, int), ...)
        *:
        animate: Boolean, whether to perform a carriage return so the print can be overwritten
    """
    REV = { val : key for key, val in TILES.items() }
    _actor = state["actor"]
    actor = {_actor : REV["actor"] if _actor not in _goals else REV["actor on goal"]}
    boxes = { pos : REV["box"] if pos not in _goals else REV["box on goal"]
                for pos in state["boxes"] }
    goals = { pos : REV["goal"]
                for pos in _goals
                if pos not in boxes and pos not in actor}
    walls = { pos : REV["wall"] for pos in _walls }

    level = actor | boxes | goals | walls

    rows, cols = max(level.keys())
    floor = {
        (row, col) : REV["floor"]
        for row in range(rows)
        for col in range(cols)
        if (row, col) not in level.keys()
    }
    level |= floor
    sor = [val for _, val in sorted(level.items(), key = lambda x: x[0])]

    if animate:
        pp = [''.join(sor[row*(cols+1):row*cols+cols+row+1]) for row in range(rows+1)]
        print('\n'.join(pp))
        print(f"\033[{rows+1}A", end="")
    else:
        for row in range(rows+1):
            p = sor[row*(cols+1):row*cols+cols+row+1]
            print(''.join(p))


def replay(
        state: dict,
        goals: set[tuple[int, int]],
        walls: set[tuple[int, int]],
        moves: list[tuple[str, str]]
    ):
    """
    Arguments:
        state: Initial state for the replay <br> \
        { actor: (int, int), boxes: set((int, int), ...), ... }

        goals: Set of coordinates for all goals

        walls: Set of coordinates for all walls

        moves: List of all moves to replay <br> \
        list( (direction, action), (direction, action), ... )

    'direction' is a string of (left, right, up, down) <br>
    'action' is a string of (walk, push)

    Example:
        >>>> state = { actor: (1,1), boxes = {(2,1), (3,1)} }
        >>>
    """
    def delay():
        _ = 1
        for i in range(1, 25000): # ~0.2 second delay
            _ *= i

    actor = state["actor"]
    boxes = state["boxes"]

    print("="*13)
    for direction, action in moves:
        push = action == "push"
        actor = pos_add(state["actor"], direction)
        boxes = {pos_add(box, direction) if actor == box else box for box in state["boxes"]} \
                    if push else state["boxes"]
        state = State(actor, boxes, [])

        pretty_print(state, goals, walls, animate = True)
        delay() # sleep(0.2)

    pretty_print(state, goals, walls)
    print("="*13)
