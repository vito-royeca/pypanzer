from gpiozero import Motor
from gpiozero import Servo
from gpiozero import AngularServo
from gpiozero import Device
from time import sleep
from pyPS4Controller.controller import Controller

from gpiozero.pins.pigpio import PiGPIOFactory

# Device.pin_factory = PiGPIOFactory()
factory = PiGPIOFactory()

class Panzer:
    def __init__(self):
        self.right_motor = Motor(17, 4)
        self.left_motor = Motor(22, 27)
        self.turret_base = AngularServo(12, min_angle=-180, max_angle=180, pin_factory=factory)
        self.turret_cannon = AngularServo(13, min_angle=-180, max_angle=180, pin_factory=factory)

        self.right_motor_off = False;
        self.left_motor_off = False;
        self.stop_motors()

    def forward(self, value):
        self.stop_motors()
        if not self.right_motor_off:
            self.right_motor.forward()
        if not self.left_motor_off:
            self.left_motor.forward()
    
    def backward(self, value):
        self.stop_motors()
        self.right_motor.backward(value)
        self.left_motor.backward(value)
    
    def turn_right(self):
        self.right_motor_off = False;
        self.left_motor_off = True;

    def turn_left(self):
        self.right_motor_off = True;
        self.left_motor_off = False;
    
    def turn_straight(self):
        self.right_motor_off = False;
        self.left_motor_off = False;

    def turn_turrent_base_left(self):
        angle = self.turret_base.angle - 20
        if angle > -180:
            self.turret_base.angle = angle
            sleep(1)

    def turn_turrent_base_right(self):
        angle = self.turret_base.angle + 20
        if angle < 180:
            self.turret_base.angle = angle
            sleep(1)

    def turn_turrent_cannon_up(self):
        angle = self.turret_cannon.angle - 20
        if angle > -180:
            self.turret_cannon.angle = angle
            sleep(1)

    def turn_turrent_cannon_down(self):
        angle = self.turret_cannon.angle + 20
        if angle > -180:
            self.turret_cannon.angle = angle
            sleep(1)

    def stop_motors(self):
        self.right_motor.stop()
        self.left_motor.stop()
        # self.turn_straight()

# Translate controller input into motor output values
def transf(raw):
    temp = (raw+32767)/65534
    # Filter values that are too weak for the motors to move
    if abs(temp) < 0.25:
        return 0
    # Return a value between 0.3 and 1.0
    else:
        return round(temp, 1)
    
class PS4Controller(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.panzer = Panzer()
        self.r3_x = 0
        self.r3_old_x = 0
        self.r3_y = 0
        self.r3_old_y = 0

    # move forward
    def on_R2_press(self, value):
        value = transf(value)
        self.panzer.forward(value)

    def on_R2_release(self):
        self.panzer.stop_motors()
        self.panzer.turn_straight()

    # move backward
    def on_L2_press(self, value):
        value = transf(value)
        self.panzer.backward(value)

    def on_L2_release(self):
        self.panzer.stop_motors()
        self.panzer.turn_straight()

    # steering
    def on_L3_up(self, value):
        ()
    def on_L3_down(self, value):
        ()
    def on_L3_left(self, value):
        self.panzer.turn_right()
    def on_L3_right(self, value):
        self.panzer.turn_left()
    def on_L3_x_at_rest(self):
        self.panzer.turn_straight()
    def on_L3_y_at_rest(self):
        self.panzer.turn_straight()

    # move the turret    
    def on_R3_up(self, value):
        self.r3_y = value
    def on_R3_down(self, value):
        self.r3_y = value
    def on_R3_left(self, value):
        self.r3_x = value
    def on_R3_right(self, value):
        self.r3_x = value
    def on_R3_x_at_rest(self):
        if self.r3_old_x != self.r3_x:
            self.r3_old_x = self.r3_x
            if self.r3_old_x < 0:
                # self.panzer.turn_turrent_base_left()
                print("turn_turrent_base_right")
            else:
                # self.panzer.turn_turrent_base_right()
                print("turn_turrent_base_left")
    def on_R3_y_at_rest(self):
        if self.r3_old_y != self.r3_y:
            self.r3_old_y = self.r3_y
            if self.r3_old_y < 0:
                # self.panzer.turn_turrent_cannon_down()
                print("turn_turrent_cannon_up")
            else:
                # self.panzer.turn_turrent_cannon_up()
                print("turn_turrent_cannon_down")


    # Press OPTIONS (=START) to stop and exit
    def on_playstation_button_press(self):
        exit(1)

controller = PS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)