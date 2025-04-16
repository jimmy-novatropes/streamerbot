import socket
import json
import time
import logging
import serial.tools.list_ports
from datetime import datetime
import os
import sys
from typing import Dict
from contextlib import contextmanager
from support_functions import (save_or_extend_json, clean_settings,
                               color_to_rgb_string, find_arduinos,
                               set_camera_setting, find_color_settings)
from server_settings import (counter_color_values, modes_2_rpm)
# import psutil

# Configure logging
logging.basicConfig(
    filename='log.txt', level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ArduinoServer:
    """Server class to handle communication with Arduinos and clients."""
    
    def __init__(self, host: str = "localhost", port: int = 65432):
        """Initialize the server with configuration."""
        self.host = host
        self.port = port
        self.settings_json = "server_settings.json"
        self.main_settings = self._load_settings()
        self.mode_2_rpm = modes_2_rpm()
        self.color_counter_vals = counter_color_values()
        
        # Initialize serial connections
        self.arduino_ports = find_arduinos()
        self.ser1 = self.arduino_ports["led"]  # Arduino for frequency & color
        self.ser2 = self.arduino_ports["motor"]  # Arduino for RPM
        self.ser3 = self.arduino_ports["shutter"]  # Arduino for Shutter and LED control
        
        logging.info(f"Server initialized with {len(self.arduino_ports)} Arduino connections")
    
    def _load_settings(self) -> Dict:
        """Load settings from JSON file."""
        if os.path.exists(self.settings_json):
            try:
                with open(self.settings_json, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Failed to parse {self.settings_json}")
                return {}
        return {}
    
    @contextmanager
    def _serial_connection(self, ser: serial.Serial, name: str):
        """Context manager for safe serial communication."""
        try:
            if ser and ser.is_open:
                yield ser
            else:
                logging.warning(f"Serial connection {name} is not available")
                yield None
        except Exception as e:
            logging.error(f"Error with serial connection {name}: {e}")
            yield None
    
    def _send_to_arduino(self, ser: serial.Serial, message: str, name: str) -> str:
        """Send message to Arduino and get response."""
        if not ser or not ser.is_open:
            logging.warning(f"Cannot send to {name}: connection not available")
            return "No connection"
        
        try:
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            ser.write(message.encode())
            logging.info(f"Sent to {name}: {message}")
            
            time.sleep(0.1)
            raw_data = ser.read(ser.in_waiting)
            response = raw_data.decode('utf-8').strip() if raw_data else "No response"
            logging.info(f"Received response from {name}: {response}")
            return response
        except Exception as e:
            logging.error(f"Error communicating with {name}: {e}")
            return f"Error: {str(e)}"
    
    def _process_command(self, command: Dict) -> Dict:
        """Process incoming command and prepare response data."""
        rpm = command.get("rpm")
        frequency = 60
        color = command.get("color")
        direction = None
        shutter_instructions = None
        rgb_string = None
        
        log_data = {
            "color": color,
            "rpm": rpm,
            "frequency": frequency,
            "direction": direction,
            "shutter_instructions": shutter_instructions,
            "source": command.get("source", "streamerbot_script")
        }
        
        # Save command to log
        save_or_extend_json(log_data, "log.json")
        
        # Process based on source
        if command.get("source") == "admin_script":
            return self._process_admin_command(command)
        else:
            return self._process_streamerbot_command(command)
    
    def _process_admin_command(self, command: Dict) -> Dict:
        """Process command from admin script."""
        rpm = command.get("rpm")
        color = command.get("color")
        
        if rpm in self.mode_2_rpm:
            rpm_true, direction = self.mode_2_rpm.get(rpm)
            rgb_string, _ = color_to_rgb_string(color)
        else:
            rpm_true = rpm
            direction = command.get("direction")
            rgb_string = color
            
        shutter_instructions = command.get("shutter_instructions")
        
        # Apply camera settings if provided
        try:
            camera_setting = command.get("camera_setting")
            camera_value = command.get("camera_value")
            if camera_setting and camera_value:
                set_camera_setting(camera_setting, int(camera_value))
        except Exception as e:
            logging.error(f"Camera setting error: {e}")
            
        return {
            "rpm_true": rpm_true,
            "direction": direction,
            "rgb_string": rgb_string,
            "shutter_instructions": shutter_instructions
        }
    
    def _process_streamerbot_command(self, command: Dict) -> Dict:
        """Process command from streamerbot script."""
        rpm = command.get("rpm")
        color = command.get("color")
        
        if rpm not in self.mode_2_rpm:
            logging.error(f"Invalid RPM: {rpm}. Command not processed.")
            return None
            
        rpm_true, direction = self.mode_2_rpm.get(rpm)
        color_settings = find_color_settings(color, self.main_settings)
        
        if not color_settings:
            logging.error(f"No color settings found for {color}")
            return None
            
        rgb_string = color_settings[0].get("color")
        shutter_instructions = color_settings[0].get("shutter_instructions")
        
        # Apply camera settings
        camera_settings = clean_settings(color_settings[0])
        for setting, value in camera_settings.items():
            set_camera_setting(setting, int(value))
            
        return {
            "rpm_true": rpm_true,
            "direction": direction,
            "rgb_string": rgb_string,
            "shutter_instructions": shutter_instructions
        }
    
    def _execute_arduino_commands(self, command_data: Dict) -> None:
        """Execute commands on Arduinos based on processed data."""
        if not command_data:
            return
            
        rgb_string = command_data.get("rgb_string")
        rpm_true = command_data.get("rpm_true")
        direction = command_data.get("direction")
        shutter_instructions = command_data.get("shutter_instructions")
        
        # Send to Arduino 1 (LED)
        if rgb_string:
            with self._serial_connection(self.ser1, "LED Arduino") as ser:
                if ser:
                    self._send_to_arduino(ser, f"count{rgb_string}\n", "LED Arduino")
        
        # Send to Arduino 2 (Motor)
        if rpm_true is not None:
            with self._serial_connection(self.ser2, "Motor Arduino") as ser:
                if ser:
                    # Format direction
                    dir_str = ""
                    if direction and direction.lower() in ["reverse", "backward"]:
                        dir_str = "-"
                    message = f"rpm{dir_str}{rpm_true}\n"
                    self._send_to_arduino(ser, message, "Motor Arduino")
        
        # Send to Arduino 3 (Shutter)
        if shutter_instructions:
            with self._serial_connection(self.ser3, "Shutter Arduino") as ser:
                if ser:
                    self._send_to_arduino(ser, f"{shutter_instructions}\n", "Shutter Arduino")





    def run(self) -> None:
        """Run the server and handle incoming connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            try:
                server.bind((self.host, self.port))
                server.listen()
                logging.info(f"Server running on {self.host}:{self.port}")
                print(f"Server running on {self.host}:{self.port}\n")
                
                while True:
                    conn, addr = server.accept()
                    with conn:
                        logging.info(f"Connection from {addr}")
                        data = conn.recv(1024)
                        if not data:
                            continue
                            
                        try:
                            command = json.loads(data.decode())
                            processed_data = self._process_command(command)
                            self._execute_arduino_commands(processed_data)
                            
                            # Log command details
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            print(f"Processed command at {timestamp}: {command}")
                            
                        except json.JSONDecodeError:
                            logging.error("Received invalid JSON")
                            print("Error: Received invalid JSON")
                        except Exception as e:
                            logging.error(f"Error processing command: {e}")
                            print(f"Error: {e}")
                            
            except Exception as e:
                logging.error(f"Server error: {e}")
                print(f"Server error: {e}")
                sys.exit(1)

if __name__ == "__main__":
    server = ArduinoServer()
    server.run()
