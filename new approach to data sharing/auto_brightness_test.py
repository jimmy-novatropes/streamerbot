import socket
import json
import time

HOST = "localhost"
PORT = 65432

COLORS = {
    "white": 0,
    "red": 0,
    "green": 0,
    "blue": 1,
    "yellow": 0,
    "magenta": 0,
    "cyan": 0,
}

BRIGHTNESS_LEVELS = [round(i * 0.1, 1) for i in range(1, 11)]  # 0.1 to 1.0

def send_to_server(rpm, color, direction, shutter, auto_wb):
    data = {
        "rpm": rpm,
        "color": color,
        "direction": direction,
        "shutter_instructions": shutter,
        "camera_setting": "white_balance_automatic",  # This is the setting for AWB
        "camera_value": auto_wb,  # Use the AWB value from COLORS
        "source": "admin_script"
    }
    print(f"Sending data: {data}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")

def set_awb(value):
    data = {
        "camera_setting": "white_balance_automatic",
        "camera_value": value,
        "source": "admin_script"
    }
    print(f"Setting AWB to {value}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
            time.sleep(1)
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server for AWB setting.")

if __name__ == "__main__":
    rpm = "1"
    direction = "forward"
    final_collection = []
    history = []

    color_keys = list(COLORS.keys())
    color_index = 0
    brightness_index = 0

    while color_index < len(color_keys):
        color = color_keys[color_index]
        awb = COLORS[color]
        set_awb(awb)  # set AWB before brightness loop

        brightness = BRIGHTNESS_LEVELS[brightness_index]
        shutter = f"d{brightness}"

        print(f"\nTesting color {color}, Shutter {shutter}, AWB {awb}")
        send_to_server(rpm, color, direction, shutter, awb)  # send the data to the server
        time.sleep(5)

        user_input = input("Enter notes, or 'b' to go back, Enter to skip: ").strip()

        if user_input.lower() == "b":
            if history:
                color_index, brightness_index = history.pop()
                print("🔁 Going back to previous combo...")
                continue
            else:
                print("⛔ Nothing to go back to.")
                continue

        if user_input:
            final_collection.append({
                "color": color,
                "shutter": shutter,
                "awb": awb,
                "notes": user_input
            })

        history.append((color_index, brightness_index))

        brightness_index += 1
        if brightness_index >= len(BRIGHTNESS_LEVELS):
            brightness_index = 0
            color_index += 1

    print("\nFinal notes collection:")
    for entry in final_collection:
        print(entry)
