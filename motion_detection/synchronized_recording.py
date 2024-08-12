import EasyPySpin
import cv2
from datetime import datetime
import time
from collections import deque


def main():
    serial_number_1 = "24122966"  # primary camera serial number
    serial_number_2 = "24122965"  # secondary camera serial number
    cap = EasyPySpin.SynchronizedVideoCapture(serial_number_1, serial_number_2)
    frame_size = 1400
    frames_0 = deque(maxlen=frame_size)
    frames_1 = deque(maxlen=frame_size)
    cap.set(cv2.CAP_PROP_FPS, 140)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
    out_0 = cv2.VideoWriter(f'motion_detection_{timestamp}_0.avi', fourcc, 140.0, (1440, 1080), isColor=False)
    out_1 = cv2.VideoWriter(f'motion_detection_{timestamp}_1.avi', fourcc, 140.0, (1440, 1080), isColor=False)
    
    if not all(cap.isOpened()):
        print("All cameras can't open\nexit")
        return -1

    start_time = time.time()
    for _ in range(frame_size):
        read_values = cap.read()
        for i, (ret, frame) in enumerate(read_values):
            if ret:
                if i == 0:
                    frames_0.append(frame)
                elif i == 1:
                    frames_1.append(frame)

    elapsed_time = time.time() - start_time
    print(elapsed_time)
    print("Finished Recording! Saving video...")

    for frame in frames_0:
        out_0.write(frame)
    for frame in frames_1:
        out_1.write(frame)
    print("Saved videos!")
    cap.release()
    out_0.release()
    out_1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()