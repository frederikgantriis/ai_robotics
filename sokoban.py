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
from constants import TILES, L, R, U, D, DIR
from kueue import Queue

#TILES = {"#": "wall", "@": "actor", "$": "box", ".": "goal", "*": "box on goal", " ": "floor"}

def parse_map(sokoban_map):
    return [list(row) for row in sokoban_map.strip().split("\n")]

def find_actor(state):
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell == "@" or cell == "+":
                return (x, y)

def find_boxes(state):
    return {(x, y) for y, row in enumerate(state) for x, cell in enumerate(row) if cell in {"$", "*"}}

def find_goals(state):
    return {(x, y) for y, row in enumerate(state) for x, cell in enumerate(row) if cell in {".", "*"}}

def is_valid(state, x, y):
    return 0 <= y < len(state) and 0 <= x < len(state[0]) and state[y][x] != "#"

def move(state, x, y, dx, dy):
    new_x, new_y = x + dx, y + dy
    if not is_valid(state, new_x, new_y):
        return None  # Can't move into walls
    
    new_state = [row[:] for row in state]
    goals = find_goals(state)  # Track goal positions
    
    cell = state[new_y][new_x]
    if cell in {"$", "*"}:  # Box present
        box_new_x, box_new_y = new_x + dx, new_y + dy
        if not is_valid(state, box_new_x, box_new_y) or state[box_new_y][box_new_x] in {"$", "*"}:
            return None  # Box is blocked
        
        # Move box to new position
        new_state[box_new_y][box_new_x] = "$" if (box_new_x, box_new_y) not in goals else "*"
        new_state[new_y][new_x] = "@" if (new_x, new_y) not in goals else "+"  # Move actor
        
        # Restore previous position, ensuring goals are maintained
        new_state[y][x] = "." if (x, y) in goals else " "
        if state[new_y][new_x] == "*":  # If the box was on a goal
            new_state[new_y][new_x] = "."  # Restore the goal
    else:
        new_state[new_y][new_x] = "@" if (new_x, new_y) not in goals else "+"  # Move actor
        
        # Restore previous position
        new_state[y][x] = "." if (x, y) in goals else " "
    
    return new_state, ("push" if cell in {"$", "*"} else "walk"), (x + dx, y + dy)

def is_solved(state):
    goals = find_goals(state)
    boxes = find_boxes(state)
    return boxes == goals  # Ensure every goal has a box

def bfs_solve(initial_state):
    moves = [(0, -1, "up"), (0, 1, "down"), (-1, 0, "left"), (1, 0, "right")]
    queue = Queue()
    queue.enqueue((initial_state, find_actor(initial_state), []))
    print(queue)
    visited = set()
    
    while not queue.is_empty():
        state, (x, y), path = queue.dequeue()
        state_tuple = tuple(map(tuple, state))
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        
        if is_solved(state):
            return path
        
        for dx, dy, direction in moves:
            result = move(state, x, y, dx, dy)
            print(result)
            if result:
                new_state, action, new_pos = result
                queue.enqueue((new_state, new_pos, path + [(direction, action)]))
    
    return None  # No solution

# Example usage
breaks = """
#####
#   #
# $ #
# *+#
#####
"""
also_breaks = """
#####
#.  #
# $ #
# *@#
#####
"""
sokoban_map = """
#####
#@  #
# $ #
# *.#
#####
"""
state = parse_map(sokoban_map)
solution = bfs_solve(state)
print(solution)

