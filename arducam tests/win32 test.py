import win32com.client
import pythoncom

# Initialize COM libraries
pythoncom.CoInitialize()

# Create System Device Enumerator
sys_dev_enum = win32com.client.Dispatch("SystemDeviceEnum")

# Create a class enumerator for video capture devices
category = "{860BB310-5D01-11D0-BD3B-00A0C911CE86}"  # CLSID_VideoInputDeviceCategory
moniker_enum = sys_dev_enum.CreateClassEnumerator(category, 0)
if not moniker_enum:
    print("No video capture devices found.")
    exit()

# Iterate over the devices to find your camera
moniker = moniker_enum.Next()
while moniker:
    prop_bag = moniker[0].BindToStorage(None, None, pythoncom.IID_IPropertyBag)
    name = prop_bag.Read("FriendlyName")
    print(f"Found device: {name}")
    if "Your Camera Name" in name:  # Replace with your camera's name
        break
    moniker = moniker_enum.Next()
else:
    print("Desired camera not found.")
    exit()

# Bind to the camera's filter
camera_filter = moniker[0].BindToObject(None, None, pythoncom.IID_IBaseFilter)

# Query for the IAMVideoProcAmp interface
video_proc_amp = camera_filter.QueryInterface(pythoncom.IID_IAMVideoProcAmp)

# Constants for VideoProcAmpProperty
VideoProcAmp_WhiteBalance = 11  # Property ID for white balance

# Disable Auto White Balance
video_proc_amp.Set(VideoProcAmp_WhiteBalance, 4000, 0)  # 4000K, manual mode

# Enable Auto White Balance
# video_proc_amp.Set(VideoProcAmp_WhiteBalance, 0, 2)  # Value ignored in auto mode

# Clean up
pythoncom.CoUninitialize()
