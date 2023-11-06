import serial
import re
import time

class SIM800L:
    def __init__(self, serial_port, baud_rate):
        self.serial = serial.Serial(serial_port, baud_rate, timeout=1)

    def clear_serial(self):
        self.serial.flushInput()
        self.serial.flushOutput()

    def close(self):
        self.serial.close()

    def read_serial(self):
        while not self.serial.in_waiting :
            time.sleep(0.01)
        if self.serial.in_waiting:
            return self.serial.read(self.serial.in_waiting).decode('utf-8')
        return ""

    def signal_strength(self):
        self.clear_serial()
        self.serial.write(b'AT+CSQ\r\n')
        serial_buffer = self.read_serial()
        print(serial_buffer)

        # time.sleep(1)
        # print(self.serial.in_waiting)
        # serial_buffer = self.serial.read(self.serial.in_waiting).decode('utf-8')

        match = re.search(r'\+CSQ: (\d+),', serial_buffer)
        print(match)
        if match:
            signal_strength = int(match.group(1))
            return signal_strength


sim800 = SIM800L('/dev/serial0', 115000) 

signal_strength = sim800.signal_strength()
print(f'Signal Strength: {signal_strength}')

sim800.close()
