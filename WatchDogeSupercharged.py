from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing.dummy import Pool as ThreadPool
import time
import ip_addresses as ip
import requests
import logging
import numpy as np
import pygame
import json

with open('configDoge.json', 'r') as config_file:
    config = json.load(config_file)

# Use the configuration
logging.basicConfig(
    filename=config['logging']['filename'],
    filemode=config['logging']['filemode'],
    format=config['logging']['format'],
    level=getattr(logging, config['logging']['level'])
)


print("""\

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⠋⠈⠙⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⢤⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠈⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠞⠀⠀⢠⡜⣦⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡃⠀⠀⠀⠀⠈⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠊⣠⠀⠀⠀⠀⢻⡘⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠙⢶⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠚⢀⡼⠃⠀⠀⠀⠀⠸⣇⢳
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⣀⠖⠀⠀⠀⠀⠉⠀⠀⠈⠉⠛⠛⡛⢛⠛⢳⡶⠖⠋⠀⢠⡞⠀⠀⠀⠐⠆⠀⠀⣿⢸
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣦⣀⣴⡟⠀⠀⢶⣶⣾⡿⠀⠀⣿⢸
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⡠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣏⠀⠀⠀⣶⣿⣿⡇⠀⠀⢏⡞
⠀⠀⠀⠀⠀⠀⢀⡴⠛⠀⠀⠀⠀⠀⠀⠀⠀⢀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⣤⣾⣿⣿⠋⠀⠀⡀⣾⠁
⠀⠀⠀⠀⠀⣠⠟⠁⠀⠀⠀⣀⠀⠀⠀⠀⢀⡟⠈⢀⣤⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⣏⡁⠀⠐⠚⠃⣿⠀
⠀⠀⠀⠀⣴⠋⠀⠀⠀⡴⣿⣿⡟⣷⠀⠀⠊⠀⠴⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠀⠀⠀⠀⢹⡆
⠀⠀⠀⣴⠃⠀⠀⠀⠀⣇⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡶⢶⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠀⠀⣸⠃⠀⠀⠀⢠⠀⠊⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⢲⣾⣿⡏⣾⣿⣿⣿⣿⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢧
⠀⢠⡇⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⠛⠿⣽⣿⡿⠏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜
⢀⡿⠀⠀⠀⠀⢀⣤⣶⣟⣶⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⢸⠇⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⣼⠀⢀⡀⠀⠀⢷⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇
⡇⠀⠈⠀⠀⠀⣬⠻⣿⣿⣿⡿⠙⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁
⢹⡀⠀⠀⠀⠈⣿⣶⣿⣿⣝⡛⢳⠭⠍⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠃⠀
⠸⡇⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⣷⣦⣀⣀⣀⣤⣤⣴⡶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠇⠀⠀
⠀⢿⡄⠀⠀⠀⠀⠀⠙⣇⠉⠉⠙⠛⠻⠟⠛⠛⠉⠙⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠋⠀⠀⠀
⠀⠈⢧⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀
⠀⠀⠘⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠱⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠛⢦⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠲⠤⣤⣤⣤⣄⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⠤⠴⠒⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

 """)
app = Flask(__name__)



def job():
    print("+--------------------------------------+")
    logging.info('Job started')
    start_time = time.time()  # Capture the start time

    NombreAPIConnceted = 0

    multi_possible(NombreAPIConnceted)
    print("J'ai fais mulit possible")
    nombremultisql = 2

    checkplusde3(nombremultisql)

    get_info()

    compteur_bille()

    deconnection()
    logging.info('Job finished')
    print(f"Execution time: {time.time() - start_time}")
    print("+--------------------------------------+")

valid_request = config['requests']
print(valid_request)
def compteur_bille():
    A = np.zeros(3, dtype=int)
    i = 0

    def fetch_data(ip_address):
        nonlocal A, i
        try:
            response = requests.get(f"http://{ip_address['RASP_catch']}:8000/compteur_bille")
            A = np.add(A, response.json())
            print(f"Matrice de l'API : {ip_address['API']} : {response.json()}")
            i += 1
        except Exception as e:
            logging.error(e)
            print("Error occurred during API request.")

    pool = ThreadPool(len(ip.ip_addresses))
    pool.map(fetch_data, ip.ip_addresses.values())
    pool.close()
    pool.join()

    print(f"Matrice totale : {A}")
    if i != len(ip.ip_addresses):
        print("Erreur de compteur")
    else:
        def send_data(ip_address):
            try:
                for i in range(3):
                    requests.get(f"http://{ip_address['RASP_catch']}:8000/compteur_bille/{i}/{A[i]}")
            except Exception as e:
                logging.error(e)
        
        pool = ThreadPool(len(ip.ip_addresses))
        pool.map(send_data, ip.ip_addresses.values())
        pool.close()
        pool.join()

