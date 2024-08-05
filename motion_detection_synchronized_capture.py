import cv2
import EasyPySpin
from time import sleep, time
import numpy as np
from datetime import datetime
from collections import deque

# OS Version: Ubuntu 22.04.4
# Python: 3.10.12
# spinnaker: 4.0.0.116
# spinnaker-python: 4.0.0.116
# EasyPySpin: 2.0.1
# opencv-python: 4.10.0.84
# numpy: 1.26.4


## CURRENTLY HAVE PROBLEM WITH RESOLUTION AND FPS
## NEED TO HANDLE CONTINUOUS MOTION DETECTION, ADD A BUFFER TIME BETWEEN EACH DETECTION?
## ANOTHER OPTION: SAVE FRAMES AS UNCOMPRESSED IMAGES (BMP)
## Consider having a third array to store buffer for the next video when recording current video.


# BEFORE SYNCHRONIZATION:
# 500x500 works with 200fps
# 1440x1080 works with <=75fps

# AFTER SYNCHRONIZATION:
# 1440X1080 with <= 40fps

serial_number_0 = "24122966"  # primary camera (set your camera's serial number)
serial_number_1 = "24122965"  # secondary camera (set your camera's serial number)
cap = EasyPySpin.SynchronizedVideoCapture(serial_number_0, serial_number_1)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_0 = None
out_1 = None
buffer_size = 600
additional_frame_size = 600
additional_frames_0 = deque(maxlen=additional_frame_size)
additional_frames_1 = deque(maxlen=additional_frame_size)
ring_buffer_0 = deque(maxlen=buffer_size)
ring_buffer_1 = deque(maxlen=buffer_size)

def detect_motion(frame, back_sub, kernel, min_contour_area, i):
    fg_mask = back_sub.apply(frame)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.medianBlur(fg_mask, 5)
    _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]

    if len(areas) == 0:
        cv2.imshow(f"frame-{i}", frame)
        if cv2.waitKey(1) == ord('q'):
            return None
    else:
        max_index = np.argmax(areas)
        if areas[max_index] > min_contour_area:
            return contours[max_index]
    return None

def motion_detection():
    sleep(5)
    print("Starting motion detection. Press Ctrl+C to stop.")
    global out_0
    global out_1
    prev_x = None
    recording = False
    frame_counter = 0

    # INCREASE varThreshold = LESS SENSITIVE MOTION DETECTION
    back_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=50, detectShadows=True)
    # INCREASE KERNEL SIZE FOR MORE AGGRESSIVE NOISE REDUCTION
    kernel = np.ones((30, 30), np.uint8)
    # DETERMINES THE CONTOUR SIZE TO BE CONSIDERED AS VALID MOTION
    # ONLY CONTOURS WITH AN AREA OF 1000 PIXELS OR MORE WILL BE CONSIDERED AS VALID MOTION.
    min_contour_area = 100

    while True:
        read_values = cap.read()
        for i, (ret, frame) in enumerate(read_values):
            if not ret:
                print("Error: Failed to capture image")
                break

            if not recording:
                if i == 0:
                    ring_buffer_0.append(frame)
                elif i == 1:
                    ring_buffer_1.append(frame)

            frame_copy = np.copy(frame)
            contour = detect_motion(frame_copy, back_sub, kernel, min_contour_area, i)

            if contour is not None:
                x, y, w, h = cv2.boundingRect(contour)
                x2 = x + int(w / 2)
                y2 = y + int(h / 2)

                cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.circle(frame_copy, (x2, y2), 4, (0, 255, 0), -1)
                text = f"x: {x2}, y: {y2}"
                cv2.putText(frame_copy, text, (x2 - 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.imshow(f"frame-{i}", frame_copy)
                if cv2.waitKey(1) == ord('q'):
                    break

                if prev_x is not None and x2 < prev_x and not recording:
                    print("Motion Detected!")
                    print("Start: ", datetime.now().strftime("%Y%-m-%d_%H:%M:%S.%f")[:-3])
                    recording = True
                    frame_counter = 0
                    frame_height, frame_width = frame.shape[:2]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                    print(frame_width, frame_height)
                    out_0 = cv2.VideoWriter(f'motion_detection_{timestamp}_0.avi', fourcc, 60.0, (frame_width, frame_height), isColor=False)
                    out_1 = cv2.VideoWriter(f'motion_detection_{timestamp}_1.avi', fourcc, 60.0, (frame_width, frame_height), isColor=False)
                prev_x = x2

            if recording:
                if i == 0:
                    additional_frames_0.append(frame)
                elif i == 1:
                    additional_frames_1.append(frame)
                frame_counter += .5 
                if frame_counter >= additional_frame_size:
                    recording = False
                    print("End: ", datetime.now().strftime("%Y%-m-%d_%H:%M:%S.%f")[:-3])
                    print("Finished recording. Retrieving buffer and saving video...")
                    for frame in ring_buffer_0:
                        out_0.write(frame)
                    for frame in additional_frames_0:
                        out_0.write(frame)
                    for frame in ring_buffer_1:
                        out_1.write(frame)
                    for frame in additional_frames_1:
                        out_1.write(frame)
                    out_0.release()
                    out_1.release()
                    print("Video Saved!")
                    additional_frames_0.clear()
                    additional_frames_1.clear()
                    ring_buffer_0.clear()
                    ring_buffer_1.clear()

if __name__ == '__main__':
    try:    
        motion_detection()
    except KeyboardInterrupt:
        print("Stopping motion detection.")
    finally:
        cap.release()
        if out_1 is not None and out_0 is not None:
            out_1.release()
            out_0.release()
        cv2.destroyAllWindows()
        print("Closing camera and resetting...")
