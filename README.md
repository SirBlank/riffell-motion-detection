# Python Scripts

The `motion_detection` folder contains the main motion detection script that you will be using and also some other scripts that can help you check the true fps and perform other simple tasks:

- **`motion_detection_synchronized_capture.py`**: This is the main python script you will be using to perform motion detection and record videos. This file contains all the instructions and comments you will need to know to make adjustments to the parameter.

- `motion_detection_synchronized_capture_bmp.py`: Same thing as `motion_detection_synchronized_capture.py` but saves the frames as bmp files instead of avi files.

- `motion_detection_no_viz.py`: Same thing as `motion_detection_synchronized_capture.py` but without the camera pop-up preview window.

- `debug_fps.py`: Use this script when you want to check the effective fps when saving frame to buffer with motion detection running.

- `easypyspin_preview_window.py`: Display a preview window for **ONE** camera (no synchronization)

- `synchronized_capture.py`: Capture an image with two synchronized cameras

- `synchronized_preview.py`: Display two preview windowos for two synchronized cameras

- `synchronized_recording.py`: Records a video with two synchronized cameras.

# Specs and Versions

- Motherboard: B650 AORUS ELITE AX V2
- GPU: RTX 4070
- Processor: Ryzen 7 7700x
- 2 cameras: Blackfly B BFS-U3-16S2M
- OS Version: Ubuntu 22.04.4
- Python: 3.10.12
- Spinnaker: 4.0.0.116
- Spinnaker-python: 4.0.0.116
- EasyPySpin: 2.0.1
- OpenCV-python: 4.10.0.84
- Numpy: 1.26.4

# Setup Instructions

##  Part 1: Installing Spinnaker and PySpin

Spinnaker SDK is the API camera library used to control USB 3.0 FLIR cameras. USB 2.0 FLIR cameras may require FlyCapture2 instead.
PySpin is the python wrapper for Spinnaker. PySpin is required if you want to control the cameras in python instead of C++.

**Step 1:** Go to the official FLIR website and download the appropriate Spinnaker file for your OS and system architecture (also download the Spinnaker for Python file with your corresponding python version if you are going to use Python instead). https://www.flir.com/support-center/iis/machine-vision/downloads/spinnaker-sdk-download/spinnaker-sdk--download-files/

**Step 2:** Unzip/untar both files and follow the steps listed in the README file from the Spinnaker folder to install Spinnaker. 

- Make sure to install numpy < 2.0.0 and all other dependencies listed in the file!
- I recommend configuring all the recommended changes during the installation process.

**Step 3:** After the installation for Spinnaker is complete, restart your computer to configure all the changes made. At this point, you should be able to run the example scripts to see if Spinnaker is properly installed. You should also be able to launch the Spinview application and view and configure your cameras there as well.

**Step 4:** To install PySpin, make sure Spinnaker is properly installed and working because PySpin is dependent on the Spinnaker library. After making sure Spinnaker is working, follow the steps in the README file from the spinnaker_python file to install the python wrapper called PySpin.
- Make sure your Python version is <= 3.10

**Step 5:** After the installation for PySpin is complete, you should be able to run the example scripts to see if PySpin is properly installed.


## Part 2: Installing EasyPySpin

EasyPySpin is an unofficial wrapper of PySpin for FLIR cameras that works with OpenCV VideoCapture class.

**Step 1:** Go to terminal and run `pip install EasyPySpin`

- You should be able to be able to read images from your FLIR cameras using this:

```
import cv2
import EasyPySpin

cap = EasyPySpin.VideoCapture(0)

ret, frame = cap.read()

cv2.imwrite("frame.png", frame)
    
cap.release()
```