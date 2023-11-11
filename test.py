from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# Function to get a list of available networks
def get_available_networks():
    result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
    networks = [line.strip() for line in result.stdout.split('ESSID:')[1:]]
    return networks

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_network = request.form['network']
        password = request.form['password']
        # Update the /etc/wpa_supplicant/wpa_supplicant.conf file with the selected network and password
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as wpa_conf:
            wpa_conf.write(f'network={{\n  ssid="{selected_network}"\n  psk="{password}"\n}}\n')
    networks = get_available_networks()
    return render_template('index.html', networks=networks)

if __name__ == '__main__':
    app.run(debug=True)
