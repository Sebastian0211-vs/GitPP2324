#-*- coding: utf-8 -*-
import asyncio
#from asyncua import Client, ua
from flask import Flask, jsonify
import S7_modul as commS7
import ip_addresses as ip

"""Dictionnary: Plc_Name -> Access Url"""
CONNECTED_PLCS = {}

async def initialisation():
    iterator = 0
    for value in ip.PLCS_IP_ADDRESSES.values():
        try:
            url = commS7.DEBUT_URL + str(value) + commS7.PORT
            print(value)
            #try:
            client = await commS7.connection(url)
            CONNECTED_PLCS[list(ip.PLCS_IP_ADDRESSES.keys())[iterator]] = url
            await commS7.disconnection(client)
            #except Exception as e:
            #    print("Error1")
        except Exception as e:
            print("Error2")

        iterator += 1
    print(CONNECTED_PLCS)

asyncio.run(initialisation())

app = Flask(__name__)

# Ensemble des modes possibles
possibles_modes = {"mono", "multi"}

@app.route('/<string:plc>/<string:mode>', methods=['GET'])
async def setMode(plc, mode):
    """Changer le mode de fonctionnement des chassis."""
    try:
        if mode in possibles_modes:
            match mode:
                case "mono":
                    print("Le mode a été changé en mono")
                    #client = await commS7.connection("opc.tcp://172.16.40.95:4840")
                    client = await commS7.connection(CONNECTED_PLCS[plc])
                    variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_IntTest")
                    await commS7.writeValue(variable, 0)
                    await commS7.disconnection(client)
                case "multi":
                    print("Le mode a été changé en multi")
                    client = await commS7.connection(CONNECTED_PLCS[plc])
                    variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_IntTest")
                    await commS7.writeValue(variable, 1)
                    await commS7.disconnection(client)
            
            return jsonify(message=f"Chassis en mode {mode}"), 200
        else:
            return jsonify(error="Mode invalide"), 404
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