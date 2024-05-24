#-*- coding: utf-8 -*-
from flask import Flask, jsonify  # Import Flask to create a web app and jsonify to return JSON responses
import ip_addresses as ip
import requests  # Imports the requests module to make HTTP requests
import os
import logging  # Imports the logging module for logging messages
import CommunicationAPIS7 as commS7
import snap7  # Imports the snap7 module for working with Siemens S7 PLCs
import json  # Imports the json module for parsing and generating JSON data
import variablesAPI
from threading import Lock  # Imports the Lock class from the threading module to handle threading synchronization
from mysql.connector import connect  # Imports the connect function from mysql.connector module for database connections
import RPi.GPIO as GPIO  # Imports the RPi.GPIO module for controlling Raspberry Pi GPIO channels
import time

# Chargement de la configuration à partir d'un fichier JSON
with open('/home/pi/Desktop/configHermes.json', 'r') as config_file:
    config = json.load(config_file)

# Configuration des GPIO pour le Raspberry Pi
GPIO.setmode(GPIO.BCM)

gpio_pins_to_free = [2, 3, 14, 15,18,8,7,1,12,20,21,13,19,10,9,11]  # Example pins for I2C and UART

# Free specific GPIO pins
for pin in gpio_pins_to_free:
    os.system(f"sudo raspi-gpio set {pin} ip")

# Configuration du système de journalisation
logging.basicConfig(filename=config['logging']['file_path'], level=logging.getLevelName(config['logging']['log_level']))

# Variables globales pour la connexion au PLC
CONNECTED_PLC = None
plc_lock = Lock()

# Configuration de la connexion à la base de données
conn = connect(
      user=config['Login_Turtle']['user'],
      password=config['Login_Turtle']['password'],
      host=config['Login_Turtle']['host'],
      database=config['Login_Turtle']['database'])

errorled = False

# Initialisation du serveur Flask
app = Flask(__name__)

# Chargement des configurations additionnelles
var_api_out = config['Var_API_Out']
var_api_in = config['Var_API_In']
id_chassis = config['id_chassis']
possibles_modes = config['possibles_modes']

# Configuration des pins GPIO pour la matrice LED
led_matrix = config['GPIO']['led_matrix']
valid_positions = set(led_matrix.keys()) 

# Combinaisons de couleurs pour les LEDs
color_combinations = config['GPIO']['color_combination']
color_list = config['GPIO']['color_list']
# Fonction pour vérifier si le PLC est connecté
def is_connected():
    return CONNECTED_PLC and CONNECTED_PLC.get_connected()

# Fonction pour assurer la connexion au PLC
def ensure_connected(ip_api):
    global CONNECTED_PLC
    if not is_connected():
        plc = snap7.client.Client()
        plc.connect(ip_api, 0, 1)
        CONNECTED_PLC = plc

# Décorateur pour synchroniser l'accès aux fonctions critiques
def synchronized(func):
    def wrapper(*args, **kwargs):
        with plc_lock:
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  
    return wrapper



# Route pour vérifier si le châssis est connecté
@app.route('/connected', methods=['GET'])
@synchronized
def connected():
    global CONNECTED_PLC
    try:
        commS7.writeMemory(CONNECTED_PLC,"Mx_master_connecte", "True")
        return jsonify(message=f"Chassis connecte")
    except Exception as e:
        logging.error(f"Error chassis non connecte")
        return jsonify(error=str(e)), 500
        
