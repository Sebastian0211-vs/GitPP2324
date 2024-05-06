from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing.dummy import Pool as ThreadPool
import time
import ip_addresses as ip
import requests
import logging
import numpy as np

app = Flask(__name__)
logging.basicConfig(filename='apps.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def job():
    print("+--------------------------------------+")
    logging.info('Job started')
    start_time = time.time()  # Capture the start time

    NombreAPIConnceted = 0

    multi_possible(NombreAPIConnceted)
    nombremultisql = 2

    checkplusde3(nombremultisql)

    get_info()

    compteur_bille()

    deconnection()
    logging.info('Job finished')
    print(f"Execution time: {time.time() - start_time}")
    print("+--------------------------------------+")

valid_request = [
    "Mx_master_demande_multi", "Mx_master_alarme_urgence", "Mx_master_probleme_obstruation",
    "Mx_master_running", "Mx_master_arret_auto","Mx_master_quittance_obstruation",
    "Mx_master_quittance_alarme","Mx_master_alerte_billes_perdus","Mx_master_alerte_sortie_secours",
    "Mw_master_nb_billes_sortie_normal","Mw_master_nb_billes_sortie_secours",
    "Mw_master_nb_billes_entree","Mx_master_cellule_alerte_stop", "Mx_master_reset_surveillance", "Mx_API_C1_normal","Mx_API_C1_attention","Mx_API_C1_alerte","Mx_API_C2_normal","Mx_API_C2_attention","Mx_API_C2_alerte","Mx_API_C3_normal","Mx_API_C3_attention","Mx_API_C3_alerte","Mx_API_C4_normal","Mx_API_C4_attention","Mx_API_C4_alerte",
    "Mx_master_cellule_alerte_stop", "Mx_master_reset_surveillance"
]

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


def get_info():
    def fetch_info(ip_address, request):
        try:
            response = requests.get(f"http://{ip_address['RASP_catch']}:8000/trigger/{request}")
            print(ip_address['API'], ": Request: ", request, "Response: ", response.json())

            if request.startswith("Mx_API_C") and response.status_code == 200:
                if request.endswith("normal"):
                    response = requests.get(f"http://{ip_address['RASP_catch']}:8000/pin/Position{request[8]}/green/high")
                    logging.info(response.json())
                elif request.endswith("attention"):
                    response = requests.get(f"http://{ip_address['RASP_catch']}:8000/pin/Position{request[8]}/yellow/high")
                    logging.info(response.json())
                elif request.endswith("alerte"):
                    response = requests.get(f"http://{ip_address['RASP_catch']}:8000/pin/Position{request[8]}/red/high")
                    logging.info(response.json())

            if response.status_code == 200:
                logging.info(response.json())    
                for ip_address in ip.ip_addresses.values():
                    try:
                        response = requests.get(f"http://{ip_address['RASP_catch']}:8000/sortie/{request}")
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
            if checker.status_code == 200:
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
scheduler.add_job(job, 'interval', seconds=1.4)  # Adjust the interval as needed

scheduler.start()

if __name__ == '__main__':
    logging.info('Application started')
    app.run(host='0.0.0.0', port=8000)
    logging.info('Application finished')
