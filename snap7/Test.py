#-*- coding: utf-8 -*-
import CommunicationAPIS7 as S7
import variablesAPI
import snap7
import time

plc = snap7.client.Client()
print(f"Client: {plc}")
error = plc.connect('172.16.2.80', 0, 1)
print(f"Connection error: {error}")

# for variable in variablesAPI.variables:
#     try:
#         S7.readMemory(plc, variable)
#     except Exception as e:
#         print(e)

while True:
    print("----------------------------")
    time.sleep(2)
    # for variable in variablesAPI.variables:
    #     print(variable)
    #     try:
    #         S7.readMemory(plc, variable)
    #     except Exception as e:
    #         print(e)