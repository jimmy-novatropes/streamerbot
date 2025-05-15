import json
import os
from datetime import datetime
import requests
import serial
import serial.tools.list_ports
import time
# import psutil


"""
Sub Queue: ~priority_queue_count~ people 
Final notes collection:
{'color': 'white', 'awb': 0, 'notes': 'good, but a tad purple'}
{'color': 'white', 'awb': 0, 'notes': 'purpleish'}
{'color': 'white', 'awb': 1, 'notes': 'greenish'}
{'color': 'red', 'awb': 0, 'notes': 'darkred'}
{'color': 'red', 'awb': 1, 'notes': 'not red but light red to orange'}
{'color': 'green', 'awb': 0, 'notes': 'intense green'}
{'color': 'green', 'awb': 1, 'notes': 'redish hue around sculpture'}
{'color': 'blue', 'awb': 0, 'notes': 'hard to see deep blue'}
{'color': 'blue', 'awb': 1, 'notes': 'easier to see but reddish hue around sculpture'}
{'color': 'yellow', 'awb': 0, 'notes': 'good yellow'}
{'color': 'yellow', 'awb': 1, 'notes': 'greenish yellow'}
{'color': 'magenta', 'awb': 0, 'notes': 'blueish magenta'}
{'color': 'magenta', 'awb': 1, 'notes': 'lighter magenta with green hue around sculpture'}
{'color': 'cyan', 'awb': 0, 'notes': 'bright cyan'}
{'color': 'cyan', 'awb': 1, 'notes': 'greenish cyan with red hue around it, looks bad'}
"""

BASE_URL = "http://192.168.4.248:5000/set"
color_counter_vals = {
    "white": [1, 0],
    "red": [1750, 0],
    "yellow": [511, 0],
    "green": [767, 0],
    "cyan": [1023, 0],
    "blue": [1279, 1],
    "magenta": [1535, 0],
    "purple": [1535, 0],
}

def save_or_extend_json(data, file_path: str):
    # Normalize single dict entry into a wrapper with timestamp
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary.")

    # Wrap if it's a single flat dict (e.g. {"status": "ok"})
    if all(not isinstance(v, dict) for v in data.values()):
        data = {
            f"entry_{datetime.now().strftime('%Y%m%d%H%M%S')}": {
                **data,
                "timestamp": datetime.now().isoformat()
            }
        }
    else:
        for key, value in data.items():
            if isinstance(value, dict):
                value["timestamp"] = datetime.now().isoformat()
            else:
                data[key] = {"value": value, "timestamp": datetime.now().isoformat()}

    # Merge with existing file
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                existing = json.load(f)
            if isinstance(existing, dict):
                existing.update(data)
            else:
                print("Warning: existing data is not a dictionary. Overwriting.")
                existing = data
        except json.JSONDecodeError:
            print("Warning: invalid JSON. Overwriting.")
            existing = data
    else:
        existing = data

    with open(file_path, 'w') as f:
        json.dump(existing, f, indent=4)


def reverse_lookup(d, value):
    return next((k for k, v in d.items() if v == value), None)

def set_camera_setting(setting: str, value: int):
    endpoints = {
        "auto_exposure": "exposure_auto",
        "exposure_time_absolute": "exposure",
        "white_balance_automatic": "white_balance_auto",
        "brightness": "brightness",
        "contrast": "contrast",
        "white_balance_temperature": "white_balance",
        "saturation": "saturation",
        "hue": "hue",
    }

    ranges = {
        "auto_exposure": (1, 3),
        "exposure_time_absolute": (1, 5000),
        "white_balance_automatic": (0, 1),
        "brightness": (-64, 64),
        "contrast": (0, 64),
        "white_balance_temperature": (2800, 6500),
        "saturation": (0, 128),
        "hue": (-40, 40),
    }

    if setting not in endpoints:
        setting = reverse_lookup(endpoints, setting)


    if isinstance(value, bool):
        value = int(value)

    min_val, max_val = ranges[setting]
    if not (min_val <= value <= max_val):
        raise ValueError(f"{setting} must be between {min_val} and {max_val}")

    url = f"{BASE_URL}/{endpoints[setting]}"
    params = {"value": value}
    print(f"Setting camera {setting} to {value}. URL: {url}, Params: {params}")
    response = requests.post(url, params=params)

    return response.status_code, response.text


