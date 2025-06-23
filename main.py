import cv2
import os
import EasyPySpin
import time
from time import sleep
import numpy as np
from datetime import datetime
import threading
import socket
import signal
import sys

# ==============================
# GLOBAL VARIABLES
# ==============================
start_motion_detection = False  # Toggled by pressing '0' in the OpenCV window

# Additional variables for manual recording
manual_recording = False
manual_frames_0 = []
manual_frames_1 = []

# Camera serial number can be found by launching SpinView with cameras plugged in.
serial_number_0 = "24122966"  # primary camera serial number
serial_number_1 = "24122965"  # secondary camera serial number
cap = EasyPySpin.SynchronizedVideoCapture(serial_number_0, serial_number_1)

# CAMERA FPS
# When you change the camera fps, make sure to also change the fps in the VideoWriter as well.
frame_rate = 140

cap.set(cv2.CAP_PROP_FPS, frame_rate)

# CAMERA RESOLUTION WIDTH
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)

# CAMERA RESOLUTION HEIGHT
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# CAMERA EXPOSURE TIME (MICROSECONDS)
cap.set(cv2.CAP_PROP_EXPOSURE, 1500)

# CAMERA GAIN
cap.set(cv2.CAP_PROP_GAIN, 0)

# NOTE: you can find all camera properties you can change in Python in the "Supported VideoCapture Properties" section of this git repo: https://github.com/elerac/EasyPySpin.
# If there are properties you can't find on that page, you can configure those properties using the SpinView application.
# You can confirm the changes that you made to the camera by printing out the camera properties like so, replace XXX with the property:
# print(cap.get(cv2.CAP_PROP_XXX))

# Duration: How long the recording should last
duration = 5.4

# Number of frames before triggering the animation
wait_frames = 20 # If changed, this value should be updated in animation_v2.py csv section

# NUMBER OF FRAMES RECORDED AFTER MOTION DETECTION = FPS * DURATION_IN_SECONDS
additional_frame_size = (duration * frame_rate + wait_frames)

# Coordinates for Region of Interest
x1, y1 = 390, 430
width_roi, height_roi = 420, 308

running_flag = threading.Event()
running_flag.set()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
additional_frames_0 = []
additional_frames_1 = []

print(cap.get(cv2.CAP_PROP_EXPOSURE))
print(cap.get(cv2.CAP_PROP_GAIN))

