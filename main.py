from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from urandom import choice
from constants import SPEED
from sokoban import play

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


def navigate_sokoban():
    # Left sensor detects table as ~50, right detects it as ~60
    # Both sensor detects tape as ~10
    print("STARTING")

    while True:
        base.drive(SPEED, 0)
        print(f"left-sensor: {s_dl.reflection()}")
        print(f"right-sensor: {s_dr.reflection()} \n")

        ###
        # Finding a piece of tape makes sensor go below 15, initiate a turn
        ###
        # Junction found (╬, ╩, ╦), update position?
        if (TAPE(s_dr) and TAPE(s_dl)):
            print("Junction found")
            direction = choice([1, -1])
            while (TAPE(s_dr) or TAPE(s_dl)):
                base.drive(SPEED, 90*direction)

        # Right Turn found (╔, ╝, ╠)
        elif TAPE(s_dr):
            print("Right turn found")
            while TAPE(s_dr):
                base.drive(SPEED, 90)

        # Left turn found (╚, ╗, ╣)
        elif TAPE(s_dl):
            print("Left turn found")
            while TAPE(s_dl):
                base.drive(SPEED, -90)

        ###
        # Reflection starts falling below 50 means we're off-course
        # 15 < x < 50
        ###
        # We're drifting starboard (towards the right)
        elif not (TAPE(s_dl) or GROUND(s_dl)):
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


navigate_sokoban()
