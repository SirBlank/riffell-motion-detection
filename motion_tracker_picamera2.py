import cv2
import numpy as np
from picamera2 import Picamera2
import time

# average the detected square coordinate (get the center of the square), retrieve those data from both cameras, compile coordinates into csv file to reconstruct the 3d flight path.
# trigger visual stimulus when motion is detected with _ of the right side of the frame.
# attempt to implement circular buffer

def main():
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (1456, 1088), "format": "RGB888"},
                                                 lores={"size": (640, 480), "format": "YUV420"},
                                                 controls={"FrameDurationLimits": (16666, 16666), "ExposureTime": 100, "Saturation": 0, "FrameRate": 60})
    picam2.configure(video_config)

    picam2.start()
    time.sleep(2)

    back_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=25, detectShadows=True)
    kernel = np.ones((20, 20), np.uint8)

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter('output.mp4', fourcc, 20, (640, 480))
    min_contour_area = 10

    start_time = time.time()

    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array("lores")

        # Use every frame to calculate the foreground mask and update the background
        fg_mask = back_sub.apply(frame)

        # Close dark gaps in foreground object using closing
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)

        # Remove salt and pepper noise with a median filter
        fg_mask = cv2.medianBlur(fg_mask, 5)

        # Threshold the image to make it either black or white
        _, fg_mask = cv2.threshold(fg_mask, 127, 255, cv2.THRESH_BINARY)

        # Find the index of the largest contour and draw bounding box
        fg_mask_bb = fg_mask
        contours, hierarchy = cv2.findContours(fg_mask_bb, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        areas = [cv2.contourArea(c) for c in contours]

        # If there are no contours
        if len(areas) < 1:
            # Display the resulting frame
            cv2.imshow('frame', frame)

            # If "q" is pressed on the keyboard, exit this loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Go to the top of the while loop
            continue
        else:
            # Find the largest moving object in the image
            max_index = np.argmax(areas)
            if areas[max_index] < min_contour_area:
                continue

        # Draw the bounding box
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Draw circle in the center of the bounding box
        x2 = x + int(w / 2)
        y2 = y + int(h / 2)
        cv2.circle(frame, (x2, y2), 4, (0, 255, 0), -1)

        # Print the centroid coordinates (we'll use the center of the bounding box) on the image
        text = "x: " + str(x2) + ", y: " + str(y2)
        cv2.putText(frame, text, (x2 - 10, y2 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard, exit this loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream
    picam2.close()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
