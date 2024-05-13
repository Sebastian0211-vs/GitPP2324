#-*- coding: utf-8 -*-
import snap7
import re
import variablesAPI # Assuming you named the module like this

"""
plc_ip_addresses = ['172.16.2.80']
plcs = []

for ip_address in range(len(plc_ip_addresses)):
	plcs.append(snap7.client.Client())
	plcs[ip_address].connect(plc_ip_addresses[ip_address], 0, 1)  # IP address, rack, slot
"""

BYTE_LENGTH = 1
WORD_LENGTH = 2  # Bytes / Word, Int
DOUBLE_WORD_LENGTH = 4  # Bytes / DWord, Real, IEC Time
BYTE_START_OFFSET = 0
NO_DB = 0

"""
def connection(ip_address):
	client = snap7.client.Client()
	print(f"Client: {client}")
	error = client.connect(ip_address, 0, 1) # IP address, rack, slot
	print(f"Connection error: {error}")

def deconnection(client):
	client.destroy()
"""

def getLength(type):
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
			print("Invalid type")

def extract_numbers(logical_address):
	# Using regular expression to find numbers
	numbers = re.findall(r'\d+', logical_address)
	return [int(number) for number in numbers] if numbers else None # Return the list of numbers, or None if no number is found

# TODO Finish
def readMemory(plc, variable):
	type = variablesAPI.variables[variable]["Data Type"]
	length = getLength(type)
	#print(f"length: {length}")
	logical_address = variablesAPI.variables[variable]["Logical Address"]
	address = extract_numbers(logical_address)
	start_address = address[0] if address != None else None
	#print(f"start_address: {start_address}")
	bit_offset = address[1] if len(address) == 2 else 0
	#print(f"bit_offset: {bit_offset}")

	reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)
	match type:
		case "Bool": 
			value = snap7.util.get_bool(reading, BYTE_START_OFFSET, bit_offset)
			return value
		
		case "Int": 
			#value = int.from_bytes(reading, byteorder='big', signed=True)
			value = snap7.util.get_int(reading, BYTE_START_OFFSET)
			return value
				
		case "Byte": 
			value = reading
			return value
		
		case "Time": 
			# TODO Useful ???
			value = int.from_bytes(reading, byteorder='big', signed=False)
			ms = value
			s = ms // 1000
			ms %= 1000
			min = s // 60
			s %= 60
			h = min // 60
			min %= 60
			print(f"{h}h {min}min {s}s {ms}ms")
			value = snap7.util.get_time(reading, BYTE_START_OFFSET)
			return value
			
		case _: 
			print("Invalid type")
			return None

# TODO Finish
def writeMemory(plc, variable, value):
	type = variablesAPI.variables[variable]["Data Type"]
	length = getLength(type)
	logical_address = variablesAPI.variables[variable]["Logical Address"]
	address = extract_numbers(logical_address)
	start_address = address[0] if address != None else None
	bit_offset = address[1] if len(address) == 2 else 0

	reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)
	match type:
		case "Bool":
			snap7.util.set_bool(reading, BYTE_START_OFFSET, bit_offset, value)   
			plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, reading)

		case "Byte": # Useful ???
			plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)

		case "Int":
			value = value.to_bytes(length, byteorder='big')
			plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)
			#snap7.util.set_int(reading, BYTE_START_OFFSET, value)

		case "Time":
			# TODO when format decided
			snap7.util.set_time(reading, BYTE_START_OFFSET, value)  # value's format: '22:3:57:28.192'

		case _:
			print("Invalid type")

"""
for plc in plcs:
	print("-----------------------------------------------")
	readMemory(plc, "Mw_API_CVEntree")
"""
