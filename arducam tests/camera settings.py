import cv2

props = {
    "FRAME_WIDTH": cv2.CAP_PROP_FRAME_WIDTH,
    "FRAME_HEIGHT": cv2.CAP_PROP_FRAME_HEIGHT,
    "BRIGHTNESS": cv2.CAP_PROP_BRIGHTNESS,
    "CONTRAST": cv2.CAP_PROP_CONTRAST,
    "SATURATION": cv2.CAP_PROP_SATURATION,
    "HUE": cv2.CAP_PROP_HUE,
    "GAIN": cv2.CAP_PROP_GAIN,
    "EXPOSURE": cv2.CAP_PROP_EXPOSURE,
    "AUTO_EXPOSURE": cv2.CAP_PROP_AUTO_EXPOSURE,
    "AUTO_WB": cv2.CAP_PROP_AUTO_WB,
    "WB_TEMPERATURE": cv2.CAP_PROP_WB_TEMPERATURE,
    "FOCUS": cv2.CAP_PROP_FOCUS,
    "ZOOM": cv2.CAP_PROP_ZOOM,
}

# Known OpenCV backends
backends = {
    "CAP_ANY": cv2.CAP_ANY,
    "CAP_MSMF": cv2.CAP_MSMF,
    "CAP_DSHOW": cv2.CAP_DSHOW,
    "CAP_VFW": cv2.CAP_VFW,
    "CAP_FFMPEG": cv2.CAP_FFMPEG,
    "CAP_GSTREAMER": cv2.CAP_GSTREAMER,
    "CAP_IMAGES": cv2.CAP_IMAGES,
    "CAP_AVFOUNDATION": cv2.CAP_AVFOUNDATION,  # macOS
    "CAP_V4L2": cv2.CAP_V4L2,                  # Linux
}

def read_props(cam_index, backend_id):
    cap = cv2.VideoCapture(cam_index, backend_id)
    if not cap.isOpened():
        return None
    result = {name: cap.get(pid) for name, pid in props.items()}
    cap.release()
    return result

cam_index = 3  # Change if needed
import time
for label, backend_id in backends.items():
    time.sleep(1)  # Delay to allow camera to initialize properly
    print(f"\n=== Testing Backend: {label} ===")
    values = read_props(cam_index, backend_id)
    if values is None:
        print("Could not open camera with this backend.")
    else:
        for name, val in values.items():
            print(f"{name:20}: {val}")
