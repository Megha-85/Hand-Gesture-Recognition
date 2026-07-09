import cv2
import mediapipe as mp
import pyautogui
import time

# Open Webcam           
cap = cv2.VideoCapture(0)

# MediaPipe Hands Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Finger tip landmark IDs
tipIds = [4, 8, 12, 16, 20]

# Timer to prevent repeated actions
last_action_time = time.time()

while True:

    success, img = cap.read()

    # Flip camera for mirror effect
    img = cv2.flip(img, 1)

    # Convert BGR to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process hand detection
    results = hands.process(imgRGB)
      
    lmList = []

    # Default action text
    action_text = "Show Gesture"

    # Detect Hands
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            # Get landmark positions
            for id, lm in enumerate(handLms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append((cx, cy))

            # Draw landmarks
            mpDraw.draw_landmarks(
                img,
                handLms,
                mpHands.HAND_CONNECTIONS
            )

        if len(lmList) != 0:

            fingers = []

            # Thumb Detection
            if lmList[4][0] > lmList[3][0]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other Fingers Detection
            for id in range(1, 5):

                if lmList[tipIds[id]][1] < lmList[tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Count fingers
            totalFingers = fingers.count(1)

            # Show finger count
            cv2.putText(
                img,
                f'Fingers: {totalFingers}',
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 0, 0),
                3
            )
            current_time = time.time()

            # Delay between actions
            if current_time - last_action_time > 1:

                # OPEN PALM → Pause / Play
                if totalFingers == 5:   

                    pyautogui.press("space")
                    action_text = "Pause / Play"

                # ONE FINGER → Volume Up
                elif totalFingers == 1:

                    pyautogui.press("volumeup")
                    action_text = "Volume Up"

                # TWO FINGERS → Volume Down
                elif totalFingers == 2: 

                    pyautogui.press("volumedown")
                    action_text = "Volume Down"

                # FIST → Mouse Click
                elif totalFingers == 0:

                    pyautogui.click()
                    action_text = "Mouse Click"

                # THREE FINGERS → Scroll Up
                elif totalFingers == 3:

                    pyautogui.scroll(300)
                    action_text = "Scroll Up"

                # FOUR FINGERS → Scroll Down
                elif totalFingers == 4:

                    pyautogui.scroll(-300)
                    action_text = "Scroll Down"

                last_action_time = current_time

            # Show action text on screen
            cv2.putText(
                img,
                action_text,
                (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3
            )

    # Show camera window
    cv2.imshow("Gesture Control System", img)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera
cap.release()

# Close all windows
cv2.destroyAllWindows()