import snap7

plc = snap7.client.Client()
plc.connect('172.16.40.95', 0, 1)  # IP address, rack, slot (from HW settings)

db_number = 3
start_offset = 0
bit_offset = 0
value = 1  # 1 = true | 0 = false

start_address = 100  # starting address
length_word = 2
length_double_word = 4

def writeBool(db_number, start_offset, bit_offset, value):
	reading = plc.db_read(db_number, start_offset, 1)    # (db number, start offset, read 1 byte)
	snap7.util.set_bool(reading, 0, bit_offset, value)   # (value 1= true;0=false) (bytearray_: bytearray, byte_index: int, bool_index: int, value: bool)
	plc.db_write(db_number, start_offset, reading)       #  write back the bytearray and now the boolean value is changed in the PLC.
	return None

def readBool(db_number, start_offset, bit_offset):
	reading = plc.db_read(db_number, start_offset, 1)
	a = snap7.util.get_bool(reading, 0, bit_offset)
	print('DB Number: ' + str(db_number) + ' Bit: ' + str(start_offset) + '.' + str(bit_offset) + ' Value: ' + str(a))
	return None

def readDB(db_number, start_offset, length):
	reading = plc.read_area(snap7.types.Areas.DB, db_number, start_offset, length)
	reading = int.from_bytes(reading, byteorder='big', signed=False)
	print(reading)

def writeDB(db_number, start_offset, length, value):
	value = value.to_bytes(length, byteorder='big')
	print(value)
	plc.write_area(snap7.types.Areas.DB, db_number, start_offset, value)

def readInput(start_offset, bit_offset, length):
	reading = plc.read_area(snap7.types.Areas.PE, 0, start_offset, length)
	value = snap7.util.get_bool(reading, start_offset, bit_offset)
	print(value)

def readOutput(start_offset, bit_offset, length):
	reading = plc.read_area(snap7.types.Areas.PA, 0, start_offset, length)
	value = snap7.util.get_bool(reading, start_offset, bit_offset)
	print(value)

# Really better not to use
def writeInput(start_offset, bit_offset, length, value):
	reading = plc.read_area(snap7.types.Areas.PE, 0, start_offset, length)   
	snap7.util.set_bool(reading, start_offset, bit_offset, value)   
	plc.write_area(snap7.types.Areas.PE, 0, start_offset, reading)          
	return None

# TODO Finish (real?)
def readMemory(start_address, bit_offset, length, type):
	reading = plc.read_area(snap7.types.Areas.MK, 0, start_address, length)
	if (type == "bool"):
		value = snap7.util.get_bool(reading, 0, bit_offset)
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

	reading = int.from_bytes(reading, byteorder='big', signed=False)
	print('Start Address: ' + str(start_address) + ' Value: ' + str(value))

# TODO Finish
def writeMemory(start_address, bit_offset, length, type, value):
	reading = plc.read_area(snap7.types.Areas.MK, 0, start_address, length)
	if (type == "bool"):
		snap7.util.set_bool(reading, 0, bit_offset, value)   
		plc.write_area(snap7.types.Areas.MK, 0, start_address, reading)
	elif (type == "byte"): # Useful ???
		plc.write_area(snap7.types.Areas.MK, 0, start_address, value)
	elif (type == "int"):
		value = value.to_bytes(length, byteorder='big')
		print(value)
		plc.write_area(snap7.types.Areas.MK, 0, start_address, value)
	elif (type == "time"):
		# TODO when format decided
		print("TODO")


# writeMemory(202, 0, 2, "int", 5)
# readMemory(202, 0, 2, "int")

# readInput(0, 0, 1)
# readOutput()

#while True:
#	writeInput(0, 0, 1, 1)

# writeBool(3, 0, 1, 0)
# readBool(db_number, start_offset, bit_offset)
# readDB(3, 2, length_word)
# writeDB(3, 2, length_word, 5)
