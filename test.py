import subprocess

def parse_wifi_list():
    try:
        # Run the 'nmcli' command and capture its output as a string
        output = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'], text=True)

        # Split the output into lines
        lines = output.splitlines()

        # Assuming the first two lines are headers, you can skip them
        if len(lines) >= 2:
            data_lines = lines[2:]
        else:
            data_lines = []

        wifi_networks = []

        # Process the data_lines and store information about available Wi-Fi networks
        for line in data_lines:
            # Split the line into columns (assuming columns are separated by whitespace)
            columns = line.split()

            if len(columns) >= 4:
                ssid = columns[0]  # The SSID of the Wi-Fi network
                mode = columns[1]  # The mode (e.g., 'Infra' for infrastructure)
                signal_strength = columns[2]  # The signal strength
                security = columns[3]  # The security type

                wifi_networks.append({
                    'SSID': ssid,
                    'Mode': mode,
                    'Signal_Strength': signal_strength,
                    'Security': security
                })

        return wifi_networks

    except subprocess.CalledProcessError as e:
        # Handle any errors that occur when running the command
        print(f"Error running 'nmcli': {e}")
        return []

# Example usage of the function
if __name__ == "__main__":
    wifi_networks = parse_wifi_list()
    for network in wifi_networks:
        print(network)