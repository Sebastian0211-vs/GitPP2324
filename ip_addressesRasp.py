#-*- coding: utf-8 -*-

from mysql.connector import connect  # Imports the connect function from mysql.connector module for database connections
import json  # Imports the json module for parsing and generating JSON data
 

with open('/home/pi/Desktop/configHermes.json', 'r') as config_file:  # Opens the file in read mode
    config = json.load(config_file)  # Loads the JSON content and converts it into a Python dictionary


# Define a connection object
conn = connect(
      user=config['Login_Turtle']['user'],
      password=config['Login_Turtle']['password'],
      host=config['Login_Turtle']['host'],
      database=config['Login_Turtle']['database'])


cursor = conn.cursor()  # Create a cursor object to execute SQL queries.

cursor.execute("SELECT API from chassis")
api_results = cursor.fetchall()
IP1api = api_results[0][0]
IP2api = api_results[1][0]
IP3api = api_results[2][0]




cursor.execute("SELECT raspCatch from chassis")
raspCatch_results = cursor.fetchall()
IP1raspCatch = raspCatch_results[0][0]
IP2raspCatch = raspCatch_results[1][0]
IP3raspCatch = raspCatch_results[2][0]

cursor.close()  # Close the cursor after completing all the SQL queries to release database resources.

# IP addresses' dictionnary
ip_addresses = {
    "Chassis1": {"API":IP1api, "RASP_catch": IP1raspCatch},
    "Chassis2": {"API":IP2api, "RASP_catch": IP2raspCatch},
    "Chassis3": {"API":IP3api, "RASP_catch": IP3raspCatch},
    
}

# Display informations
print(ip_addresses)

print("+------------------------------------------------+")

print("IP1api : ", IP1api)
print("IP2api : ", IP2api)
print("IP3api : ", IP3api)



print("+------------------------------------------------+")

print("IP1raspCatch : ", IP1raspCatch)
print("IP2raspCatch : ", IP2raspCatch)
print("IP3raspCatch : ", IP3raspCatch)


# Close the database connection
conn.commit()
conn.close()