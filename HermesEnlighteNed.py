#-*- coding: utf-8 -*-
from flask import Flask, jsonify
import ip_addresses as ip
import requests
import os
import logging
import CommunicationAPIS7 as commS7
import snap7
import variablesAPI
from threading import Lock
from mysql.connector import connect
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

# Set up logging
logging.basicConfig(filename='/home/pi/Desktop/hermes.log', level=logging.INFO)

CONNECTED_PLC = None
plc_lock = Lock()
conn = connect(
      user = 'root',
      password = 'billes1234',
      host = '172.16.0.18',
      database = 'nuc_db')

errorled= False
app = Flask(__name__)

var_api_out = ["Mw_API_CVSortieStandard", "Mw_API_CVSortieSecours", "Mw_API_CVEntree"]
var_api_in = ["Mw_master_nb_billes_sortie_normal", "Mw_master_nb_billes_sortie_secours", "Mw_master_nb_billes_entree"]

id_chassis = 0
possibles_modes = {"mono", "multi"}

def is_connected():
    return CONNECTED_PLC and CONNECTED_PLC.get_connected()

def ensure_connected(ip_api):
    global CONNECTED_PLC
    if not is_connected():
        plc = snap7.client.Client()
        plc.connect(ip_api, 0, 1)
        CONNECTED_PLC = plc

def synchronized(func):
    def wrapper(*args, **kwargs):
        with plc_lock:
            return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Preserve the original function name
    return wrapper


@app.route('/check_possible/<string:ip_api>', methods=['GET'])
@synchronized
def check_possible(ip_api):
    try:
        ensure_connected(ip_api)
        return jsonify(message=f"API connecté"), 200
    except Exception as e:
        logging.error(f"Error in /check_possible: {str(e)}")
        return jsonify(error=str(e)), 500

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

@app.route('/sortie/<string:request>', methods=['GET'])
def demande_multi(request):
    with plc_lock:
        global CONNECTED_PLC
        try:
            commS7.writeMemory(CONNECTED_PLC, request, True)
            return jsonify(message=f"Sortie set for {request}"), 200
        except Exception as e:
            logging.error(f"Error in /sortie: {str(e)}")
            return jsonify(error=str(e)), 500

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

#************************************************************************************************************************************************************************************
GPIO.setmode(GPIO.BCM)

# Définition d'un dictionnaire pour mapper les positions aux numéros des broches
led_matrix = {
    "Position1": {"red": 17, "green": 27, "blue": 22, "white": 10},
    "Position2": {"red": 18, "green": 23, "blue": 24, "white": 25},
    "Position3": {"red": 5, "green": 6, "blue": 12, "white": 13},
    "Position4": {"red": 19, "green": 16, "blue": 26, "white": 20},
    "Position5": {"red": 21, "green": 20, "blue": 7, "white": 8},
}

# Ensemble de positions valides
valid_positions = {"Position1", "Position2", "Position3", "Position4", "Position5"}

color_combinations = {
    "yellow": ["red", "green"],
    "cyan": ["green", "blue"],
    "magenta": ["red", "blue"],
}

def setup_and_activate(position, colors, state):
    """Configure the GPIO pin for a specific color and state."""
    if not isinstance(colors, list):
        colors = [colors]
    for color in colors:
        pin_number = led_matrix[position][color]
        GPIO.setup(pin_number, GPIO.OUT)
        GPIO.output(pin_number, state)

@app.route('/pin/<string:position>/<string:couleur>/high', methods=['GET'])
def pin_HIGH(position, couleur):

    try:
        for color in ["red","yellow","green","cyan","blue","magenta","white"]:
            pin_LOW(position, color)

    except Exception as e:
        return jsonify(error=str(e)), 500


    """Activer la couleur spécifiée à la position donnée."""
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



@app.route('/pin/<string:position>/<string:couleur>/low', methods=['GET'])
def pin_LOW(position, couleur):
    """Éteindre la couleur spécifiée à la position donnée."""
    
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

@app.route('/reset', methods=['GET'])
def reset_all_pins():
    """Réinitialiser tous les pins GPIO à l'état bas (LOW)."""
    for position in led_matrix.values():
        for color_pin in position.values():
            GPIO.setup(color_pin, GPIO.OUT)
            GPIO.output(color_pin, GPIO.LOW)
    return jsonify({"message": "Tous les pins ont été réinitialisés à l'état LOW"}), 200



@app.route('/rainbow/<string:position>', methods=['GET'])
def rainbow(position):
    """Appliquer un effet arc-en-ciel à la position spécifiée."""
    try:
        for color in ["red","yellow","green","cyan","blue","magenta","white"]:
            pin_LOW(position, color)

    except Exception as e:
        return jsonify(error=str(e)), 500

    try:
        if position in valid_positions:
            for couleur in ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']:
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
    app.run(host='0.0.0.0', port=8000)
