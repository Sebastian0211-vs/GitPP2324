#-*- coding: utf-8 -*-
import asyncio
from asyncua import Client, ua

url = "opc.tcp://172.16.40.95:4840"

async def main(var_name, value):

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
        my_var = await interface.get_child(f"{nsidx}:{var_name}")
        
        reading = await my_var.read_value()
        print(f"MyVariable value is {reading}")

        var_type = await my_var.read_data_type_as_variant_type()

        new_value = ua.DataValue(ua.Variant(value, var_type))

        await my_var.write_value(new_value)

        reading = await my_var.read_value()
        print(f"MyVariable value is {reading}")


if __name__ == "__main__":
    asyncio.run(main("Mx_IntTest", 3))
