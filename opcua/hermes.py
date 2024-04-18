#-*- coding: utf-8 -*-
import asyncio
from asyncua import Client, ua
from flask import Flask, jsonify
import S7_modul as commS7
import ip_addresses as ip

#connected_plcs_ip_addresses = []
#plcs = []
connected_plcs = {}

async def initialisation():
    #nbr_plcs = len(ip.PLCS_IP_ADDRESSES)
    iterator = 0
    #list_of_value = list(ip.PLCS_IP_ADDRESSES.values())
    for value in ip.PLCS_IP_ADDRESSES.values():
        try:
            #position = list_of_value.index(value)
            url = commS7.DEBUT_URL + str(value) + commS7.PORT
            print(value)
            #connected_plcs_ip_addresses.append(value)
            try:
                client = await commS7.connection(url)
                #connected_plcs[list(ip.PLCS_IP_ADDRESSES.keys())[iterator]] = client
                connected_plcs[list(ip.PLCS_IP_ADDRESSES.keys())[iterator]] = url
                #plcs.append(client)
                #connected_plcs_ip_addresses.append(value)
                # TODO try with disconnection(client)
                await commS7.disconnection(connected_plcs[list(ip.PLCS_IP_ADDRESSES.keys())[iterator]])
            except Exception as e:
                print("Error1")
                #connected_plcs_ip_addresses.pop(iterator)
                #iterator -= 1
                #nbr_plcs -= 1
        except Exception as e:
            print("Error2")
            #connected_plcs_ip_addresses.pop(iterator)
            #plcs.pop(iterator)
            #iterator -= 1
            #nbr_plcs -= 1

        iterator += 1
        #ip_address += 1
    print(connected_plcs)

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
                    client = await commS7.connection(connected_plcs[plc])
                    variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_IntTest")
                    await commS7.writeValue(variable, 0)
                    print("SALUT")
                    await commS7.disconnection(client)
                case "multi":
                    print("Le mode a été changé en multi")
                    client = await commS7.connection(connected_plcs[plc])
                    variable = await commS7.getVariable(client, commS7.NAMESPACE, "Mx_IntTest")
                    await commS7.writeValue(variable, 1)
                    print("SALUT")
                    #await commS7.disconnection(connected_plcs[plc])
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