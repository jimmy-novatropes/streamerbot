# import socket
# import json
# import serial
# import time
# import logging
#
#
# logging.basicConfig(
#     filename='log.txt', level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
#
# def color_to_rgb_string(color):
#     """Convert color name to RGB string. Return None if not recognized."""
#     return color_counter_vals.get(color.lower())
#
# # Arduino Serial Connection
# SERIAL_PORT = "COM5"  # Adjust for your system
# BAUD_RATE = 9600
#
# try:
#     ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2, dsrdtr=False)
#     time.sleep(2)  # Allow Arduino to stabilize
#     print("Connected to Arduino.")
# except serial.SerialException as e:
#     print(f"Error opening serial port: {e}")
#     ser = None  # Prevent crash if serial is unavailable
#
# # Server Socket Details
# HOST = "localhost"
# PORT = 65432
# color_counter_vals = {
#     "white": 1,
#     "red": 255,
#     "yellow": 511,
#     "green": 767,
#     "cyan": 1023,
#     "blue": 1279,
#     "magenta": 1535,
#     "purple": 1535,
# }
#
# # Create a socket server
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#     server.bind((HOST, PORT))
#     server.listen()
#     print(f"Server running on {HOST}:{PORT}")
#
#     while True:
#         conn, addr = server.accept()
#         with conn:
#             data = conn.recv(1024)
#             if not data:
#                 continue
#
#             # Parse JSON data
#             # Parse JSON data
#             try:
#                 command = json.loads(data.decode())
#                 rpm = command.get("rpm")
#                 color = command.get("color")
#                 direction = command.get("direction")
#                 print(f"Received: rpm {rpm}, Color {color}", f"Direction {direction}")
#
#                 rgb_string = color_to_rgb_string(color)
#                 if rgb_string is None:
#                     logging.error(f"Invalid color: {color}. Command not sent.")
#                     print(f"Invalid color: {color}. Command not sent.")
#                 else:
#                     print(f"rpm: {rpm}, RGB String: {rgb_string}")
#
#                     # Send command to Arduino
#                     if ser and ser.is_open:
#                         ser.reset_input_buffer()  # Clears input buffer before sending new command
#                         ser.reset_output_buffer()  # Clears output buffer
#
#                         message = f"{60},{rgb_string}\n"
#                         ser.write(message.encode())
#                         print(f"Sent to Arduino: {message}")
#
#                         time.sleep(0.1)  # Give Arduino a moment to respond
#
#                         # ------------------------------------------------------------ Read response
#                         raw_data = ser.read(ser.in_waiting)  # Read raw bytes
#                         print(f"Raw Data Received: {raw_data}")  # Debugging step
#
#                         try:
#                             response = raw_data.decode('utf-8')  # Try decoding as UTF-8
#                         except UnicodeDecodeError:
#                             response = raw_data.decode('latin-1')  # Use Latin-1 as fallback
#
#                         response = response.strip()
#                         logging.info(f"Received response: {response}")
#                         print(f"Decoded Response: {response}")
#
#                         ser.reset_input_buffer()  # Ensure buffer is empty after reading
#
#             except json.JSONDecodeError:
#                 print("Error: Received invalid JSON")
#


# import socket
# import json
# import serial
# import time
# import logging
#
# logging.basicConfig(
#     filename='log.txt', level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
#
# def color_to_rgb_string(color):
#     """Convert color name to RGB string. Return None if not recognized."""
#     return color_counter_vals.get(color.lower())
#
# # Define Arduino Serial Connections
# ARDUINO_1_PORT = "COM5"  # Adjust as needed
# ARDUINO_2_PORT = "COM6"  # Adjust as needed
# BAUD_RATE = 9600
#
# try:
#     ser1 = serial.Serial(ARDUINO_1_PORT, BAUD_RATE, timeout=2, dsrdtr=False)
#     time.sleep(2)
#     print("Connected to Arduino 1.")
# except serial.SerialException as e:
#     print(f"Error opening serial port {ARDUINO_1_PORT}: {e}")
#     ser1 = None
#
# try:
#     ser2 = serial.Serial(ARDUINO_2_PORT, BAUD_RATE, timeout=2, dsrdtr=False)
#     time.sleep(2)
#     print("Connected to Arduino 2.")
# except serial.SerialException as e:
#     print(f"Error opening serial port {ARDUINO_2_PORT}: {e}")
#     ser2 = None
#
# # Server Socket Details
# HOST = "localhost"
# PORT = 65432
# color_counter_vals = {
#     "white": 1,
#     "red": 255,
#     "yellow": 511,
#     "green": 767,
#     "cyan": 1023,
#     "blue": 1279,
#     "magenta": 1535,
#     "purple": 1535,
# }
#
# # Create a socket server
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
#     server.bind((HOST, PORT))
#     server.listen()
#     print(f"Server running on {HOST}:{PORT}")
#
#     while True:
#         conn, addr = server.accept()
#         with conn:
#             data = conn.recv(1024)
#             if not data:
#                 continue
#
#             try:
#                 command = json.loads(data.decode())
#                 rpm = command.get("rpm")
#                 frequency = command.get("frequency")
#                 color = command.get("color")
#                 print(f"Received: rpm {rpm}, frequency {frequency}, color {color}")
#
#                 rgb_string = color_to_rgb_string(color)
#                 if rgb_string is None:
#                     logging.error(f"Invalid color: {color}. Command not sent.")
#                     print(f"Invalid color: {color}. Command not sent.")
#                 else:
#                     # Send to Arduino 1: Frequency & Color
#                     if ser1 and ser1.is_open:
#                         message_arduino1 = f"{frequency},{rgb_string}\n"
#                         ser1.reset_input_buffer()
#                         ser1.reset_output_buffer()
#                         ser1.write(message_arduino1.encode())
#                         print(f"Sent to Arduino 1: {message_arduino1}")
#
#                         time.sleep(0.1)
#                         raw_data1 = ser1.read(ser1.in_waiting)
#                         try:
#                             response1 = raw_data1.decode('utf-8')
#                         except UnicodeDecodeError:
#                             response1 = raw_data1.decode('latin-1')
#
#                         response1 = response1.strip()
#                         logging.info(f"Received response from Arduino 1: {response1}")
#                         print(f"Decoded Response from Arduino 1: {response1}")
#
#                         ser1.reset_input_buffer()
#
#                     # Send to Arduino 2: RPM
#                     if ser2 and ser2.is_open:
#                         message_arduino2 = f"{rpm}\n"
#                         ser2.reset_input_buffer()
#                         ser2.reset_output_buffer()
#                         ser2.write(message_arduino2.encode())
#                         print(f"Sent to Arduino 2: {message_arduino2}")
#
#                         time.sleep(0.1)
#                         raw_data2 = ser2.read(ser2.in_waiting)
#                         try:
#                             response2 = raw_data2.decode('utf-8')
#                         except UnicodeDecodeError:
#                             response2 = raw_data2.decode('latin-1')
#
#                         response2 = response2.strip()
#                         logging.info(f"Received response from Arduino 2: {response2}")
#                         print(f"Decoded Response from Arduino 2: {response2}")
#
#                         ser2.reset_input_buffer()
#
#             except json.JSONDecodeError:
#                 print("Error: Received invalid JSON")

