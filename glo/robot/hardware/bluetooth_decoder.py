import logging
import os
import time
from subprocess import Popen

import serial


class BluetoothDecoder():
    open_comm_tries = 0
    OPEN_COMM_MAX_TRIES = 2
    stopBits = ('0', '1', '1', '1', '1', '1', '1', '1', '1')
    logger = logging.getLogger("remote")

    def __init__(self):
        os.system("sudo hciconfig hci0 down")
        time.sleep(1)
        os.system("sudo hciconfig hci0 up")
        time.sleep(5)
        self.conn = Popen("sudo rfcomm connect 0 20:13:11:01:27:77".split(" "))
        time.sleep(10)
        os.system("sudo chmod a+wrx /dev/rfcomm0")
        self.ser = serial.Serial()
        self.ser.port = '/dev/rfcomm0'
        self.ser.baudrate = 9600
        self.ser.timeout = 0.1
        self.open_comm()

    def open_comm(self):
        if not self.ser.isOpen():
            try:
                self.ser.open()
                time.sleep(2)
            except serial.SerialException:
                self.logger.error("Could not open bluetooth serial port, retrying in 1 sec.")
                time.sleep(1)
                if self.open_comm_tries != self.OPEN_COMM_MAX_TRIES:
                    self.open_comm_tries += 1
                    return self.open_comm()
                else:
                    return

    def read_code(self):
        self.logger.info('Reading manchester code')
        self.ser.flushInput()
        self.ser.flushOutput()
        time.sleep(0.2)
        last_value = self.ser.read().decode('ascii')
        while last_value in ['\r', '\n']:
            last_value = self.ser.read().decode('ascii')
        bitTable = self.read_bites(last_value)
        finalStr = self.get_byte_from_table(bitTable)
        self.logger.info("Decoded letter: " + chr(int(finalStr, 2)))
        return chr(int(finalStr, 2))

    def read_bites(self, last_value):
        bitTable = []
        counter = 1
        bits = 0
        while bits < 32:
            new_value = self.ser.read().decode('ascii')
            if new_value != last_value and new_value not in ['\r', '\n']:
                last_value = new_value
                if counter >= 3:
                    bitTable.append(new_value)
                    bits += 1
                    counter = 0
                else:
                    counter += 1
            else:
                counter += 1
                if counter >= 10:
                    self.logger.info('Manchester BitTable : %s' % bitTable)
                    raise Exception("No manchester detected!")
        return bitTable

    def get_byte_from_table(self, bitTable):
        truncTable = bitTable[16:]
        index = self.find_stop_bits_index(truncTable)
        finalTable = []
        i = (index + 9) % 16
        while i != index:
            finalTable.insert(0, truncTable[i])
            i = (i + 1) % 16
        return ''.join(finalTable)

    def find_stop_bits_index(self, bitTable):
        for i in range(0, 16):
            matching = True
            for j in range(0, 9):
                if bitTable[(i + j) % 16] != self.stopBits[j]:
                    matching = False
            if matching: return i
        raise Exception("manchester read, but no stopbit sequence found!")
