import cv2
import mediapipe as mp
import pyautogui
import math
import pickle
import time
from collections import deque, Counter

mp_face_mesh = mp.solutions.face_mesh

LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

MODEL_FILE = "eye_gesture_model.pkl"

screen_width, screen_height = pyautogui.size()


def eye_aspect_ratio(landmarks, eye_points, width, height):
    points = []

    for point in eye_points:
        x = int(landmarks[point].x * width)
        y = int(landmarks[point].y * height)
        points.append((x, y))

    vertical_1 = math.dist(points[1], points[5])
    vertical_2 = math.dist(points[2], points[4])
    horizontal = math.dist(points[0], points[3])

    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def get_features(landmarks, width, height):

    left_ear = eye_aspect_ratio(
        landmarks, LEFT_EYE, width, height
    )

    right_ear = eye_aspect_ratio(
        landmarks, RIGHT_EYE, width, height
    )

    left_iris_x = sum(
        landmarks[i].x for i in LEFT_IRIS
    ) / 5

    left_iris_y = sum(
        landmarks[i].y for i in LEFT_IRIS
    ) / 5

    right_iris_x = sum(
        landmarks[i].x for i in RIGHT_IRIS
    ) / 5

    right_iris_y = sum(
        landmarks[i].y for i in RIGHT_IRIS
    ) / 5

    iris_x = (left_iris_x + right_iris_x) / 2
    iris_y = (left_iris_y + right_iris_y) / 2

    left_eye_left = landmarks[362].x
    left_eye_right = landmarks[263].x

    right_eye_left = landmarks[33].x
    right_eye_right = landmarks[133].x

    left_eye_top = landmarks[386].y
    left_eye_bottom = landmarks[374].y

    right_eye_top = landmarks[159].y
    right_eye_bottom = landmarks[145].y

    left_ratio_x = (
        (left_iris_x - left_eye_left)
        / (left_eye_right - left_eye_left)
    )

    right_ratio_x = (
        (right_iris_x - right_eye_left)
        / (right_eye_right - right_eye_left)
    )

    left_ratio_y = (
        (left_iris_y - left_eye_top)
        / (left_eye_bottom - left_eye_top)
    )

    right_ratio_y = (
        (right_iris_y - right_eye_top)
        / (right_eye_bottom - right_eye_top)
    )

    gaze_x = (left_ratio_x + right_ratio_x) / 2
    gaze_y = (left_ratio_y + right_ratio_y) / 2

    return [
        left_ear,
        right_ear,
        iris_x,
        iris_y,
        gaze_x,
        gaze_y,
        left_ratio_x,
        right_ratio_x,
        left_ratio_y,
        right_ratio_y
    ], left_ear, right_ear, iris_x, iris_y


with open(MODEL_FILE, "rb") as file:
    model = pickle.load(file)

print()
print("====================================")
print("       EYEASSIST AI MOUSE")
print("====================================")
print()
print("Model loaded successfully!")
print()
print("Controls:")
print("Left Blink  -> Right Click")
print("Right Blink -> Left Click")
print("Both Blink  -> Double Click")
print("P           -> Pause / Resume Mouse")
print("Q           -> Quit")
print()
print("Starting calibration...")
print("Keep BOTH eyes OPEN for 3 seconds.")
print()


camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

calibration_values = []

calibration_time = 3

start_time = time.time()

calibrated = False

left_threshold = 0.25
right_threshold = 0.25

left_was_closed = False
right_was_closed = False

last_click_time = 0

click_delay = 0.5

mouse_enabled = True

prediction_history = deque(maxlen=6)

stable_gesture = "WAITING"


cv2.namedWindow(
    "EyeAssist AI Mouse",
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    "EyeAssist AI Mouse",
    640,
    480
)


