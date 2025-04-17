import os
import json
import subprocess
import socket
import tkinter as tk
import threading
# import psutil

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
SETTINGS_FILE = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\GUI Build\saved_settings.json"


def on_rpm_mode_change(rpm_mode_var, rpm_entry, direction_var):
    mode = rpm_mode_var.get()
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
        print("StreamLabs launched.")
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
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")

def on_color_change(color_var, color_value_entry):
    selected = color_var.get()
    color_value_entry.delete(0, tk.END)
    color_value_entry.insert(0, str(color_counter_vals.get(selected, 0)))


def on_send(
        rpm_entry, color_value_entry, direction_var,
        shutter_entry, setting_entries):
    rpm = rpm_entry.get()
    color = color_value_entry.get()
    direction = direction_var.get()
    shutter = shutter_entry.get()

    for setting, entry in setting_entries.items():
        value = entry.get()
        if value.strip() == "":
            print(f"{setting}: default")
        else:
            send_to_server(rpm, color, direction, shutter, setting, value)
    send_to_server(rpm, color, direction, shutter)

def on_save(color_var, color_value_entry, rpm_entry, direction_var,
            shutter_entry, comments_entry, setting_entries):
    selected_color = color_var.get()
    color_value = color_value_entry.get().strip() or "0"

    entry_data = {
        "timestamp": datetime.now().isoformat(),
        "color_name": selected_color,
        "color": color_value,
        "rpm": rpm_entry.get(),
        "direction": direction_var.get(),
        "shutter_instructions": shutter_entry.get(),
        "comments": comments_entry.get("1.0", "end").strip()
    }

    for setting, entry in setting_entries.items():
        entry_data[setting] = entry.get() or "default"

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
        print(f"Updated color '{selected_color}' to {new_color_val} in colors.json.")
    except ValueError:
        print(f"Invalid number entered for color '{selected_color}', not saved.")


def run_server_script():
    def target():
        try:
            script_path = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\server script.py"
            script_dir = os.path.dirname(script_path)

            proc = subprocess.Popen(
                ["python", script_path],
                cwd=script_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in proc.stdout:
                print(line, end="")  # or redirect to console widget
            for line in proc.stderr:
                print("ERROR:", line, end="")

        except Exception as e:
            print(f"Failed to start script: {e}")

    threading.Thread(target=target, daemon=True).start()


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
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")
