import paramiko
import os

pi_chassis_ip = [
    "172.16.0.3" #Raspberry de Test
]

pi_disponibles = []

username = "pi"
password = "pi"

Command = "python ~/Desktop/BillesMasterAPI.py"    
Command2 = ""                                                                                                              
local_file = "BillesMasterAPI.py"
target_dest = "/home/pi/Desktop/BillesMasterAPI.py"

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
        print("Installation de Flask sur le Raspberry Pi")
        stdin, stdout, stderr = client.exec_command("pip install flask")
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode(errors='ignore')  
        error = stderr.read().decode(errors='ignore')
        print(f"Terminal de {ip}: {output}")
        if error:
            print(f"Erreur de {ip}: {error}")
        

    except Exception as e : 
        print(f"Echec de l'exécution du script sur {ip}: {e}")

for ip in pi_chassis_ip:
    check_pass(ip,username,password)

for ip in pi_disponibles :
    ssh_and_run(ip,username,password,local_file,target_dest,Command2)





