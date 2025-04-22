import tkinter as tk
from tkinter import ttk
import sys
import json
from support_functions import (
    on_send,
    on_save,
    run_server_script,
    run_streamerbot_script,
    stop_sculpture,
    reset_arduinos,
    update_timers,
    reset_timer_variables

)

# Load color settings from JSON



def get_saved_settings():
    with open(r"A:\Desktop\Novatropes Stream\server_settings.json", "r") as f:
        color_settings_data = json.load(f)
    return color_settings_data

    # return [
    #     {
    #         "timestamp": "2025-04-01T15:01:04.005931",
    #         "color_name": "white",
    #         "color": "0",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d.9",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "1",
    #         "white_balance": "3000",
    #         "brightness": "-15",
    #         "contrast": "30",
    #         "saturation": "90",
    #         "hue": "0"
    #     },
    #     {
    #         "timestamp": "2025-04-01T15:09:23.323638",
    #         "color_name": "red",
    #         "color": "255",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d.6",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "0",
    #         "white_balance": "4500",
    #         "brightness": "-10",
    #         "contrast": "50",
    #         "saturation": "60",
    #         "hue": "0"
    #     },
    #     {
    #         "timestamp": "2025-04-01T15:16:29.796479",
    #         "color_name": "yellow",
    #         "color": "480",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d.7",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "0",
    #         "white_balance": "4500",
    #         "brightness": "-10",
    #         "contrast": "40",
    #         "saturation": "90",
    #         "hue": "10"
    #     },
    #     {
    #         "timestamp": "2025-04-01T15:22:46.058417",
    #         "color_name": "green",
    #         "color": "775",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d.6",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "0",
    #         "white_balance": "5500",
    #         "brightness": "-20",
    #         "contrast": "35",
    #         "saturation": "50",
    #         "hue": "-10"
    #     },
    #     {
    #         "timestamp": "2025-04-01T15:36:31.924739",
    #         "color_name": "cyan",
    #         "color": "950",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d.5",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "0",
    #         "white_balance": "4500",
    #         "brightness": "-20",
    #         "contrast": "35",
    #         "saturation": "60",
    #         "hue": "-3"
    #     },
    #     {
    #         "timestamp": "2025-04-01T15:43:34.908912",
    #         "color_name": "blue",
    #         "color": "1300",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d1.8",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "1",
    #         "white_balance": "6500",
    #         "brightness": "-20",
    #         "contrast": "30",
    #         "saturation": "60",
    #         "hue": "-10"
    #     },
    #     {
    #         "timestamp": "2025-04-01T15:58:02.441811",
    #         "color_name": "magenta",
    #         "color": "1575",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d.9",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "0",
    #         "white_balance": "5000",
    #         "brightness": "-20",
    #         "contrast": "35",
    #         "saturation": "70",
    #         "hue": "20"
    #     },
    #     {
    #         "timestamp": "2025-04-01T16:07:30.438273",
    #         "color_name": "purple",
    #         "color": "1470",
    #         "rpm": "685",
    #         "direction": "forward",
    #         "shutter_instructions": "d.9",
    #         "comments": "",
    #         "exposure": "1",
    #         "white_balance_auto": "0",
    #         "white_balance": "4750",
    #         "brightness": "-20",
    #         "contrast": "35",
    #         "saturation": "80",
    #         "hue": "0"
    #     }
    # ]
color_settings_data = get_saved_settings()

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

