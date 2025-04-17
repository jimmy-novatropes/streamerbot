"""
-1 great
-2 ok but nothing special
-3 great but same pattern
-4 great but same pattern
-5 confusing
-6 great but same pattern
-7 great but same pattern
5 confusing
"""

import sys
import socket
import json
import time
from typing import final

# Server socket details
HOST = "localhost"
PORT = 65432  # Same as in arduino_server.py


COLORS = [
    "white",
    "red",
    "green",
    "blue",
    "yellow",
    "magenta",
    "cyan"

]

# DUTY_CYCLES = [round(i * 0.1, 1) for i in range(11)]  # 0.0 to 1.0 in steps
DUTY_CYCLES = [i * 0.01 for i in range(1, 11)]  # 0.1 to 1.0 in steps  # 0.0 to 1.0 in steps
rpm_modes = ["-1", "-2", "-3", "-4", "-5", "-6", "-7",\
             "1", "2", "3", "4", "5", "6", "7"]

def send_to_server(rpm, color, direction, shutter):
    data = {
        "rpm": rpm,
        "color": color,
        "direction": direction,
        "shutter_instructions": shutter
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")


if __name__ == "__main__":
    rpm = "1"
    direction = "forward"
    shutter = "d.9"
    final_collection = []

    best_combo = None


    for color in COLORS:
        # for duty in DUTY_CYCLES:
        for rpm in rpm_modes:


            print(f"Testing color {color} with rpm {rpm}")
            color = f"{color}"
            # shutter = f"d.{duty}"
            send_to_server(rpm, color, direction, shutter)
            time.sleep(35)  # time to observe

            # user_input = input("Keep this combo? (y/N): ").strip().lower()
            # if user_input == 'y':
            #     best_combo = color + f" with duty cycle {rpm}"
            #     print(f"Saved combo: {best_combo}\n")
            #     final_collection.append({
            #         "color": color,
            #         "rpm": rpm
            #     })
            #     break

    print("Final collection of selected combos:" + str(final_collection))
