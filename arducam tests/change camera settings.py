import ArducamEvkSDK as arducam
import time

# List available cameras
devices = arducam.DeviceList()
devs = devices.devices()
param = arducam.Param()

# Open first camera
camera = arducam.Camera()
print(camera.open(param))

# param.config_file_name = config_path  # a path of config file
# param.bin_config = config_path.endswith(".bin")  # if the config file is a bin file
param.device = 0
print(camera.open(param))

if not devices:
    print("No Arducam cameras found.")
    exit()



camera.init()
time.sleep(1)  # Give it a second to initialize

# Disable Auto White Balance
camera.set_control("AutoWhiteBalance", 0)

# Optional: Set Manual White Balance (e.g., 4500K)
# camera.set_control("WhiteBalance", 4500)

# Print to confirm
print("Auto White Balance disabled, manual white balance set to 4500K.")

# Cleanup
camera.stop()
camera.close()
