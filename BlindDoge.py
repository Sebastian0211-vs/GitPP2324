from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import aiohttp
import time
import ip_addresses as ip
import logging
import numpy as np
import pygame
import json

with open('configDoge.json', 'r') as config_file:
    config = json.load(config_file)

# Use the configuration
logging.basicConfig(
    filename=config['logging']['filename'],
    filemode=config['logging']['filemode'],
    format=config['logging']['format'],
    level=getattr(logging, config['logging']['level'])
)

print("""



    _   ________   ____  ___   _____    __    ___    _   __________________     __
   / | / / ____/  / __ \/   | / ___/   / /   /   |  / | / / ____/ ____/ __ \   / /
  /  |/ / __/    / /_/ / /| | \__ \   / /   / /| | /  |/ / /   / __/ / /_/ /  / / 
 / /|  / /___   / ____/ ___ |___/ /  / /___/ ___ |/ /|  / /___/ /___/ _, _/  /_/  
/_/ |_/_____/  /_/   /_/  |_/____/  /_____/_/  |_/_/ |_/\____/_____/_/ |_|  (_)   
                                                                                  




""")

print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣄⠀⠀⠀⠀⢀⣴⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣷⣶⣶⣶⣾⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢼⣿⡿⣿⣿⣿⣟⢿⣿⣑⣻⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣿⡟⠛⡟⠻⡿⣿⣿⠿⣙⠿⣭⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⢻⡷⢤⣄⣀⠀⣁⣉⣨⣿⣿⣶⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⠙⣿⣦⠈⢩⣉⠿⣿⣿⣿⣿⠟⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡏⠉⢱⡄⢻⡖⠀⡌⣷⠒⠛⢫⠁⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⣿⠀⠀⠀⠤⠉⣅⠛⠉⠧⢜⣢⣬⠟⢛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⢀⣠⣴⣿⡱⣿⠀⠠⠖⠒⠓⠉⡑⠌⠦⣴⡀⠂⠀⢘⡷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣴⣶⣶⣿⣷⣶⣶⣶⡾⠿⠿⣩⣿⣿⣶⣿⠀⠁⣀⣂⠓⢰⠤⢍⠲⡤⢉⠀⠀⢌⣿⡶⣝⣷⣦⡴⣤⠦⣤⣤⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⡾⢟⠉⠉⠉⠉⠉⠛⣛⣷⣬⣁⣍⣳⣶⠿⢏⢩⢌⣿⠐⠏⢉⠈⠠⡁⢌⡤⢓⡔⠢⠘⣠⡿⠻⠿⣽⡭⠻⢷⣮⠷⠶⠛⡛⠉⢉⡛⢿⣦⡀⠀⠀⠀
⠀⠀⠀⠀⢀⣴⠿⢉⠐⠨⠷⠈⠑⠉⠆⠆⡉⢀⣉⣉⣉⠩⢉⠛⡉⢂⠆⡸⢷⡪⠴⣈⣕⠰⡈⠔⡨⠦⣡⡾⠟⢃⠠⣁⠢⣀⠡⢈⡅⣦⡤⢍⠉⠱⣯⠉⠀⠝⣷⡄⠀⠀
⠀⠀⠀⠀⣼⣿⠂⠋⠠⠀⢄⠓⡈⢒⡈⠒⠄⢣⠐⣈⠀⢡⠌⠆⡍⠻⠶⠷⡛⢷⣵⣄⣪⣝⣩⡙⣤⣷⠿⠷⠈⢂⠒⠄⢢⠄⠃⢆⠸⣿⡆⠀⠲⢀⠉⢀⠃⢠⠸⣿⡀⠀
⠀⠀⠀⢸⣿⠇⡴⠀⠄⢁⡆⠀⢧⡀⢠⠉⠚⡠⢁⢂⣉⠡⠒⠆⣈⠹⡞⡐⢋⠤⡙⠯⡉⣍⢛⣿⡼⣧⠂⠒⠃⠌⠜⡠⢁⣌⠩⡀⠍⣿⡆⢈⠒⠀⢊⠀⠄⡀⠁⣹⡇⠀
⠀⠀⠀⣾⡇⡴⠀⡘⠀⡌⠠⠁⠚⣿⡄⠡⠒⠤⡁⠆⠠⢉⠲⠈⠔⡘⡇⠐⢎⠐⣁⠂⠡⡄⠈⢹⣷⣿⡔⢂⢋⠱⡈⠔⣃⠀⢢⠁⠎⢼⣧⠎⡰⢀⠢⠈⠄⡐⠀⢼⡇⠀
⠀⢀⣼⣿⠃⡇⠐⣈⠀⢸⡇⠘⡄⣹⣷⡡⢉⢰⣀⠎⡡⢀⠧⠎⠄⠣⡜⠈⠴⠈⣥⠀⢱⡀⠈⠄⣿⣻⡇⠄⠎⡔⢩⠐⠤⢉⠂⡉⡜⢨⣿⠀⢐⣢⠐⢈⠀⠄⡁⢸⣧⠀
⠀⣾⣿⢃⡆⣱⡇⠠⠀⣿⢰⡆⣷⢠⡿⣷⡆⢠⠐⢢⠑⢃⠰⢂⠆⡡⠸⡄⢈⠒⡈⢆⠰⠁⠠⡈⢿⣯⣿⠀⠆⢐⢂⡁⢋⠤⣁⠒⡨⣽⢻⡃⠠⢳⠀⠠⠈⠐⡀⢎⣿⡇
⢘⣿⡏⣿⠡⢸⡇⠐⣠⢻⣏⡇⢿⣦⡓⠽⣿⣀⠎⢡⠊⡄⢃⠆⢠⠁⡀⠐⢂⠡⡀⢈⠐⠰⠃⢌⣿⣿⡿⠀⢉⡠⢂⠜⡄⢢⢱⣮⡵⡏⣼⠁⠃⣼⠀⠁⢀⠡⡘⠤⣿⡇
⠠⣿⢱⡿⢀⢹⣿⠰⣿⣬⠛⣿⣘⣿⣷⡈⢻⣿⣾⣄⡡⠘⡈⠐⣀⠂⠠⠁⡀⢂⠅⠀⠎⡐⠠⠐⣾⣟⣇⣠⡤⢂⡥⣊⡜⣲⣿⣿⠥⣳⡿⢀⡇⠽⢀⠁⢂⡑⢌⢣⣿⡇
⠀⣿⣿⠃⡄⠊⡽⠀⠟⣻⣷⣾⣿⠟⠙⢷⣤⡈⠿⣿⣵⣣⡌⠥⣈⠀⠠⢀⡄⣼⣤⣂⣆⣧⣤⣿⠿⣿⣠⣧⣭⣽⣦⣽⣿⢿⣿⢶⣽⣿⣷⢾⠃⡐⡈⠞⡐⠤⢈⢶⣿⠁
⢠⣿⠏⠰⣀⠣⠙⢆⡁⠆⢨⡟⢿⡄⠀⠀⠘⣷⠙⢩⡙⠿⠿⢷⠶⡿⠿⠿⡟⠿⣛⢛⣛⣭⣿⣭⣶⣩⣍⣭⡽⣌⣙⠋⢾⣼⡷⡾⠙⢿⣿⣏⢤⣽⠇⡐⠄⢆⠌⣿⡏⠀
⢸⡟⠘⠰⠄⢂⠧⣀⡙⢄⠂⢹⡄⢻⣆⠀⠀⠘⣷⠂⡈⡔⢃⠢⠐⠠⢘⣿⠬⠷⡌⢞⠻⠋⠉⠉⣙⣯⣌⣥⣴⠞⣹⡟⢈⣿⡼⠁⠀⠀⣿⣿⡿⠁⢒⢈⠒⣨⠐⢸⡇⠀
⣼⡇⢸⢃⠛⡀⡄⣀⠛⢄⠸⢠⠘⢣⣿⡄⠀⠀⢸⣇⠠⡘⢠⠃⡘⠀⣻⢿⣿⢇⣟⣘⣜⣿⣿⡿⢿⣟⡛⣃⣀⣼⣿⠀⠀⣿⠇⠀⠀⣸⡿⢛⠃⠄⣛⠀⡄⢀⡘⢠⡇⠀
⣿⡇⠢⢌⠂⠴⡐⢄⠪⢄⠃⠆⣣⢡⣿⣿⠀⠀⠀⢻⡗⣷⣶⣕⣶⣬⣿⣆⣻⣎⣘⣛⡛⢭⡅⣀⣾⠿⠖⠛⣋⣴⣿⡆⠀⣿⠀⠀⣼⢯⡑⠌⠆⢒⠰⡈⠔⠰⢐⠠⡇⠀
⢻⣿⢰⡄⠛⠠⣀⠂⡅⢊⠘⠠⢁⠆⣿⡿⠀⠀⠀⢸⣿⣜⣧⣻⣄⣤⡴⠿⢿⣿⣛⠛⠿⠷⠛⠁⣸⣷⡶⣿⣋⣼⣟⠁⢠⣿⡆⢰⣿⡟⠤⡉⡘⢄⠣⡘⠠⡉⠆⣸⡇⠀
⠈⢿⣿⠁⠈⡴⠉⡐⢈⠠⠉⠄⠠⣿⣿⠁⠀⠀⠀⢸⣷⠿⣿⣷⣼⣀⣀⠀⠀⢻⣿⠿⢶⣯⡷⠛⢻⣿⡴⢏⣼⠟⣉⣛⣿⣿⠃⠸⣿⣮⡐⠡⡘⠠⢃⠤⡁⠅⠢⣽⡇⠀
⠀⠈⢳⣭⠀⡐⠤⣉⠄⢂⠁⣀⡴⣿⣇⠀⠀⠀⠀⠈⣻⣷⣌⣍⠉⠉⢉⣹⣄⠀⠹⣿⡶⠾⢷⣶⣼⣯⣰⡟⣡⢤⣼⣻⠟⠁⠀⠀⠹⣿⣟⠁⠐⠁⢂⠒⠡⢀⠱⡿⠀⠀
⠀⠀⠀⠻⣦⡦⠐⢠⠂⠂⠂⢉⡁⠛⢿⣦⡐⠀⠀⢸⣿⣏⠛⠻⠶⢿⣯⣭⢉⠐⢂⠈⢻⣿⣦⣶⣶⣿⣿⡍⠁⠎⠨⣽⣿⠀⠀⢀⣴⣿⠟⡀⠒⠈⠲⠌⠐⣶⡾⠃⠀⠀
⠀⠀⠀⠀⠙⢧⡂⠀⠀⢄⠠⢀⠀⠐⡘⠻⣿⣆⠀⠘⣿⠶⠏⠠⠁⢆⡐⢈⠂⡉⢤⡙⣦⡿⠁⠀⣻⡇⠀⢀⠙⢂⠱⣿⠏⠀⣴⣿⡿⠁⠀⠀⠈⠀⠀⡀⣢⡞⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠻⢷⠇⡀⠀⠀⡐⠀⣠⣜⡻⣿⠏⠀⠘⣷⡀⠁⠉⡤⢈⠉⡀⠄⢀⣿⠟⠀⠀⠀⠀⣿⠐⢀⠘⣄⣴⡏⢀⣼⣿⡏⠀⠀⠀⠁⠈⠙⣻⣹⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")
app = Flask(__name__)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def job():
    print("+--------------------------------------+")
    logging.info('Job started')
    start_time = time.time()  # Capture the start time

    NombreAPIConnceted = 0

    NombreAPIConnceted = await multi_possible(NombreAPIConnceted)
    nombremultisql = 2

    await checkplusde3(nombremultisql)

    await get_info(NombreAPIConnceted)

    await compteur_bille()

    await deconnection()
    logging.info('Job finished')
    print(f"Execution time: {time.time() - start_time}")
    print("+--------------------------------------+")

