import cv2
import numpy as np
import mediapipe as mp
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

landmarker = HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
canvas = None
xp, yp = 0, 0
tip_ids = [4, 8, 12, 16, 20]

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )

    frame_timestamp_ms = int(time.time() * 1000)

    detection_result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            lm_list = []
            h, w, c = frame.shape

            for id, lm in enumerate(hand_landmarks):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), cv2.FILLED)

            if len(lm_list) != 0:
                fingers = []

                if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                for id in range(1, 5):
                    if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                x1, y1 = lm_list[8][1:]
                x2, y2 = lm_list[12][1:]

                if fingers[1] == 0 and fingers[2] == 0:
                    xp, yp = 0, 0

                elif fingers[1] == 1 and fingers[2] == 0:
                    cv2.circle(frame, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1
                    cv2.line(canvas, (xp, yp), (x1, y1), (0, 0, 255), 5)
                    xp, yp = x1, y1

                elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    cv2.circle(frame, (x1, y1), 20, (0, 0, 0), cv2.FILLED)
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1
                    cv2.line(canvas, (xp, yp), (x1, y1), (0, 0, 0), 40)
                    xp, yp = x1, y1

                elif sum(fingers) == 5:
                    canvas = np.zeros_like(frame)
                    xp, yp = 0, 0

                else:
                    xp, yp = 0, 0

    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, img_inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Tasks API Writing Board", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()