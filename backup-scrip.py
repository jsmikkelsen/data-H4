import os
from netmiko import ConnectHandler
from datetime import datetime
import getpass

# Konfiguration
DEVICES = ['192.0.30.10', '192.1.30.11', '192.1.30.12', '192.1.30.13', '192.1.30.14', '192.2.31.11', '192.2.31.12', '192.2.31.13', '192.2.31.14']
BACKUP_DIR = "cisco_backups"

# Opret mappe hvis den ikke findes
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def get_backup():
    user = input("Indtast SSH brugernavn: ")
    secret = getpass.getpass("Indtast SSH password: ")

    for ip in DEVICES:
        device_params = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': user,
            'password': secret,
            'conn_timeout': 10,
        }

        try:
            print(f"---> Forbinder til {ip}...")
            with ConnectHandler(**device_params) as net_connect:
                # Find hostname (fjerner # og >)
                hostname = net_connect.find_prompt()[:-1]
                
                print(f"Henter konfiguration fra {hostname}...")
                config = net_connect.send_command('show run')

                # Filnavn med hostname og dato
                date_str = datetime.now().strftime("%Y-%m-%d")
                filename = f"{hostname}_{date_str}.txt"
                filepath = os.path.join(BACKUP_DIR, filename)

                with open(filepath, 'w') as f:
                    f.write(config)
                
                print(f"Færdig! Gemt i: {filepath}")

        except Exception as e:
            print(f"FEJL: Kunne ikke forbinde til {ip}. Årsag: {e}")

if __name__ == "__main__":
    get_backup()
