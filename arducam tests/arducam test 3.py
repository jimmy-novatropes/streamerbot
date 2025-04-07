import sys
import arducam_config_parser
from ArducamSDK import *

# Initialize the camera
index = 0  # Use 0 or your actual camera index
ret, camera_handle, config = Arducam_autoopenCamera(index)
if ret != 0:
    print("Failed to open camera.")
    sys.exit()

# Disable auto white balance
Arducam_setCtrl(camera_handle, CTRL_WB_AUTO, 0)

# Set manual white balance temperature (e.g. 4500K)
Arducam_setCtrl(camera_handle, CTRL_WB_TEMPERATURE, 4500)

# Optional: Save settings or preview image here...

# Close camera
Arducam_closeCamera(camera_handle)
