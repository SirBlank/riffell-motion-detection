import numpy as np
import cv2
from time import sleep, time
from threading import Thread, Event
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
import gpiozero

# CURRENT FUNCTIONAL VERSION OF MOTION DETECTION

# GPIO setup
input_pin = gpiozero.InputDevice(22)
output_pin = gpiozero.OutputDevice(17)

# Define ROIs (Region of Interest) with new coordinates
# ROI01 = {"start": (560, 0), "end": (640, 480)}
# ROI02 = {"start": (480, 80), "end": (560, 400)}
# ROI03 = {"start": (400, 160), "end": (480, 320)}
ROI01 = {"start": (540, 180), "end": (640, 300)}
ROI02 = {"start": (440, 180), "end": (540, 300)}
ROI03 = {"start": (340, 180), "end": (440, 300)}

# Define thresholds for each ROI with updated values
Threshold_ROI01 = 10000
Threshold_ROI02 = 10000
Threshold_ROI03 = 10000

# Define image size
lsize = (640, 480)
picam2 = Picamera2()

video_config = picam2.create_video_configuration(main={"size": (1456, 1088), "format": "RGB888"}, lores={
                                                 "size": lsize, "format": "YUV420"})
picam2.configure(video_config)
picam2.start_preview(Preview.QT)
encoder = H264Encoder(1000000, repeat=True)
encoder.output = CircularOutput()
picam2.start()
picam2.start_encoder(encoder)

def detect_motion_in_roi(current_frame, previous_frame, roi, threshold):
    """
    Detect motion within a specified ROI.
    """
    roi_frame_current = current_frame[roi["start"][1]:roi["end"][1], roi["start"][0]:roi["end"][0]]
    roi_frame_previous = previous_frame[roi["start"][1]:roi["end"][1], roi["start"][0]:roi["end"][0]]

    # Gaussian blur
    roi_frame_current = cv2.GaussianBlur(roi_frame_current, (31, 31), 0)
    roi_frame_previous = cv2.GaussianBlur(roi_frame_previous, (31, 31), 0)

    frame_delta = cv2.absdiff(roi_frame_current, roi_frame_previous)
    delta_sum = np.sum(frame_delta)
    print(delta_sum)
    return delta_sum > threshold

def motion_detection(stop_event):
    previous_frame = picam2.capture_array().astype(np.int16)
    monitoring_ROI01 = True
    start_time_ROI02 = None
    start_time_ROI03 = None

    while not stop_event.is_set():
        current_frame = picam2.capture_array().astype(np.int16)
        
        if monitoring_ROI01:
            if detect_motion_in_roi(current_frame, previous_frame, ROI01, Threshold_ROI01):
                print("ROI01")
                monitoring_ROI01 = False
                start_time_ROI02 = time()
                previous_frame_ROI02 = current_frame.copy()
        elif start_time_ROI02 is not None and time() - start_time_ROI02 <= 1:
            if detect_motion_in_roi(current_frame, previous_frame_ROI02, ROI02, Threshold_ROI02):
                print("ROI02")
                start_time_ROI02 = None
                start_time_ROI03 = time()
                previous_frame_ROI03 = current_frame.copy()
        elif start_time_ROI03 is not None and time() - start_time_ROI03 <= 1:
            if detect_motion_in_roi(current_frame, previous_frame_ROI03, ROI03, Threshold_ROI03):
                print("Motion detected in ROI03 within 1 second. Sending signal.")
                # turn on signal when motion is detected
                output_pin.on()
                sleep(0.5)
                output_pin.off()
                start_time_ROI03 = None
                monitoring_ROI01 = True
            elif time() - start_time_ROI03 > 1:
                print("No motion detected in ROI03 within 1 second. Switching back to ROI01.")
                start_time_ROI03 = None
                monitoring_ROI01 = True
        else:
            monitoring_ROI01 = True

        if monitoring_ROI01:
            previous_frame = current_frame.copy()

def signal_listener(stop_event):
    while not stop_event.is_set():
        if input_pin.is_active:
            print("Signal received from circuit, saving recording.")
            epoch = int(time())
            encoder.output.fileoutput = f"{epoch}.h264"
            encoder.output.start()
            # After signal is received, record for 10 additional seconds (may not need this)
            sleep(10)
            encoder.output.stop()
            print(f"Saved video as {epoch}.h264.")
            break
        sleep(0.1)

try:
    print("Starting motion detection and signal listening. Press Ctrl+C to stop.")
    sleep(5)

    stop_event = Event()
    motion_thread = Thread(target=motion_detection, args=(stop_event,))
    signal_thread = Thread(target=signal_listener, args=(stop_event,))

    motion_thread.start()
    signal_thread.start()

    motion_thread.join()
    signal_thread.join()

except KeyboardInterrupt:
    print("Stopping motion detection and signal listening.")
finally:
    stop_event.set()
    motion_thread.join()
    signal_thread.join()
    picam2.stop_encoder()
    picam2.stop()
    input_pin.close()
    output_pin.close()
    print("Closing pins and resetting...")
