import cv2
import numpy as np
from picamera2 import Picamera2
import time
import gpiozero
from time import sleep

def main():
    # GPIO setup
    input_pin = gpiozero.InputDevice(22)
    output_pin = gpiozero.OutputDevice(17)

    # Initialize the camera
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (640, 480)}, controls={'FrameRate': 60})
    picam2.configure(config)

    # Start the camera
    picam2.start()
    time.sleep(2)

    # Create background subtractor and morphological kernel
    # INCREASE varThreshold = LESS SENSITIVE MOTION DETECTION
    back_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=50, detectShadows=True)
    # INCREASE KERNEL SIZE FOR MORE AGGRESSIVE NOISE REDUCTION
    kernel = np.ones((30, 30), np.uint8)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

    start_time = time.time()
    prev_x = None
    # DETERMINES CONTOUR SIZE TO BE CONSIDERED AS VALID MOTION
    min_contour_area = 1000

    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()

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

        if len(areas) > 0:
            # Find the largest moving object in the image
            max_index = np.argmax(areas)
            # Check if the largest contour area is greater than the minimum contour area
            if areas[max_index] > min_contour_area:
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

                # Check for motion from right to left
                if prev_x is not None and x2 < prev_x:
                    # Send signal through the output pin
                    print("Motion Detected! Sending signal...")
                    output_pin.on()
                    sleep(0.5)
                    output_pin.off()

                prev_x = x2

        # Write the frame into the file 'output.mp4'
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # If "q" is pressed on the keyboard, exit this loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close down the video stream and the video writer
    picam2.close()
    out.release()
    cv2.destroyAllWindows()
    input_pin.close()
    output_pin.close()
    print("Quitting and resetting...")

if __name__ == '__main__':
    main()
