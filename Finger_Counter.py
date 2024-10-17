import os
import cv2 as cv
import HandTrackingModule as htm
import time

# Initialize camera and load images
cap = cv.VideoCapture(0)
images = [os.path.join('IMAGES', image) for image in os.listdir('IMAGES')]

if not cap.isOpened():
    raise Exception("Error: couldn't open the camera!")

# Getting video properties and setting up the video writer
f_w, f_h = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT))
filename = "VIDEOS/finger_counter.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"XVID"), 25, (f_w, f_h))

detector = htm.HandDetector(detectionCon=0.7)
ptime, recording = 0, False

# Define the IDs for the tips of the fingers
tip_IDS = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect hands and find landmarks
    frame = detector.findHands(frame)
    landmarks = detector.findPositions(frame)
    frame = cv.flip(frame, 1)  # Flip frame for mirroring

    if len(landmarks) > 0:
        fingers = []

        # Determine if it is a left or right hand
        wrist_x = landmarks[0][0]  # Wrist x-coordinate
        thumb_x = landmarks[1][0]  # Thumb CMC x-coordinate

        if thumb_x > wrist_x:
            # Right hand (Thumb is to the right of the wrist)
            # Check the thumb
            if landmarks[tip_IDS[0]][0] > landmarks[tip_IDS[0] - 2][0]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            # Left hand (Thumb is to the left of the wrist)
            # Check the thumb
            if landmarks[tip_IDS[0]][0] < landmarks[tip_IDS[0] - 2][0]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Check the state of the other four fingers
        for ID in range(1, 5):
            if landmarks[tip_IDS[ID]][1] < landmarks[tip_IDS[ID] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)

        # Display corresponding image
        if total_fingers > 0 and total_fingers <= len(images):
            img = cv.imread(images[total_fingers - 1])
            img = cv.resize(img, (200, 200))
            h, w, _ = img.shape
            frame[0:h, 0:w] = img

        # Draw finger count
        cv.rectangle(frame, (20, 225), (170, 425), (255, 255, 255), cv.FILLED)
        label = "RIGHT HAND FINGERS" if thumb_x > wrist_x else "LEFT HAND FINGERS"
        cv.putText(frame, label, (22, 235), cv.FONT_HERSHEY_PLAIN, 0.75,
                   (128, 0, 0), 1)
        cv.putText(frame, str(total_fingers), (45, 375), cv.FONT_HERSHEY_SIMPLEX,
                   5, (237, 149, 0), 25)

    # Calculate and display FPS
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv.putText(frame, f"FPS: {int(fps)}", (500, 50), cv.FONT_HERSHEY_SIMPLEX,
               1, (255, 0, 0), 3)

    # Write to file if recording
    if recording:
        out.write(frame)

    # Show the frame
    cv.imshow("Hands", frame)

    # Toggle recording with 'r' and exit with 'p'
    key = cv.waitKey(1) & 0xFF
    if key == ord('r'):
        recording = not recording
    elif key == ord('p'):
        break

cap.release()
out.release()
cv.destroyAllWindows()
