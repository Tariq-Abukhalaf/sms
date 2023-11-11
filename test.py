import subprocess
import re

def parse_wifi_networks():
    output = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'], text=True)
    pattern = r'(?P<SSID>.+?)\s+(?P<BSSID>\S+)\s+(?P<MODE>\S+)\s+(?P<FREQ>\S+)\s+(?P<RATE>\S+)\s+(?P<SIGNAL>\S+)\s+(?P<SECURITY>.+)$'
    wifi_networks = []
    for match in re.finditer(pattern, output, re.MULTILINE):
        wifi_networks.append(match.groupdict()+'\n')
    return wifi_networks
    
print(parse_wifi_networks())