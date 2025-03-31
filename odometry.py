from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.geometry import Matrix, 
from urandom import choice
from constants import SPEED
from sokoban import sokoban, reader
from umath import cos, sin

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



# Constants: Robot physical parameters (fixed)
DT = 0.1  # Time step for odometry updates (seconds)
D = 5.25 # Wheel diameter
R = D/2 # Wheel radius
L = 132.89 / 10 / 2 # Length from robot origin to wheels (mm -> cm)


# dynamic variables
x, y, theta = 0.0, 0.0, 0.0  # Position (in meters) and orientation (in radians)


def get_wheel_velocities(motor):
    """Get wheel angular velocities in radians per second."""
    # use motor.speed() to return the current angular velocity of the motor in degrees per second
    return motor.speed() / 2

def update_odometry():
    """Update the robot's position using kinematic equations."""
    global x, y, theta

    phi_r = get_wheel_velocities(right)
    phi_l = get_wheel_velocities(left)

    _theta = R * phi_r / (2 * L) - R * phi_l / (2 * L)


    x += R/2 * (phi_r + phi_l) * cos(_theta) * DT
    y += R/2 * (phi_r + phi_l) * sin(_theta) * DT 
    theta += R/(2*L) * (phi_r + phi_l) * DT



def move_robot(left_speed, right_speed, duration):
    """Move the robot with given wheel speeds for a given duration and do odometry."""
    left.run(left_speed)
    right.run(right_speed)

    for _ in range(int(duration / DT)):
        update_odometry()
        # print of you want:
        # print(x,y,degrees(theta))
        wait(int(DT * 1000))  # Convert seconds to milliseconds

    left.stop()
    right.stop()


# Example movement sequence:
# move forward for n sec
move_robot(...)
# turn in place for m sec
move_robot(...)
# move forward for k seconds
move_robot(...)
print("Final Position:", x, y, degrees(theta))
