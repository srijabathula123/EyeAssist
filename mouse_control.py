import cv2
import mediapipe as mp
import pyautogui
import math
import time

mp_face_mesh = mp.solutions.face_mesh

LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

screen_width, screen_height = pyautogui.size()

camera = cv2.VideoCapture(0)

mouse_enabled = True

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

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:

            landmarks = results.multi_face_landmarks[0].landmark

            left_iris_x = sum(landmarks[i].x for i in LEFT_IRIS) / 5
            left_iris_y = sum(landmarks[i].y for i in LEFT_IRIS) / 5

            right_iris_x = sum(landmarks[i].x for i in RIGHT_IRIS) / 5
            right_iris_y = sum(landmarks[i].y for i in RIGHT_IRIS) / 5

            iris_x = (left_iris_x + right_iris_x) / 2
            iris_y = (left_iris_y + right_iris_y) / 2

            target_x = iris_x * screen_width
            target_y = iris_y * screen_height

            current_x, current_y = pyautogui.position()

            smooth_x = current_x + (target_x - current_x) * 0.08
            smooth_y = current_y + (target_y - current_y) * 0.08

            if mouse_enabled:
                pyautogui.moveTo(
                    int(smooth_x),
                    int(smooth_y),
                    duration=0.01
                )

            left_ear = eye_aspect_ratio(
                landmarks,
                LEFT_EYE,
                width,
                height
            )

            right_ear = eye_aspect_ratio(
                landmarks,
                RIGHT_EYE,
                width,
                height
            )

            if not calibrated:

                calibration_values.append(
                    (left_ear, right_ear)
                )

                elapsed = time.time() - start_time

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
                    "Keep both eyes OPEN",
                    (20, 80),
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

                    print("Calibration complete")
                    print(f"Left threshold: {left_threshold:.2f}")
                    print(f"Right threshold: {right_threshold:.2f}")

            else:

                left_closed = left_ear < left_threshold
                right_closed = right_ear < right_threshold

                current_time = time.time()

                # BOTH EYES BLINK → DOUBLE LEFT CLICK
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

                    cv2.putText(
                        frame,
                        "DOUBLE CLICK",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        3
                    )

                # LEFT EYE BLINK → RIGHT CLICK
                elif (
                    left_closed
                    and not right_closed
                    and not left_was_closed
                    and current_time - last_click_time > click_delay
                ):

                    pyautogui.click(button="right")

                    last_click_time = current_time

                    cv2.putText(
                        frame,
                        "RIGHT CLICK",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                # RIGHT EYE BLINK → LEFT CLICK
                elif (
                    right_closed
                    and not left_closed
                    and not right_was_closed
                    and current_time - last_click_time > click_delay
                ):

                    pyautogui.click(button="left")

                    last_click_time = current_time

                    cv2.putText(
                        frame,
                        "LEFT CLICK",
                        (20, 140),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                left_was_closed = left_closed
                right_was_closed = right_closed

                cv2.putText(
                    frame,
                    f"Left: {left_ear:.2f}",
                    (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Right: {right_ear:.2f}",
                    (20, 210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        cv2.imshow(
            "EyeAssist - Face Mouse + Blink Click",
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