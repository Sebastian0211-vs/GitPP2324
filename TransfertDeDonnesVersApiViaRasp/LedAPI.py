import snap7
from snap7.util import set_bool

ip = '192.168.1.100'  # Adresse IP de l'automate
rack = 0  # Rack de l'automate
slot = 1  # Slot de l'automate

client = snap7.client.Client()
client.connect(ip, rack, slot)

# Exemple : écriture dans une zone de mémoire (M) pour simuler une entrée
db_number = 1  # Numéro de bloc de données utilisé pour la simulation
start = 0  # Position de départ dans le bloc de données
size = 1  # Taille des données à écrire (1 octet pour un booléen)
data = bytearray(size)
set_bool(data, 0, 0, True)  # Simulation de l'entrée comme étant "active"

client.db_write(db_number, start, data)  # Écriture dans le bloc de données

client.disconnect()