color_translations = {
    "rojo": "red", "rouge": "red", "vermelho": "red",
    "verde": "green", "vert": "green",
    "azul": "blue", "bleu": "blue",
    "amarillo": "yellow", "jaune": "yellow", "amarelo": "yellow",
    "morado": "purple", "violet": "purple", "roxo": "purple",
    "blanco": "white", "branco": "white", "blanc": "white",
    "cian": "cyan", "cyan": "cyan", "turquesa": "cyan",
    "magenta": "magenta",
    "negro": "black", "preto": "black", "noir": "black",
    "naranja": "orange", "laranja": "orange", "orange": "orange",
    "rosa": "pink", "rose": "pink",
    "gris": "gray", "cinza": "gray", "gray": "gray"
}


# def color_to_rgb_string(color):
#     """Convert color name to RGB string. Return None if not recognized."""
#     return color_counter_vals.get(color.lower())

def color_to_rgb_string(color):
    normalized = color.lower()
    english_color = color_translations.get(normalized, normalized)
    print(f"Normalized color: {normalized}, English color: {english_color}")
    return color_counter_vals.get(english_color)


# Scan and assign Arduino COM ports
def find_arduinos():
    arduinos = {
        "shutter": None,
        "led": None,
        "motor": None
                }  # Initialize with None

    # available_ports = [port.device for port in serial.tools.list_ports.comports()
    # Get a list of all available serial ports
    ports = serial.tools.list_ports.comports()

    # Print details of each port
    for port in ports:
        print(
            f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}\n")

    available_ports = [
        port.device for port in serial.tools.list_ports.comports()
        if
        "Arduino" in port.description
        or "ttyUSB" in port.device
        or "ttyACM" in port.device
        or "USB-SERIAL CH340" in port.description
        or "USB Serial Port (COM" in port.description
        # or "USB Serial Port (COM"
    ]

    print(f"Available COM ports: {available_ports}")

    for port in available_ports:
        try:
            ser = serial.Serial(port, 9600, timeout=5, dsrdtr=False)
            # ser = serial.Serial(port, 9600, timeout=5, dsrdtr=True)
            time.sleep(3)  # Allow Arduino to initialize

            ser.write(b"whoareyou\n")  # Ask Arduino for its identifier
            time.sleep(0.5)

            raw_data = ser.read(ser.in_waiting)  # Read available bytes
            response = raw_data.decode('utf-8', errors='ignore').strip()  # Decode safely & remove whitespace

            # print(f"Response from {port}: {response}")

            if response in arduinos.keys():
                if response in arduinos:
                    arduinos[response] = ser
                    print(f"Assigned {port} to {response}")
                else:
                    ser.close()  # Close if not recognized
                continue

            for dict_key in arduinos.keys():
                if dict_key in response:
                    arduinos[dict_key] = ser
                    print(f"Assigned {port} to {dict_key}")
                    continue


            if response not in arduinos.keys():
                counter = 0
                while ser.in_waiting == 0:
                    ser.write(b"whoareyou\n")
                    time.sleep(0.5)
                    response = ser.read(ser.in_waiting).decode('utf-8').strip()
                    print("attempt # ", counter)
                    if response in arduinos.keys():
                        arduinos[response] = ser
                        print(f"Assigned {port} to {response}")
                        break
                    counter += 1
                    if counter > 10:
                        break
        except serial.SerialException as e:
            print(f"Could not open {port}: {e}")
            # free_com_port(port)

    return arduinos


def clean_settings(entry):
    exclude_keys = {
        "timestamp", "color_name", "color", "rpm",
        "direction", "shutter_instructions", "comments"
    }
    return {
        k: v for k, v in entry.items()
        if v not in ("default", "") and k not in exclude_keys
    }


def find_color_settings(color_name, color_data):
    normalized = color_name.lower()
    english_color = color_translations.get(normalized, normalized)
    results = [entry for entry in color_data if entry.get("color_name") == english_color.lower()]
    return results

# def free_com_port(port):
#     port = port.upper()
#     for proc in psutil.process_iter(["pid", "name", "cmdline"]):
#         try:
#             cmdline_list = proc.info.get("cmdline")
#             if not cmdline_list:
#                 continue
#             cmdline = " ".join(cmdline_list).upper()
#             if port in cmdline:
#                 print(f"Killing PID {proc.pid} using {port}")
#                 proc.kill()
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             continue
#     print(f"No process found using {port}")
#     return False