import socket
import json
import serial
import time
import logging
import serial.tools.list_ports

logging.basicConfig(
    filename='log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def color_to_rgb_string(color):
    """Convert color name to RGB string. Return None if not recognized."""
    return color_counter_vals.get(color.lower())


# Scan and assign Arduino COM ports
def find_arduinos():
    arduinos = {"led": None, "motor": None}

    available_ports = [port.device for port in serial.tools.list_ports.comports()]
    print(f"Available COM ports: {available_ports}")

    for port in available_ports:
        try:
            ser = serial.Serial(port, 9600, timeout=2, dsrdtr=False)
            time.sleep(2)  # Allow Arduino to initialize

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


            if response not in arduinos.keys():
                counter = 0
                while ser.in_waiting == 0:
                    # ser.write(b"whoareyou\n")
                    # time.sleep(0.5)
                    response = ser.read(ser.in_waiting).decode('utf-8').strip()
                    if response in arduinos.keys():
                        break
                    counter += 1
                    if counter > 50000:
                        break
        except serial.SerialException as e:
            print(f"Could not open {port}: {e}")

    return arduinos


# Find Arduinos dynamically
arduino_ports = find_arduinos()
ser1 = arduino_ports["led"]  # Arduino for frequency & color
ser2 = arduino_ports["motor"]  # Arduino for RPM

# Server Socket Details
HOST = "localhost"
PORT = 65432
color_counter_vals = {
    "white": 1,
    "red": 255,
    "yellow": 511,
    "green": 767,
    "cyan": 1023,
    "blue": 1279,
    "magenta": 1535,
    "purple": 1535,
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

            try:
                command = json.loads(data.decode())
                rpm = command.get("rpm")
                frequency = 60
                color = command.get("color")
                direction = command.get("direction")
                print(f"Received: rpm {rpm}, frequency {frequency}, color {color}", f"Direction {direction}")

                rgb_string = color_to_rgb_string(color)
                if rgb_string is None:
                    logging.error(f"Invalid color: {color}. Command not sent.")
                    print(f"Invalid color: {color}. Command not sent.")
                else:
                    # Send to Arduino 1: Frequency & Color
                    if ser1 and ser1.is_open:
                        message_arduino1 = f"{frequency},{rgb_string}\n"
                        ser1.reset_input_buffer()
                        ser1.reset_output_buffer()
                        ser1.write(message_arduino1.encode())
                        print(f"Sent to Arduino 1: {message_arduino1}")

                        time.sleep(0.1)
                        raw_data1 = ser1.read(ser1.in_waiting)
                        response1 = raw_data1.decode('utf-8').strip() if raw_data1 else "No response"
                        logging.info(f"Received response from Arduino 1: {response1}")
                        print(f"Decoded Response from Arduino 1: {response1}")

                    # Send to Arduino 2: RPM
                    if ser2 and ser2.is_open:

                        message_arduino2 = f"{rpm}, {direction}\n"
                        ser2.reset_input_buffer()
                        ser2.reset_output_buffer()
                        ser2.write(message_arduino2.encode())
                        print(f"Sent to Arduino 2: {message_arduino2}")

                        time.sleep(0.1)
                        raw_data2 = ser2.read(ser2.in_waiting)
                        response2 = raw_data2.decode('utf-8').strip() if raw_data2 else "No response"
                        logging.info(f"Received response from Arduino 2: {response2}")
                        print(f"Decoded Response from Arduino 2: {response2}")

            except json.JSONDecodeError:
                print("Error: Received invalid JSON")
