import subprocess

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
    
print(get_available_network_ssids())