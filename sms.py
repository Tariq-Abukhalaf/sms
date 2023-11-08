import serial
import re
import time
from decorator import time_it
import requests

class SIM800L:
    def __init__(self, serial_port, baud_rate):
        self.serial = serial.Serial(serial_port, baud_rate, timeout=0.1)

    def set_timeout(self,timeout=0.1):
        self.serial.timeout = timeout

    def clear_serial(self):
        self.serial.flushInput()
        self.serial.flushOutput()

    def close(self):
        self.serial.close()

    def read_serial(self, prompt=b'OK\r\n>'):
        return self.serial.read_until(prompt).decode('utf-8') 
        
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
        if modem_name == -1 :
            return -1
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
        if mcc_mnc_2digit == -1:
            return -1,-1
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
    
    @time_it
    def set_text_mode(self, mode):
        """
            AT command sets the GSM modem in SMS Text Mode or SMS PDU Mode.
            0 = PDU Mode
            1 = Text Mode
        """
        self.clear_serial()
        self.serial.write(f'AT+CMGF={mode}\r\n'.encode())
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
            return True
        return False
    
    @time_it
    def is_hexadecimal(self,text):
        # return True if arabic
        hex_pattern = r'^[0-9A-Fa-f]+$'
        return bool(re.match(hex_pattern, text))
    
    @time_it
    def hex_to_human_readable(self,hex_message):
        # only arabic 
        segments        = [hex_message[i:i+4] for i in range(0, len(hex_message), 4)]
        decoded_message = ''.join([chr(int(segment, 16)) for segment in segments])
        return decoded_message

    @time_it
    def read_sms(self,id):
        """
            AT command is used to get msg by index id
            ex: 
                26
                REC READ
                +962795514170
                23/11/07 14:00:58+12
                A steady diet of dog food may cause blindness in your cat - it lacks taurine.
        """
        if (sim800.set_text_mode(1)):
            self.clear_serial()
            self.serial.write(f'AT+CMGR={id}\r\n'.encode())
            serial_buffer = self.read_serial()
            if 'OK' in serial_buffer:
                serial_buffer  = serial_buffer.replace('AT+CMGR={}'.format(id), '').replace('"','').replace('+CMGR: ', '').replace('OK', '')
                parts          = serial_buffer.split('\n')
                filtered_list  = [item.replace('\r', '') for item in parts]
                filtered_list  = [item for item in filtered_list if item.strip()]
                info           = filtered_list[0].split(',')
                msg            = filtered_list[1].strip()
                if self.is_hexadecimal(msg):   
                    msg = self.hex_to_human_readable(msg)
                return id,info[0].strip(),info[1].strip(),info[3].strip()+' '+info[4].strip(),msg
            return -1,-1,-1,-1,-1
        return -1,-1,-1,-1,-1
    
    @time_it
    def list_sms_indices(self):
        """
            AT command is used to list all indices sms messages
            ex: 
                [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        """
        if (sim800.set_text_mode(1)):
            self.clear_serial()
            self.serial.write(f'AT+CMGL="ALL"\r\n'.encode())
            self.set_timeout(2)
            serial_buffer = self.read_serial()
            self.set_timeout(0.1)
            indices = re.findall(r'\+CMGL: (\d+),', serial_buffer)
            int_list = [int(index) for index in indices]
            return int_list
        return []
    
    @time_it
    def get_balance(self,ussd_code):
        """
            AT command is used to get balance
        """
        if (sim800.set_text_mode(0)):
            self.clear_serial()
            self.serial.write(f'AT+CUSD=1,"{ussd_code}",15'.encode())
            time.sleep(10)
            serial_buffer = self.serial.read().decode('utf-8') 
            print(serial_buffer)
            if 'OK' in serial_buffer:
                # serial_buffer  = serial_buffer.replace('+CUSD: 0, ','').replace('"','').replace('OK', '')
                balance = serial_buffer
                return balance
            return -1
        return -1
    
    @time_it
    def delete_sms(self,id):
        """
            AT command is used to remove sms msg
        """
        self.clear_serial()
        self.serial.write(f'AT+CMGD={id}\r\n'.encode())
        serial_buffer = self.read_serial()
        if 'OK' in serial_buffer:
           return True
        return False
    
    @time_it
    def delete_sms_all(self):
        """
            AT command is used to delete all msgs
        """
        pass

    def get_api_data(self,uri):
        # phone number: sent to 
        # msg: 
        try:
            response = requests.get(uri)
            if response.status_code == 200:
                data = response.json() 
                return data
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None

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
print('**************************************',end='\n')
index,status,phone,dt_message,message= sim800.read_sms(31)
print('Message Index:',index,end='\n')
print('Status:',status,end='\n')
print('Phone Number Sender:',phone,end='\n')
print('Timestamp:',dt_message,end='\n')
print('Message:',message,end='\n')
print('**************************************',end='\n')
list_sms_indices = sim800.list_sms_indices()
print(list_sms_indices)
print('**************************************',end='\n')

if len(list_sms_indices) != 0:
    for index in list_sms_indices:
        index,status,phone,dt_message,message= sim800.read_sms(index)
        print('Message Index:',index,end='\n')
        print('Status:',status,end='\n')
        print('Phone Number Sender:',phone,end='\n')
        print('Timestamp:',dt_message,end='\n')
        print('Message:',message,end='\n')
        print('------------------',end='\n')

sim800.delete_sms(44)

api_data = sim800.get_api_data("https://catfact.ninja/fact")
if api_data:
    print(api_data["fact"])

balance = sim800.get_balance('*155#')

sim800.close()




