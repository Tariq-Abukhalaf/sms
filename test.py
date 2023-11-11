import subprocess

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
            })
        return wifi_networks

    except subprocess.CalledProcessError as e:
        print(f"Error running 'nmcli': {e}")
        return []

if __name__ == "__main__":
    wifi_networks = parse_wifi_list()
    print(wifi_networks)
