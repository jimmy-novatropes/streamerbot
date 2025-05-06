import os
import json
import subprocess
import socket
import tkinter as tk
import threading
import requests
import sys
# import psutil
import serial
import serial.tools.list_ports
import time
import requests


from datetime import datetime
COLOR_FILE = "colors.json"
RPM_FILE = "rpm.json"
# Load color values
def load_colors():
    if os.path.exists(COLOR_FILE):
        with open(COLOR_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Invalid color JSON, using default.")
    return {}

# Load RPM values
def load_rpm_options():
    if os.path.exists(RPM_FILE):
        with open(RPM_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Invalid rpm JSON, using default.")
    return {}

color_counter_vals = load_colors()
mode_2_rpm = load_rpm_options()


HOST = "localhost"
PORT = 65432
# SETTINGS_FILE = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\GUI Build\saved_settings.json"
SETTINGS_FILE = r"A:\Desktop\Novatropes Stream\saved_settings.json"


def on_rpm_mode_change(rpm_mode_var, rpm_entry, direction_var):
    mode = rpm_mode_var.text
    rpm_val, dir_val = mode_2_rpm.get(mode, [0, "forward"])
    rpm_entry.delete(0, tk.END)
    rpm_entry.insert(0, str(rpm_val))
    direction_var.set(dir_val)


def run_streamerbot_script():
    try:
        subprocess.Popen([
            r"C:\\Users\\BloomTech\\Documents\\Streamer.bot-x64-0.2.6(1)\\Streamer.bot.exe"
        ])
        print("Streamer.bot launched.")
        subprocess.Popen([
            r"C:\Program Files\Streamlabs OBS\Streamlabs OBS.exe"
        ])
        print("++++++++++++++ GUI Command: StreamLabs launched.")
    except Exception as e:
        print(f"Failed to launch software: {e}")


def send_to_server(rpm, color, direction, shutter, cam_setting=None, cam_value=None):
    data = {
        "rpm": rpm,
        "color": color,
        "direction": direction,
        "shutter_instructions": shutter,
        "source": "admin_script"
    }
    if cam_setting and cam_value is not None:
        data["camera_setting"] = cam_setting
        data["camera_value"] = cam_value
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
        print("++++++++++++++ GUI Command: Data sent to Arduino server.")
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")

def on_color_change(color_var, color_value_entry):
    selected = color_var.text
    color_value_entry.delete(0, tk.END)
    color_value_entry.insert(0, str(color_counter_vals.get(selected, 0)))


def on_send(
        rpm_entry, color_value_entry, direction_var,
        shutter_entry, setting_entries):
    rpm = rpm_entry.text
    color = color_value_entry.text
    direction = direction_var.text
    shutter = shutter_entry.text

    for setting, entry in setting_entries.items():
        value = entry.text
        if value.strip() == "":
            print(f"{setting}: default")
        else:
            send_to_server(rpm, color, direction, shutter, setting, value)
    send_to_server(rpm, color, direction, shutter)

def on_save(color_var, color_value_entry, rpm_entry, direction_var,
            shutter_entry, comments_entry, setting_entries):
    selected_color = color_var.text
    color_value = color_value_entry.text.strip() or "0"

    entry_data = {
        "timestamp": datetime.now().isoformat(),
        "color_name": selected_color,
        "color": color_value,
        "rpm": rpm_entry.text,
        "direction": direction_var.text,
        "shutter_instructions": shutter_entry.text,
        "comments": comments_entry.text
    }

    for setting, entry in setting_entries.items():
        entry_data[setting] = entry.text or "default"

    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                all_data = json.load(f)
                if not isinstance(all_data, list):
                    all_data = []
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []

    updated = False
    for i, entry in enumerate(all_data):
        if isinstance(entry, dict) and entry.get("color") == color_value:
            all_data[i] = entry_data
            updated = True
            break
    if not updated:
        all_data.append(entry_data)

    with open(SETTINGS_FILE, "w") as f:
        json.dump(all_data, f, indent=4)
    print("Settings saved.")

    try:
        new_color_val = int(color_value)
        color_counter_vals[selected_color] = new_color_val
        with open(COLOR_FILE, "w") as f:
            json.dump(color_counter_vals, f, indent=4)
        print(f"++++++++++++++ GUI Command: Updated color '{selected_color}' to {new_color_val} in colors.json.")
    except ValueError:
        print(f"Invalid number entered for color '{selected_color}', not saved.")

import os

def run_server_script():
    try:
        script_path = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\server script.py"
        os.startfile(script_path)
        print("✅ Server script launched.")
    except Exception as e:
        print(f"❌ Failed to launch server script: {e}")


import multiprocessing

# def launch_script():
#     script_path = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\server script.py"
#     with open(script_path, encoding="utf-8") as f:
#         exec(f.read(), {'__name__': '__main__'})
#
# def run_server_script():
#     try:
#         multiprocessing.Process(target=launch_script).start()
#     except Exception as e:
#         print(f"Failed to run server: {e}")


# def run_server_script():
#     def target():
#         try:
#             script_path = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\server script.py"
#             script_dir = os.path.dirname(script_path)
#             print(
#                 "+++++++++++++++ GUI Command: Python Server script started.")
#             proc = subprocess.Popen(
#                 ["python", script_path],
#                 cwd=script_dir,
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True
#             )
#             for line in proc.stdout:
#                 print(line, end="")  # or redirect to console widget
#             for line in proc.stderr:
#                 print("ERROR:", line, end="")
#
#
#         except Exception as e:
#             print(f"Failed to start script: {e}")
#
#     threading.Thread(target=target, daemon=True).start()


# def free_com_port(self, port):
#     port = port.upper()
#     for proc in psutil.process_iter(["pid", "name", "cmdline"]):
#         try:
#             cmdline = " ".join(proc.info["cmdline"]).upper()
#             if port in cmdline:
#                 print(f"Killing PID {proc.pid} using {port}")
#                 proc.kill()
#                 return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue
#     print(f"No process found using {port}")
#     return False

def stop_sculpture(cam_setting=None, cam_value=None):
    data = {
        "rpm": 0,
        "color": 1,
        "direction": "forward",
        "shutter_instructions": "d.9",
        "source": "admin_script"
    }
    if cam_setting and cam_value is not None:
        data["camera_setting"] = cam_setting
        data["camera_value"] = cam_value
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
        print("++++++++++++++ GUI Command: Stopped the sculpture.")
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")


def reset_arduinos():
    data = {
        "reset_coms": True
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
        print("++++++++++++++ GUI Command: Resetting Arduino COM ports.")
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")

def sculpture_change_complete():
    data = {
        "load_last_command": True
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
        print("++++++++++++++ GUI Command: Sculpture change complete.")
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")

def update_timers(free_timer, priority_timer):
    args = {}


    if free_timer.text != "":
        if free_timer.text is not None:
            args["time_left_free"] = free_timer.text
    if priority_timer.text != "":
        if priority_timer.text is not None:
            args["time_left_priority"] = priority_timer.text

    if args:
        try:
            trigger_action_http(args)
            print("++++++++++++++ GUI Command: Timers updated.")
        except Exception as e:
            print(f"Error triggering action: {e}")


def reset_timer_variables():
    args = {
        "timer_active": "0",
        "timer_ended": "0",
        "time_left": "00:00"
    }
    try:
        trigger_action_http(args)
        print("++++++++++++++ GUI Command: Timer variables reset.")
    except Exception as e:
        print(f"Error triggering action: {e}")


def trigger_action_http(args):
    action_id = "2f1d77c1-7060-4420-9afa-e0a56109b97a"
    action_name = "9 - update variables"

    url = "http://127.0.0.1:7474/DoAction"
    payload = {
        "action": {
            "id": action_id,
            "name": action_name
        },
        "args": args
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.ok:
        print("✅ Action triggered")
    else:
        print("❌ Error:", response.text)



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
    results = [entry for entry in color_data if entry.get("color_name") == color_name.lower()]
    return results


def restart_sculpture():
    pass