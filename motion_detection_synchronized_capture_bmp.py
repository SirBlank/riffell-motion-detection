import cv2
import os
import EasyPySpin
import time
from time import sleep
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


# Camera serial number can be found by launching SpinView with cameras plugged in.
serial_number_0 = "24122966"  # primary camera serial number
serial_number_1 = "24122965"  # secondary camera serial number
cap = EasyPySpin.SynchronizedVideoCapture(serial_number_0, serial_number_1)

# CAMERA FPS
# When you change the camera fps, make sure to also change the fps in the VideoWriter as well.
cap.set(cv2.CAP_PROP_FPS, 226)

# CAMERA RESOLUTION WIDTH
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)

# CAMERA RESOLUTION HEIGHT
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# CAMERA EXPOSURE TIME (MICROSECONDS)
cap.set(cv2.CAP_PROP_EXPOSURE, 4000)

# CAMERA GAIN
cap.set(cv2.CAP_PROP_GAIN, 10)

# NOTE: you can find all camera properties you can change in Python in the "Supported VideoCapture Properties" section of this git repo: https://github.com/elerac/EasyPySpin. If there are properties you can't find on that page, you can configure those properties using the SpinView application.
# You can confirm the changes that you made to the camera by printing out the camera properties like so, replace XXX with the property:
# print(cap.get(cv2.CAP_PROP_XXX))

# NUMBER OF FRAMES IN CIRCULAR BUFFER = FPS * DURATION_IN_SECONDS
buffer_size = 180

# NUMBER OF FRAMES RECORDED AFTER MOTION DETECTION = FPS * DURATION_IN_SECONDS
additional_frame_size = 1356

fourcc = cv2.VideoWriter_fourcc(*'XVID')
additional_frames_0 = deque(maxlen=additional_frame_size)
additional_frames_1 = deque(maxlen=additional_frame_size)
ring_buffer_0 = deque(maxlen=buffer_size)
ring_buffer_1 = deque(maxlen=buffer_size)
print(cap.get(cv2.CAP_PROP_EXPOSURE))
print(cap.get(cv2.CAP_PROP_GAIN))

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
    prev_x = None
    recording = False
    frame_counter = 0
    is_motion_detected_0 = False
    is_motion_detected_1 = False

    # THE HISTORY PARAMETER SPECIFIES THE NUMBER OF PREVIOUS FRAMES THAT THE ALGORITHM CONSIDERS WHEN UPDATING THE BACKGROUND MODEL.
    # INCREASE history = SLOWER ADAPTATION TO CHANGES, LESS SENSITIVE TO SUDDEN OR SHORT-TERM CHANGES IN THE FRAME.
    # INCREASE varThreshold = LESS SENSITIVE MOTION DETECTION
    back_sub = cv2.createBackgroundSubtractorMOG2(history=180, varThreshold=60, detectShadows=False)
    # INCREASE KERNEL SIZE FOR MORE AGGRESSIVE NOISE REDUCTION
    kernel = np.ones((30, 30), np.uint8)
    # DETERMINES THE CONTOUR SIZE TO BE CONSIDERED AS VALID MOTION
    # Example: ONLY CONTOURS WITH AN AREA OF 100 PIXELS OR MORE WILL BE CONSIDERED AS VALID MOTION.
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
            if not recording:
                contour = detect_motion(frame_copy, back_sub, kernel, min_contour_area, i)

            if contour is not None:
                x, y, w, h = cv2.boundingRect(contour)
                x2 = x + int(w / 2)
                y2 = y + int(h / 2)

                cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.circle(frame_copy, (x2, y2), 4, (0, 255, 0), -1)
                text = f"x: {x2}, y: {y2}"
                cv2.putText(frame_copy, text, (x2 - 10, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if i == 0:
                    is_motion_detected_0 = True
                elif i == 1:
                    is_motion_detected_1 = True

                cv2.imshow(f"frame-{i}", frame_copy)
                if cv2.waitKey(1) == ord('q'):
                    break

                # STARTING VIDEO RECORDING
                if is_motion_detected_0 and is_motion_detected_1 and prev_x is not None and x2 < prev_x and not recording:
                    print("Motion Detected!")
                    log_time = datetime.now().strftime("%Y-%-m-%d_%H:%M:%S.%f")[:-3]
                    print("Start: ", log_time)
                    start_time = time.time()
                    # Logs start_time
                    with open("time_log.txt", mode='a') as file:
                        file.write(f"Start time: {log_time} \n")
                    recording = True
                    frame_counter = 0
                    frame_height, frame_width = frame.shape[:2]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                    print(frame_width, frame_height)

                    is_motion_detected_0 = False
                    is_motion_detected_1 = False

                prev_x = x2
            else:
                if i == 0:
                    is_motion_detected_0 = False
                elif i == 1:
                    is_motion_detected_1 = False

            if recording:
                if i == 0:
                    additional_frames_0.append(frame)
                elif i == 1:
                    additional_frames_1.append(frame)
                frame_counter += .5 
                if frame_counter >= additional_frame_size:
                    recording = False
                    print("End: ", datetime.now().strftime("%Y%-m-%d_%H:%M:%S.%f")[:-3])
                    print("Finished recording. Retrieving buffer and saving images...")
                    print("Elapsed time:", time.time() - start_time)
                    folder_name_0 = f'images_{log_time}_0'
                    folder_name_1 = f'images_{log_time}_1'
                    # SPECIFY SAVED FOLDER LOCATION HERE
                    os.makedirs(folder_name_0, exist_ok=True)
                    os.makedirs(folder_name_1, exist_ok=True)
                    combined_frames_0 = np.concatenate((ring_buffer_0, additional_frames_0))
                    for idx, frame in enumerate(combined_frames_0):
                        cv2.imwrite(os.path.join(folder_name_0, f'frame_{idx}_0.bmp'), frame)
                    combined_frames_1 = np.concatenate((ring_buffer_1, additional_frames_1))
                    for idx, frame in enumerate(combined_frames_1):
                        cv2.imwrite(os.path.join(folder_name_1, f'frame_{idx}_1.bmp'), frame)
                    print("Images Saved!")
                    additional_frames_0.clear()
                    additional_frames_1.clear()
                    ring_buffer_0.clear()
                    ring_buffer_1.clear()
                    del combined_frames_0
                    del combined_frames_1
                    back_sub = cv2.createBackgroundSubtractorMOG2(history=180, varThreshold=60, detectShadows=False)
                    print("Resuming motion detection...")

if __name__ == '__main__':
    try:    
        motion_detection()
    except KeyboardInterrupt:
        print("Stopping motion detection.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Closing camera and resetting...")
