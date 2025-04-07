import comtypes.client

# Initialize COM library
comtypes.CoInitialize()

# Create the MediaCapture object
media_capture = comtypes.client.CreateObject("Windows.Media.Capture.MediaCapture")

# Initialize the MediaCapture object
media_capture.Initialize()

# Get the VideoDeviceController
video_device_controller = media_capture.VideoDeviceController

# Check if white balance control is supported
if video_device_controller.WhiteBalanceControl.Supported:
    # Disable auto white balance
    video_device_controller.WhiteBalanceControl.SetPresetAsync(0)  # 0 corresponds to manual
    # Set manual white balance value (e.g., 4500K)
    video_device_controller.WhiteBalanceControl.SetValueAsync(4500)
else:
    print("White balance control is not supported.")

# Clean up
comtypes.CoUninitialize()
