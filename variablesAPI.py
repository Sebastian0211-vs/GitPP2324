#-*- coding: utf-8 -*-
""" Define a dictionary called 'variables' to store PLC variables and their properties """
variables = {
    # Integer type variables with their logical addresses in the PLC
    "Mw_API_CVEntree": {"Data Type": "Int", "Logical Address": "%MW506"},
    "Mw_API_CVSortieStandard": {"Data Type": "Int", "Logical Address": "%MW508"},
    "Mw_API_CVSortieSecours": {"Data Type": "Int", "Logical Address": "%MW510"},
    "Mw_master_nb_billes_entree": {"Data Type": "Int", "Logical Address": "%MW500"},
    "Mw_master_nb_billes_sortie_normal": {"Data Type": "Int", "Logical Address": "%MW502"},
    "Mw_master_nb_billes_sortie_secours": {"Data Type": "Int", "Logical Address": "%MW504"},

    # Boolean type variables for control, indication, and alarms with their specific bit addresses in the PLC
    "Mx_master_start": {"Data Type": "Bool", "Logical Address": "%M320.1"},
    "Mx_master_pause": {"Data Type": "Bool", "Logical Address": "%M320.0"},
    "Mx_master_multi_possible": {"Data Type": "Bool", "Logical Address": "%M320.2"},
    "Mx_master_multi+de3": {"Data Type": "Bool", "Logical Address": "%326.2"},
    "Mx_master_demande_multi": {"Data Type": "Bool", "Logical Address": "%M301.6"},
    "Mx_master_alarme_urgence": {"Data Type": "Bool", "Logical Address": "%M325.0"},
    "Mx_master_quittance_obstruation": {"Data Type": "Bool", "Logical Address": "%M325.3"},
    "Mx_master_quittance_urgence": {"Data Type": "Bool", "Logical Address": "%M325.1"},
    "Mx_master_connecte": {"Data Type": "Bool", "Logical Address": "%M310.0"},
    "Mx_master_alarme_obstruation": {"Data Type": "Bool", "Logical Address": "%M325.3"},
    "Mx_master_quittance_distribution": {"Data Type": "Bool", "Logical Address": "%M325.5"},
    "Mx_master_quittance_sortie_secours": {"Data Type": "Bool", "Logical Address": "%M325.7"},
    "Mx_master_alarme_surveillance_bille": {"Data Type": "Bool", "Logical Address": "%M326.0"},
    "Mx_master_quittance_surveillance_bille": {"Data Type": "Bool", "Logical Address": "%M326.1"},

    # Boolean type variables for specific alerts and warnings for control areas with their specific bit addresses
    "Mx_API_C1_attention": {"Data Type": "Bool", "Logical Address": "%M135.4"},
    "Mx_API_C1_alerte": {"Data Type": "Bool", "Logical Address": "%M135.0"},
    "Mx_API_C2_attention": {"Data Type": "Bool", "Logical Address": "%M135.5"},
    "Mx_API_C2_alerte": {"Data Type": "Bool", "Logical Address": "%M135.1"},
    "Mx_API_C3_attention": {"Data Type": "Bool", "Logical Address": "%M135.6"},
    "Mx_API_C3_alerte": {"Data Type": "Bool", "Logical Address": "%M135.2"},
    "Mx_API_C4_attention": {"Data Type": "Bool", "Logical Address": "%M135.7"},
    "Mx_API_C4_alerte": {"Data Type": "Bool", "Logical Address": "%M135.3"},
}

"""
This script initializes a dictionary storing metadata about PLC variables which can be used 
for reading from and writing to the PLC in automation systems. Each entry includes the variable's data type and 
its logical address in the memory of the PLC, necessary for data manipulation tasks.
"""
