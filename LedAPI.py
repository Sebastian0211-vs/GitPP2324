import snap7
from snap7.util import *
from time import sleep

# Paramètres de connexion à l'API
ip = '192.168.1.100'  # IP de l'API
rack = 0  # Rack de l'API
slot = 1  # Slot de l'API

# Adresse de la LED
byte_index = 0  # Index du byte dans le bloc de données ou espace IO
bit_index = 0  # Index du bit correspondant à la LED

# Créer une connexion au PLC
client = snap7.client.Client()
client.connect(ip, rack, slot)

try:
    while True:
        # Lire l'état actuel de la LED
        state = client.read_area(snap7.types.Areas.MK, 0, byte_index, 1)
        bit_status = get_bool(state, 0, bit_index)
        
        # Inverser l'état de la LED
        new_state = not bit_status
        set_bool(state, 0, bit_index, new_state)
        client.write_area(snap7.types.Areas.MK, 0, byte_index, state)
        
        # Attendre avant de changer à nouveau l'état
        sleep(1)  # Délai de 1 seconde
finally:
    client.disconnect()
