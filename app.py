#!/usr/bin/python3

from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_network = request.form['network']
        password = request.form['password']
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as wpa_conf:
            wpa_conf.write(f'network={{\n  ssid="{selected_network}"\n  psk="{password}"\n}}\n')
    networks = get_available_network_ssids()
    return render_template('index.html', networks=networks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)


