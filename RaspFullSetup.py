import paramiko  # Import paramiko for SSH and SFTP connectivity and operations.
import os
import requests  # Imports the requests module to make HTTP requests
import json  # Imports the json module for parsing and generating JSON data
from ip_addresses import fetch_latest_ip_addresses   # Imports the fetch_latest_ip_addresses function from ip_addresses module
from mysql.connector import connect  # Imports the connect function from mysql.connector module for database connections


with open('configHermes.json', 'r') as config_file:  # Opens the file in read mode
    config = json.load(config_file)  # Loads the JSON content and converts it into a Python dictionary

# Define a connection object
conn = connect(
      user=config['Login_Turtle']['user'],
      password=config['Login_Turtle']['password'],
      host=config['Login_Turtle']['host'],
      database=config['Login_Turtle']['database'])

ip_addresses = fetch_latest_ip_addresses()

for ip_adresses in ip_addresses.values():
    try:
        requests.get(f"http://{ip_adresses['RASP_catch']}:8000/kill")
    except Exception as e:
        print(e)

pi_disponibles = []

username = config['RASP_login']['user']
password = config['RASP_login']['password']


username = config['RASP_login']['user']
password = config['RASP_login']['password']

Command = config['LOCAL_file']['launch'] 

local_file_1 = config['LOCAL_file']['local_file_1']
local_file_2 = config['LOCAL_file']['local_file_2']
local_file_3 = config['LOCAL_file']['local_file_3']
local_file_4 = config['LOCAL_file']['local_file_4']
local_file_5 = config['LOCAL_file']['local_file_5']


target_dest_1 = config['LOCAL_file']['remote_file_1']
target_dest_2 = config['LOCAL_file']['remote_file_2']
target_dest_3 = config['LOCAL_file']['remote_file_3']
target_dest_4 = config['LOCAL_file']['remote_file_4']
target_dest_5 = config['LOCAL_file']['remote_file_5']


def check_pass(ip,username,password):
    global pi_disponibles
    try :
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password)

        print(f"{ip} : Connexion réussi, ajout à la liste de Raspberry valide : ")
        pi_disponibles.append(ip)

    except Exception as e:
        print(f"{ip} : Failed to connect. {e}. ")

def ssh_and_run(ip,username,password,local_file, target_dest,command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip,username=username,password=password)

        try:
            sftp = client.open_sftp()
            sftp.put(local_file,target_dest)
            sftp.close()
            print("Fichiers Transférés avec succès ! ")
            sftp = client.open_sftp()
            sftp.put(local_file_2,target_dest_2)
            sftp.close()
            print("Fichiers Transférés avec succès ! ")
            sftp = client.open_sftp()
            sftp.put(local_file_3,target_dest_3)
            sftp.close()
            print("Fichiers Transférés avec succès ! ")
            sftp = client.open_sftp()
            sftp.put(local_file_4,target_dest_4)
            sftp.close()
        except Exception as e:
            print(f"Le transfert a rencontré un problème : {e}")
        

        print("Creating a virtual environment on the Raspberry Pi")
        stdin, stdout, stderr = client.exec_command("python3 -m venv ~/venv")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Activating the virtual environment")
        stdin, stdout, stderr = client.exec_command("source ~/venv/bin/activate")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Installing asyncua in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install asyncua")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")



        print("Installing Flask in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install flask")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Installing Flask in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install flask[async]")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Installing requests in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install requests")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Installing APScheduler in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install APScheduler")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Installing mysql.connector in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install mysql.connector.python")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Installing Snap7 in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install python-snap7")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Installing Rpi.GPIO in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/pip install RPi.GPIO")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print("Running the script in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/python " + command)
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        
        

        print(f"Script exécuté avec succès sur {ip}")
        client.close()
        

    except Exception as e : 
        print(f"Echec de l'exécution du script sur {ip}: {e}")

for ip_adresses in ip_addresses.values():
    check_pass(ip_adresses,username,password)

for ip_adresses in pi_disponibles :
    ssh_and_run(ip_adresses,username,password,local_file_1,target_dest_1,Command)
