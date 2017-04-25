# coding=utf-8
import math
import threading
import time

from robot.hardware.bluetooth_decoder import BluetoothDecoder
from serial_wrapper import SerialWrapper, SERIAL_LOCK
from servos_wrapper import ServosWrapper

SERIAL = SerialWrapper()
SERVOS = ServosWrapper()

BT = BluetoothDecoder()


class WheelController:
    """ Class to control the movements of the bot.
        TODO: Add possibility of multiple commands to be called at once.
            Example: call to rotate while bot if moving foward. curently: must
            wait for methods to return.
    """
    wheel_diameter = 0.07  # m = 7cm
    wheel_circumference = math.pi * 0.07  # m
    # rotation_circumference = 0.701430 #m
    rotation_circumference = 0.71
    minFreqMesure = 130
    maxFreqMesure = 2400
    sensorFrequencyConstant = 1600
    tuning_const_A = 1
    tuning_const_B = 1
    tuning_const_C = 1.1
    tuning_const_D = 1
    time_tuning_const = 3
    rotate_const = 1

    def rotate(self, degree, speed):
        """ Use to rotate the orientation of the bot.
            +90 degrees will make the bot turn left on itself. The speed
            is in degrees per seconds (omega).
            :param degree:
            :param speed:
        """
        wheelSpeed = self.rotation_circumference * speed / (360 * math.cos(math.pi / 8))
        freq = self._pulse_freq(wheelSpeed)
        if freq > self.maxFreqMesure:
            raise Exception('Wheel speed is too fast')
        SERIAL_LOCK.acquire(True)
        if degree < 0:
            SERIAL.send('@%s,%s,%s,%s,' % (int(self.tuning_const_A * freq),
                                           int(self.tuning_const_B * freq),
                                           int(self.tuning_const_C * freq),
                                           int(self.tuning_const_D * freq)))
        else:
            SERIAL.send('@%s,%s,%s,%s,' % (-int(self.tuning_const_A * freq),
                                           -int(self.tuning_const_B * freq),
                                           -int(self.tuning_const_C * freq),
                                           -int(self.tuning_const_D * freq)))
        time.sleep(self.rotate_const + abs(degree) / speed)
        self.stop()
        time.sleep(0.2)
        SERIAL_LOCK.release()
        return 'ok'

    def _pulse_freq(self, speed):
        return int(self.sensorFrequencyConstant * speed / self.wheel_circumference)

    def move_forward(self, distance, speed):
        return self.move_lateral_cart(0, distance, speed)

    def move_lateral_polar(self, orientation, distance, speed):
        """ Use to move laterally in a given "orientation" in degrees.
            The bot will keep facing in the same direction, while moving
            sideways or in a given direction. Angle is calculated from
            the front of the bot. (foward is 0 degree, backward is 180 degree.)
        """
        orientation = (orientation + 180) % 360
        distance_x = distance * math.sin(math.radians(orientation))
        distance_y = distance * math.cos(math.radians(orientation))
        return self.move_lateral_cart(distance_x, distance_y, speed)

    def move_lateral_cart(self, distance_x, distance_y, speed):
        """ Use to move laterally in given X and Y directions.
            The bot will keep facing in the same direction, while moving
            sideways or in a given direction. X moves sideways, Y moves foward and backward.
            Speed is the bot's total movement speed.
        """
        distance_t = math.sqrt(distance_x ** 2 + distance_y ** 2)
        speed_x = speed * distance_x / distance_t
        speed_y = speed * distance_y / distance_t
        val_a = int(self._pulse_freq(speed_y) * self.tuning_const_A)
        val_b = int(self._pulse_freq(speed_x) * self.tuning_const_B)
        val_c = int(-self._pulse_freq(speed_y) * self.tuning_const_C)
        val_d = int(-self._pulse_freq(speed_x) * self.tuning_const_D)
        if any(i > self.maxFreqMesure for i in [val_a, val_b, val_c, val_d]):
            raise Exception('Wheel speed is too fast')
        SERIAL_LOCK.acquire(True)
        SERIAL.send("@%s,%s,%s,%s," % (val_a, val_b, val_c, val_d))
        time.sleep(self.time_tuning_const * distance_t / speed)
        self.stop()
        time.sleep(0.1)
        SERIAL_LOCK.release()
        return 'ok'

    def stop(self):
        """ Use to stop the bot abruptly in case of emergency.
        """
        SERIAL.send("@0,0,0,0,")


# remap a value, given a min and max, to another range, given new min and max
# ex: remap(3, 0, 10, 0, 100) will return 30
remap = lambda val, vn, mx, omn, omx: omn + (omx - omn) * (val - vn) / (mx - vn)


