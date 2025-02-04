import sys
import logging
import serial
import time

def color_to_rgb_string(color):
    """Convert color name to RGB string. Return None if the color is not recognized."""
    rgb = color_counter_vals.get(color.lower())
    print("RGB:", rgb)
    return rgb

def send_command_to_arduino(frequency, color):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            logging.info(f"Opened serial connection on {SERIAL_PORT} at {BAUD_RATE} baud")
            print(f"Opened serial connection on {SERIAL_PORT} at {BAUD_RATE} baud")

            rgb_string = color_to_rgb_string(color)
            if not rgb_string:
                logging.error("Invalid color. Command not sent.")
                print("Invalid color. Command not sent.")
                return

            message = f"{frequency},{rgb_string}\n"

            ser.reset_input_buffer()  # Clear previous data to avoid buffer overflow
            ser.write(message.encode())  # Send command once
            logging.info(f"Sent to Arduino: {message}")
            print(f"Sent to Arduino: {message}")

            time.sleep(0.5)  # Reduced sleep time to avoid watchdog resets

            if ser.in_waiting > 0:
                response = ser.read(ser.in_waiting).decode('utf-8').strip()
                logging.info(f"Received response from Arduino: {response}")
                print(f"Received response from Arduino: {response}")
            else:
                logging.info("No response from Arduino.")
                print("No response from Arduino.")

    except serial.SerialException as e:
        logging.error(f"Error with serial connection: {e}")
        print(f"Error with serial connection: {e}")

def log_and_send_message(frequency, color):
    logging.info(f"Script started with frequency: {frequency} and color: {color}")
    send_command_to_arduino(frequency, color)
    logging.info("Script completed.")
    print("Script completed.")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        filename='../log.txt', level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Replace with your Arduino's serial port (Windows: COMx, Mac/Linux: /dev/ttyUSBx or /dev/ttyACMx)
    SERIAL_PORT = 'COM7'  # Change this to your correct COM port
    BAUD_RATE = 9600  # Ensure this matches the baud rate in your Arduino sketch

    # Mapping colors to RGB values
    color_counter_vals = {
        "red": 255,
        "green": 767,
        "blue": 1279,
        "yellow": 511,
        "cyan": 1023,
        "magenta": 1535,
        "white": 1
    }

    # Check if both arguments are provided
    if len(sys.argv) > 2:
        frequency = sys.argv[1]  # First argument
        color = sys.argv[2]  # Second argument
        frequency = 60  # Override with fixed frequency

        logging.info(f"Sending command to Arduino with frequency: {frequency} and color: {color}")
        log_and_send_message(frequency, color)
    else:
        logging.error("Not enough arguments provided!")
        print("Usage: python script.py <frequency> <color>")