def on_color_change(color_var, color_value_entry, rpm_entry, direction_var, shutter_entry, setting_entries):
    def handler(event=None):
        color_name = color_var.get().lower()
        match = next((c for c in color_settings_data if c["color_name"] == color_name), None)
        if not match:
            return

        color_value_entry.delete(0, tk.END)
        color_value_entry.insert(0, match["color"])

        rpm_entry.delete(0, tk.END)
        rpm_entry.insert(0, match["rpm"])

        direction_var.set(match["direction"])

        shutter_entry.delete(0, tk.END)
        shutter_entry.insert(0, match["shutter_instructions"])

        setting_entries["exposure_time_absolute"].delete(0, tk.END)
        setting_entries["exposure_time_absolute"].insert(0, match["exposure"])

        setting_entries["white_balance_automatic"].delete(0, tk.END)
        setting_entries["white_balance_automatic"].insert(0, match["white_balance_auto"])

        setting_entries["white_balance_temperature"].delete(0, tk.END)
        setting_entries["white_balance_temperature"].insert(0, match["white_balance"])

        setting_entries["brightness"].delete(0, tk.END)
        setting_entries["brightness"].insert(0, match["brightness"])

        setting_entries["contrast"].delete(0, tk.END)
        setting_entries["contrast"].insert(0, match["contrast"])

        setting_entries["saturation"].delete(0, tk.END)
        setting_entries["saturation"].insert(0, match["saturation"])

        setting_entries["hue"].delete(0, tk.END)
        setting_entries["hue"].insert(0, match["hue"])
    return handler

