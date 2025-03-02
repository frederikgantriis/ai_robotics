from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop, Axis
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch, multitask, vector, run_task
from urandom import choice
from umath import pi, radians
from music import mii_music, imperial_march
from constants import CENTER, RIGHT, LEFT

hub = PrimeHub()

# Initialize Motors from wheels
right = Motor(Port.F)
left = Motor(Port.E, positive_direction=Direction.COUNTERCLOCKWISE)
s_dr = ColorSensor(Port.B)
s_dl = ColorSensor(Port.A)
s_f = ColorSensor(Port.C)


axle_track = 132.89

# Initialize Drivetrain with left, right, wheel diameter and distance between wheels
base = DriveBase(left_motor=left, right_motor=right, wheel_diameter=56.5, axle_track=132.89)

# Quick PID Controller
base.use_gyro(True)

#TODO: Play music async
hub.speaker.volume(20)
#hub.speaker.play_notes(imperial_march)

#TODO: Use IMU to check if the robot is stopping

def run_robot():
    while True:
        base.drive(200,0)

        if s_dl.reflection() < 10 or s_dr.reflection() < 10 or s_f.reflection() > 0:
            base.stop()

            #wait(200)

            if s_dl.reflection() < 10 and s_dr.reflection() < 10:
                print(f"left-sensor is over the edge: {s_dl.reflection()}")
                print(f"right-sensor is over the edge: {s_dr.reflection()} \n")
                base.straight(-70)
                base.turn(choice([90, -90]), wait=True)

            while s_dr.reflection() < 10:
                print(f"right-sensor is over the edge: {s_dr.reflection()} \n")
                base.straight(-70)
                base.turn(-90, wait=True)
                continue

            while s_dl.reflection() < 10:
                print(f"left-sensor is over the edge: {s_dl.reflection()} \n")
                base.straight(-70)
                base.turn(90, wait=True)
                continue
            
            if s_f.reflection() > 0:
                print(f"forward-sensor is close to something: {s_f.reflection()}")
                base.straight(-100)
                base.turn(choice([90, -90]))

def navigate_maze():
    print("STARTING")
    
    while True:
        base.drive(200,0)

        if (s_dr.reflection() > 20 and s_dl.reflection() > 20) or s_f.reflection() > 0:
            base.stop()

            while s_dr.reflection() > 20 or s_f.reflection() > 0:
                base.turn(20)

        while s_dr.reflection() > 20:
            if s_dl.reflection() > 20:
                break

            base.drive(200, -30)

        while s_dl.reflection() > 20:
            if s_dr.reflection() > 20:
                break

            base.drive(200, 30)
        

navigate_maze()

