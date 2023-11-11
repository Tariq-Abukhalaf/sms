import subprocess

def get_available_networks():
    result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
    networks = [line.strip() for line in result.stdout.split('ESSID:')[1:]]
    print(networks)
    return networks


get_available_networks()