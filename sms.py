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
        while not self.serial.in_waiting:
            time.sleep(0.01)
        if self.serial.in_waiting:
            return self.serial.read(self.serial.in_waiting).decode('utf-8')
        return ""
    
    def read_serial_timeout(self,timeout):
        start_time = time.time()
        while not self.serial.in_waiting and time.time() - start_time < timeout:
            time.sleep(0.01)
        if self.serial.in_waiting:
            return self.serial.read(self.serial.in_waiting).decode('utf-8')
        return ""

    def signal_strength(self):
        """
            AT command returns the signal strength of the device.
            <min>: 2
            <max>: 31
            return ratio of 100%  
        """
        self.clear_serial()
        self.serial.write(b'AT+CSQ\r\n')
        serial_buffer = self.read_serial()
        print(serial_buffer,end='\n')
        if 'OK' in serial_buffer:
            match = re.search(r'\+CSQ: (\d+),', serial_buffer)
            if match:
                signal_strength = int(match.group(1))
                return round(signal_strength/31,2)
            return -1
        return -1
    
    def iccid(self):
        """
            AT command is used to read the ICCID from the SIM.
        """
        self.clear_serial()
        self.serial.write(b'AT+CCID\r\n')
        serial_buffer = self.read_serial()
        print('***',end='\n')
        print(serial_buffer,end='\n')
        print('***',end='\n')
        if 'OK' in serial_buffer:
            serial_buffer.replace('AT+CCID', '')
            serial_buffer.replace('OK', '')
            match = re.search(r'(\w+)', serial_buffer)
            if match:
                iccid = int(match.group(0))
                return iccid
            return -1
        return -1
        


sim800 = SIM800L('/dev/serial0', 115000) 

signal_strength = sim800.signal_strength()
print(f'Signal Strength: {signal_strength}')

iccid = sim800.iccid()
print(f'iccid: {iccid}')

sim800.close()
