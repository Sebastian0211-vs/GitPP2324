#-*- coding: utf-8 -*-
import CommunicationAPIS7 as S7
import variablesAPI
import snap7

plc = snap7.client.Client()
print(plc)
error = plc.connect('172.16.2.80', 0, 1)
print(error)

for variable in variablesAPI.variables:
    try:
        S7.readMemory(plc, variable)
    except Exception as e:
        print(e)

# while True:
#     for variable in variablesAPI.variables:
#         try:
#             S7.readMemory(plc, variable)
#         except Exception as e:
#             print(e)