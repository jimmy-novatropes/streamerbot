import cv2
import time
import numpy as np

# Open camera
cap = cv2.VideoCapture(1)  # Change if multiple cameras are connected
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # Use MJPG format for better performance

# Define test parameters
# fps_values = [30, 40, 50, 60, 75, 85, 90, 100]  # Test different FPS values
fps_values = [60.4, 60.5]
# exposure_values = [-9, -6, -3, 0, 3, 6]  # Experiment with different exposure levels
exposure_values = [ 1/60, 1/120, 1/180]
test_duration = 5  # Seconds to display each combination

print("Testing different FPS and exposure combinations...")

for fps in fps_values:
    cap.set(cv2.CAP_PROP_FPS, fps)
    strobe_interval = 1.0 / fps  # Compute frame interval

    for exposure in exposure_values:
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)  # Adjust exposure
        time.sleep(0.5)  # Give the camera time to adjust

        print(f"Testing FPS: {fps} | Exposure: {exposure} | Strobe Interval: {strobe_interval:.4f} sec")

        start_time = time.time()
        while time.time() - start_time < test_duration:
            ret, frame = cap.read()
            if not ret:
                break

            # Overlay text for FPS & exposure settings
            cv2.putText(frame, f"FPS: {fps}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Exposure: {exposure}", (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Strobe: {strobe_interval:.4f}s", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Arducam Testing", frame)

            # Ensure sync with strobe interval
            elapsed = time.time() - start_time
            sleep_time = max(0, strobe_interval - elapsed % strobe_interval)
            time.sleep(sleep_time)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit()

print("Testing complete. Check the video for the best settings.")
cap.release()
cv2.destroyAllWindows()
