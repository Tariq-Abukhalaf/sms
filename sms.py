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
            ex:0.97
        """
        self.clear_serial()
        self.serial.write(b'AT+CSQ\r\n')
        serial_buffer = self.read_serial()
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
            ex: 8996277010560617686f
        """
        self.clear_serial()
        self.serial.write(b'AT+CCID\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer = serial_buffer.replace('AT+CCID', '')
            serial_buffer = serial_buffer.replace('OK', '')
            iccid         = serial_buffer
            return iccid.strip()
        return -1
    
    def device_information(self):
        """
            AT commands to get device information
            ex: SIM800 R14.18
        """
        self.clear_serial()
        self.serial.write(b'ATI\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer      = serial_buffer.replace('ATI', '')
            serial_buffer      = serial_buffer.replace('OK', '')
            device_information = serial_buffer
            return device_information.strip()
        return -1
    
    def sim_status(self):
        """
            AT commands for SIM presence and status
            ex: READY
        """
        self.clear_serial()
        self.serial.write(b'AT+CPIN?\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer      = serial_buffer.replace('AT+CPIN?', '')
            serial_buffer      = serial_buffer.replace('OK', '')
            serial_buffer      = serial_buffer.replace('+CPIN: ', '')
            sim_status         = serial_buffer
            return sim_status.strip()
        return -1
    
    def sim_response(self):
        """
            AT commands for check communication between the module and the computer.
            ex: READY
        """
        self.clear_serial()
        self.serial.write(b'AT\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer      = serial_buffer.replace('AT', '')
            sim_status         = serial_buffer
            return sim_status.strip()
        return -1
        



# print('***',end='\n')
# print(serial_buffer,end='\n')
# print('***',end='\n')

sim800 = SIM800L('/dev/serial0', 115000) 

signal_strength = sim800.signal_strength()
print(f'Signal Strength: {signal_strength}')

iccid = sim800.iccid()
print(f'ICCID: {iccid}')

device_information = sim800.device_information()
print(f'Device Information: {device_information}')

sim_status = sim800.sim_status()
print(f'Sim Status: {sim_status}')

sim_response = sim800.sim_response()
print(f'Sim Response: {sim_response}')

sim800.close()
