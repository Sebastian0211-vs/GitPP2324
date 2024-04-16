#-*- coding: utf-8 -*-
import snap7
from flask import Flask, jsonify
import CommunicationAPIS7 as commS7

# Initialisation de l'application Flask
app = Flask(__name__)

"""Adresses IP des APIs:"""
plcs_ip_addresses = {
    "Cellule1": {"ip": '172.16.x.x'},
    "Cellule2": {"ip": '172.16.x.x'},
    "Cellule3": {"ip": '172.16.x.x'},
    "Cellule4": {"ip": '172.16.x.x'},
    "Cellule5": {"ip": '172.16.x.x'},
    "Cellule6": {"ip": '172.16.x.x'},
    "Cellule7": {"ip": '172.16.x.x'},
    "Cellule8": {"ip": '172.16.x.x'},
    "Cellule9": {"ip": '172.16.x.x'},
    "Cellule10": {"ip": '172.16.x.x'},
    "Cellule11": {"ip": '172.16.x.x'},
    "Cellule12": {"ip": '172.16.x.x'},
    "Cellule13": {"ip": '172.16.x.x'},
}

"""
DATABASES dans les APIs:
1 - ...
2 - ...
3 - ...
"""

# This is a test
test_connected_plcs_ip_addresses = []
test_plcs = []

for ip_address in range(len(plcs_ip_addresses)):
    test_connected_plcs_ip_addresses.append(plcs_ip_addresses[ip_address]["ip"])
    test_plcs.append(snap7.client.Client())

for plc in test_plcs:
    id = test_plcs.index(plc)
    if (not plc.get_connected()):
        plc.destroy()
        print(f"No connection with PLC - {test_plcs[id]}")
        test_connected_plcs_ip_addresses.pop(id)
        test_plcs.pop(id)
    else:
        plc.connect(test_connected_plcs_ip_addresses[id], 0, 1)  # IP address, rack, slot
        print(f"Connection with PLC - {test_connected_plcs_ip_addresses[id]} - OK")
# End of test

connected_plcs_ip_addresses = ['172.16.40.95']
plcs = []

# Ensemble des modes possibles
possibles_modes = {"Mono", "Multi"}

for ip_address in range(len(connected_plcs_ip_addresses)):
	plcs.append(snap7.client.Client())
	plcs[ip_address].connect(connected_plcs_ip_addresses[ip_address], 0, 1)  # IP address, rack, slot

# Does not work - TODO Try to use before client.connect()
for plc in plcs:
	id = plcs.index(plc)
	if (not plc.get_connected()):
		print(f"Connection lost with PLC - {connected_plcs_ip_addresses[id]}")
	else:
		print(f"Connection with PLC - {connected_plcs_ip_addresses[id]} - OK")

@app.route('/api/<string:mode>', methods=['GET'])
def setMode(mode):
    """Changer le mode de fonctionnement des chassis."""
    try:
        if mode in possibles_modes:
            commS7.writeBool(plcs[0], 3, 0, 1, 1)
            print("Le mode a été changé")
            return jsonify(message=f"Chassis en mode {mode}"), 200
        else:
            return jsonify(error="Mode invalide"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# Gestionnaires d'erreur
@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Non trouvé"), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="Erreur interne du serveur"), 500

# Point d'entrée principal pour exécuter l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)