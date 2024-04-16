#-*- coding: utf-8 -*-
import snap7
from flask import Flask, jsonify
#import CommunicationAPIS7 as commS7

# Initialisation de l'application Flask
app = Flask(__name__)

WORD_LENGTH = 2  # Bytes / Word, Int
DOUBLE_WORD_LENGTH = 4  # Bytes / DWord, Real, IEC Time
BYTE_START_OFFSET = 0
NO_DB = 0

"""
DATABASES dans les APIs:
1 - ...
2 - ...
3 - ...
"""

plc_ip_addresses = []
plcs = []

# Ensemble des modes possibles
possibles_modes = {"Mono", "Multi"}

""" To test without a plc
for ip_address in range(len(plc_ip_addresses)):
    plcs[ip_address] = snap7.client.Client()
    plcs[ip_address].connect(plc_ip_addresses[ip_address], 0, 1)  # IP address, rack, slot

for plc in plcs:
    if (not plc.get_connected()):
        print(f"Connection lost with PLC - {plc}")
"""

@app.route('/api/<string:mode>', methods=['GET'])
def setMode(mode):
    """Changer le mode de fonctionnement des chassis."""
    try:
        if mode in possibles_modes:
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