import cv2
import EasyPySpin
import numpy as np
from time import perf_counter
from collections import deque

serial_number_0 = "24122966"  # primary camera serial number
serial_number_1 = "24122965"  # secondary camera serial number
cap = EasyPySpin.SynchronizedVideoCapture(serial_number_0, serial_number_1)

# CHANGE CAMERA SETTINGS HERE
cap.set(cv2.CAP_PROP_FPS, 140)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

buffer_size = 1400
ring_buffer = deque(maxlen=buffer_size)
ring_buffer_2 = deque(maxlen=buffer_size)
frames_processed = 0
start_time = perf_counter()

# Initialize background subtractor and kernel for motion detection
back_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=50, detectShadows=True)
kernel = np.ones((30, 30), np.uint8)
min_contour_area = 100

def detect_motion(frame):
    fg_mask = back_sub.apply(frame)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.medianBlur(fg_mask, 5)
    _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]

    if len(areas) == 0:
        return None
    else:
        max_index = np.argmax(areas)
        if areas[max_index] > min_contour_area:
            return contours[max_index]
    return None

while len(ring_buffer) < buffer_size:
    read_values = cap.read()
    for i, (ret, frame) in enumerate(read_values):
        if not ret:
            print("Error: Failed to capture image")
            break
        if i == 0:
            ring_buffer.append(frame)
        elif i == 1:
            ring_buffer_2.append(frame)
        frames_processed += .5
        contour = detect_motion(frame)
        # contour = None

        if frames_processed % 100 == 0:
            elapsed_time = perf_counter() - start_time
            print(f"Captured {frames_processed} frames in {elapsed_time:.2f} seconds.")



    # ret, frame = cap.read()
    # if not ret:
    #     print("Error: Failed to capture image")
    #     break

    # ring_buffer.append(frame)
    # frames_processed += 1

    # # Perform motion detection
    # contour = detect_motion(frame)
    # # contour = None
    # if contour is not None:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     x2 = x + int(w / 2)
    #     y2 = y + int(h / 2)
    #     print(f"Motion detected at x2: {x2}, y2: {y2}")

    # # Debug output
    # if frames_processed % 100 == 0:  # Print every 100 frames
    #     elapsed_time = perf_counter() - start_time
    #     print(f"Captured {frames_processed} frames in {elapsed_time:.2f} seconds.")

end_time = perf_counter()
elapsed_time = end_time - start_time

print(f"Captured {len(ring_buffer)} frames in {elapsed_time:.2f} seconds.")
print(f"Effective frame rate: {len(ring_buffer) / elapsed_time:.2f} FPS")

cap.release()