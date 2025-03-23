"""
Silly pretty printing of sokoban algorithm
"""
from constants import TILES
from utils import pos_add, State

def pretty_print(state: dict, _goals: set, _walls: set, *, animate: bool = False):
    REV = { val : key for key, val in TILES.items() }
    _actor = state["actor"]
    actor = {_actor : REV["actor"] if _actor not in _goals else REV["actor on goal"]}
    boxes = { pos : REV["box"] if pos not in _goals else REV["box on goal"] for pos in state["boxes"] }
    goals = { pos : REV["goal"] for pos in _goals if pos not in boxes.keys() and pos not in actor.keys()}
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
    sor = [val for _, val in sorted([(pos, val) for pos, val in level.items()], key = lambda x: x[0])]

    if animate:
        pp = [''.join(sor[row*(cols+1):row*cols+cols+row+1]) for row in range(rows+1)]
        print('\n'.join(pp))
        print(f"\033[{rows+1}A", end="")
    else:
        for row in range(rows+1):
            p = sor[row*(cols+1):row*cols+cols+row+1]
            print(''.join(p))


def replay(state, goals, walls, moves):
    def delay():
        _ = 1
        for i in range(1, 25000): # ~0.2 second delay
            _ *= i

    actor = state["actor"]
    boxes = state["boxes"]

    print("="*13)
    for dir, action in moves:
        push = action == "push"
        actor = pos_add(state["actor"], dir)
        boxes = {pos_add(box, dir) if actor == box else box for box in state["boxes"]} if push else state["boxes"]
        state = State(actor, boxes, [])

        pretty_print(state, goals, walls, animate = True)
        delay() # sleep(0.2)

    pretty_print(state, goals, walls)
    print("="*13)
