#-*- coding: utf-8 -*-
import asyncio
from asyncua import Client, ua
from flask import Flask, jsonify
import S7_modul as commS7
import ip_addresses as ip

connected_plcs_ip_addresses = []
plcs = []

async def initialisation():
    nbr_plcs = len(ip.PLCS_IP_ADDRESSES)
    iterator = 0
    ip_address = 0
    while (iterator < nbr_plcs):
        try:
            url = commS7.DEBUT_URL + str(ip.PLCS_IP_ADDRESSES[ip_address][1]) + commS7.PORT
            print(ip.PLCS_IP_ADDRESSES[ip_address][1])
            connected_plcs_ip_addresses.append(ip.PLCS_IP_ADDRESSES[ip_address][1])
            try:
                client = await commS7.connection(url)
                plcs.append(client)
            except Exception as e:
                print("Error1")
                connected_plcs_ip_addresses.pop(iterator)
                #plcs.pop(iterator)
                iterator -= 1
                nbr_plcs -= 1
            #plcs.append(client)
            #plcs[ip_address].connect(connected_plcs_ip_addresses[ip_address], 0, 1)
        except Exception as e:
            print("Error2")
            connected_plcs_ip_addresses.pop(iterator)
            plcs.pop(iterator)
            iterator -= 1
            nbr_plcs -= 1

        iterator += 1
        ip_address += 1

asyncio.run(initialisation())

app = Flask(__name__)

# Ensemble des modes possibles
possibles_modes = {"mono", "multi"}

@app.route('/<string:plc>/<string:mode>', methods=['GET'])
async def setMode(mode):
    """Changer le mode de fonctionnement des chassis."""
    try:
        if mode in possibles_modes:
            match mode:
                case "mono":
                    print("Le mode a été changé en mono")
                    #client = await commS7.connection(commS7.URL)
                    variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_IntTest")
                    await commS7.writeValue(variable, 0)
                    await commS7.disconnection(client)
                case "multi":
                    print("Le mode a été changé en multi")
                    #client = await commS7.connection(commS7.URL)
                    variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_IntTest")
                    await commS7.writeValue(variable, 1)
                    await commS7.disconnection(client)
            return jsonify(message=f"Chassis en mode {mode}"), 200
        else:
            return jsonify(error="Mode invalide"), 404
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