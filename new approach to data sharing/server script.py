import socket
import json
import serial
import time
import logging
import serial.tools.list_ports
from datetime import datetime
import requests
import os

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

logging.basicConfig(
    filename='log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BASE_URL = "http://192.168.4.248:5000/set"
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



def color_to_rgb_string(color):
    """Convert color name to RGB string. Return None if not recognized."""
    return color_counter_vals.get(color.lower())


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

    return arduinos


# Find Arduinos dynamically
arduino_ports = find_arduinos()
ser1 = arduino_ports["led"]  # Arduino for frequency & color
ser2 = arduino_ports["motor"]  # Arduino for RPM
ser3 = arduino_ports["shutter"]  # Arduino for Shutter and LED control

# Server Socket Details
HOST = "localhost"
PORT = 65432
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



mode_2_rpm = {
    #"-7": [820, "forward"],
    "-6": [945, "backward"],
    "-5": [265, "backward"],
    "-4": [1375, "backward"], #same as 820
    "-3": [425, "forward"],
    "-2": [685, "backward"],
    "-1": [1118, "forward"],
    "1": [1118, "backward"],
    "2": [685, "forward"],
    "3": [425, "backward"],
    "4": [1375, "forward"],
    "5": [265, "forward"],
    "6": [945, "forward"]
    #"7": [820, "backward"], #same as 1375 but rougher
}
settings_json = "server_settings.json"
if os.path.exists(settings_json):
    with open(settings_json, "r") as f:
        main_settings = json.load(f)


def find_color_settings(color_name, color_data):
    results = [entry for entry in color_data if entry.get("color_name") == color_name.lower()]
    return results

color_settings = find_color_settings("white", main_settings)
def clean_settings(entry):
    exclude_keys = {
        "timestamp", "color_name", "color", "rpm",
        "direction", "shutter_instructions", "comments"
    }
    return {
        k: v for k, v in entry.items()
        if v not in ("default", "") and k not in exclude_keys
    }


# Create a socket server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}\n")

    while True:
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue

            try:
                command = json.loads(data.decode())
                rpm = command.get("rpm")
                frequency = 60
                color = command.get("color")
                shutter_instructions = None  # Default to None, will be set if provided in command


                if rpm in mode_2_rpm.keys() and command.get("source") != "admin_script":
                    rpm_true, direction = mode_2_rpm.get(rpm)
                    color_settings = find_color_settings(color, main_settings)
                    rgb_string = color_settings[0].get("color") if color_settings else None
                    shutter_instructions = color_settings[0].get("shutter_instructions") if color_settings else None
                    camera_settings = clean_settings(color_settings[0])
                    for setting, value in camera_settings.items():
                        set_camera_setting(setting, int(value))



                elif command.get("source") == "admin_script":

                    if rpm in mode_2_rpm.keys():
                        rpm_true, direction = mode_2_rpm.get(rpm)
                        rgb_string, auto_wb  = color_to_rgb_string(color)
                    else:
                        rpm_true = rpm
                        direction = command.get("direction")
                        rgb_string = color
                    shutter_instructions = command.get("shutter_instructions")
                    try:
                        camera_setting = command.get("camera_setting")
                        camera_value = command.get("camera_value")
                        set_camera_setting(camera_setting, int(camera_value))
                    except Exception as e:
                        print(f"No camera setting: {e}. ")
                # Ensure value is int for API

                else:
                    print(f"Invalid RPM: {rpm}. Command not sent.")
                    continue


                # Get the current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"Received: rpm {rpm}, frequency {frequency}, "
                      f"color {color}", f"Direction {direction}, "
                      f"Shutter Instructions {shutter_instructions}"
                      f"  Timestamp: {timestamp}")

                # rgb_string = color_to_rgb_string(color)
                if rgb_string is None:
                    logging.error(f"Invalid color: {color}. Command not sent.")
                    print(f"Invalid color: {color}. Command not sent.")
                else:
                    # Send to Arduino 1: Frequency & Color
                    # print("test - 1")
                    if ser1 and ser1.is_open:
                        message_arduino1 = f"count{rgb_string}\n"
                        ser1.reset_input_buffer()
                        ser1.reset_output_buffer()
                        ser1.write(message_arduino1.encode())
                        print(f"----------------------- \nSent to Arduino 1: {message_arduino1}")

                        time.sleep(0.1)
                        raw_data1 = ser1.read(ser1.in_waiting)
                        response1 = raw_data1.decode('utf-8').strip() if raw_data1 else "No response"
                        logging.info(f"Received response from Arduino 1: {response1}")
                        # print(f"Decoded Response from Arduino 1: {response1} \n")
                    # print("test - 2")
                    # Send to Arduino 2: RPM
                    if ser2 and ser2.is_open:

                        # rpm_true = mode_2_rpm.get(rpm)
                        # print(f"RPM True: {rpm_true}, RPM: {rpm}")
                        if direction.lower() == "forward":
                            direction = ""
                        elif direction.lower() == "reverse":
                            direction = "-"
                        elif direction.lower() == "backward":
                            direction = "-"
                        message_arduino2 = f"rpm{direction}{rpm_true}\n"

                        ser2.reset_input_buffer()
                        ser2.reset_output_buffer()
                        ser2.write(message_arduino2.encode())
                        print(f"Sent to Arduino 2: {message_arduino2}")

                        time.sleep(0.1)
                        raw_data2 = ser2.read(ser2.in_waiting)
                        response2 = raw_data2.decode('utf-8').strip() if raw_data2 else "No response"
                        logging.info(f"Received response from Arduino 2: {response2}")
                        # print(f"Decoded Response from Arduino 2: {response2}")
                        # ================================================================
                        # time.sleep(2)
                        # if direction.lower() == "forward":
                        #     direction = "f"
                        # elif direction.lower() == "reverse":
                        #     direction = "b"
                        # elif direction.lower() == "backward":
                        #     direction = "b"
                        # else:
                        #     print(f"Invalid direction: {direction}. Command not sent.")
                        #
                        # if direction in ["f", "b"]:
                        #     message_arduino2 = f"{direction}\n"
                        #     ser2.reset_input_buffer()
                        #     ser2.reset_output_buffer()
                        #     ser2.write(message_arduino2.encode())
                        #     print(f"Sent to Arduino 2: {message_arduino2}")
                        #
                        #     time.sleep(0.1)
                        #     raw_data2 = ser2.read(ser2.in_waiting)
                        #     response2 = raw_data2.decode('utf-8').strip() if raw_data2 else "No response"
                        #     logging.info(f"Received response from Arduino 2: {response2}")
                            # print(f"Decoded Response from Arduino 2: {response2}")# Send to Arduino 2: RPM

                    # print("test - 3")
                    # print(ser3.is_open, ser2.is_open, ser1.is_open)
                    if ser3 and ser3.is_open and shutter_instructions is not None:
                        # print(f"Shutter Instructions: {shutter_instructions}")

                        message_arduino3 = f"{shutter_instructions}\n"
                        # print(f"Message to Arduino 3: {message_arduino3}")

                        ser3.reset_input_buffer()
                        ser3.reset_output_buffer()
                        ser3.write(message_arduino3.encode())
                        print(f"Sent to Arduino 3: {message_arduino3}")

                        time.sleep(0.1)
                        raw_data3 = ser3.read(ser3.in_waiting)
                        response3 = raw_data3.decode('utf-8').strip() if raw_data3 else "No response"
                        logging.info(f"Received response from Arduino 3: {response3}")
                        # print(f"Decoded Response from Arduino 3: {response3}")
                        # ================================================================


            except json.JSONDecodeError:
                print("Error: Received invalid JSON")
