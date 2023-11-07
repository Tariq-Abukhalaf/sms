import serial
import re
import time
from decorator import time_it

class SIM800L:
    def __init__(self, serial_port, baud_rate):
        self.serial = serial.Serial(serial_port, baud_rate, timeout=1)
        self._buffer = ""

    def clear_serial(self):
        self.serial.flushInput()
        self.serial.flushOutput()

    def close(self):
        self.serial.close()

    def read_serial(self):
        while not self.serial.in_waiting:
            time.sleep(0.04)

        if self.serial.in_waiting:
            return self.serial.read(self.serial.in_waiting).decode('utf-8')
        return ""
    
    def read_serial_timeout(self,timeout):
        start_time = time.time()
        while not self.serial.in_waiting and time.time() - start_time < timeout:
            time.sleep(0.04)
        if self.serial.in_waiting:
            return self.serial.read(self.serial.in_waiting).decode('utf-8')
        return ""

    @time_it
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
                return round((signal_strength/31)*100,2)
            return -1
        return -1
    
    @time_it
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
    
    @time_it
    def device_information(self):
        """
            AT command to get device information
            ex: SIM800 R14.18
        """
        self.clear_serial()
        self.serial.write(b'ATI\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer      = serial_buffer.replace('ATI', '')
            serial_buffer      = serial_buffer.replace('OK', '')
            device_information = serial_buffer
            return device_information.strip().upper()
        return -1
    
    @time_it
    def modem_name(self):
        """
            ex: SIM800
        """
        modem_name = self.device_information()
        parts = modem_name.split(' ')
        return parts[0].upper()

    @time_it
    def sim_status(self):
        """
            AT command for SIM presence and status
            ex: READY
        """
        self.clear_serial()
        self.serial.write(b'AT+CPIN?\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer   = serial_buffer.replace('AT+CPIN?', '')
            serial_buffer   = serial_buffer.replace('OK', '')
            serial_buffer   = serial_buffer.replace('+CPIN: ', '')
            sim_status      = serial_buffer
            return sim_status.strip().upper()
        return -1
    
    @time_it
    def sim_response(self):
        """
            AT command for check communication between the module and the computer.
            ex: OK
        """
        self.clear_serial()
        self.serial.write(b'AT\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer = serial_buffer.replace('AT', '')
            sim_response  = serial_buffer
            return sim_response.strip().upper()
        return -1
    
    @time_it
    def imsi(self):
        """
            AT command returns IMSI (International Mobile Subscriber Identity) of the mobile terminal.
            ex: 416770126242644
        """
        self.clear_serial()
        self.serial.write(b'AT+CIMI\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            serial_buffer  = serial_buffer.replace('AT+CIMI', '')
            serial_buffer  = serial_buffer.replace('OK', '')
            imsi           = serial_buffer
            return imsi.strip()
        return -1
    
    @time_it
    def mcc_mnc_digit(self,mcn_digit=2):
        """
            The first 3 digits of the IMSI represent the MCC (Mobile Country Code).
            The next 2 or 3 digits represent the MNC (Mobile Network Code).
            ex: 416 77 
        """
        mcc_mnc_2digit = self.imsi()
        mcc = mcc_mnc_2digit[0:3]
        mnc = mcc_mnc_2digit[3:3+mcn_digit]
        return mcc, mnc
    
    @time_it
    def service_provider(self):
        """
            AT command is used to get the service provider name from the SIM.
            ex: Orange JO 
        """
        self.clear_serial()
        self.serial.write(b'AT+CSPN?\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            match = re.search(r'\+CSPN: "([^"]+)"', serial_buffer)
            if match:
                service_provider = match.group(1)
                return service_provider.upper()
            return -1
        return -1
    
    @time_it
    def network(self):
        """
            AT command is used to Check the current network
            ex: MOBILECOM
        """
        self.clear_serial()
        self.serial.write(b'AT+COPS?\r\n')
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            match = re.search(r'\+COPS: (\d+),(\d+),"(.+)"', serial_buffer)
            if match:
                network = match.group(3)
                return network.upper()
            return -1
        return -1


    def read_sms(self,id):
        """
            AT command is used to get msg by index id
            ex: 
        """
        self.clear_serial()
        self.serial.write(b'AT+CMGR=16\r\n')
        serial_buffer = self.read_serial()
        print(serial_buffer)
        # if 'OK' in serial_buffer:
        #     match = re.search(r'\+COPS: (\d+),(\d+),"(.+)"', serial_buffer)
        #     if match:
        #         network = match.group(3)
        #         return network.upper()
        #     return -1
        # return -1

        # result = self.command('AT+CMGR={}\n'.format(id),99)
        # if result:
        #     params=result.split(',')
        #     if not params[0] == '':
        #         params2 = params[0].split(':')
        #         if params2[0]=='+CMGR':
        #             number = params[1].replace('"',' ').strip()
        #             date   = params[3].replace('"',' ').strip()
        #             time   = params[4].replace('"',' ').strip()
        #             return  [number,date,time,self.savbuf]
        # return None    




    
    def read_all_sms(self):
            """
                AT command is used to read all sms sent by others to this chip
                ex: 
            """
            self.clear_serial()
            self.serial.write(b'AT+CMGF=1\r\n')
            serial_buffer = self.read_serial()
            if 'OK' in serial_buffer:
                self.clear_serial()
                self.serial.write(b'AT+CMGL="ALL"\r\n')
                serial_buffer = self.read_serial()
                print(serial_buffer)


            # self.serial.write(b'AT+CMGL=\"ALL\"')
            # print(serial_buffer)

    def list(self, onlyUnread=False):
        if onlyUnread:
            self.serial.write(b'AT+CMGL="REC UNREAD",1\r')
        else:
            self.serial.write(b'AT+CMGL="ALL",1\r')

        time.sleep(30)

        return_data = ""

        if "ERROR" in self._buffer:
            return_data = "ERROR"
        else:
            if "+CMGL:" in self._buffer:
                data = self._buffer
                quit_loop = False
                return_data = ""
                while not quit_loop:
                    if "+CMGL:" not in data:
                        quit_loop = True
                        continue
                    data = data[data.index("+CMGL: ") + 7:]
                    metin = data[:data.index(",")].strip()

                    if return_data == "":
                        return_data += "SMSIndexNo:" + metin
                    else:
                        return_data += "," + metin
            else:
                return_data = "NO_SMS"

        return return_data


sim800 = SIM800L('/dev/serial0', 115000) 

signal_strength = sim800.signal_strength()
print(f'Signal Strength: {signal_strength}')
iccid = sim800.iccid()
print(f'ICCID: {iccid}')
device_information = sim800.device_information()
print(f'Device Information: {device_information}')
modem_name = sim800.modem_name()
print(f'Modem Name: {modem_name}')
sim_status = sim800.sim_status()
print(f'Sim Status: {sim_status}')
sim_response = sim800.sim_response()
print(f'Sim Response: {sim_response}')
imsi = sim800.imsi()
print(f'IMSI: {imsi}')
mcc,mnc = sim800.mcc_mnc_digit()
print(f'MCC: {mcc}')
print(f'MNC: {mnc}')
service_provider = sim800.service_provider()
print(f'Service Provider: {service_provider}')
network = sim800.network()
print(f'Network : {network}')

test = sim800.read_sms(16)
print(test)

sim800.close()



