import socket
import json
import time

HOST = "localhost"
PORT = 65432

COLORS = [
    "white",
    "red",
    "green",
    "blue",
    "yellow",
    "magenta",
    "cyan"
]

AUTO_WHITE_BALANCE_OPTIONS = [0, 1]

def send_to_server(rpm, color, direction, shutter, awb):
    data = {
        "rpm": rpm,
        "color": color,
        "direction": direction,
        "shutter_instructions": shutter,
        "camera_setting": "white_balance_automatic",
        "camera_value": awb,
        "source": "admin_script"
    }
    print(f"Sending data: {data}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server.")

if __name__ == "__main__":
    rpm = "1"
    direction = "forward"
    shutter = "d.7"
    final_collection = []
    history = []

    color_index = 0
    awb_index = 0

    while color_index < len(COLORS):
        color = COLORS[color_index]
        awb = AUTO_WHITE_BALANCE_OPTIONS[awb_index]

        print(f"\nTesting color {color}, AWB {awb}")
        send_to_server(rpm, color, direction, shutter, awb)
        time.sleep(5)

        user_input = input("Enter notes, or 'b' to go back, Enter to skip: ").strip()

        if user_input.lower() == "b":
            if history:
                last = history.pop()
                color_index, awb_index = last
                print("🔁 Going back to previous combo...")
                continue
            else:
                print("⛔ Nothing to go back to.")
                continue

        if user_input:
            final_collection.append({
                "color": color,
                "awb": awb,
                "notes": user_input
            })

        history.append((color_index, awb_index))

        # Move to next
        awb_index += 1
        if awb_index >= len(AUTO_WHITE_BALANCE_OPTIONS):
            awb_index = 0
            color_index += 1

    print("\nFinal notes collection:")
    for entry in final_collection:
        print(entry)