def start_gui():
    root = tk.Tk()
    root.title("Command Sender")
    root.configure(bg='#2871C9')
    root.minsize(800, 700)

    container = tk.Frame(root, bg='#2871C9')
    container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    for col in range(4):
        container.grid_columnconfigure(col, weight=1)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Segoe UI", 16), background='#2871C9', foreground='white')
    style.configure("TEntry", font=("Segoe UI", 16), relief="flat", padding=3)
    style.configure("TCombobox", font=("Segoe UI", 16), padding=3)
    style.configure("RoundedButton.TButton", font=("Segoe UI", 16), padding=3, relief="flat",
                    borderwidth=0, background="#ffffff", foreground="#2871C9")
    style.map("RoundedButton.TButton", background=[("active", "#f0f0f0")], foreground=[("active", "#1d4f91")])

    pad = {'padx': 2, 'pady': 7}
    row = 0

    # RPM + Direction
    ttk.Label(container, text="RPM:").grid(row=row, column=0, sticky="w", **pad)
    rpm_entry = ttk.Entry(container, width=8)
    rpm_entry.grid(row=row, column=1, sticky="w", **pad)

    direction_var = tk.StringVar()
    direction_menu = ttk.Combobox(container, textvariable=direction_var, values=["forward", "backward"], width=10)
    direction_menu.grid(row=row, column=2, sticky="w", **pad)
    row += 1

    # Color + Value
    ttk.Label(container, text="Color:").grid(row=row, column=0, sticky="w", **pad)
    color_var = tk.StringVar()
    color_menu = ttk.Combobox(container, textvariable=color_var,
                               values=[c["color_name"] for c in color_settings_data], width=10)
    color_menu.grid(row=row, column=1, sticky="w", **pad)

    color_value_entry = ttk.Entry(container, width=12)
    color_value_entry.grid(row=row, column=2, sticky="w", **pad)
    row += 1

    # Shutter + Comments
    ttk.Label(container, text="Shutter:").grid(row=row, column=0, sticky="w", **pad)
    shutter_entry = ttk.Entry(container)
    shutter_entry.grid(row=row, column=1, **pad)

    ttk.Label(container, text="Comments:").grid(row=row, column=2, sticky="nw", **pad)
    row += 1
    comments_entry = tk.Text(container, height=8, width=40, font=("Segoe UI", 14))
    comments_entry.grid(row=row, column=2, rowspan=6, sticky="n", **pad)

    # Camera settings
    camera_settings = {
        "exposure_time_absolute": (1, 5000),
        "white_balance_automatic": (0, 1),
        "white_balance_temperature": (2800, 6500),
        "brightness": (-64, 64),
        "contrast": (0, 64),
        "saturation": (0, 128),
        "hue": (-40, 40),
    }

    setting_entries = {}
    # for setting, (min_val, max_val) in camera_settings.items():
    #     ttk.Label(container, text=f"{setting.replace('_', ' ').title()} ({min_val}-{max_val}):").grid(row=row, column=0, sticky="w", **pad)
    #     entry = ttk.Entry(container)
    #     entry.grid(row=row, column=1, **pad)
    #     setting_entries[setting] = entry
    #     row += 1


    total = len(camera_settings)
    for i, (setting, (min_val, max_val)) in enumerate(
            camera_settings.items()):



        label_text = f"{setting.replace('_', ' ').title()} ({min_val}-{max_val}):"
        ttk.Label(container, text=label_text).grid(row=row, column=0,
                                                   sticky="w", **pad)
        entry = ttk.Entry(container)
        entry.grid(row=row, column=1, **pad)
        setting_entries[setting] = entry

        if i == total - 2:
            label_text = f"Time Left (free):"
            ttk.Label(container, text=label_text).grid(row=row, column=2,
                                                       sticky="w", **pad)
            free_timer = ttk.Entry(container)
            free_timer.grid(row=row, column=3, **pad)
        if i == total - 1:
            label_text = f"Time Left (priority):"
            ttk.Label(container, text=label_text).grid(row=row, column=2,
                                                       sticky="w", **pad)
            priority_timer = ttk.Entry(container)
            priority_timer.grid(row=row, column=3, **pad)
        row += 1

    # Bind color change
    color_handler = on_color_change(color_var, color_value_entry, rpm_entry, direction_var, shutter_entry, setting_entries)
    color_menu.bind("<<ComboboxSelected>>", color_handler)

    # Set initial values using "white"
    color_var.set("white")
    color_handler()
    # Buttons
    button_width = 30
    # Buttons
    ttk.Button(container,
               text="Send Command to Novatrope",
               command=lambda: on_send(
                   rpm_entry,
                   color_value_entry,
                   direction_var,
                   shutter_entry, setting_entries
               ),
               width=button_width,
               style="RoundedButton.TButton").grid(row=row, column=0, **pad)
    ttk.Button(container, text="Save Current Settings", width=button_width,
               command=lambda: on_save(
                     color_var,
                        color_value_entry,
                        rpm_entry,
                        direction_var,
                        shutter_entry,
                        comments_entry,
                        setting_entries
                ),

               style="RoundedButton.TButton").grid(row=row,
                                                                    column=1,
                                                                    **pad)
    ttk.Button(container,
               text="Start Twitch Python Server",
               width=button_width,
               command=run_server_script, style="RoundedButton.TButton").grid(
        row=row, column=2, **pad)
    ttk.Button(container,
               text="Update Timers",
               width=button_width,
               command=lambda: update_timers(
                    free_timer,
                    priority_timer
               ),
               style="RoundedButton.TButton").grid(
        row=row, column=3, **pad)
    row += 1
    ttk.Button(container,
               text="Start Stream Apps", width=button_width,
               command=run_streamerbot_script,
               style="RoundedButton.TButton").grid(row=row, column=0, **pad)

    ttk.Button(container,
               text="Change the Sculpture", width=button_width,
               command=stop_sculpture, style="RoundedButton.TButton").grid(
        row=row, column=1, **pad)
    ttk.Button(container,
               text="Reset Arduino", width=button_width,
               command=reset_arduinos, style="RoundedButton.TButton").grid(
        row=row, column=2, **pad)
    ttk.Button(container,
               text="Clear Timer Variables", width=button_width,
               command=reset_timer_variables, style="RoundedButton.TButton").grid(
        row=row, column=3, **pad)
    row += 1
    row += 1

    # Console output
    console_output = tk.Text(container, height=10, width=150, bg="black", fg="white")
    console_output.grid(row=row, column=0, columnspan=4, padx=10, pady=10)
    sys.stdout = TextRedirector(console_output)
    sys.stderr = TextRedirector(console_output)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
