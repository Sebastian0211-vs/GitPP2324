from flask import Flask, jsonify  # Import Flask to create a web app and jsonify to return JSON responses
from apscheduler.schedulers.background import BackgroundScheduler  # Import APScheduler for background task scheduling
from multiprocessing.dummy import Pool as ThreadPool  # Import ThreadPool for parallel task execution
import time
from ip_addresses import fetch_latest_ip_addresses  # Import the fetch_latest_ip_addresses function from ip_addresses.py
import requests  # Imports the requests module to make HTTP requests
import logging  # Imports the logging module for logging messages
import numpy as np  # Import NumPy for numerical operations
import pygame  # Import Pygame for creating video games
import json  # Imports the json module for parsing and generating JSON data

# Chargement de la configuration à partir d'un fichier JSON
with open('configDoge.json', 'r') as config_file:
    config = json.load(config_file)
grosse_horloge = time.time()
running_time = time.time()

def create_logs():
# Use the configuration
    logging.basicConfig(
        filename=config['logging']['filename'],
        filemode=config['logging']['filemode'],
        format=config['logging']['format'],
        level=getattr(logging, config['logging']['level'])
    )

create_logs()
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

# Starts the web app
app = Flask(__name__)


def job():
    global running_time
    """
    A scheduled job function to handle a series of tasks periodically. 
    It reschedules itself and logs execution time and completion.
    """
    print("+--------------------------------------+")
    logging.info('Job started')
    start_time = time.time()  # Capture the start time

    NombreAPIConnceted = 0

    NombreAPIConnceted = multi_possible(NombreAPIConnceted,fetch_latest_ip_addresses())
    nombremultisql = NombreAPIConnceted

    checkplusde3(nombremultisql,fetch_latest_ip_addresses())
    get_info(NombreAPIConnceted,fetch_latest_ip_addresses())
    compteur_bille(fetch_latest_ip_addresses())
    deconnection(fetch_latest_ip_addresses())

    logging.info('Job finished')
    print(f"Execution time: {time.time() - start_time}")
    temps_depuis_le_lancement = time.time() - grosse_horloge
    print(f"Temps depuis le lancement : {temps_depuis_le_lancement//3600} heures {temps_depuis_le_lancement%3600//60} minutes {temps_depuis_le_lancement%60} secondes")
    if time.time() - running_time > config['logging']['time_before_flush']:
        # if the program has been running for more than an hour, delete the logs
        open(config['logging']['filename'], 'w').close()
        running_time = time.time()
        create_logs()

    scheduler.add_job(job)  # Reschedule the job for future execution
    
    print("+--------------------------------------+")  # Print a separator to distinguish between different job executions

valid_request = config['requests']

def compteur_bille(ip_addresses):
    """ Computes the number of marbles in the circuit """
    A = np.zeros(3, dtype=int)  # Initialize an array to store counts of 'compteur_bille' with three zeros
    i = 0  # Counter for tracking successful API responses

    # Function to fetch the number of marbles from each PLC
    def fetch_data(ip_address):
        nonlocal A, i  # Allow the function to modify A and i defined in the outer scope
        try:
            response = requests.get(f"http://{ip_address['RASP_catch']}:8000/compteur_bille")
            A = np.add(A, response.json())  # Add the received data to the existing matrix A
            print(f"Matrice de l'API : {ip_address['API']} : {response.json()}")
            i += 1
        except Exception as e:
            logging.error(e)
            print("Error occurred during API request.")

    pool = ThreadPool(len(ip_addresses))  # Create a thread pool with a size equal to the number of IP addresses
    pool.map(fetch_data, ip_addresses.values())  # Map the fetch_data function to each IP address, running them concurrently
    pool.close()  # Close the pool
    pool.join()   # and wait for all tasks to complete

    print(f"Matrice totale : {A}")
    if i != len(ip_addresses):  # Check if all PLC responses were successful
        print("Erreur de compteur")
    else:
        # Function to send the total counts back to each PLC
        def send_data(ip_address):
            try:
                for i in range(3):
                    requests.get(f"http://{ip_address['RASP_catch']}:8000/compteur_bille/{i}/{A[i]}")
            except Exception as e:
                logging.error(e)
        
        pool = ThreadPool(len(ip_addresses))  # Idem
        pool.map(send_data, ip_addresses.values())
        pool.close()
        pool.join()