class CameraController:
    """ Class to control the orientation of the camera support.
    """
    hlimits = (1664, 10048)
    vlimits = (2624, 7744)

    def __init__(self):
        SERVOS.set_limits(1, self.vlimits[0], self.vlimits[1])
        SERVOS.set_limits(2, self.hlimits[0], self.hlimits[1])

    def reset_orientation(self):
        self.set_orientation(0, 0)

    def set_orientation(self, verticalAngle, horizontalAngle):
        """ Use to face both orientations at the same time.
            Angles are given between +- 90 degrees.
        """
        v = self.set_vertical(verticalAngle)
        h = self.set_horizontal(horizontalAngle)
        return v, h

    def set_vertical(self, angle):
        """ Use to face in a given vertical position. Angle between -90 and +45 degrees.
        """
        angle = remap(angle, -90, 45, self.vlimits[0], self.vlimits[1])
        pos = SERVOS.set_position(1, angle)
        return remap(pos, self.vlimits[0], self.vlimits[1], -90, 45)

    def set_horizontal(self, angle):
        """ Use to face in a given horizontal position. Angle is +- 90 degrees.
        """
        angle = remap(angle, -90, 90, self.hlimits[0], self.hlimits[1])
        pos = SERVOS.set_position(2, angle)
        return remap(pos, self.hlimits[0], self.hlimits[1], -90, 90)


class PrehensorController:
    """ Class to control the electromagnet movements and activation
    """

    limits = (3000, 8500)

    def __init__(self):
        SERVOS.set_limits(3, self.limits[0], self.limits[1])

    def set_magnet(self, value):
        """ value: <boolean>
            value == true: enable the discharging of the capacitor, powering the magnet
            value == false: disable the magnet, conserves power.
            to note that either way, the capacitor can still be charged via the power station.
        """
        if SERIAL_LOCK.acquire(True):  # non-blocking acquire
            if value:
                SERIAL.send('#')
            else:
                SERIAL.send('&')
            SERIAL_LOCK.release()

    def set_up_down(self, value):
        """ value: <string>
            value == 'up': sets the prehensor up
            value == 'down': sets the prehensor down, it then touches the ground.
        """
        if value == 'up':
            pos = self.limits[1]
        elif value == 'down':
            pos = self.limits[0]
        else:
            raise Exception('"value" must be "up" or "down"')
        pos = SERVOS.set_position(3, pos)
        return pos

    def get_capacitor_tension(self):
        """ return the current voltage of the capacitor, with a resolution of
            5V/1024bits = 4.8 mV
        """
        SERIAL_LOCK.acquire(True)
        value = SERIAL.send_and_receive('$')
        # time.sleep(0.1)
        SERIAL_LOCK.release()
        try:
            return float(value)
        except:
            return 0
        return 0


class ManchesterCodeReceiver:
    """ Use to retrieve manchester-encoded character
    """

    def get_code(self):
        value = None
        while not value:
            try:
                value = BT.read_code()
            except:
                print("error while reading code")
                BT.open_comm()
        return value


def fire_capacitor_commands():
    pre = PrehensorController()

    for i in range(15):
        print (pre.get_capacitor_tension())
        time.sleep(0.4)


def fire_magnet_commands():
    pre = PrehensorController()
    for i in range(10):
        pre.set_up_down(pos)
        if pos == 'up':
            pos = 'down'
        else:
            pos = 'up'
        time.sleep(0.7)


def fire_manchester_commands():
    print("manchester!")
    man = ManchesterCodeReceiver()
    for i in range(10):
        print(man.get_code())
        time.sleep(0.7)


def fire_wheel_commands():
    rob = WheelController()
    for i in range(1):
        print rob.move_lateral_polar(0, 0.04, 0.1)
        print rob.move_lateral_polar(90, 0.04, 0.1)
        print rob.move_lateral_polar(180, 0.04, 0.1)
        print rob.move_lateral_polar(270, 0.04, 0.1)
        print(rob.rotate(4, 20))
        print(rob.rotate(-4, 20))


def warm_that_bitch_up():
    thread1 = threading.Thread(target=fire_capacitor_commands, args=())
    thread1.start()
    thread2 = threading.Thread(target=fire_magnet_commands, args=())
    thread2.start()
    thread3 = threading.Thread(target=fire_manchester_commands, args=())
    thread3.start()
    thread4 = threading.Thread(target=fire_wheel_commands, args=())
    thread4.start()


if __name__ == "__main__":
    warm_that_bitch_up()
