import socket
import json
import serial
import time
import logging


logging.basicConfig(
    filename='log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def color_to_rgb_string(color):
    """Convert color name to RGB string. Return None if not recognized."""
    return color_counter_vals.get(color.lower())

# Arduino Serial Connection
SERIAL_PORT = "COM5"  # Adjust for your system
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2, dsrdtr=False)
    time.sleep(2)  # Allow Arduino to stabilize
    print("Connected to Arduino.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    ser = None  # Prevent crash if serial is unavailable

# Server Socket Details
HOST = "localhost"
PORT = 65432
color_counter_vals = {
    "red": 255,
    "green": 767,
    "blue": 1279,
    "yellow": 511,
    "cyan": 1023,
    "magenta": 1535,
    "purple": 1535,
    "white": 1
}

# Create a socket server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue

            # Parse JSON data
            # Parse JSON data
            try:
                command = json.loads(data.decode())
                frequency = command.get("frequency")
                color = command.get("color")
                print(f"Received: Frequency {frequency}, Color {color}")

                rgb_string = color_to_rgb_string(color)
                if rgb_string is None:
                    logging.error(f"Invalid color: {color}. Command not sent.")
                    print(f"Invalid color: {color}. Command not sent.")
                else:
                    print(f"Frequency: {frequency}, RGB String: {rgb_string}")

                    # Send command to Arduino
                    if ser and ser.is_open:
                        ser.reset_input_buffer()  # Clears input buffer before sending new command
                        ser.reset_output_buffer()  # Clears output buffer

                        message = f"{frequency},{rgb_string}\n"
                        ser.write(message.encode())
                        print(f"Sent to Arduino: {message}")

                        time.sleep(0.1)  # Give Arduino a moment to respond

                        # ------------------------------------------------------------ Read response
                        raw_data = ser.read(ser.in_waiting)  # Read raw bytes
                        print(f"Raw Data Received: {raw_data}")  # Debugging step

                        try:
                            response = raw_data.decode('utf-8')  # Try decoding as UTF-8
                        except UnicodeDecodeError:
                            response = raw_data.decode('latin-1')  # Use Latin-1 as fallback

                        response = response.strip()
                        logging.info(f"Received response: {response}")
                        print(f"Decoded Response: {response}")

                        ser.reset_input_buffer()  # Ensure buffer is empty after reading

            except json.JSONDecodeError:
                print("Error: Received invalid JSON")

