import cv2
import EasyPySpin
import numpy as np

cap = EasyPySpin.VideoCapture(0)
cap.set(cv2.CAP_PROP_EXPOSURE, 150)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 10)
print(cap.get(cv2.CAP_PROP_EXPOSURE))
print(cap.get(cv2.CAP_PROP_BRIGHTNESS))

while True:
    ret, frame = cap.read()
    frame_copy = np.copy(frame)
    cv2.imshow('camera', frame_copy)

    if cv2.waitKey(1) == (ord('q')):
        break