import cv2 as cv
import HandTrackingModule as htm
import time

# Initialize camera
cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise Exception("Error: couldn't open the camera!")

f_w, f_h = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT))
filename = "VIDEOS/identify_fingers.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"XVID"), 25, (f_w, f_h))

detector = htm.HandDetector(detectionCon=0.7)
ptime, recording = 0, False

# Define the IDs for the tips of the fingers
tip_IDS = {
    "Thumb": 4,
    "Index": 8,
    "Middle": 12,
    "Ring": 16,
    "Pinky": 20
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect hands and find landmarks
    frame = detector.findHands(frame)
    landmarks = detector.findPositions(frame)
    frame = cv.flip(frame, 1)  # Flip frame for mirroring

    if len(landmarks) > 0:
        # Determine if it is a left or right hand
        wrist_x = landmarks[0][0]  # Wrist x-coordinate
        thumb_x = landmarks[tip_IDS["Thumb"]][0]  # Thumb tip x-coordinate

        # Identify if the hand is right or left
        right_hand = thumb_x > wrist_x

        # For Right Hand
        if right_hand:
            # Thumb condition for right hand
            if landmarks[tip_IDS['Thumb']][0] > landmarks[tip_IDS["Thumb"] - 2][0]:
                tx, ty = f_w - landmarks[tip_IDS['Thumb']][0], landmarks[tip_IDS['Thumb']][1]
                cv.putText(frame, "Thumb", (tx, ty - 10), cv.FONT_HERSHEY_PLAIN, 1.25,
                           (255, 255, 255), 2)

            # Other fingers condition for right hand
            for finger, finger_id in zip(["Index", "Middle", "Ring", "Pinky"], [8, 12, 16, 20]):
                if landmarks[finger_id][1] < landmarks[finger_id - 2][1]:
                    fx, fy = f_w - landmarks[finger_id][0], landmarks[finger_id][1]
                    cv.putText(frame, f"{finger}", (fx, fy - 10), cv.FONT_HERSHEY_PLAIN,
                               1.25, (255, 255, 255), 2)

        # For Left Hand
        else:
            # Thumb condition for left hand
            if landmarks[tip_IDS['Thumb']][0] < landmarks[tip_IDS["Thumb"] - 2][0]:
                tx, ty = f_w - landmarks[tip_IDS['Thumb']][0], landmarks[tip_IDS['Thumb']][1]
                cv.putText(frame, "Thumb", (tx, ty - 10), cv.FONT_HERSHEY_PLAIN, 1.25,
                           (255, 255, 255), 2)

            # Other fingers condition for left hand
            for finger, finger_id in zip(["Index", "Middle", "Ring", "Pinky"], [8, 12, 16, 20]):
                if landmarks[finger_id][1] < landmarks[finger_id - 2][1]:
                    fx, fy = f_w - landmarks[finger_id][0], landmarks[finger_id][1]
                    cv.putText(frame, f"{finger}", (fx, fy - 10), cv.FONT_HERSHEY_PLAIN,
                               1.25, (255, 255, 255), 2)

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



