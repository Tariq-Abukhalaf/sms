import subprocess
import re

def parse_wifi_networks():
    output = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'], text=True)
    pattern = r'(?P<SSID>.+?)\s+(?P<BSSID>\S+)\s+(?P<MODE>\S+)\s+(?P<FREQ>\S+)\s+(?P<RATE>\S+)\s+(?P<SIGNAL>\S+)\s+(?P<SECURITY>.+)$'
    wifi_networks = []
    for match in re.finditer(pattern, output, re.MULTILINE):
        network_info = match.groupdict()
        # Create a new dictionary with only BSSID, SSID, and SIGNAL
        simplified_network_info = {
            'BSSID': network_info['BSSID'],
            'SSID': network_info['SSID'],
            'SIGNAL': network_info['SIGNAL']
        }
        wifi_networks.append(simplified_network_info)
    return wifi_networks
    
print(parse_wifi_networks())