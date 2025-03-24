from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from urandom import choice
from constants import SPEED
from sokoban import sokoban, reader

hub = PrimeHub()

# Initialize Motors from wheels
right = Motor(Port.F)
left = Motor(Port.E, positive_direction=Direction.COUNTERCLOCKWISE)
s_dr = ColorSensor(Port.B)
s_dl = ColorSensor(Port.A)

axle_track = 132.89

# Initialize Drivetrain with left, right, wheel diameter
# and distance between wheels
base = DriveBase(left_motor=left, right_motor=right,
                 wheel_diameter=56.5, axle_track=132.89)

# Quick PID Controller
base.use_gyro(True)

# TODO: Use IMU to check if the robot is stopping


def TAPE(x): return x.reflection() < 15
def GROUND(x): return 35 < x.reflection()

def init():
    COMP = """
    #######
    #@   .#
    # $   # 
    #.$   #
    # $  .#
    #######
    """

    COMP = """
    ####
    #@ #
    #$ #
    #. #
    ####

    """

    split = lambda s: [line.strip() for line in s.split('\n') if line.strip()]
    level = split(COMP)
    init_state, init_goals, init_walls = reader(level)
    return sokoban(init_state, init_goals, init_walls)

def junction():
    while not (TAPE(s_dl) or TAPE(s_dr)):
        if not (TAPE(s_dl) or GROUND(s_dl)):
            print("Drifting starboard")
            hub.speaker.beep(duration=50)
            base.drive(SPEED, -20)
            wait(200)

        # We're drifting port (towards the left)
        elif not (TAPE(s_dr) or GROUND(s_dr)):
            print("Drifting port")
            hub.speaker.beep(duration=50)
            base.drive(SPEED, 20)
            wait(200)

        else:
            base.drive(SPEED, 0)


def push(direction: int) -> int:
    # Go straight into a tomato can pushing it to the next junction (walk twice 0 heading)
    # Turn around and go back to previous junction (walk once +/-180 heading)

    walk(0)
    junction()
    base.drive(-SPEED, 0)
    wait(200)
    walk(180)


def walk(direction):
    # Given a heading turn to that side, if 0 continue straight ahead

    if direction > 90:
        base.turn(direction)

    while (TAPE(s_dr) or TAPE(s_dl)):
        base.drive(SPEED, direction)


def navigate_sokoban():
    # Left sensor detects table as ~50, right detects it as ~60
    # Both sensor detects tape as ~10
    print("STARTING")
    solution = init()
    heading = 0 # We always start looking "up"
    headings = {"up": 0, "right": 90, "down": 180, "left": 270}
    actions = {"walk": walk, "push": push}
    

    for direction, action in solution:
        turn = heading + (headings[direction] - heading)
        junction()
        base.drive(SPEED, 0)
        func = actions[action]
        func(turn)
        heading = headings[direction] if action == walk else (heading + 180) % 360

        #print(f"left-sensor: {s_dl.reflection()}")
        #print(f"right-sensor: {s_dr.reflection()} \n")
        ###
        # Finding a piece of tape makes sensor go below 15, initiate a turn
        ###
        # Junction found (╬, ╩, ╦), update position?
        # if (TAPE(s_dr) and TAPE(s_dl)):
        #     print("Junction found")
            #direction = choice([1, -1, 0])
            # func(heading)

            # while (TAPE(s_dr) or TAPE(s_dl)):
            #     base.drive(SPEED, 90*direction)

        # Right Turn found (╔, ╝, ╠)
        # elif TAPE(s_dr):
        #     print("Right turn found")
        #     while TAPE(s_dr): 
        #         base.drive(SPEED, 90)

        # Left turn found (╚, ╗, ╣)
        # elif TAPE(s_dl):
        #     print("Left turn found")
        #     while TAPE(s_dl):
        #         base.drive(SPEED, -90)

        ###
        # Reflection starts falling below 50 means we're off-course
        # 15 < x < 50
        ###
        # We're drifting starboard (towards the right)
        # if not (TAPE(s_dl) or GROUND(s_dl)):
        #     print("Drifting starboard")
        #     hub.speaker.beep(duration=50)
        #     base.drive(SPEED, -20)
        #     wait(200)

        # # We're drifting port (towards the left)
        # elif not (TAPE(s_dr) or GROUND(s_dr)):
        #     print("Drifting port")
        #     hub.speaker.beep(duration=50)
        #     base.drive(SPEED, 20)
        #     wait(200)

        # else:
        #     base.drive(SPEED, 0)


navigate_sokoban()
