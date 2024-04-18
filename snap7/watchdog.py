#-*- coding: utf-8 -*-
import requests

while True:
    """Appel de toutes les valeurs nécessaires"""
    response = requests.get("http://localhost:5000/api/mono")

    """Watchdog"""
    nbr_billes_entree_chassis = 0
    nbr_billes_sortie_chassis = 0
    nbr_billes_secours_chassis = 0

    nbr_billes_entree_cell1 = 0
    nbr_billes_entree_cell2 = 0
    nbr_billes_entree_cell3 = 0
    nbr_billes_entree_cell4 = 0

    if (nbr_billes_secours_chassis > 0):
        print("Problème")

    