def signal_handler(sig, frame):
    print("Cameras exiting gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def detect_motion(frame, back_sub, kernel, min_contour_area, max_contour_area):
    """
    Applies background subtraction and returns the largest contour if in the valid area range.
    Otherwise returns None.
    """
    fg_mask = back_sub.apply(frame)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    fg_mask = cv2.medianBlur(fg_mask, 5)
    _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return None

    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    if min_contour_area < areas[max_index] < max_contour_area:
        return contours[max_index]
    return None

def motion_detection():
    """
    Continuously read frames from the cameras.
    Toggles detection on/off by pressing '0' in the OpenCV window.
    Press 'q' to quit.
    """
    global start_motion_detection
    global manual_recording

    recording = False
    frame_counter = 0

    # THE HISTORY PARAMETER SPECIFIES THE NUMBER OF PREVIOUS FRAMES THAT THE ALGORITHM CONSIDERS WHEN UPDATING THE BACKGROUND MODEL.
    # INCREASE history = SLOWER ADAPTATION TO CHANGES, LESS SENSITIVE TO SUDDEN OR SHORT-TERM CHANGES IN THE FRAME.
    # INCREASE varThreshold = LESS SENSITIVE MOTION DETECTION
    back_sub = cv2.createBackgroundSubtractorMOG2(history=400, varThreshold=60, detectShadows=False)
    # INCREASE KERNEL SIZE FOR MORE AGGRESSIVE NOISE REDUCTION
    kernel = np.ones((30, 30), np.uint8)
    # DETERMINES THE CONTOUR SIZE TO BE CONSIDERED AS VALID MOTION
    # Example: ONLY CONTOURS WITH AN AREA OF 100 PIXELS OR MORE WILL BE CONSIDERED AS VALID MOTION.
    min_contour_area = 100
    max_contour_area = 400 # original: 1552681

    host = 'localhost'
    port = 3000

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print("[INPUT]\nPress '0' in the preview window to toggle motion detection \nPress '1' to start/stop manual recording \nPress 'q' to quit the cameras. \n'CTRL+C' to kill the script.")

            # The loop to check for motion detection in each camera (Please don't change unless it is necessary)
            while running_flag.is_set():
                read_values = cap.read()
                for i, (ret, frame) in enumerate(read_values):
                    if not ret:
                        print("Error: Failed to capture image.")
                        break

                    # Show the frames
                    cv2.imshow(f"Camera {i}", frame)

                    # Append frames to the manual recording lists
                    if manual_recording:
                        if i == 0:
                            manual_frames_0.append(frame)
                        else:
                            manual_frames_1.append(frame)
                    
                    # Check key from OpenCV window
                    key = cv2.waitKey(1) & 0xFF

                    # ---- Motion Detection Toggle ----
                    if key == ord('0'):
                        start_motion_detection = not start_motion_detection
                        print(f"[INFO] Motion detection: {start_motion_detection}")

                    # ---- Manual Recording Toggle ----
                    if key == ord('1'):
                        if not manual_recording:
                            manual_recording = True
                            manual_frames_0.clear()
                            manual_frames_1.clear()
                            manual_start = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
                            print(f"[RECORDING] Recording started at {manual_start}")
                        else:
                            manual_recording = False
                            manual_end = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
                            print(f"[RECORDING] Recording stopped at {manual_end}. Saving frames...")

                            base_folder = '/mnt/data/DATA'
                            folder_name_0 = os.path.join(base_folder, f'manual_images_{manual_end}_a')
                            folder_name_1 = os.path.join(base_folder, f'manual_images_{manual_end}_b')
                            os.makedirs(folder_name_0, exist_ok=True)
                            os.makedirs(folder_name_1, exist_ok=True)

                            for idx, frm in enumerate(manual_frames_0):
                                cv2.imwrite(os.path.join(folder_name_0, f'frame_{idx:04d}_a.bmp'), frm)
                            for idx, frm in enumerate(manual_frames_1):
                                cv2.imwrite(os.path.join(folder_name_1, f'frame_{idx:04d}_b.bmp'), frm)

                            manual_frames_0.clear()
                            manual_frames_1.clear()
                            print("[RECORDING] Frames saved successfully.")

                    # ---- Quit ----
                    if key == ord('q'):
                        running_flag.clear()
                        break

                    # If detection is disabled, skip
                    if not start_motion_detection:
                        continue

                    # Only do motion detection on camera 0
                    if i == 0 and not recording:
                        # here we can add a mask to the copied frame to implement motion detection selectively
                        # frame_copy[:,720:] = 255 #this will make the right half of the frame white
                        # frame_copy[:350,:720] = 255 #adds a mask over the IR lights
                        # ORIGINAL MASKS:
                        # frame_copy[:, :500] = 255
                        # frame_copy[:, 1000:] = 255
                        frame_copy = frame[y1:y1+height_roi, x1:x1+width_roi]
                        contour = detect_motion(frame_copy, back_sub, kernel, min_contour_area, max_contour_area)
                        if contour is not None:
                            # STARTING VIDEO RECORDING
                            recording = True
                            frame_counter = 0
                            log_time = int(time.time() * 1000)
                            start_elapse = time.time()
                            start_time = datetime.now().strftime("%Y-%-m-%d_%H-%M-%S.%f")[:-3]
                            print("Start: ", start_time)
                            with open("time_log.txt", mode='a') as file:
                                file.write(f"Start time: {log_time} \n")

                    # If we are recording, capture frames
                    if recording:
                        if frame_counter <= additional_frame_size:
                            if frame_counter == wait_frames:
                                # SENDING SIGNAL TO ANIMATION
                                print("Stimulus Starting...")
                                s.sendall(b'signal')

                            if i == 0:
                                additional_frames_0.append(frame)
                            else:
                                additional_frames_1.append(frame)
                            frame_counter += 0.5
                        else:
                            # STOP RECORDING
                            recording = False
                            print("End: ", datetime.now().strftime("%Y%-m-%d_%H:%M:%S.%f")[:-3])
                            print("Finished recording. Retrieving buffer and saving images...")
                            print("Elapsed time:", time.time() - start_elapse)

                            # SPECIFY SAVED FOLDER LOCATION HERE
                            # base_folder = os.path.expanduser('~/Desktop/flight_arena/Final_Versions/DATA/')
                            base_folder = '/mnt/data/DATA'
                            folder_name_0 = os.path.join(base_folder, f'{log_time}_main_images_a')
                            folder_name_1 = os.path.join(base_folder, f'{log_time}_main_images_b')
                            os.makedirs(folder_name_0, exist_ok=True)
                            os.makedirs(folder_name_1, exist_ok=True)

                            for idx, frm in enumerate(additional_frames_0):
                                cv2.imwrite(os.path.join(folder_name_0, f'frame_{idx:04d}_a.bmp'), frm)
                            for idx, frm in enumerate(additional_frames_1):
                                cv2.imwrite(os.path.join(folder_name_1, f'frame_{idx:04d}_b.bmp'), frm)
                            print("Images saved successfully.")

                            additional_frames_0.clear()
                            additional_frames_1.clear()
                            back_sub = cv2.createBackgroundSubtractorMOG2(history=400, 
                                                                          varThreshold=60, 
                                                                          detectShadows=False)
                            print("Resuming motion detection...")

    finally:
        print("motion_detection() closing.")
        cv2.destroyAllWindows()
        cap.release()

if __name__ == '__main__':
    try:
        motion_detection()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Stopping.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Cameras closed. Exiting.")
