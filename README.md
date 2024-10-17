# Finger Tracking and Counting Projects using MediaPipe and OpenCV

## Overview
This repository contains two Python scripts (`finger_tracker.py` and `finger_counter.py`) that use the `HandTrackingModule` to detect, track, and analyze hand gestures using MediaPipe's hand landmarks detection.

The `HandTrackingModule` is a custom-built class that wraps MediaPipe's hand detection functionality, allowing easy detection of hand landmarks and tracking their positions in real-time.

## Dependencies
Before running the scripts, ensure the following dependencies are installed:
- Python 3.x
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)

You can install these dependencies using:
```bash
pip install opencv-python mediapipe
```

## HandTrackingModule
This module provides a `HandDetector` class used in both scripts for hand detection and drawing landmarks. The class includes methods like:
- `findHands`: Detects hands in a video frame and draws the landmarks.
- `findPositions`: Returns the (x, y) coordinates of hand landmarks.
- `fingersUp`: Determines which fingers are extended.

The `HandDetector` class is used in both scripts to simplify hand tracking and finger state detection.

## Scripts

### 1. Finger Tracker (`finger_tracker.py`)
The `finger_tracker.py` script tracks and labels each finger (Thumb, Index, Middle, Ring, Pinky) based on the detected hand landmarks. It determines whether the detected hand is right or left and labels the fingers accordingly.

https://github.com/user-attachments/assets/a87656b3-e3dd-40f5-8e6b-eb3f6c6e267a

#### Key Features:
- Detects hands and draws hand landmarks on the video stream.
- Identifies and labels each finger based on hand orientation (left/right hand).
- Supports recording the video output when toggled.
- Displays real-time frames per second (FPS) for performance monitoring.

#### Usage:
```bash
python finger_tracker.py
```
Press `r` to toggle recording, and press `p` to stop the script.

### 2. Finger Counter (`finger_counter.py`)
The `finger_counter.py` script tracks the number of fingers extended on a detected hand and displays an image corresponding to the number of fingers held up. This script can be used to visually count fingers in real time.



https://github.com/user-attachments/assets/5423949d-41a4-435b-b5f6-1aa07edfc080



#### Key Features:
- Counts the number of fingers extended on a hand.
- Displays an image based on the number of fingers extended (e.g., an image for one finger, two fingers, etc.).
- Draws the count of extended fingers on the video frame.
- Supports recording the video output when toggled.
- Displays FPS for performance monitoring.

#### Usage:
```bash
python finger_counter.py
```
Press `r` to toggle recording, and press `p` to stop the script.

## Recording Videos
Both scripts allow recording the video output:
- Press the `r` key to start or stop recording.
- The output video files will be saved in the `VIDEOS` directory.

### Output Files:
- `identify_fingers.mp4` for `finger_tracker.py`
- `finger_counter.mp4` for `finger_counter.py`

## Conclusion
These scripts demonstrate basic hand tracking and finger counting using the MediaPipe framework, providing an interactive way to track and analyze hand gestures in real time. Feel free to extend the functionality or adapt it for custom applications such as gesture control, sign language interpretation, or touchless interfaces.

