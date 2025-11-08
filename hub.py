from pybricks.hubs import MoveHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = MoveHub()

sensor = ColorDistanceSensor(Port.C) # change this to Port.D if you plugged it in there.

O = Color.YELLOW
I = Color.RED
delay = 300 # milliseconds

bits = []
counter = 0

while True:
    bit = sensor.color()
    if bit in [O, I]:
        counter = 0
        if bit == O:
            bits.append(0)
        else:
            bits.append(1)
        wait(delay)
    else:
        counter += 1
    if counter >= 1000 and bits != []:
        counter = 0
        print(''.join(str(b) for b in bits) + '#')
        bits.clear()