valid_request = config['requests']

async def compteur_bille():
    A = np.zeros(3, dtype=int)
    i = 0

    async def fetch_data(ip_address):
        nonlocal A, i
        try:
            response = await fetch(session, f"http://{ip_address['RASP_catch']}:8000/compteur_bille")
            A = np.add(A, response)
            print(f"Matrice de l'API : {ip_address['API']} : {response}")
            i += 1
        except Exception as e:
            logging.error(e)
            print("Error occurred during API request.")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(ip_addr) for ip_addr in ip.ip_addresses.values()]
        await asyncio.gather(*tasks)

    print(f"Matrice totale : {A}")
    if i != len(ip.ip_addresses):
        print("Erreur de compteur")
    else:
        async def send_data(ip_address):
            try:
                for i in range(3):
                    await fetch(session, f"http://{ip_address['RASP_catch']}:8000/compteur_bille/{i}/{A[i]}")
            except Exception as e:
                logging.error(e)

        async with aiohttp.ClientSession() as session:
            tasks = [send_data(ip_addr) for ip_addr in ip.ip_addresses.values()]
            await asyncio.gather(*tasks)

triggered = False

async def get_info(NombreAPIConnceted):
    async def fetch_info(ip_address, request):
        nonlocal NombreAPIConnceted
        global triggered
        try:
            response = await fetch(session, f"http://{ip_address['RASP_catch']}:8000/trigger/{request}")

            if request.startswith("Mx_API_C") and response:
                print("j'ai reçu une alerte True")
                if request.endswith("normal"):
                    print("Tout va bien")
                    logging.info(response)
                elif request.endswith("attention"):
                    await SOS_Warning(1, f"http://{ip_address['RASP_catch']}:8000", "yellow", f"Position{request[8]}")
                    logging.info(response)
                elif request.endswith("alerte"):
                    print("J'ai reçu une alerte critique !!")
                    await SOS_Warning(1, f"http://{ip_address['RASP_catch']}:8000", "red", f"Position{request[8]}")
                    print(response)
                    logging.info(response)

            if response and request.startswith("Mx"):
                print(ip_address['API'], ": Request: ", request, "Response: ", response)
                logging.info(response)
                compteur = 0
                for ip_address in ip.ip_addresses.values():
                    try:
                        compteur += 1 
                        await fetch(session, f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/True")
                        if compteur == NombreAPIConnceted:
                            for ip_address in ip.ip_addresses.values():
                                try:
                                    await fetch(session, f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/False")
                                except Exception as e:
                                    logging.error(e)
                        logging.info(response)
                    except Exception as e:
                        logging.error(e)
                return
            elif response:
                print(ip_address['API'], ": Request: ", request, "Response: ", response)
                logging.info(response)
                for ip_address in ip.ip_addresses.values():
                    try:
                        await fetch(session, f"http://{ip_address['RASP_catch']}:8000/sortie/{request}/True")
                        logging.info(response)
                    except Exception as e:
                        logging.error(e)
            else:
                logging.error(response)
        except Exception as e:
            logging.error(e)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_info(ip_addr, request) for request in valid_request for ip_addr in ip.ip_addresses.values()]
        await asyncio.gather(*tasks)

async def multi_possible(NombreAPIConnceted):
    async def check_api(ip_address):
        nonlocal NombreAPIConnceted
        try:
            checker = await fetch(session, f"http://{ip_address['RASP_catch']}:8000/check_possible/{ip_address['API']}")

            if checker:
                multi = await fetch(session, f"http://{ip_address['RASP_catch']}:8000/connected")
                NombreAPIConnceted += 1
                print(f"{ip_address['API']} : API connected = {NombreAPIConnceted}")
        except Exception as e:
            logging.error(e)

    async with aiohttp.ClientSession() as session:
        tasks = [check_api(ip_addr) for ip_addr in ip.ip_addresses.values()]
        await asyncio.gather(*tasks)

    async def set_multi(ip_address, enabled):
        try:
            await fetch(session, f"http://{ip_address['RASP_catch']}:8000/multi/{enabled}")
        except Exception as e:
            logging.error(e)

    enabled = "True" if NombreAPIConnceted > 1 else "False"
    print(f"Mode multi {'disponible' if enabled == 'True' else 'indisponible'}")
    async with aiohttp.ClientSession() as session:
        tasks = [set_multi(ip_addr, enabled) for ip_addr in ip.ip_addresses.values()]
        await asyncio.gather(*tasks)
    return NombreAPIConnceted

async def SOS_Warning(times, base_url, color, position):
    morse_code_sos = "...---..."

    pygame.mixer.init()
    pygame.mixer.music.load(mp3file=config['sound_file'])
    pygame.mixer.music.play()

    morse_code_to_duration = {
        ".": 0.1,  # Short flash
        "-": 0.3,  # Long flash
        " ": 0.2   # Pause
    }

    async with aiohttp.ClientSession() as session:
        for _ in range(times):
            for symbol in morse_code_sos:
                # Turn on the light
                response = await fetch(session, f"{base_url}/pin/{position}/{color}/high")
                if response.status_code != 200:
                    print(f"Error turning on the light: {response.json()}")

                await asyncio.sleep(morse_code_to_duration[symbol])

                response = await fetch(session, f"{base_url}/pin/{position}/{color}/low")
                if response.status_code != 200:
                    print(f"Error turning off the light: {response.json()}")

                await asyncio.sleep(0.1)

async def checkplusde3(nombremultisql):
    async def set_multinbr(ip_address, enabled):
        try:
            await fetch(session, f"http://{ip_address['RASP_catch']}:8000/multinbr/{enabled}")
        except Exception as e:
            logging.error(e)

    enabled = "True" if nombremultisql >= 3 else "False"
    print(f"Multi sur {'plus' if enabled == 'True' else 'moins'} de 3 châssis")
    async with aiohttp.ClientSession() as session:
        tasks = [set_multinbr(ip_addr, enabled) for ip_addr in ip.ip_addresses.values()]
        await asyncio.gather(*tasks)

async def deconnection():
    async def disconnect(ip_address):
        try:
            await fetch(session, f"http://{ip_address['RASP_catch']}:8000/deconnection")
        except Exception as e:
            logging.error(e)

    async with aiohttp.ClientSession() as session:
        tasks = [disconnect(ip_addr) for ip_addr in ip.ip_addresses.values()]
        await asyncio.gather(*tasks)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(lambda: asyncio.run(job()), 'interval', seconds=config['scheduler']['interval'])

scheduler.start()

if __name__ == '__main__':
    logging.info('Application started')
    app.run(host=config['flask']['host'], port=config['flask']['port'])
    logging.info('Application finished')
