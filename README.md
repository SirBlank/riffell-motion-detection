# Overview

## Free-Flight Arena for Multisensory Integration in Mosquitoes


This research, conducted by University of Washington's Riffell Lab and led by C. Ruiz, aims to characterize steering behavior in free-flying yellow fever mosquitoes, focusing on how olfactory cues influence visual preferences. A Linux-based system controls four modules:

- **Imaging:** High-resolution cameras track flight patterns.
- **Odor Delivery:** Releases a controlled mix of CO2 and test odors.
- **Projection:** Displays visual stimuli to observe responses.
- **IR Synchronization:** Blinking IR LEDs encode and timestamp visual events for synchronization.

## Scripts

- **`main.py`**: The primary script for performing motion detection, sending signal to trigger the animation script, recording image frames, and saving image frames as BMP files. This file includes comprehensive instructions and comments for adjusting motion detection parameters and camera properties.
- **`animation.py`**: The animation script that renders a moving bar as visual stimulus when triggered by motion detection.
- **`alicat_input.py`**: The mass flow controller script that adjusts and toggles airflow based on user input.

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

### Step 6: EasyPySpin Installation

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

## Part 3: Running an Experiment

### Step 7: Preparing Terminals

1. Open two terminal windows and ensure that your environment or virtual environment is set up in both.

2. On terminal 1, run `bash start.sh`. On terminal 2, run `python alicat_input.py`.

3. Follow the instructions displayed in your terminal to use the console. To stop the scripts, press `CTRL+C` in both terminals to terminate the Python processes.