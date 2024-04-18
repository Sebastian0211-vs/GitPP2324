#-*- coding: utf-8 -*-
import snap7
from flask import Flask, jsonify
import CommunicationAPIS7 as commS7
#import ip_addresses


# Initialisation de l'application Flask
app = Flask(__name__)

"""Adresses IP des APIs:"""
plcs_ip_addresses = [
    ["Cellule1", '172.16.40.95'],
    ["Cellule2", '172.16.x.x'],
    ["Cellule3", '172.16.x.x'],
    ["Cellule4", '172.16.x.x'],
    ["Cellule5", '172.16.x.x'],
    ["Cellule6", '172.16.x.x'],
    ["Cellule7", '172.16.x.x'],
    ["Cellule8", '172.16.x.x'],
    ["Cellule9", '172.16.x.x'],
    ["Cellule10", '172.16.x.x'],
    ["Cellule11", '172.16.x.x'],
    ["Cellule12", '172.16.x.x'],
    ["Cellule13", '172.16.x.x']
]

"""
DATABASES dans les APIs:
1 - ...
2 - ...
3 - ...
"""

connected_plcs_ip_addresses = []
plcs = []

# TODO change ip_address to iterator -> See hermes.py
nbr_plcs = len(plcs_ip_addresses)
ip_address = 0
while (ip_address < nbr_plcs):
    try:
        print(ip_address)
        connected_plcs_ip_addresses.append(plcs_ip_addresses[ip_address][1])
        plcs.append(snap7.client.Client())
        plcs[ip_address].connect(connected_plcs_ip_addresses[ip_address], 0, 1)
    except Exception as e:
        connected_plcs_ip_addresses.pop(ip_address)
        plcs.pop(ip_address)
        ip_address -= 1
        nbr_plcs -= 1

    ip_address += 1

# Does not work -> Why ???
"""
for plc in test_plcs:
    id = test_plcs.index(plc)
    print(plc.get_connected())
    if (not plc.get_connected()):
        plc.destroy()
        print(f"No connection with PLC - {test_plcs[id]}")
        test_connected_plcs_ip_addresses.pop(id)
        test_plcs.pop(id)
    else:
        plc.connect(test_connected_plcs_ip_addresses[id], 0, 1)  # IP address, rack, slot
        print(f"Connection with PLC - {test_connected_plcs_ip_addresses[id]} - OK")
"""

print()
print(connected_plcs_ip_addresses)
print()
print(plcs)

# Ensemble des modes possibles
possibles_modes = {"mono", "multi"}

@app.route('/api/<string:mode>', methods=['GET'])
def setMode(mode):
    """Changer le mode de fonctionnement des chassis."""
    try:
        if mode in possibles_modes:
            match mode:
                case "mono":
                    print("Le mode a été changé en mono")
                    commS7.writeBool(plcs[0], 3, 0, 1, 0)
                case "multi":
                    print("Le mode a été changé en multi")
                    commS7.writeBool(plcs[0], 3, 0, 1, 1)
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