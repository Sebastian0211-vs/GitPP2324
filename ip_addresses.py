#-*- coding: utf-8 -*-


# import the connect method 
from mysql.connector import connect
import json
 

with open('configHermes.json', 'r') as config_file:
    config = json.load(config_file)


# define a connection object
conn = connect(
      user=config['Login_Turtle']['user'],
      password=config['Login_Turtle']['password'],
      host=config['Login_Turtle']['host'],
      database=config['Login_Turtle']['database'])



cursor = conn.cursor()
cursor.execute("SELECT API from chassis")
api_results = cursor.fetchall()
IP1api = api_results[0][0]
IP2api = api_results[1][0]
IP3api = api_results[2][0]

cursor.execute("SELECT raspLED from chassis")
raspLED_results = cursor.fetchall()
IP1raspLED = raspLED_results[0][0]
IP2raspLED = raspLED_results[1][0]
IP3raspLED = raspLED_results[2][0]

cursor.execute("SELECT raspCatch from chassis")
raspCatch_results = cursor.fetchall()
IP1raspCatch = raspCatch_results[0][0]
IP2raspCatch = raspCatch_results[1][0]
IP3raspCatch = raspCatch_results[2][0]


cursor.close()

# Dictionnary: Plc_Name -> IP Address
ip_addresses = {
    "Chassis1": {"API":IP1api, "RASP_catch": IP1raspCatch, "RASP_LED": IP1raspLED},
    "Chassis2": {"API":IP2api, "RASP_catch": IP2raspCatch, "RASP_LED": IP2raspLED},
    "Chassis3": {"API":IP3api, "RASP_catch": IP3raspCatch, "RASP_LED": IP3raspLED},
    
}

print(ip_addresses)

print("+------------------------------------------------+")

print("IP1api : ", IP1api)
print("IP2api : ", IP2api)
print("IP3api : ", IP3api)

print("+------------------------------------------------+")

print("IP1raspLED : ", IP1raspLED)
print("IP2raspLED : ", IP2raspLED)
print("IP3raspLED : ", IP3raspLED)

print("+------------------------------------------------+")

print("IP1raspCatch : ", IP1raspCatch)
print("IP2raspCatch : ", IP2raspCatch)
print("IP3raspCatch : ", IP3raspCatch)


# close the database connection
conn.commit()
conn.close()