with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    while True:

        success, frame = camera.read()

        if not success:
            print("Camera not detected")
            break

        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:

            landmarks = results.multi_face_landmarks[0].landmark

            (
                features,
                left_ear,
                right_ear,
                iris_x,
                iris_y
            ) = get_features(
                landmarks,
                width,
                height
            )

            if not calibrated:

                calibration_values.append(
                    (left_ear, right_ear)
                )

                elapsed = time.time() - start_time

                remaining = max(
                    0,
                    calibration_time - int(elapsed)
                )

                cv2.putText(
                    frame,
                    "CALIBRATION",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    3
                )

                cv2.putText(
                    frame,
                    "Keep BOTH eyes OPEN",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Starting in: {remaining}",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )

                if elapsed >= calibration_time:

                    left_average = sum(
                        value[0]
                        for value in calibration_values
                    ) / len(calibration_values)

                    right_average = sum(
                        value[1]
                        for value in calibration_values
                    ) / len(calibration_values)

                    left_threshold = left_average * 0.75
                    right_threshold = right_average * 0.75

                    calibrated = True

                    print("Calibration complete!")
                    print(
                        f"Left threshold: {left_threshold:.3f}"
                    )
                    print(
                        f"Right threshold: {right_threshold:.3f}"
                    )

            else:

                left_closed = left_ear < left_threshold
                right_closed = right_ear < right_threshold

                current_time = time.time()

                blink_detected = False

                if (
                    left_closed
                    and right_closed
                    and not left_was_closed
                    and not right_was_closed
                    and current_time - last_click_time > click_delay
                ):

                    pyautogui.doubleClick(
                        button="left",
                        interval=0.15
                    )

                    last_click_time = current_time

                    stable_gesture = "both_blink"

                    blink_detected = True

                elif (
                    left_closed
                    and not right_closed
                    and not left_was_closed
                    and current_time - last_click_time > click_delay
                ):

                    pyautogui.click(button="right")

                    last_click_time = current_time

                    stable_gesture = "left_blink"

                    blink_detected = True

                elif (
                    right_closed
                    and not left_closed
                    and not right_was_closed
                    and current_time - last_click_time > click_delay
                ):

                    pyautogui.click(button="left")

                    last_click_time = current_time

                    stable_gesture = "right_blink"

                    blink_detected = True

                if not blink_detected:

                    prediction = model.predict(
                        [features]
                    )[0]

                    prediction_history.append(
                        prediction
                    )

                    counts = Counter(
                        prediction_history
                    )

                    gesture, count = counts.most_common(1)[0]

                    if count >= 4:

                        if gesture not in [
                            "left_blink",
                            "right_blink",
                            "both_blink"
                        ]:

                            stable_gesture = gesture

                if mouse_enabled:

                    margin_x = 0.15
                    margin_y = 0.15

                    normalized_x = (
                        (iris_x - margin_x)
                        / (1 - 2 * margin_x)
                    )

                    normalized_y = (
                        (iris_y - margin_y)
                        / (1 - 2 * margin_y)
                    )

                    normalized_x = max(
                        0,
                        min(1, normalized_x)
                    )

                    normalized_y = max(
                        0,
                        min(1, normalized_y)
                    )

                    target_x = normalized_x * screen_width
                    target_y = normalized_y * screen_height

                    current_x, current_y = pyautogui.position()

                    smooth_x = (
                        current_x
                        + (target_x - current_x) * 0.07
                    )

                    smooth_y = (
                        current_y
                        + (target_y - current_y) * 0.07
                    )

                    pyautogui.moveTo(
                        int(smooth_x),
                        int(smooth_y),
                        duration=0.005
                    )

                left_was_closed = left_closed
                right_was_closed = right_closed

                cv2.putText(
                    frame,
                    f"GESTURE: {stable_gesture.upper()}",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    "MOUSE ON" if mouse_enabled else "MOUSE PAUSED",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

        else:

            prediction_history.clear()

            cv2.putText(
                frame,
                "NO FACE",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

        cv2.imshow(
            "EyeAssist AI Mouse",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("p"):

            mouse_enabled = not mouse_enabled

            print(
                "Mouse ON"
                if mouse_enabled
                else "Mouse PAUSED"
            )

        elif key == ord("q"):

            break


camera.release()
cv2.destroyAllWindows()

print()
print("EyeAssist stopped.")