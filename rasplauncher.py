import paramiko
import os
import requests



pi_chassis_ip = [
    "172.16.0.17", #Raspberry de Test
]
try:
    requests.get(f"http://{pi_chassis_ip[0]}:8000/kill")
except Exception as e:
    print(e)

pi_disponibles = []






username = "pi"
password = "pi"

Command = "~/Desktop/HermesEnlighteNed.py"   

local_file_1 = "HermesEnlighteNed.py"
local_file_2 = "ip_addresses.py"
local_file_3 = "CommunicationAPIS7.py"
local_file_4 = "variablesAPI.py"


target_dest_1 = "/home/pi/Desktop/HermesEnlighteNed.py"
target_dest_2 = "/home/pi/Desktop/ip_addresses.py"
target_dest_3 = "/home/pi/Desktop/CommunicationAPIS7.py"
target_dest_4 = "/home/pi/Desktop/variablesAPI.py"



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
        except Exception as e:
            print(f"Le transfert a rencontré un problème : {e}")




        print("Running the script in the virtual environment")
        stdin, stdout, stderr = client.exec_command("~/venv/bin/python " + command)
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")

        print(f"Script exécuté avec succès sur {ip}")
        client.close()

    except Exception as e:
        print(f"Erreur de {ip}: {e}")


for ip in pi_chassis_ip:
    ssh_and_run(ip,username,password,local_file_1,target_dest_1,Command)
    pi_disponibles.append(ip)