triggered= False
def get_info():
    def fetch_info(ip_address, request):
        global triggered
        try:
            response = requests.get(f"http://{ip_address['RASP_catch']}:8000/trigger/{request}")
            print(ip_address['API'], ": Request: ", request, "Response: ", response.json())

            if request.startswith("Mx_API_C") and response.status_code == 200:
                print("j'ai reçu une alerte True")
                if request.endswith("normal"):
                    print("Tout va bien")
                    logging.info(response.json())
                elif request.endswith("attention"):
                    SOS_Warning(1, f"http://{ip_address['RASP_catch']}:8000", "yellow", f"Position{request[8]}")
                    logging.info(response.json())
                elif request.endswith("alerte"):
                    print("J'ai reçu une alerte critique !!")
                    SOS_Warning(1, f"http://{ip_address['RASP_catch']}:8000", "red", f"Position{request[8]}")
                    print(response.json())
                    logging.info(response.json())

            if response.status_code == 200:


                logging.info(response.json())    

                for ip_address in ip.ip_addresses.values():
                    try:
                        if not triggered:
                            response = requests.get(f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/True")
                            if ip_address == ip.ip_addresses.values()[-1]:
                                triggered = True
                        else:
                            response = requests.get(f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/False")
                            if ip_address == ip.ip_addresses.values()[-1]:
                                triggered = False
                        logging.info(response.json())
                    except Exception as e:
                        logging.error(e)
                return
            else:
                logging.error(response.json())
        except Exception as e:
            logging.error(e)

    pool = ThreadPool(len(ip.ip_addresses) * len(valid_request))
    for request in valid_request:
        pool.map(lambda ip_addr: fetch_info(ip_addr, request), ip.ip_addresses.values())
    pool.close()
    pool.join()


def multi_possible(NombreAPIConnceted):
    def check_api(ip_address):
        nonlocal NombreAPIConnceted
        try:
            checker = requests.get(f"http://{ip_address['RASP_catch']}:8000/check_possible/{ip_address['API']}")
            print(checker.json())
            if checker.status_code == 200:
                multi = requests.get(f"http://{ip_address['RASP_catch']}:8000/connected")
                NombreAPIConnceted += 1
                print(f"{ip_address['API']} : API connected = {NombreAPIConnceted}")
        except Exception as e:
            logging.error(e)

    pool = ThreadPool(len(ip.ip_addresses))
    pool.map(check_api, ip.ip_addresses.values())
    pool.close()
    pool.join()

    def set_multi(ip_address, enabled):
        try:
            requests.get(f"http://{ip_address['RASP_catch']}:8000/multi/{enabled}")
        except Exception as e:
            logging.error(e)

    enabled = "True" if NombreAPIConnceted > 1 else "False"
    print(f"Mode multi {'disponible' if enabled == 'True' else 'indisponible'}")
    pool = ThreadPool(len(ip.ip_addresses))
    pool.map(lambda ip_addr: set_multi(ip_addr, enabled), ip.ip_addresses.values())
    pool.close()
    pool.join()

def SOS_Warning(times, base_url,color,position):

    
    morse_code_sos = "...---..."

    pygame.mixer.init()
    pygame.mixer.music.load(mp3file=config['sound_file'])
    pygame.mixer.music.play()

    for _ in range(times):

        morse_code_to_duration = {
        ".": 0.1,  # Short flash
        "-": 0.3,  # Long flash
        " ": 0.2   # Pause
        }



 
        for symbol in morse_code_sos:
        # Turn on the light
            response = requests.get(f"{base_url}/pin/{position}/{color}/high")
            if response.status_code != 200:
                print(f"Error turning on the light: {response.json()}")


            time.sleep(morse_code_to_duration[symbol])

            response = requests.get(f"{base_url}/pin/{position}/{color}/low")
            if response.status_code != 200:
                print(f"Error turning off the light: {response.json()}")

            time.sleep(0.1)

def checkplusde3(nombremultisql):
    def set_multinbr(ip_address, enabled):
        try:
            requests.get(f"http://{ip_address['RASP_catch']}:8000/multinbr/{enabled}")
        except Exception as e:
            logging.error(e)

    enabled = "True" if nombremultisql >= 3 else "False"
    print(f"Multi sur {'plus' if enabled == 'True' else 'moins'} de 3 châssis")
    pool = ThreadPool(len(ip.ip_addresses))
    pool.map(lambda ip_addr: set_multinbr(ip_addr, enabled), ip.ip_addresses.values())
    pool.close()
    pool.join()


def deconnection():
    def disconnect(ip_address):
        try:
            requests.get(f"http://{ip_address['RASP_catch']}:8000/deconnection")
        except Exception as e:
            logging.error(e)

    pool = ThreadPool(len(ip.ip_addresses))
    pool.map(disconnect, ip.ip_addresses.values())
    pool.close()
    pool.join()

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(job, 'interval',  seconds=config['scheduler']['interval'])

scheduler.start()

if __name__ == '__main__':
    logging.info('Application started')
    app.run(host=config['flask']['host'], port=config['flask']['port'])
    logging.info('Application finished')
