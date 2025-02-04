import asyncio
import websockets
import logging
import time
import serial
import serial.tools.list_ports

# Set up logging
logging.basicConfig(
    filename='../log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Detect available COM ports (useful for debugging)
available_ports = [port.device for port in serial.tools.list_ports.comports()]
print(f"Available COM ports: {available_ports}")

# Replace with your Arduino's COM port
SERIAL_PORT = 'COM5'  # Update this for your system
BAUD_RATE = 9600  # Ensure this matches the Arduino sketch

# Color mappings
color_counter_vals = {
    "red": 255,
    "green": 767,
    "blue": 1279,
    "yellow": 511,
    "cyan": 1023,
    "magenta": 1535,
    "white": 1
}

# Open Serial Connection (Keep it open)
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2, dsrdtr=False)
    time.sleep(2)  # Allow serial to stabilize
    logging.info("Serial connection established.")
except serial.SerialException as e:
    logging.error(f"Serial connection error: {e}")
    print(f"Serial connection error: {e}")
    ser = None  # Handle failure gracefully

def color_to_rgb_string(color):
    """Convert color name to RGB string. Return None if not recognized."""
    return color_counter_vals.get(color.lower())

async def handle_websocket(websocket, path):
    """Handles incoming WebSocket messages."""
    async for message in websocket:
        try:
            logging.info(f"Received WebSocket message: {message}")
            print(f"Received: {message}")

            parts = message.split(",")  # Expecting "frequency,color"
            if len(parts) != 2:
                logging.error("Invalid message format. Expected: frequency,color")
                await websocket.send("Error: Invalid format. Use 'frequency,color'")
                continue

            frequency, color = parts
            rgb_string = color_to_rgb_string(color)

            if rgb_string is None:
                logging.error(f"Invalid color: {color}. Command not sent.")
                await websocket.send(f"Error: Invalid color '{color}'")
                continue

            command = f"{frequency},{rgb_string}\n"

            if ser and ser.is_open:
                ser.write(command.encode())  # Send command
                logging.info(f"Sent to Arduino: {command}")
                print(f"Sent to Arduino: {command}")

                time.sleep(0.5)  # Give Arduino time to process

                # Read response
                raw_data = ser.read(ser.in_waiting)  # Read raw bytes
                if raw_data:
                    try:
                        response = raw_data.decode('utf-8').strip()
                    except UnicodeDecodeError:
                        response = raw_data.decode('latin-1').strip()
                    logging.info(f"Received response: {response}")
                    print(f"Decoded Response: {response}")

                    await websocket.send(f"Arduino Response: {response}")
                else:
                    await websocket.send("No response from Arduino.")

            else:
                await websocket.send("Error: Serial connection not available.")

        except Exception as e:
            logging.error(f"Error processing message: {e}")
            await websocket.send(f"Error: {e}")

# Start WebSocket server
start_server = websockets.serve(handle_websocket, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
