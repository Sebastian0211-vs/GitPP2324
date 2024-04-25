#-*- coding: utf-8 -*-
import asyncio
from asyncua import Client, ua

url = "opc.tcp://172.16.40.95:4840"  

async def main():

    print(f"Connecting to {url} ...")
    async with Client(url=url) as client:
        # Getting the namespace index
        namespace = "Interface serveur_1"
        nsidx = await client.get_namespace_index("http://" + namespace)
        print(nsidx)

        # Getting the root node
        root = client.nodes.root
        print(f"Root: {root}")

        # Navigate to the Objects node
        objects = client.nodes.objects

        print(f"Objects: {objects}")

        server_interfaces = await objects.get_child(f"3:ServerInterfaces")

        # Navigate to the specific object and variable
        interface = await server_interfaces.get_child(f"{nsidx}:{namespace}")
        my_var = await interface.get_child(f"{nsidx}:Mx_TimeTest")
        
        # Lecture de la valeur dans la variable
        value = await my_var.read_value()
        print(f"MyVariable value is {value}")

        # Transformation en format horaire
        ms = value
        s = ms // 1000
        ms %= 1000
        min = s // 60
        s %= 60
        h = min // 60
        min %= 60
        print(f"{h}h {min}min {s}s {ms}ms")

        # Création d'une DataValue (obligatoire pour faire fonctionner la fonction write_value())
        # ua.DataValue(ua.Variant(VALEUR, TYPE <ua.VariantType.TYPE>))
        new_value = ua.DataValue(ua.Variant(1563, ua.VariantType.Int32))

        # Ecriture de la nouvelle valeur dans la variable
        value = await my_var.write_value(new_value)

        # Lecture de la valeur dans la variable
        value = await my_var.read_value()
        print(f"MyVariable value is {value}")


if __name__ == "__main__":
    asyncio.run(main())
