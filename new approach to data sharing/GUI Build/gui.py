import tkinter as tk
from tkinter import ttk
from support_functions import (
    load_colors, load_rpm_options, on_send,
    on_save, run_server_script,
    on_rpm_mode_change, run_streamerbot_script,
    on_color_change, stop_sculpture
)
import sys

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass


def start_gui():
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

    root = tk.Tk()
    root.title("Command Sender")
    root.configure(bg='#2871C9')
    root.minsize(800, 700)

    container = tk.Frame(root, bg='#2871C9')
    container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Reduce spacing between columns
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

    # RPM Mode
    ttk.Label(container, text="RPM Mode:").grid(row=row, column=0, sticky="w", **pad)
    rpm_mode_var = tk.StringVar()
    rpm_mode_menu = ttk.Combobox(container, textvariable=rpm_mode_var, values=list(mode_2_rpm.keys()), width=8)
    rpm_mode_menu.grid(row=row, column=1, sticky="w", **pad)
    rpm_mode_menu.set("2")

    rpm_entry = ttk.Entry(container, width=8)
    rpm_entry.grid(row=row, column=2, sticky="w", **pad)
    rpm_entry.insert(0, str(mode_2_rpm.get("2", [0])[0]))

    direction_var = tk.StringVar()
    direction_menu = ttk.Combobox(container, textvariable=direction_var, values=["forward", "backward"], width=8)
    direction_menu.grid(row=row, column=3, sticky="w", **pad)
    direction_menu.set(mode_2_rpm.get("2", [0, "forward"])[1])
    rpm_mode_menu.bind("<<ComboboxSelected>>", on_rpm_mode_change(rpm_mode_var, rpm_entry, direction_var))
    row += 1

    # Color
    ttk.Label(container, text="Color:").grid(row=row, column=0, sticky="w", **pad)
    color_var = tk.StringVar()
    color_menu = ttk.Combobox(container, textvariable=color_var, values=list(color_counter_vals.keys()), width=8)
    color_menu.grid(row=row, column=1, sticky="w", **pad)
    color_menu.set("white")

    color_value_entry = ttk.Entry(container, width=12)
    color_value_entry.grid(row=row, column=2, columnspan=2, sticky="w", **pad)
    color_value_entry.insert(0, str(color_counter_vals.get("white", 0)))
    color_menu.bind("<<ComboboxSelected>>", on_color_change(color_var, color_value_entry))
    row += 1

    # Shutter
    ttk.Label(container, text="Shutter:").grid(row=row, column=0, sticky="w",
                                               **pad)
    shutter_entry = ttk.Entry(container)
    shutter_entry.grid(row=row, column=1, **pad)
    shutter_entry.insert(0, "d.9")

    # Comments on the right of shutter
    ttk.Label(container, text="Comments:").grid(row=row, column=2,
                                                sticky="nw", **pad)


    row += 1  # Move to next row for settings
    comments_entry = tk.Text(container, height=8, width=40,
                             font=("Segoe UI", 14))
    comments_entry.grid(row=row, column=2, rowspan=6, sticky="n",
                        **pad)  # Tall, aligned top

    # Camera settings
    setting_entries = {}
    for setting, (min_val, max_val) in camera_settings.items():
        ttk.Label(container,
                  text=f"{setting.replace('_', ' ').title()} ({min_val}-{max_val}):").grid(
            row=row, column=0, sticky="w", **pad)
        entry = ttk.Entry(container)
        entry.grid(row=row, column=1, **pad)
        setting_entries[setting] = entry
        row += 1

    button_width = 30
    # Buttons
    ttk.Button(container,
               text="Send Command to Novatrope",
               command=on_send,
               width=button_width,
               style="RoundedButton.TButton").grid(row=row, column=0, **pad)
    ttk.Button(container, text="Save Current Settings", width=button_width,
               command=on_save, style="RoundedButton.TButton").grid(row=row, column=1, **pad)
    ttk.Button(container,
               text="Start Twitch Python Server",
               width=button_width,
               command=run_server_script, style="RoundedButton.TButton").grid(row=row, column=2, **pad)
    row += 1
    ttk.Button(container,
               text="Start Stream Apps", width=button_width,
               command=run_streamerbot_script, style="RoundedButton.TButton").grid(row=row, column=0, **pad)

    ttk.Button(container,
               text="Change the Sculpture", width=button_width,
               command=stop_sculpture, style="RoundedButton.TButton").grid(row=row, column=1, **pad)
    row += 1

    # Console
    console_output = tk.Text(container, height=10, width=150, bg="black", fg="white")
    console_output.grid(row=row, column=0, columnspan=6, padx=10, pady=10)
    sys.stdout = TextRedirector(console_output)
    sys.stderr = TextRedirector(console_output)

    root.mainloop()
