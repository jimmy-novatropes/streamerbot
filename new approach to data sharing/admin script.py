import sys
import socket
import json
import time
from typing import final

# Server socket details
HOST = "localhost"
PORT = 65432  # Same as in arduino_server.py


COLORS = [
    "red",
    "green",
    "blue",
    "yellow",
    "magenta",
    "cyan",
    "white"
]

# DUTY_CYCLES = [round(i * 0.1, 1) for i in range(11)]  # 0.0 to 1.0 in steps
DUTY_CYCLES = [i * 0.01 for i in range(1, 11)]  # 0.1 to 1.0 in steps  # 0.0 to 1.0 in steps

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
        for duty in DUTY_CYCLES:
            print(f"Testing color {color} with duty cycle {duty}")
            color = f"{color}"
            shutter = f"d.{duty}"
            send_to_server(rpm, color, direction, shutter)
            time.sleep(1)  # time to observe

            user_input = input("Keep this combo? (y/N): ").strip().lower()
            if user_input == 'y':
                best_combo = color + f" with duty cycle {duty}"
                print(f"Saved combo: {best_combo}\n")
                final_collection.append({
                    "color": color,
                    "duty_cycle": duty
                })
                break

    print("Final collection of selected combos:" + str(final_collection))
