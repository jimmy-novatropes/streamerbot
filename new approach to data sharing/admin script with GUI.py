import tkinter as tk
from tkinter import ttk
import socket
import json
import os
from datetime import datetime

HOST = "localhost"
PORT = 65432
SETTINGS_FILE = "saved_settings.json"
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

camera_settings = {
    "exposure_time_absolute": (1, 5000),
    "white_balance_automatic": (0, 1),
    "white_balance_temperature": (2800, 6500),
    "brightness": (-64, 64),
    "contrast": (0, 64),
    "saturation": (0, 128),
    "hue": (-40, 40),
}

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

def on_send():
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
    send_to_server(rpm, color, direction, shutter)  # Send without camera settings for backward compatibility

def on_save():
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

    # Update colors.json with new value for selected color
    try:
        new_color_val = int(color_value)
        color_counter_vals[selected_color] = new_color_val
        with open(COLOR_FILE, "w") as f:
            json.dump(color_counter_vals, f, indent=4)
        print(f"Updated color '{selected_color}' to {new_color_val} in colors.json.")
    except ValueError:
        print(f"Invalid number entered for color '{selected_color}', not saved.")
# GUI Setup
root = tk.Tk()
root.title("Command Sender")
root.configure(bg='#2871C9')
root.minsize(600, 600)

container = tk.Frame(root, bg='#2871C9')
container.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 16), background='#2871C9', foreground='white')
style.configure("TEntry", font=("Segoe UI", 16), relief="flat", padding=6)
style.configure("TCombobox", font=("Segoe UI", 16), padding=6)
style.configure("RoundedButton.TButton", font=("Segoe UI", 16), padding=6, relief="flat", borderwidth=0, background="#ffffff", foreground="#2871C9")
style.map("RoundedButton.TButton", background=[("active", "#f0f0f0")], foreground=[("active", "#1d4f91")])

pad = {'padx': 10, 'pady': 10}

row = 0

# RPM Mode, RPM, Direction in one row
ttk.Label(container, text="RPM Mode:").grid(row=row, column=0, sticky="w", **pad)
rpm_mode_var = tk.StringVar()
rpm_mode_menu = ttk.Combobox(container, textvariable=rpm_mode_var, values=list(mode_2_rpm.keys()), width=8)
rpm_mode_menu.grid(row=row, column=1, sticky="w", **pad)
rpm_mode_menu.set("2")

rpm_entry = ttk.Entry(container, width=8)
rpm_entry.grid(row=row, column=2, sticky="w", **pad)
rpm_entry.insert(0, str(mode_2_rpm.get("2", [0])[0]))

direction_var = tk.StringVar()
direction_menu = ttk.Combobox(container, textvariable=direction_var, values=["forward", "backward"], width=10)
direction_menu.grid(row=row, column=3, sticky="w", **pad)
direction_menu.set(mode_2_rpm.get("2", [0, "forward"])[1])
row += 1

def on_rpm_mode_change(event):
    mode = rpm_mode_var.get()
    rpm_val, dir_val = mode_2_rpm.get(mode, [0, "forward"])
    rpm_entry.delete(0, tk.END)
    rpm_entry.insert(0, str(rpm_val))
    direction_var.set(dir_val)

rpm_mode_menu.bind("<<ComboboxSelected>>", on_rpm_mode_change)

# Color and Color Value in one row
ttk.Label(container, text="Color:").grid(row=row, column=0, sticky="w", **pad)
color_var = tk.StringVar()
color_menu = ttk.Combobox(container, textvariable=color_var, values=list(color_counter_vals.keys()), width=12)
color_menu.grid(row=row, column=1, sticky="w", **pad)
color_menu.set("white")

color_value_entry = ttk.Entry(container, width=12)
color_value_entry.grid(row=row, column=2, columnspan=2, sticky="w", **pad)
color_value_entry.insert(0, str(color_counter_vals.get("white", 0)))
row += 1

def on_color_change(event):
    selected = color_var.get()
    color_value_entry.delete(0, tk.END)
    color_value_entry.insert(0, str(color_counter_vals.get(selected, 0)))

color_menu.bind("<<ComboboxSelected>>", on_color_change)

shutter_entry = ttk.Entry(container)
shutter_entry.grid(row=row, column=1, **pad)
shutter_entry.insert(0, "d.9")
ttk.Label(container, text="Shutter:").grid(row=row, column=0, sticky="w", **pad)
row += 1

# Camera settings
setting_entries = {}
for setting, (min_val, max_val) in camera_settings.items():
    ttk.Label(container, text=f"{setting.replace('_', ' ').title()} ({min_val}-{max_val}):").grid(row=row, column=0, sticky="w", **pad)
    entry = ttk.Entry(container)
    entry.grid(row=row, column=1, **pad)
    setting_entries[setting] = entry
    row += 1

# Comments
ttk.Label(container, text="Comments:").grid(row=row, column=0, sticky="nw", **pad)
comments_entry = tk.Text(container, height=4, width=30, font=("Segoe UI", 14))
comments_entry.grid(row=row, column=0, columnspan=3, **pad)

send_btn = ttk.Button(container, text="Send", command=on_send, style="RoundedButton.TButton")
send_btn.grid(row=row, column=3, **pad)

save_btn = ttk.Button(container, text="Save Settings", command=on_save, style="RoundedButton.TButton")
save_btn.grid(row=row, column=4, **pad)

row += 1


root.mainloop()
