#-*- coding: utf-8 -*-
import snap7  # Import Snap7 library to handle communication with Siemens PLCs
import re     # Import regex module for string operations
import variablesAPI

# Sample test block to check connectivity and basic operations outside the main project
"""
plc_ip_addresses = ['172.16.2.80']  # List of PLC IP addresses
plcs = []  # List to store Snap7 client objects

for ip_address in range(len(plc_ip_addresses)):
    plcs.append(snap7.client.Client())  # Create a new Snap7 client
    plcs[ip_address].connect(plc_ip_addresses[ip_address], 0, 1)  # Connect to the PLC at the given IP, rack, and slot
"""

# Constants for different data types' lengths
BYTE_LENGTH = 1  # Length of a Byte
WORD_LENGTH = 2  # Length of a Word (2 Bytes) for Word, Int
DOUBLE_WORD_LENGTH = 4  # Length of a Double Word (4 Bytes) for DWord, Real, IEC Time
BYTE_START_OFFSET = 0  # Starting byte offset for bit extraction
NO_DB = 0  # No specific DB (used for certain read/write areas)

def getLength(type):
    """ Determine and return the length of the PLC data type """
    match type:
        case "Bool": 
            return BYTE_LENGTH
        case "Int": 
            return WORD_LENGTH
        case "Word": 
            return WORD_LENGTH
        case "Byte": 
            return DOUBLE_WORD_LENGTH
        case "Time": 
            return DOUBLE_WORD_LENGTH
        case _: 
            print("Invalid type")  # Handle unexpected type input

def extract_numbers(logical_address):
    """ Extract numerical values from a logical address string using regular expressions """
    numbers = re.findall(r'\d+', logical_address)
    return [int(number) for number in numbers] if numbers else None  # Convert found numbers to integers and return the list, or return None

""" Function to read memory from PLC, given a variable name """
def readMemory(plc, variable):
    type = variablesAPI.variables[variable]["Data Type"]  # Get the data type of the variable from the API
    length = getLength(type)  # Get the length of the data based on its type
    logical_address = variablesAPI.variables[variable]["Logical Address"]  # Get the logical address of the variable
    address = extract_numbers(logical_address)  # Extract numerical address
    start_address = address[0] if address != None else None  # Determine the start address
    bit_offset = address[1] if len(address) == 2 else 0  # Determine the bit offset if available

    reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)  # Read data from PLC
    match type:
        case "Bool": 
            value = snap7.util.get_bool(reading, BYTE_START_OFFSET, bit_offset)  # Get boolean value from the data
            return value
        case "Int": 
            value = snap7.util.get_int(reading, BYTE_START_OFFSET)  # Get integer value from the data
            return value
        case "Byte": 
            return reading  # Return raw byte data
        case "Time": 
            # Interpret bytes as time, displaying hours, minutes, seconds, milliseconds
            value = snap7.util.get_time(reading, BYTE_START_OFFSET)  # Use snap7 utility to parse time
            return value
        case _: 
            print("Invalid type")
            return None

""" Function to write memory to PLC, given a variable name and a value to write """
def writeMemory(plc, variable, value):
    type = variablesAPI.variables[variable]["Data Type"]  # Get the data type of the variable from the API
    length = getLength(type)  # Get the length of the data based on its type
    logical_address = variablesAPI.variables[variable]["Logical Address"]  # Get the logical address of the variable
    address = extract_numbers(logical_address)  # Extract numerical address
    start_address = address[0] if address != None else None  # Determine the start address
    bit_offset = address[1] if len(address) == 2 else 0  # Determine the bit offset if available

    reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)
    match type:
        case "Bool":
            snap7.util.set_bool(reading, BYTE_START_OFFSET, bit_offset, value)  # Set boolean value in the data
            plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, reading)  # Write back the modified data
        case "Byte":
            plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)  # Write byte data directly
        case "Int":
            value = value.to_bytes(length, byteorder='big')  # Convert integer to bytes
            plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)  # Write integer data
        case "Time":
            # Set and write time data after deciding on the format
            snap7.util.set_time(reading, BYTE_START_OFFSET, value)  # Set time data
        case _:
            print("Invalid type")

# Uncomment for functional testing of reading from configured PLCs
"""
for plc in plcs:
    print("-----------------------------------------------")
    readMemory(plc, "Mw_API_CVEntree")
"""
