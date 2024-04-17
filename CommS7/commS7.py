#-*- coding: utf-8 -*-
import asyncio
from asyncua import Client

url = "opc.tcp://172.16.40.95:4840"

# Not useful - To delete
async def browse_objects(url):
    client = Client(url=url)
    try:
        await client.connect()
        objects = client.nodes.objects
        children = await objects.get_children()
        for child in children:
            browse_name = await child.read_browse_name()
            print()
            print(f"Node: {child}, NodeId: {child.nodeid}, BrowseName: {browse_name}")
    finally:
        await client.disconnect()

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

        sous_dossier = await objects.get_child(f"3:ServerInterfaces")

        # Navigate to the specific object and variable
        my_obj = await sous_dossier.get_child(f"{nsidx}:{namespace}")
        #my_var = await my_obj.get_child(f"{nsidx}:MyVariable")
        my_var = await my_obj.get_child(f"{nsidx}:Mx_BoolTest")
        
        value = await my_var.read_value()
        print(f"MyVariable value is {value}")

        """
        # Getting a variable node using its browse path
        var = await client.nodes.objects.get_child(["0:MyObject", "0:MyVariable"])
        value = await var.read_value()
        print(f"MyVariable value is {value}")
        """

if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.run(browse_objects(url))