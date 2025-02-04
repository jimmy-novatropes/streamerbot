import sys
import socket
import json

# Server socket details
HOST = "localhost"
PORT = 65432  # Same as in arduino_server.py


def send_to_server(frequency, color):
    """Sends frequency and color command to the always-running Python server."""
    data = {"frequency": frequency, "color": color}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(json.dumps(data).encode())  # Send data as JSON
    except ConnectionRefusedError:
        print("Error: Could not connect to the Arduino server. Is it running?")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python streamerbot_handler.py <frequency> <color>")
        sys.exit(1)
    print(sys.argv)

    frequency = sys.argv[1]
    color = sys.argv[2]

    send_to_server(frequency, color)
