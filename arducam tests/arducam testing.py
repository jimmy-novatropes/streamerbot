import cv2

# def find_camera_indices(max_tested=10):
#     available = []
#     for i in range(max_tested):
#         cap = cv2.VideoCapture(i)
#         if cap.isOpened():
#             available.append(i)
#             cap.release()
#     return available
#
# print(find_camera_indices())

# print("Available cameras:", cameras)
# cam_index = int(input(f"Select camera index [{cameras[0]}]: ") or cameras[0])
cam_index = 1

# Open selected camera
# cap = cv2.VideoCapture(cam_index, cv2.CAP_MSMF)
# cap = cv2.VideoCapture("video=Arducam OV9782 USB Camera", cv2.CAP_DSHOW)
cap = cv2.VideoCapture(1)  # Change to your camera index or name
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(r"video=@device_pnp_\\?\usb#vid_0c45&pid_6366&mi_00#8&f3abe03&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global"
# , cv2.CAP_FFMPEG)



# Camera settings
cap.set(cv2.CAP_PROP_AUTO_WB, 1.0)  # Disable auto white balance
cap.get(cv2.CAP_PROP_AUTO_WB)  # Ensure auto white balance is off
print("Auto White Balance:", cap.get(cv2.CAP_PROP_AUTO_WB))
cap.set(cv2.CAP_PROP_EXPOSURE, -6.0)
print("Exposure set to:", cap.get(cv2.CAP_PROP_EXPOSURE))

print("Camera settings applied.")
cap.release()
