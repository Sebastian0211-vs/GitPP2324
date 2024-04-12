import paramiko
import os

pi_chassis_ip = [
    "172.16.0.9" #Raspberry de Test
]

pi_disponibles = []

username = "pi"
password = "pi"

Command = "python ~/Desktop/LedAPI.py"
cat = "cat"                                                                                                                   
local_file = "LedAPI.py"
target_dest = "/home/pi/Desktop/LedAPI.py"

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
        except Exception as e:
            print(f"Le transfert a rencontré un problème : {e}")

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")
        client.close()

    except Exception as e : 
        print(f"Echec de l'exécution du script sur {ip}: {e}")

for ip in pi_chassis_ip:
    check_pass(ip,username,password)

for ip in pi_disponibles :
    ssh_and_run(ip,username,password,local_file,target_dest,Command)





