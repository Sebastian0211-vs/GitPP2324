#-*- coding: utf-8 -*-
import snap7
import re
import variablesAPI

"""
plc_ip_addresses = ['172.16.40.95',
					'172.16.40.96']
plcs = []

for ip_address in range(len(plc_ip_addresses)):
	plcs.append(snap7.client.Client())
	plcs[ip_address].connect(plc_ip_addresses[ip_address], 0, 1)  # IP address, rack, slot

# Does not work
for plc in plcs:
	id = plcs.index(plc)
	if (not plc.get_connected()):
		print(f"Connection lost with PLC - {plc_ip_addresses[id]}")
	else:
		print(f"Connection with PLC - {plc_ip_addresses[id]} - OK")

db_number = 3
start_offset = 0
bit_offset = 0
value = 1  # 1 = true | 0 = false
"""

BYTE_LENGTH = 1
WORD_LENGTH = 2  # Bytes / Word, Int
DOUBLE_WORD_LENGTH = 4  # Bytes / DWord, Real, IEC Time
BYTE_START_OFFSET = 0
NO_DB = 0

def writeBool(plc, db_number, start_address, bit_offset, value):
	reading = plc.db_read(db_number, start_address, 1)    # (db number, start offset, read 1 byte)
	snap7.util.set_bool(reading, BYTE_START_OFFSET, bit_offset, value)   # (value 1= true;0=false) (bytearray_: bytearray, byte_index: int, bool_index: int, value: bool)
	plc.db_write(db_number, start_address, reading)       #  write back the bytearray and now the boolean value is changed in the PLC.

def readBool(plc, db_number, start_address, bit_offset):
	reading = plc.db_read(db_number, start_address, 1)
	a = snap7.util.get_bool(reading, BYTE_START_OFFSET, bit_offset)
	print('DB Number: ' + str(db_number) + ' Bit: ' + str(start_address) + '.' + str(bit_offset) + ' Value: ' + str(a))

# TODO Try using this type of methods : total_prod = snap7.util.get_int(DB_bytearray,0)
def readDB(plc, db_number, start_address, length):
	reading = plc.read_area(snap7.types.Areas.DB, db_number, start_address, length)
	reading = int.from_bytes(reading, byteorder='big', signed=False)
	print(reading)

def writeDB(plc, db_number, start_address, length, value):
	value = value.to_bytes(length, byteorder='big')
	print(value)
	plc.write_area(snap7.types.Areas.DB, db_number, start_address, value)

def readInput(plc, start_address, bit_offset, length):
	reading = plc.read_area(snap7.types.Areas.PE, NO_DB, start_address, length)
	value = snap7.util.get_bool(reading, BYTE_START_OFFSET, bit_offset)
	print(value)

def readOutput(plc, start_address, bit_offset, length):
	reading = plc.read_area(snap7.types.Areas.PA, NO_DB, start_address, length)
	value = snap7.util.get_bool(reading, BYTE_START_OFFSET, bit_offset)
	print(value)

# Really better not to use
def writeInput(plc, start_address, bit_offset, length, value):
	reading = plc.read_area(snap7.types.Areas.PE, NO_DB, start_address, length)   
	snap7.util.set_bool(reading, BYTE_START_OFFSET, bit_offset, value)   
	plc.write_area(snap7.types.Areas.PE, NO_DB, start_address, reading)          

# TODO Finish (real?)
def oldReadMemory(plc, start_address, bit_offset, length, type):
	reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)
	if (type == "bool"):
		value = snap7.util.get_bool(reading, BYTE_START_OFFSET, bit_offset)
		print(value)
	elif (type == "byte"): # Useful ???
		value = reading
		print(value)
	elif (type == "int"):
		value = int.from_bytes(reading, byteorder='big', signed=True)
		print(value)
	elif (type == "time"):
		value = int.from_bytes(reading, byteorder='big', signed=False)
		ms = value
		s = ms // 1000
		ms %= 1000
		min = s // 60
		s %= 60
		h = min // 60
		min %= 60
		print(f"{h}h {min}min {s}s {ms}ms")
	else:
		print("Invalid type")

	print('Start Address: ' + str(start_address) + ' Value: ' + str(value))

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
	return numbers if numbers else None  # Return the first found number, or None if no number is found

# TODO Finish (real?)
def readMemory(plc, variable):
	type = variablesAPI.variables[variable]["Data Type"]
	length = getLength(type)
	logical_address = variablesAPI.variables[variable]["Logical Address"]
	address = extract_numbers(logical_address)
	start_address = address[0] if address != None else None
	bit_offset = address[1] if len(address) == 2 else 0

	reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)
	if (type == "Bool"):
		value = snap7.util.get_bool(reading, BYTE_START_OFFSET, bit_offset)
		print(value)
	elif (type == "Byte"): # Useful ???
		value = reading
		print(value)
	elif (type == "Int"):
		value = int.from_bytes(reading, byteorder='big', signed=True)
		print(value)
	elif (type == "Time"):
		value = int.from_bytes(reading, byteorder='big', signed=False)
		ms = value
		s = ms // 1000
		ms %= 1000
		min = s // 60
		s %= 60
		h = min // 60
		min %= 60
		print(f"{h}h {min}min {s}s {ms}ms")
	else:
		print("Invalid type")

	print('Start Address: ' + str(start_address) + ' Value: ' + str(value))

# TODO Finish
def oldWriteMemory(plc, start_address, bit_offset, length, type, value):
	reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)
	if (type == "bool"):
		snap7.util.set_bool(reading, BYTE_START_OFFSET, bit_offset, value)   
		plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, reading)
	elif (type == "byte"): # Useful ???
		plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)
	elif (type == "int"):
		value = value.to_bytes(length, byteorder='big')
		print(value)
		plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)
	elif (type == "time"):
		# TODO when format decided
		print("TODO")
	else:
		print("Invalid type")

# TODO Finish
def writeMemory(plc, variable, value):
	type = variablesAPI.variables[variable]["Data Type"]
	length = getLength(type)
	logical_address = variablesAPI.variables[variable]["Logical Address"]
	address = extract_numbers(logical_address)
	start_address = address[0] if address != None else None
	bit_offset = address[1] if len(address) == 2 else 0

	reading = plc.read_area(snap7.types.Areas.MK, NO_DB, start_address, length)
	if (type == "Bool"):
		snap7.util.set_bool(reading, BYTE_START_OFFSET, bit_offset, value)   
		plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, reading)
	elif (type == "Byte"): # Useful ???
		plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)
	elif (type == "Int"):
		value = value.to_bytes(length, byteorder='big')
		print(value)
		plc.write_area(snap7.types.Areas.MK, NO_DB, start_address, value)
	elif (type == "Time"):
		# TODO when format decided
		print("TODO")
	else:
		print("Invalid type")


# address = extract_numbers(variablesAPI.variables["Mw_API_CVEntree"]["Logical Address"])
# print(address)
# start_address = address[0] if address != None else None
# print(start_address)
# bit_offset = address[1] if len(address) == 2 else 0
# print(bit_offset)

# writeMemory(202, 0, 2, "int", 5)
# readMemory(202, 0, 2, "int")

# readInput(0, 0, 1)
# readOutput()

#while True:
#	writeInput(0, 0, 1, 1)

# writeBool(plcs[0], 3, 0, 1, 0)
# readBool(db_number, start_offset, bit_offset)
# readDB(3, 2, length_word)
# writeDB(3, 2, length_word, 5)
