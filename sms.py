import serial
import re
import time

class SIM800L:
    def __init__(self, serial_port, baud_rate):
        self.serial = serial.Serial(serial_port, baud_rate, timeout=1)

    def clear_serial(self):
        self.serial.flushInput()
        self.serial.flushOutput()

    def signal_strength(self):
        self.clear_serial()
        self.serial.write(b'AT+CSQ\r\n')
        
        while self.serial.in_waiting > 0:
            print("Inside while")
            

        time.sleep(1)  
        serial_buffer = self.serial.read(self.serial.in_waiting).decode('utf-8')

        match = re.search(r'\+CSQ: (\d+),', serial_buffer)
        if match:
            signal_strength = int(match.group(1))
            return signal_strength


sim800 = SIM800L('/dev/serial0', 115000, 5) 

signal_strength = sim800.signal_strength()
print(f'Signal Strength: {signal_strength}')

sim800.serial.close()