triggered= False
def get_info(NombreAPIConnceted,ip_addresses):
    """
    Retrieves and processes information for each connected PLC based on predefined requests.
    It sends requests to each IP address for each type of configured request, processes the responses,
    and may trigger warnings or further actions depending on the response content.
    """
    def fetch_info(ip_address, request):
        nonlocal NombreAPIConnceted
        global triggered
        try:
            response = requests.get(f"http://{ip_address['RASP_catch']}:8000/trigger/{request}")
            
            # Handle PLC requests that begin with "Mx_API_C". These are alerts.
            if request.startswith("Mx_API_C") and response.status_code == 200:
                # Check for various suffixes in the request to determine the type of alert
                if request.endswith("normal"):
                    print("Tout va bien")
                    logging.info(response.json())
                elif request.endswith("attention"):
                    SOS_Warning(1, f"http://{ip_address['RASP_catch']}:8000", "yellow", f"Position{request[8]}")
                    logging.info(response.json())
                elif request.endswith("alerte"):
                    print("Alerte Critique :")
                    print(ip_address['API'], ": Request: ", request, "Response: ", response.json())
                    SOS_Warning(1, f"http://{ip_address['RASP_catch']}:8000", "red", f"Position{request[8]}")

                    print(response.json())
                    logging.info(response.json())

            # Handle general "Mx" (BOOL) prefixed requests that are successful.
            if response.status_code == 200 and request.startswith("Mx"):
                print(ip_address['API'], ": Request: ", request, "Response: ", response.json())
                logging.info(response.json())    
                compteur = 0
                for ip_address in ip_addresses.values():
                    try:
                        compteur += 1 
                        response = requests.get(f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/True")
                        # If all connected PLCs have responded, send a "reset" command.
                        if compteur == NombreAPIConnceted:
                            for ip_address in ip_addresses.values():
                                try:
                                    response = requests.get(f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/False")
                                except Exception as e:
                                    logging.error(e)
                        
                        logging.info(response.json())
                    except Exception as e:
                        logging.error(e)
                return
            
            # Handle successful responses that doesn't fit the previous categories.
            elif response.status_code == 200:
                print(ip_address['API'], ": Request: ", request, "Response: ", response.json())
                logging.info(response.json())
                for ip_address in ip_addresses.values():
                    try:
                        response = requests.get(f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/True")
                        logging.info(response.json())
                    except Exception as e:
                        logging.error(e)

            else:
                logging.error(response.json())
        except Exception as e:
            logging.error(e)

    pool = ThreadPool(len(ip_addresses) * len(valid_request))  # Idem
    for request in valid_request:
        pool.map(lambda ip_addr: fetch_info(ip_addr, request), ip_addresses.values())
    pool.close()
    pool.join()


def multi_possible(NombreAPIConnceted,ip_addresses):
    """ This function checks each PLC's connection status and updates the count of connected PLCs. """
    def check_api(ip_address):
        nonlocal NombreAPIConnceted
        try:
            checker = requests.get(f"http://{ip_address['RASP_catch']}:8000/check_possible/{ip_address['API']}")

            if checker.status_code == 200:  # If the PLC is accessible
                multi = requests.get(f"http://{ip_address['RASP_catch']}:8000/connected")
                NombreAPIConnceted += 1  # If the PLC is connected
                print(f"{ip_address['API']} : API connected ")

            else:
                print(f"{ip_address['API']} : API not connected")

        except Exception as e:
            logging.error(e)

    pool = ThreadPool(len(ip_addresses))  # Idem
    pool.map(check_api, ip_addresses.values())
    pool.close()
    pool.join()
    

    def set_multi(ip_address, enabled):
        try:
            requests.get(f"http://{ip_address['RASP_catch']}:8000/multi/{enabled}")
        except Exception as e:
            logging.error(e)

    enabled = "True" if NombreAPIConnceted > 1 else "False"  # Enable multi-mode if more than one PLC is connected
    print(f"Mode multi {'disponible' if enabled == 'True' else 'indisponible'}")
    
    pool = ThreadPool(len(ip_addresses))  # Idem
    pool.map(lambda ip_addr: set_multi(ip_addr, enabled), ip_addresses.values())
    pool.close()
    pool.join()

    return NombreAPIConnceted

def SOS_Warning(times, base_url,color,position):
    """ Sends an SOS signal by flashing lights in Morse code and playing a sound. """
    
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

            # Turn off the light
            response = requests.get(f"{base_url}/pin/{position}/{color}/low")
            if response.status_code != 200:
                print(f"Error turning off the light: {response.json()}")

            time.sleep(0.1)

def checkplusde3(nombremultisql,ip_addresses):
    """ Checks if the number of connected PLCs is equal or greater than 3. """
    def set_multinbr(ip_address, enabled):
        try:
            requests.get(f"http://{ip_address['RASP_catch']}:8000/multinbr/{enabled}")
        except Exception as e:
            logging.error(e)

    enabled = "True" if nombremultisql >= 3 else "False"
    print(f"Multi sur {'plus' if enabled == 'True' else 'moins'} de 3 châssis")
    
    pool = ThreadPool(len(ip_addresses))  # Idem
    pool.map(lambda ip_addr: set_multinbr(ip_addr, enabled), ip_addresses.values())
    pool.close()
    pool.join()


def deconnection(ip_addresses):
    """ Disconnects all devices by sending a deconnection request to each IP address listed. """
    def disconnect(ip_address):
        try:
            requests.get(f"http://{ip_address['RASP_catch']}:8000/deconnection")
        except Exception as e:
            logging.error(e)

    pool = ThreadPool(len(ip_addresses))  # Create a ThreadPool with a number of threads equal to the number of IP addresses
    pool.map(disconnect, ip_addresses.values())  # Use the pool to run the function on each value in ip_addresses concurrently
    pool.close()  # Close the pool to prevent any more tasks from being submitted to it
    pool.join()  # Wait for all the worker threads to finish


scheduler = BackgroundScheduler(daemon=True)  # Create a background scheduler; daemon=True allows the program to exit if this is the only running thread
scheduler.add_job(job)  # Schedule a job to be executed

scheduler.start()  # Start the scheduler to begin executing jobs

# Entry point for the application
if __name__ == '__main__':
    logging.info('Application started')
    app.run(host=config['flask']['host'], port=config['flask']['port'])  # Start the Flask application with the host and port from config
    logging.info('Application finished')
