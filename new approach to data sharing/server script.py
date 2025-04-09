import socket
import json
import serial
import time
import logging
import serial.tools.list_ports
from datetime import datetime
import requests
import os
from support_functions import (save_or_extend_json, clean_settings,
                               color_to_rgb_string, find_arduinos,
                               set_camera_setting, find_color_settings)
from server_settings import (counter_color_values, modes_2_rpm)

logging.basicConfig(
    filename='log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Find Arduinos dynamically
arduino_ports = find_arduinos()
ser1 = arduino_ports["led"]  # Arduino for frequency & color
ser2 = arduino_ports["motor"]  # Arduino for RPM
ser3 = arduino_ports["shutter"]  # Arduino for Shutter and LED control

# Server Socket Details
HOST = "localhost"
PORT = 65432
color_counter_vals = counter_color_values()

mode_2_rpm = modes_2_rpm()
settings_json = "server_settings.json"
if os.path.exists(settings_json):
    with open(settings_json, "r") as f:
        main_settings = json.load(f)

color_settings = find_color_settings("white", main_settings)
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
                direction = None
                shutter_instructions = None  # Default to None, will be set if provided in command
                log_data = {
                    "color": color,
                    "rpm": rpm,
                    "frequency": frequency,
                    "direction": direction,
                    "shutter_instructions": shutter_instructions,
                }
                if command.get("source") == "admin_script":
                    log_data["source"] = "admin_script"
                else:
                    log_data["source"] = "streamerbot_script"
                save_or_extend_json(log_data, "log.json")

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

                if rgb_string is None:
                    logging.error(f"Invalid color: {color}. Command not sent.")
                    print(f"Invalid color: {color}. Command not sent.")
                else:

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

                    if ser2 and ser2.is_open:

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

                    if ser3 and ser3.is_open and shutter_instructions is not None:

                        message_arduino3 = f"{shutter_instructions}\n"
                        ser3.reset_input_buffer()
                        ser3.reset_output_buffer()
                        ser3.write(message_arduino3.encode())
                        print(f"Sent to Arduino 3: {message_arduino3}")
                        time.sleep(0.1)
                        raw_data3 = ser3.read(ser3.in_waiting)
                        response3 = raw_data3.decode('utf-8').strip() if raw_data3 else "No response"
                        logging.info(f"Received response from Arduino 3: {response3}")

            except json.JSONDecodeError:
                print("Error: Received invalid JSON")
