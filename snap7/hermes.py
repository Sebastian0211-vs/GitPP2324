#-*- coding: utf-8 -*-
#from asyncua import Client, ua
from flask import Flask, jsonify
import CommunicationAPIS7 as commS7
import ip_addresses as ip
import requests
import snap7

CONNECTED_PLC = None

var_api_out = ["Mw_API_CVSortieStandard","Mw_API_CVSortieSecours","Mw_API_CVEntree"]

var_api_in = ["Mw_master_nb_billes_sortie_normal","Mw_master_nb_billes_sortie_secours","Mw_master_nb_billes_entree"]

app = Flask(__name__)

"""
@app.route('/API_IP/<string:ip>', methods=['GET'])
def API_IP(ip):
    global CONNECTED_PLC 
    try:
        plc = snap7.client.Client()
        plc.connect(ip, 0, 1)  # IP address, rack, slot
        CONNECTED_PLC = plc
        return jsonify(message=f"API IP: {ip}"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500
"""

# Ensemble des modes possibles
possibles_modes = {"mono", "multi"}
@app.route('/check_possible', methods=['GET'])
def check_possible():
    global CONNECTED_PLC
    try:
        plc = snap7.client.Client()
        plc.connect(ip, 0, 1)  # IP address, rack, slot
        CONNECTED_PLC = plc
        return jsonify(message=f"API connecté"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/multi/<string:BOOL>', methods=['GET'])
def multi(BOOL):
    global CONNECTED_PLC
    try:
        if BOOL == "True":
            commS7.writeMemory(CONNECTED_PLC, "Mx_master_multi_possible", True)
        else:
            commS7.writeMemory(CONNECTED_PLC, "Mx_master_multi_possible", False)

        return jsonify(message=f"Mode multi activé"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500



@app.route('/sortie/<string:request>', methods=['GET'])
def demande_multi(request):
    global CONNECTED_PLC
    try:
        commS7.writeMemory(CONNECTED_PLC, request, True)
    except Exception as e :
        return jsonify(error=str(e)), 500
    

@app.route('/trigger/<string:request>', methods=['GET'])
def trigger(request):
    global CONNECTED_PLC
    try:
        valeur = commS7.readMemory(CONNECTED_PLC, request)
        if valeur:
            return jsonify(message=f"{valeur}"), 200
        else :
            return jsonify(message=f"{valeur}"), 300
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/multinbr/<string:BOOL>', methods=['GET'])
def multinbr(BOOL):
    global CONNECTED_PLC
    try:
        if BOOL == "True":
            commS7.writeMemory(CONNECTED_PLC, "Mx_master_multi+de3", True)
        else:
            commS7.writeMemory(CONNECTED_PLC, "Mx_master_multi+de3", False)

        return jsonify(message=f"Mode multi activé"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/compteur_bille', methods=['GET'])
def compteur_bille():
    global CONNECTED_PLC
    storage = []
    for name in var_api_out:
        try:
            storage.append(commS7.readMemory(CONNECTED_PLC, name))
        except Exception as e:
            return jsonify(error=str(e)), 500
    return jsonify(storage), 200


@app.route('/compteur_bille/<int:val>', methods=['GET'])
def set_compteur_bille(val):
    global CONNECTED_PLC
    try:
        for name in var_api_in:
            commS7.writeMemory(CONNECTED_PLC, name, val)
        return jsonify(message=f"Valeur de compteur bille modifiée"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/deconnection', methods=['GET'])
def deconnection():
    global CONNECTED_PLC
    try:
        CONNECTED_PLC.destroy()
        CONNECTED_PLC = None
        return jsonify(message=f"API déconnecté"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

# Gestionnaires d'erreur
@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Non trouve"), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="Erreur interne du serveur"), 500


# Point d'entrée principal pour exécuter l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)