import requests
import time
import pygame
import random
# Define the base URL of the API
base_url = "http://172.16.0.3:8000"  # Replace with the actual URL if different

valid_positions = {"Position1", "Position2", "Position3", "Position4", "Position5"}



def SOS_Warning(times):
    # Define the Morse code for SOS
    
    morse_code_sos = "...---..."

    pygame.mixer.init()
    pygame.mixer.music.load("nuke.mp3")
    pygame.mixer.music.play()

    for _ in range(times):
        # Define the mapping from Morse code to durations (in seconds)
        morse_code_to_duration = {
        ".": 0.1,  # Short flash
        "-": 0.3,  # Long flash
        " ": 0.2   # Pause
        }

        # Define the position and color for the light show
        position = "Position1"  # Replace with the actual position
        color = "red"

        # Send requests to the API to execute the light show
        for symbol in morse_code_sos:
        # Turn on the light
            response = requests.get(f"{base_url}/pin/{position}/{color}/high")
            if response.status_code != 200:
                print(f"Error turning on the light: {response.json()}")

        # Wait for the duration corresponding to the Morse code symbol
            time.sleep(morse_code_to_duration[symbol])

    # Turn off the light
    # Assuming there's a similar route to turn off the light
            response = requests.get(f"{base_url}/pin/{position}/{color}/low")
            if response.status_code != 200:
                print(f"Error turning off the light: {response.json()}")

    # Wait for a short duration before the next symbol
            time.sleep(0.1)


def china_warning(times):
    # Define the colors for the light show
    colors = ["red", "yellow"]

    pygame.mixer.init()
    pygame.mixer.music.load("mao.mp3")
    pygame.mixer.music.play()

    for _ in range(times):
        # Flicker each position with red color
        for position in valid_positions:
            for _ in range(3):
                # Turn on the light with red color
                response = requests.get(f"{base_url}/pin/{position}/{colors[0]}/high")
                if response.status_code != 200:
                    print(f"Error turning on the light: {response.json()}")
                # Wait for a short duration
                time.sleep(0.2)
                # Turn off the light
                response = requests.get(f"{base_url}/pin/{position}/{colors[0]}/low")
                if response.status_code != 200:
                    print(f"Error turning off the light: {response.json()}")
                # Wait for a short duration
                time.sleep(0.2)

        # Turn on all positions with yellow color
        for position in valid_positions:
            # Turn on the light with yellow color
            response = requests.get(f"{base_url}/pin/{position}/{colors[1]}/high")
            if response.status_code != 200:
                print(f"Error turning on the light: {response.json()}")
        # Wait for a short duration
        time.sleep(2)
        # Turn off all positions
        for position in valid_positions:
            # Turn off the light
            response = requests.get(f"{base_url}/pin/{position}/{colors[1]}/low")
            if response.status_code != 200:
                print(f"Error turning off the light: {response.json()}")

        # Wait for a short duration
        time.sleep(0.2)

        # Turn off all positions
        for position in valid_positions:
            # Turn off the light
            response = requests.get(f"{base_url}/pin/{position}/{colors[0]}/low")
            if response.status_code != 200:
                print(f"Error turning off the light: {response.json()}")

        # Wait for a short duration
        time.sleep(0.2)

        # Turn on all positions with yellow color
        for position in valid_positions:
            # Turn on the light with yellow color
            response = requests.get(f"{base_url}/pin/{position}/{colors[1]}/high")
            if response.status_code != 200:
                print(f"Error turning on the light: {response.json()}")


def Startup_Sequence():
    # Define the colors for the light show
    colors = ["blue", "green"]

    # Flicker each position with blue color
    for position in valid_positions:
        for _ in range(3):
            # Turn on the light with blue color
            response = requests.get(f"{base_url}/pin/{position}/{colors[0]}/high")
            if response.status_code != 200:
                print(f"Error turning on the light: {response.json()}")

            # Wait for a short duration
            time.sleep(0.2)

            # Turn off the light
            response = requests.get(f"{base_url}/pin/{position}/{colors[0]}/low")
            if response.status_code != 200:
                print(f"Error turning off the light: {response.json()}")

            # Wait for a short duration
            time.sleep(0.2)

    # Turn on all positions with green color
    for position in valid_positions:
        # Turn on the light with green color
        response = requests.get(f"{base_url}/pin/{position}/{colors[1]}/high")
        if response.status_code != 200:
            print(f"Error turning on the light: {response.json()}")

    # Wait for a short duration
    time.sleep(2)

    # Turn off all positions
    for position in valid_positions:
        # Turn off the light
        response = requests.get(f"{base_url}/pin/{position}/{colors[1]}/low")
        if response.status_code != 200:
            print(f"Error turning off the light: {response.json()}")


def epileptia(times):
    

    for _ in range(times):
        # Define the colors for the light show
        colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "white"]

        # Loop for a certain number of times
        for _ in range(10):
            # Randomly select a position
            position = "Position1"

            # Randomly select a color
            color = random.choice(colors)

            # Turn on the light with the random color
            response = requests.get(f"{base_url}/pin/{position}/{color}/high")
            if response.status_code != 200:
                print(f"Error turning on the light: {response.json()}")

            # Wait for a short duration

            # Turn off the light
            response = requests.get(f"{base_url}/pin/{position}/{color}/low")
            if response.status_code != 200:
                print(f"Error turning off the light: {response.json()}")

            # Wait for a short duration
            time.sleep(0.1)

epileptia(10)