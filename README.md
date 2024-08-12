# Python Scripts Overview

The `motion_detection` folder contains the main motion detection script that you will be using and also some other scripts that can help you check the true fps and perform other simple tasks:

1. **`motion_detection_synchronized_capture.py`**: The primary script for performing motion detection and recording videos. This file includes comprehensive instructions and comments for adjusting parameters.

2. **`motion_detection_synchronized_capture_bmp.py`**: Similar to the main script but saves frames in BMP format instead of AVI.

3. **`motion_detection_no_viz.py`**: A variant of the main script that operates without displaying a camera preview window.

4. **`debug_fps.py`**: Useful for checking the effective FPS during frame saving to a buffer while motion detection is active.

5. **`easypyspin_preview_window.py`**: Displays a preview window for a single camera, without synchronization.

6. **`synchronized_capture.py`**: Captures images using two synchronized cameras.

7. **`synchronized_preview.py`**: Provides preview windows for two synchronized cameras.

8. **`synchronized_recording.py`**: Records video using two synchronized cameras.

# System Specifications and Software Versions

- **Motherboard**: B650 AORUS ELITE AX V2
- **GPU**: RTX 4070
- **Processor**: Ryzen 7 7700x
- **Cameras**: 2 x Blackfly B BFS-U3-16S2M
- **Operating System**: Ubuntu 22.04.4
- **Python Version**: 3.10.12
- **Spinnaker SDK**: 4.0.0.116
- **Spinnaker-python**: 4.0.0.116
- **EasyPySpin**: 2.0.1
- **OpenCV-python**: 4.10.0.84
- **NumPy**: 1.26.4

# Setup Instructions

## Part 1: Installing Spinnaker and PySpin

### Step 1: Download Spinnaker SDK

1. Visit the [FLIR website](https://www.flir.com/support-center/iis/machine-vision/downloads/spinnaker-sdk-download/spinnaker-sdk--download-files/) and download the appropriate Spinnaker SDK for your OS and system architecture. Also, download the corresponding Spinnaker for Python package compatible with your Python version if you intend to use Python.

### Step 2: Install Spinnaker SDK

1. Unzip or untar the downloaded files.
2. Follow the installation steps outlined in the README file within the Spinnaker folder.
3. Ensure that NumPy version is less than 2.0.0 and install all other dependencies as listed.
4. Configure all recommended changes during the installation process.

### Step 3: Post-Installation Check

1. Restart your computer to apply the installation changes.
2. Run the example scripts provided with Spinnaker to verify proper installation.
3. Launch the SpinView application to view and configure your cameras.

### Step 4: Install PySpin

1. Ensure Spinnaker is installed and functional.
2. Follow the instructions in the README file from the spinnaker_python package to install PySpin.
3. Ensure your Python version is ≤ 3.10.

### Step 5: Verify PySpin Installation

1. Run the provided example scripts to confirm PySpin is correctly installed.

## Part 2: Installing EasyPySpin

### Step 1: EasyPySpin Installation

1. Open a terminal and execute the following command:
   ```bash
   pip install EasyPySpin

2. After installation, you can read images from your FLIR cameras using the following Python script:

    ```
    import cv2
    import EasyPySpin

    cap = EasyPySpin.VideoCapture(0)

    ret, frame = cap.read()

    cv2.imwrite("frame.png", frame)

    cap.release()
    ```
