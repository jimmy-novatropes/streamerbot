import psutil
import os

import serial

try:
    ser = serial.Serial('COM15', 9600, timeout=5)
    print("✅ Port opened successfully!")
    ser.close()
except Exception as e:
    print(f"❌ {e}")


def find_and_kill_com_locks(com_ports):
    print("🔍 Checking for processes using COM ports...")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline_list = proc.info.get('cmdline') or []
            cmdline = ' '.join(cmdline_list).lower()
            for port in com_ports:
                if port.lower() in cmdline:
                    print(f"❌ Killing process {proc.pid} ({proc.info['name']}) using {port}")
                    proc.kill()
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            continue

def release_tcp_port(port):
    print(f"🔍 Checking for processes using TCP port {port}...")
    result = os.popen(f'netstat -ano | findstr :{port}').read()
    for line in result.splitlines():
        if "LISTENING" in line or "ESTABLISHED" in line:
            pid = line.strip().split()[-1]
            print(f"❌ Killing PID {pid} using port {port}")
            os.system(f'taskkill /PID {pid} /F')

# 🔧 Customize this list as needed
com_ports_to_clear = ['COM10', 'COM15', 'COM18']
tcp_port_to_clear = 5000  # Change if needed

# 🚀 Run both
find_and_kill_com_locks(com_ports_to_clear)
release_tcp_port(tcp_port_to_clear)
