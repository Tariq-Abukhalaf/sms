#!/usr/bin/python3

from flask import Flask, render_template, request
import subprocess
import re
import os

app = Flask(__name__)

def parse_wifi_list():
    try:
        output = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'], text=True)
        lines = output.splitlines()
        wifi_networks = []
        for line in lines[1:]:
            columns = line.split()
            active   = False
            if len(columns)>9:
                columns=columns[1:]
                active = True

            bssid    = columns[0]
            ssid     = columns[1]
            mode     = columns[2]
            chan     = columns[3]
            rate     = columns[4]+' '+columns[5]
            signal   = columns[6]
            bars     = columns[7]
            security = columns[8]

            wifi_networks.append({
                "BSSID"   : bssid,
                "SSID"    : ssid,
                "MODE"    : mode,
                "CHAN"    : chan,
                "RATE"    : rate,
                "SIGNAL"  : signal,
                "BARS"    : bars,
                "SECURITY" : security,
                "ACTIVE"  : active,
            })
        return wifi_networks

    except subprocess.CalledProcessError as e:
        print(f"Error running 'nmcli': {e}")
        return []

def get_available_network_ssids():
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            network_info = result.stdout.split('ESSID:')[1:]
            ssids = [line.split('\n')[0].strip().strip('"') for line in network_info]
            return ssids
        else:
            print("Error: 'iwlist' command returned a non-zero exit code.")
            return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []




def get_nm_connections():
    try:
        files = os.listdir('/etc/NetworkManager/system-connections')
        return files
    except FileNotFoundError:
        return None
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_network = request.form['network']
        password = request.form['password']

        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as wpa_conf:
            wpa_conf.write(f'network={{\n  ssid="{selected_network}"\n  psk="{password}"\n}}\n')
    
    wifi_data = parse_wifi_list()
    networks = get_available_network_ssids()
    nm_connections = get_nm_connections()
    return render_template('index.html', wifi_data=wifi_data, networks_list=networks, nm_connections=nm_connections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)


