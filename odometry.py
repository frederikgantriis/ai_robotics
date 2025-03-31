from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from umath import cos, sin, degrees, radians

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
D = 5.25  # Wheel diameter
R = D/2  # Wheel radius
L = 132.89 / 10 / 2  # Length from robot origin to wheels (mm -> cm)


# dynamic variables
# Position (in meters) and orientation (in radians)
x, y, theta = 0.0, 0.0, 0.0


def get_wheel_velocities(motor):
    """Get wheel angular velocities in radians per second."""
    # use motor.speed() to return the current angular velocity of the motor in degrees per second
    return radians(motor.speed())


def update_odometry():
    """Update the robot's position using kinematic equations."""
    global x, y, theta

    phi_r = get_wheel_velocities(right)
    phi_l = get_wheel_velocities(left)

    _theta = R / (2*L) * (phi_r - phi_l)


    x += R/2 * (phi_r + phi_l) * cos(theta) * DT
    y += R/2 * (phi_r + phi_l) * sin(theta) * DT 
    theta += _theta * DT


def move_robot(left_speed, right_speed, duration):
    """Move the robot with given wheel speeds
    for a given duration and do odometry."""
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
move_robot(100, 100, 2)
# turn in place for m sec
move_robot(80, 0, 3)
# move forward for k seconds
move_robot(100, 100, 2)
print("Final Position:", x, y, degrees(theta) % 360)
print(f"heading: {hub.imu.heading()}")
