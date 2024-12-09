# import sys
# import logging
# import serial
# import time
#
# # Set up logging to log to a file named 'log.txt'
# logging.basicConfig(
#     filename='log.txt', level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s')
#
# # Replace with your Arduino's serial port (on Windows it might be COM3, COM4, etc.)
# SERIAL_PORT = 'COM9'  # Replace with the correct COM port for the FTDI
# BAUD_RATE = 9600  # Ensure this matches the baud rate in your Arduino sketch
#
# # Dictionary to map color names to RGB values
# color_to_rgb = {
#     "red": (255, 0, 0),
#     "green": (0, 255, 0),
#     "blue": (0, 0, 255),
#     "yellow": (255, 255, 0),
#     "cyan": (0, 255, 255),
#     "magenta": (255, 0, 255),
#     "white": (255, 255, 255),
#     "black": (0, 0, 0)
#     # Add more colors if needed
# }
#
#
# def color_to_rgb_string(color):
#     """Convert color name to RGB string. Return None if the color is not recognized."""
#     rgb = color_to_rgb.get(color.lower())
#     if rgb:
#         return f"{rgb[0]},{rgb[1]},{rgb[2]}"
#     else:
#         logging.error(f"Unrecognized color: {color}")
#         return None
#
#
# def send_command_to_arduino(frequency, color):
#     try:
#         # Set up the serial connection
#         with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
#             logging.info(f"Opened serial connection on {SERIAL_PORT} at {BAUD_RATE} baud")
#
#             # Convert color to RGB string
#             rgb_string = color_to_rgb_string(color)
#             if not rgb_string:
#                 logging.error("Invalid color. Command not sent.")
#                 return  # If the color is invalid, don't send the command
#
#             # Format the message to be sent to the Arduino
#             message = f"{frequency},{rgb_string}\n"
#
#             # Send the message to the Arduino
#             ser.write(message.encode())  # Send as bytes
#             logging.info(f"Sent to Arduino: {message}")
#
#             # Optional: wait for a response from Arduino
#             time.sleep(2)  # Allow time for Arduino to respond, if needed
#             if ser.in_waiting > 0:
#                 response = ser.readline().decode('utf-8').strip()
#                 logging.info(f"Received response from Arduino: {response}")
#
#     except serial.SerialException as e:
#         logging.error(f"Error with serial connection: {e}")
#
#
# def log_and_send_message(frequency, color):
#     logging.info(f"Script started with frequency: {frequency} and color: {color}")
#     send_command_to_arduino(frequency, color)
#     logging.info("Script completed.")
#
#
# if __name__ == "__main__":
#     # Check if both arguments are provided
#     if len(sys.argv) > 2:
#         frequency = sys.argv[1]  # First argument
#         color = sys.argv[2]  # Second argument
#         log_and_send_message(frequency, color)
#     else:
#         logging.error("Not enough arguments provided!")


import sys
import logging
import serial
import time

# Set up logging to log to a file named 'log.txt'
logging.basicConfig(
    filename='log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your Arduino's serial port (on Windows it might be COM3, COM4, etc.)
SERIAL_PORT = 'COM1'  # Replace with the correct COM port for the FTDI
BAUD_RATE = 9600  # Ensure this matches the baud rate in your Arduino sketch

# Dictionary to map color names to RGB values
color_to_rgb = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
    # Add more colors if needed
}

color_counter_vals = {
    "red": 255,
    "green": 767,
    "blue": 1279,
    "yellow": 511,
    "cyan": 1023,
    "magenta": 1535,
    "white": 0
}


def color_to_rgb_string(color):
    """Convert color name to RGB string. Return None if the color is not recognized."""
    rgb = color_counter_vals.get(color.lower())
    return rgb
    # if rgb:
    #     return f"{rgb[0]},{rgb[1]},{rgb[2]}"
    # else:
    #     logging.error(f"Unrecognized color: {color}")
    #     return None


def send_command_to_arduino(frequency, color):
    try:
        # Set up the serial connection
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=10) as ser:
            logging.info(f"Opened serial connection on {SERIAL_PORT} at {BAUD_RATE} baud")

            # Convert color to RGB string
            rgb_string = color_to_rgb_string(color)
            if not rgb_string:
                logging.error("Invalid color. Command not sent.")
                return  # If the color is invalid, don't send the command

            # Format the message to be sent to the Arduino
            message = f"{frequency},{rgb_string}\n"

            # Send the message to the Arduino
            ser.write(message.encode())  # Send as bytes
            logging.info(f"Sent to Arduino: {message}")

            # Wait and read response from Arduino
            time.sleep(3)  # Allow time for Arduino to respond, if needed
            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting).decode('utf-8').strip()
                logging.info(f"Received response from Arduino: {response}")
            else:
                logging.info("No response from Arduino.")

    except serial.SerialException as e:
        logging.error(f"Error with serial connection: {e}")


def log_and_send_message(frequency, color):
    logging.info(f"Script started with frequency: {frequency} and color: {color}")
    send_command_to_arduino(frequency, color)
    logging.info("Script completed.")


if __name__ == "__main__":
    # Check if both arguments are provided
    if len(sys.argv) > 2:
        frequency = sys.argv[1]  # First argument
        color = sys.argv[2]  # Second argument
        log_and_send_message(frequency, color)
    else:
        logging.error("Not enough arguments provided!")

