import EasyPySpin
import cv2
from datetime import datetime
import time
import os


"""
This Python script captures frames from two synchronized cameras, records them when the user presses the 'b' key, and saves the frames as image files.
The recording will automatically stop after 15 seconds, but can also be manually stopped by pressing 'b' again.
Uses the EasyPySpin library for camera control and OpenCV for displaying the captured frames.
"""

def main():
    serial_number_1 = "24122966"  # primary camera serial number
    serial_number_2 = "24122965"  # secondary camera serial number
    cap = EasyPySpin.SynchronizedVideoCapture(serial_number_1, serial_number_2)

    # Camera settings
    cap.set(cv2.CAP_PROP_FPS, 140)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_EXPOSURE, 1600)
    cap.set(cv2.CAP_PROP_GAIN, 0)

    if not all(cap.isOpened()):
        print("All cameras can't open. Exiting...")
        return -1

    print("Press 'b' to start/stop recording.")
    print("After recording starts, it will stop automatically after 15 seconds.")
    print("Press 'q' to quit the program.")

    try:
        while True:
            frames_0 = []
            frames_1 = []
            recording = False
            start_time = None
            frame_count_0 = 0
            frame_count_1 = 0

            while True:
                # Check for key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('b'):
                    if not recording:
                        recording = True
                        start_time = time.time()
                        print("Recording started...")
                    else:
                        # Stop recording
                        recording = False
                        break

                if key == ord('q'):
                    print("Exiting program...")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                # Capture frames
                read_values = cap.read()
                for i, (ret, frame) in enumerate(read_values):
                    if ret:
                        cv2.imshow(f"camera-{i}", frame)
                        if recording:
                            if i == 0:
                                frames_0.append(frame)
                                frame_count_0 += 1
                            elif i == 1:
                                frames_1.append(frame)
                                frame_count_1 += 1

                # Automatically stop recording after 15 seconds
                if recording and time.time() - start_time >= 15:
                    print("15 seconds passed, stopping recording automatically...")
                    recording = False
                    break

            if frames_0 or frames_1:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                output_dir_0 = f"frames_{timestamp}_0"
                output_dir_1 = f"frames_{timestamp}_1"
                os.makedirs(output_dir_0, exist_ok=True)
                os.makedirs(output_dir_1, exist_ok=True)

                stop_time = time.time()
                print("Recording stopped manually.")
                print("Recorded for: ", stop_time - start_time)
                print("Actual frame rate:", frame_count_0 / (stop_time - start_time))

                print("Saving frames...")
                for idx, frame in enumerate(frames_0):
                    cv2.imwrite(os.path.join(output_dir_0, f'frame_{idx:04d}_0.bmp'), frame)
                for idx, frame in enumerate(frames_1):
                    cv2.imwrite(os.path.join(output_dir_1, f'frame_{idx:04d}_1.bmp'), frame)
                print("Images Saved!")

    except KeyboardInterrupt:
        print("Recording interrupted by user...")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Program exited.")


if __name__ == "__main__":
    main()
