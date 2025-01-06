"""Example of synchronized capture with multiple cameras.

You need to create a physical connection between the cameras by linking their GPIO pins, as follows:
https://www.flir.com/support-center/iis/machine-vision/application-note/configuring-synchronized-capture-with-multiple-cameras/
"""
import EasyPySpin
import cv2


def main():
    serial_number_1 = "24122966"  # primary camera (set your camera's serial number)
    serial_number_2 = "24122965"  # secondary camera (set your camera's serial number)
    cap = EasyPySpin.SynchronizedVideoCapture(serial_number_1, serial_number_2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    print(cap.get(cv2.CAP_PROP_EXPOSURE))

    if not all(cap.isOpened()):
        print("All cameras can't open\nexit")
        return -1

    while True:
        read_values = cap.read()

        for i, (ret, frame) in enumerate(read_values):
            if not ret:
                continue
            cv2.imshow(f"frame-{i}", frame)

        key = cv2.waitKey(30)
        if key == ord("q"):
            break
    
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()