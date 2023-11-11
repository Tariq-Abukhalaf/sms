import subprocess
import re

def parse_wifi_networks():
    output = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'], text=True)
    pattern = r'(?P<INUSE>.+?)\s+(?P<BSSID>.+?)\s+(?P<SSID>\S+)\s+(?P<MODE>\S+)\s+(?P<CHAN>.+?)\s+(?P<RATE>\S+)\s+(?P<SIGNAL>\S+)\s+(?P<BARS>\S+)\s+(?P<SECURITY>.+)$'
    wifi_networks = []
    for match in re.finditer(pattern, output, re.MULTILINE):
        wifi_networks.append(match.groupdict())
    return wifi_networks
    
print(parse_wifi_networks())