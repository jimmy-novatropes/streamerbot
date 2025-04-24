import subprocess
import sys

script_path = r"C:\Users\BloomTech\Documents\twitch streaming\streamerbot\new approach to data sharing\server script.py"
print("Running:", script_path)

proc = subprocess.Popen(
    [sys.executable, script_path],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

out, err = proc.communicate()

print("STDOUT:", out)
print("STDERR:", err)
