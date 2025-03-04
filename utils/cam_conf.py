import EasyPySpin
import cv2


serial_number_0 = "24122966"  # primary camera serial number
serial_number_1 = "24122965"  # secondary camera serial number
cap = EasyPySpin.SynchronizedVideoCapture(serial_number_0, serial_number_1)

cap.set(cv2.CAP_PROP_FPS, 200)

# CAMERA RESOLUTION WIDTH
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)

# CAMERA RESOLUTION HEIGHT
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# CAMERA EXPOSURE TIME (MICROSECONDS)
cap.set(cv2.CAP_PROP_EXPOSURE, 4000)

# CAMERA GAIN
cap.set(cv2.CAP_PROP_GAIN, 0)