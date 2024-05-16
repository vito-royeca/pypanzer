from gpiozero import Motor
from time import sleep
from pyPS4Controller.controller import Controller
    
class Panzer:
    def __init__(self):
        self.rightMotor = Motor(4, 17)
        self.leftMotor = Motor(27, 22)
        self.stop()

    # def forward(self, value):
    #     self.stop()
    #     self.rightMotor.forward(value)
    #     self.leftMotor.forward(value)
    
    # def backward(self, value):
    #     self.stop()
    #     self.rightMotor.backward(value)
    #     self.leftMotor.backward(value)

    # def turn_right(self, value):
    #     self.stop()
    #     self.rightMotor.forward(value)

    # def turn_left(self, value):
    #     self.stop()
    #     self.leftMotor.forward(value)

    def stop(self):
        self.rightMotor.stop()
        self.leftMotor.stop()

    def move_left(self, value):
        if value > 0:
            self.leftMotor.forward(value)
        elif value < 0:
            self.leftMotor.backward(value)
        else:
            self.leftMotor.stop()

    def move_right(self, value):
        if value > 0:
            self.rightMotor.forward(value)
        elif value < 0:
            self.rightMotor.backward(value)
        else:
            self.rightMotor.stop()

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

    # def on_R2_press(self, value):
    #     value = transf(value)
    #     self.panzer.forward(value)

    # def on_R2_release(self):
    #     self.panzer.stop()

    def on_L3_up(self, value):
        value = transf(value)
        self.panzer.move_left(value)

    def on_L3_down(self, value):
        value = transf(value)
        self.panzer.move_left(value)
    
    def on_L3_x_at_rest(self):
        self.panzer.stop()

    def on_L3_y_at_rest(self):
        self.panzer.stop()

    def on_R3_up(self, value):
        value = transf(value)
        self.panzer.move_right(value)

    def on_R3_down(self, value):
        value = transf(value)
        self.panzer.move_right(value)

    def on_R3_x_at_rest(self):
        self.panzer.stop()

    def on_R3_y_at_rest(self):
        self.panzer.stop()

    # def on_L3_down(self, value):
    #     # 'value' becomes 0 or a float between -1.0 and -0.3
    #     value = -transf(value)
    #     print(f"on_L3_down: {value}")
    #     self.panzer.backward(-value)
    
    # def on_L3_right(self, value):
    #     value = transf(value)
    #     print(f"on_L3_right: {value}")
    #     self.panzer.turn_right(value)
    
    # def on_L3_left(self, value):
    #     value = transf(value)
    #     print(f"on_L3_left: {value}")
    #     self.panzer.turn_left(value)
    
    # def on_L3_x_at_rest(self):
    #     print(f"on_L3_x_at_rest")
    #     self.panzer.stop()

    # def on_L3_y_at_rest(self):
    #     print(f"on_L3_y_at_rest")
    #     self.panzer.stop()

    # Press OPTIONS (=START) to stop and exit
    def on_playstation_button_press(self):
        exit(1)

controller = PS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)