# Route pour vérifier la possibilité de connexion via IP
@app.route('/check_possible/<string:ip_api>', methods=['GET'])
@synchronized
def check_possible(ip_api):
    global CONNECTED_PLC
    try:
        plc = snap7.client.Client()
        plc.connect(ip_api, 0, 1)  # IP address, rack, slot
        CONNECTED_PLC = plc
        return jsonify(message=f"API connecté"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

# Route pour écrire si le mode multi est possible
@app.route('/multi/<string:BOOL>', methods=['GET'])
def multi(BOOL):
    with plc_lock:
        global CONNECTED_PLC
        try:
            commS7.writeMemory(CONNECTED_PLC, "Mx_master_multi_possible", BOOL == "True")
            return jsonify(message=f"Mode multi activé"), 200
        except Exception as e:
            logging.error(f"Error in /multi: {str(e)}")
            return jsonify(error=str(e)), 500

# Route pour écrire si le mode multi est possible sur plus de 3 châssis
@app.route('/multinbr/<string:BOOL>', methods=['GET'])
def multinbr(BOOL):
    with plc_lock:
        global CONNECTED_PLC
        try:
            commS7.writeMemory(CONNECTED_PLC, "Mx_master_multi+de3", BOOL == "True")
            return jsonify(message=f"Mode multi activé"), 200
        except Exception as e:
            logging.error(f"Error in /multinbr: {str(e)}")
            return jsonify(error=str(e)), 500
        
# Route pour lire une variable du PLC
@app.route('/trigger/<string:request>', methods=['GET'])
def trigger(request):
    with plc_lock:
        global CONNECTED_PLC
        try:
            valeur = commS7.readMemory(CONNECTED_PLC, request)
            if valeur:
                return jsonify(message=f"{valeur}"), 200
            else:
                return jsonify(message=f"{valeur}"), 300
        except Exception as e:
            logging.error(f"Error in /trigger: {str(e)}")
            return jsonify(error=str(e)), 500

# Route pour lire les données des compteurs de billes
@app.route('/compteur_bille', methods=['GET'])
def compteur_bille():
    with plc_lock:
        global CONNECTED_PLC
        storage = []
        try:
            for name in var_api_out:
                storage.append(commS7.readMemory(CONNECTED_PLC, name))
            return jsonify(storage), 200
        except Exception as e:
            logging.error(f"Error in /compteur_bille: {str(e)}")
            return jsonify(error=str(e)), 500

# Route pour écrire les données des compteurs de billes
@app.route('/compteur_bille/<int:index>/<int:val>', methods=['GET'])
def set_compteur_bille(index, val):
    with plc_lock:
        global CONNECTED_PLC
        try:
            commS7.writeMemory(CONNECTED_PLC, var_api_in[index], val)
            return jsonify(message=f"Valeur de compteur bille modifiée"), 200
        except Exception as e:
            logging.error(f"Error in /compteur_bille (set): {str(e)}")
            return jsonify(error=str(e)), 500

# Route pour écrire True ou False dans une variable du PLC
@app.route('/sortie/<string:request>/<string:VAR>', methods=['GET'])
def demande_multi(request, VAR):
    with plc_lock:
        global CONNECTED_PLC
        try:
            if VAR == "True":
                commS7.writeMemory(CONNECTED_PLC, request, True)
                logging.info(f"Sortie set for {request}")
            else:
                commS7.writeMemory(CONNECTED_PLC, request, False)
            return jsonify(message=f"Sortie set for {request}"), 200
        except Exception as e:
            logging.error(f"Error in /sortie: {str(e)}")
            return jsonify(error=str(e)), 500

# Route de déconnexion du PLC
@app.route('/deconnection', methods=['GET'])
def deconnection():
    with plc_lock:
        global CONNECTED_PLC
        try:
            CONNECTED_PLC.disconnect()
            CONNECTED_PLC = None
            return jsonify(message=f"API déconnecté"), 200
        except Exception as e:
            logging.error(f"Error in /deconnection: {str(e)}")
            return jsonify(error=str(e)), 500

"""


   ______          __  _                __    __________ 
  / ____/__  _____/ /_(_)___  ____     / /   / ____/ __ \
 / / __/ _ \/ ___/ __/ / __ \/ __ \   / /   / __/ / / / /
/ /_/ /  __(__  ) /_/ / /_/ / / / /  / /___/ /___/ /_/ / 
\____/\___/____/\__/_/\____/_/ /_/  /_____/_____/_____/  
                                                         


"""
def setup_and_activate(position, colors, state):
    """Configure the GPIO pin for a specific color and state."""
    if not isinstance(colors, list):
        colors = [colors]
    for color in colors:
        pin_number = led_matrix[position][color]
        GPIO.setup(pin_number, GPIO.OUT)
        GPIO.output(pin_number, state)

# Route pour allumer, de la couleur donnée, les LEDs d'une position donnée
@app.route('/pin/<string:position>/<string:couleur>/high', methods=['GET'])
def pin_HIGH(position, couleur):
    try:
        for color in color_list:
            pin_LOW(position, color)

    except Exception as e:
        return jsonify(error=str(e)), 500

    try:
        if position in valid_positions:
            if couleur in color_combinations:
                for color in color_combinations[couleur]:
                    setup_and_activate(position, color, GPIO.HIGH)
                return jsonify(message="Cellule à la position {0} a ete mise en {1}".format(position, couleur)), 200
            
            setup_and_activate(position, couleur, GPIO.HIGH)
            return jsonify(message="Cellule à la position {0} a ete mise en {1}".format(position, couleur)), 200
        else:
            return jsonify(error="Position de cellule invalide"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# Route pour éteindre, la couleur donnée, sur les LEDs d'une position donnée
@app.route('/pin/<string:position>/<string:couleur>/low', methods=['GET'])
def pin_LOW(position, couleur):
    try:
        if position in valid_positions:
            if couleur in color_combinations:
                for color in color_combinations[couleur]:
                    setup_and_activate(position, color, GPIO.LOW)
                return jsonify(message="Cellule à la position {0} : la couleur {1} a été éteinte".format(position, couleur)), 200
            else:
                setup_and_activate(position, couleur, GPIO.LOW)
                return jsonify(message="Cellule à la position {0} : la couleur {1} a été éteinte".format(position, couleur)), 200
        else:
            return jsonify(error="Position de cellule invalide"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# Route pour éteindre toutes les LEDs
@app.route('/reset', methods=['GET'])
def reset_all_pins():

    for position in led_matrix.values():
        for color_pin in position.values():
            GPIO.setup(color_pin, GPIO.OUT)
            GPIO.output(color_pin, GPIO.LOW)
    return jsonify({"message": "Tous les pins ont été réinitialisés à l'état LOW"}), 200


@app.route('/reset/<string:position>', methods=['GET'])
def reset_pin(position):
    try:
        if position in valid_positions:
            for color_pin in led_matrix[position].values():
                GPIO.setup(color_pin, GPIO.OUT)
                GPIO.output(color_pin, GPIO.LOW)
            return jsonify(message=f"La position {position} a été réinitialisée"), 200
        else:
            return jsonify(error="Position de cellule invalide"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
    
# ROute pour activer l'animation "rainbow" sur toutes les positions 
@app.route('/rainbow', methods=['GET'])
def rainbow_all():
    try:
        for color in color_list:
            for position in valid_positions:
                pin_LOW(position, color)

    except Exception as e:
        return jsonify(error=str(e)), 500

    try:
        for position in valid_positions:
            for couleur in color_list:
                if couleur in color_combinations:
                    for color in color_combinations[couleur]:
                        setup_and_activate(position, color, GPIO.HIGH)
                    time.sleep(0.1)
                    for color in color_combinations[couleur]:
                        setup_and_activate(position, color, GPIO.LOW)
                else:
                    setup_and_activate(position, couleur, GPIO.HIGH)
                    time.sleep(0.1)
                    setup_and_activate(position, couleur, GPIO.LOW)
        return jsonify(message="Effet arc-en-ciel appliqué à toutes les positions"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
    
# Route pour activer l'animation "rainbow" sur les LEDs d'une position donnée
@app.route('/rainbow/<string:position>', methods=['GET'])
def rainbow(position):

    try:
        for color in color_list:
            pin_LOW(position, color)

    except Exception as e:
        return jsonify(error=str(e)), 500

    try:
        if position in valid_positions:
            for couleur in color_list:
                if couleur in color_combinations:
                    for color in color_combinations[couleur]:
                        setup_and_activate(position, color, GPIO.HIGH)
                    time.sleep(0.1)
                    for color in color_combinations[couleur]:
                        setup_and_activate(position, color, GPIO.LOW)
                else:
                    setup_and_activate(position, couleur, GPIO.HIGH)
                    time.sleep(0.1)
                    setup_and_activate(position, couleur, GPIO.LOW)
            return jsonify(message="Effet arc-en-ciel appliqué à la position {0}".format(position)), 200
        else:
            return jsonify(error="Position de cellule invalide"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# Route pour allumer, de la couleur donnée, les LEDs de toutes les positions
@app.route('/all/<string:couleur>', methods=['GET'])
def all_pins_color(couleur):
    """Appliquer la couleur spécifiée à toutes les positions."""
    try:
        if couleur in color_combinations:
            for position in valid_positions:
                for color in color_combinations[couleur]:
                    setup_and_activate(position, color, GPIO.HIGH)
            return jsonify(message="Toutes les positions ont été mises en {0}".format(couleur)), 200
        else:
            for position in valid_positions:
                setup_and_activate(position, couleur, GPIO.HIGH)
            return jsonify(message="Toutes les positions ont été mises en {0}".format(couleur)), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

# Route pour arrêter ce script
@app.route('/kill', methods=['GET'])
def kill_script():
    logging.info("Kill script called")
    os._exit(0)

# Gestion des erreurs
@app.errorhandler(Exception)
def handle_exception(e):
    global CONNECTED_PLC
    logging.error(f"Unexpected error: {str(e)}")
    if CONNECTED_PLC:
        CONNECTED_PLC.disconnect()
        CONNECTED_PLC = None
    return jsonify(error="Erreur interne du serveur"), 500

@app.errorhandler(404)
def not_found(error):
    logging.error(f"404 error: {str(error)}")
    return jsonify(error="Non trouvé"), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"500 error: {str(error)}")
    return jsonify(error="Erreur interne du serveur"), 500

# Entry point for the application
if __name__ == '__main__':
    app.run(host=config['flask_app']['host'], port=config['flask_app']['port'])