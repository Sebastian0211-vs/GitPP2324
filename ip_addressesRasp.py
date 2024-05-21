#-*- coding: utf-8 -*-

from mysql.connector import connect  # Imports the connect function from mysql.connector module for database connections
import json  # Imports the json module for parsing and generating JSON data
 

def fetch_latest_ip_addresses():
    with open('/home/pi/Desktop/configHermes.json', 'r') as config_file:  # Opens the file in read mode
        config = json.load(config_file)  # Loads the JSON content and converts it into a Python dictionary


    # Define a connection object
    conn = connect(
        user=config['Login_Turtle']['user'],
        password=config['Login_Turtle']['password'],
        host=config['Login_Turtle']['host'],
        database=config['Login_Turtle']['database'])


    cursor = conn.cursor()  # Create a cursor object to execute SQL queries.

    cursor.execute("SELECT * from chassis")
    # fetch the db results in a dictionary
    dico = {}
    for row in cursor.fetchall():
        dico[f"Chassis{row[0]}"] = {"API": row[3], "RASP_catch": row[1]}


    print(dico)

    # Close the database connection
    conn.commit()
    conn.close()

    return dico