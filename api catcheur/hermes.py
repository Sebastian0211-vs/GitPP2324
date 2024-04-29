#-*- coding: utf-8 -*-
import asyncio
#from asyncua import Client, ua
from flask import Flask, jsonify
import S7_modul as commS7
import ip_addresses as ip
import requests

CONNECTED_PLC = ""

var_api_out = ["Mw_API_CVSortieStandard","Mw_API_CVSortieSecours","Mw_API_CVEntree"]

var_api_in = ["Mw_master_nb_billes_sortie_normal","Mw_master_nb_billes_sortie_secours","Mw_master_nb_billes_entree"]

app = Flask(__name__)
@app.route('/API_IP/<string:ip>', methods=['GET'])
async def API_IP(ip):
    global CONNECTED_PLC 
    CONNECTED_PLC = ip
    return jsonify(message=f"API IP: {ip}"), 200

# Ensemble des modes possibles
possibles_modes = {"mono", "multi"}
@app.route('/check_possible', methods=['GET'])
async def check_possible():
    try:
        client = await commS7.connection(CONNECTED_PLC)
        await commS7.disconnection(client)
        return jsonify(message=f"API connecté"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/multi/<string:BOOL>', methods=['GET'])
async def multi(BOOL):
    try:
        client = await commS7.connection(CONNECTED_PLC)
        variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_master_multi_possible")
        if BOOL == "True":
            await commS7.writeValue(variable, True)
        else:
            await commS7.writeValue(variable, False)
        await commS7.disconnection(client)
        return jsonify(message=f"Mode multi activé"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500



@app.route('/sortie/<string:request>', methods=['GET'])
async def demande_multi(request):
    try:
        client = await commS7.connection(CONNECTED_PLC)
        variable = await commS7.getVariable(client, commS7.NAMESPACE, request)
        await commS7.writeValue(variable, True)
        await commS7.disconnection(client)
    except Exception as e :
        return jsonify(error=str(e)), 500
    

@app.route('/trigger/<string:request>', methods=['GET'])
async def trigger(request):
    try:
        client = await commS7.connection(CONNECTED_PLC)
        variable = await commS7.getVariable(client, commS7.NAMESPACE, request)

        valeur = await commS7.readValue(variable)
        await commS7.disconnection(client)
        if valeur:
            return jsonify(message=f"{valeur}"), 200
        else :
            return jsonify(message=f"{valeur}"), 300
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/multinbr/<string:BOOL>', methods=['GET'])
async def multinbr(BOOL):
    try:
        client = await commS7.connection(CONNECTED_PLC)
        variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_master_multi+de3")
        if BOOL == "True":
            await commS7.writeValue(variable, True)
        else:
            await commS7.writeValue(variable, False)
        await commS7.disconnection(client)
        return jsonify(message=f"Mode multi activé"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500



@app.route('/compteur_bille', methods=['GET'])
async def compteur_bille():
    storage = []
    for name in var_api_out:
        try:
            client = await commS7.connection(CONNECTED_PLC)
            variable = await commS7.getVariable(client, commS7.NAMESPACE, name)
            storage.append(await commS7.readValue(variable))
            await commS7.disconnection(client)
        except Exception as e:
            return jsonify(error=str(e)), 500
    return jsonify(storage), 200


@app.route('/compteur_bille/<int:val>', methods=['GET'])
async def set_compteur_bille(val):
    try:
        client = await commS7.connection(CONNECTED_PLC)
        for name in var_api_in:
            variable = await commS7.getVariable(client, commS7.NAMESPACE, name)
            await commS7.writeValue(variable, val)
        await commS7.disconnection(client)
        return jsonify(message=f"Valeur de compteur bille modifiée"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/resetConnections', methods=['GET'])
async def resetConnections():
    """Scanner et enregistrer les apis connectés"""
    try:
        await initialisation()
        return jsonify(message=f"Liste des apis connectés réinitialisée"), 200
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