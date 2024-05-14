import paramiko
import os
import requests
import json
import ip_addresses as ip
from mysql.connector import connect




with open('configHermes.json', 'r') as config_file:
    config = json.load(config_file)

conn = connect(
      user=config['Login_Turtle']['user'],
      password=config['Login_Turtle']['password'],
      host=config['Login_Turtle']['host'],
      database=config['Login_Turtle']['database'])



for ip_adresses in ip.ip_addresses.values():
    try:
        requests.get(f"http://{ip_adresses['RASP_catch']}:8000/kill")
    except Exception as e:
        print(e)

pi_disponibles = []





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
            print("Fichiers Transférés avec succès ! ")
            sftp = client.open_sftp()
            sftp.put(local_file_5,target_dest_5)
            sftp.close()
            print("Fichiers Transférés avec succès ! ")
        except Exception as e:
            print(f"Le transfert a rencontré un problème : {e}")




        print("Running the script in the virtual environment")
        stdin, stdout, stderr = client.exec_command("nohup ~/venv/bin/python " + command + " > /dev/null 2>&1 & disown")
        exit_status = stdout.channel.recv_exit_status()  # Get the exit status of the command
        client.close()
        print(f"Exit status of the command on {ip}: {exit_status}")

    except Exception as e:
        print(f"Erreur de {ip}: {e}")

        print(f"Script exécuté avec succès sur {ip}")
        

    except Exception as e:
        print(f"Erreur de {ip}: {e}")



for ip_adresses in ip.ip_addresses.values():
    ssh_and_run(ip_adresses['RASP_catch'],username,password,local_file_1,target_dest_1,Command)
    print(f"Script exécuté avec succès sur {ip_adresses}")
