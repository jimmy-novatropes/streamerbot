import sys
import logging
import time
import serial.tools.list_ports  # Ensures we're using pyserial

# Set up logging
logging.basicConfig(
    filename='../log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Detect available COM ports (useful for debugging)
available_ports = [port.device for port in serial.tools.list_ports.comports()]
print(f"Available COM ports: {available_ports}")

# Replace with your Arduino's COM port
SERIAL_PORT = 'COM5'  # Ensure this is correct for your system
BAUD_RATE = 9600  # Must match the baud rate in your Arduino sketch
# BAUD_RATE = 115200  # Update to match the baud rate in your Arduino sketch

# Dictionary mapping color names to values
color_counter_vals = {
    "red": 255,
    "green": 767,
    "blue": 1279,
    "yellow": 511,
    "cyan": 1023,
    "magenta": 1535,
    "white": 1
}

def color_to_rgb_string(color):
    """Convert color name to RGB string. Return None if not recognized."""
    return color_counter_vals.get(color.lower())


def send_command_to_arduino(frequency, color):
    """Send a command to Arduino using pyserial, ensuring a stable connection."""
    rgb_string = color_to_rgb_string(color)
    if rgb_string is None:
        logging.error(f"Invalid color: {color}. Command not sent.")
        print(f"Invalid color: {color}. Command not sent.")
        return

    message = f"{frequency},{rgb_string}\n"

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2, dsrdtr=False) as ser:
            time.sleep(0.2)  # Allow serial to stabilize
            ser.write(message.encode())  # Send command
            logging.info(f"Sent to Arduino: {message}")
            print(f"Sent to Arduino: {message}")

            time.sleep(0.5)  # Give Arduino time to process

            # Read response
            raw_data = ser.read(ser.in_waiting)  # Read raw bytes
            print(f"Raw Data Received: {raw_data}")  # Debugging step

            try:
                response = raw_data.decode('utf-8')  # Try decoding as UTF-8
            except UnicodeDecodeError:
                response = raw_data.decode('latin-1')  # Use Latin-1 as fallback

            response = response.strip()
            logging.info(f"Received response: {response}")
            print(f"Decoded Response: {response}")

    except serial.SerialException as e:
        logging.error(f"Serial connection error: {e}")
        print(f"Serial connection error: {e}")


if __name__ == "__main__":
    logging.info("Script started.")

    # Ensure correct number of arguments are passed from Streamer.bot
    if len(sys.argv) > 2:
        frequency = sys.argv[1]  # First argument from Streamer.bot
        color = sys.argv[2]  # Second argument from Streamer.bot
        print(f"Frequency: {frequency}, Color: {color}")

        # Send command to Arduino
        send_command_to_arduino(frequency, color)
    else:
        logging.error("Not enough arguments provided!")
        print("Usage: python script.py <frequency> <color>")
