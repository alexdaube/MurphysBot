import threading
import time

import serial

SERIAL_LOCK = threading.Lock()


class SerialWrapper():
    open_comm_tries = 0
    OPEN_COMM_MAX_TRIES = 2

    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = '/dev/arduino0'
        self.ser.timeout = 100
        self.ser.baudrate = 9600
        self.ser.timeout = 1
        self.open_comm()

    def open_comm(self):
        if not self.ser.isOpen():
            try:
                self.ser.open()
                time.sleep(2)
            except serial.SerialException:
                print ("could not open Arduino serial port, retrying in 1 sec.")
                time.sleep(1)
                if self.open_comm_tries != self.OPEN_COMM_MAX_TRIES:
                    self.open_comm_tries += 1
                    return self.open_comm()
                else:
                    return

    def close_comm(self):
        if self.ser.isOpen():
            self.ser.close()

    def send(self, command):
        self.ser.flushInput()
        while self.ser.out_waiting > 0:
            continue
        self.ser.write(command)

    def receive(self):
        value = self.ser.read(8)
        return value

    def send_and_receive(self, command):
        value = None
        self.send(command)
        value = self.ser.read(8)
        return value


remap = lambda val, vn, mx, omn, omx: omn + (omx - omn) * (val - vn) / (mx - vn)
