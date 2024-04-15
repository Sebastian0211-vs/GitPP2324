import snap7

WORD_LENGTH = 2  # Bytes / Word, Int
DOUBLE_WORD_LENGTH = 4  # Bytes / DWord, Real, IEC Time
BYTE_START_OFFSET = 0
NO_DB = 0

"""
DATABASES:
1 - ...
2 - ...
3 - ...
"""

plc_ip_addresses = []
plcs = []

for ip_address in range(len(plc_ip_addresses)):
    plcs[ip_address] = snap7.client.Client()
    plcs[ip_address].connect(plc_ip_addresses[ip_address], 0, 1)  # IP address, rack, slot

for plc in plcs:
    if (not plc.get_connected()):
        print(f"Connection lost with PLC - {plc}")