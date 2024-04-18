#-*- coding: utf-8 -*-
import asyncio
from asyncua import Client, ua

#URL = "opc.tcp://172.16.40.95:4840" # For tests purposes
DEBUT_URL = "opc.tcp://"
PORT = ":4840"
NAMESPACE = "Interface serveur_1"

async def getVariable(client, namespace, var_name):
    # Getting the namespace index
    nsidx = await client.get_namespace_index("http://" + namespace)

    # Navigate to the Objects node
    objects = client.nodes.objects

    # Navigate to the server interface
    server_interfaces = await objects.get_child(f"3:ServerInterfaces")

    # Navigate to the specific object
    interface = await server_interfaces.get_child(f"{nsidx}:{namespace}")
    variable = await interface.get_child(f"{nsidx}:{var_name}")

    return variable

async def readValue(variable):
    reading = await variable.read_value()
    return reading

async def writeValue(variable, value):
    var_type = await variable.read_data_type_as_variant_type()
    new_value = ua.DataValue(ua.Variant(value, var_type))
    await variable.write_value(new_value)

async def connection(url):
    client = Client(url=url)
    await client.connect()
    return client

async def disconnection(client):
    await client.disconnect()

""" Zone de test de ce programme
async def main(url, namespace):
    client = await connection(url)
    variable = await getVariable(client, namespace, "Mx_IntTest")
    await writeValue(variable, 3)
    await disconnection(client)

asyncio.run(main(URL, NAMESPACE))
"""