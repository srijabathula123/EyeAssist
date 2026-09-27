import cv2
import mediapipe as mp
import math
import time

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

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

camera = cv2.VideoCapture(0)

calibration_values = []
calibration_time = 3
start_time = time.time()
calibrated = False

left_threshold = 0.25
right_threshold = 0.25

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

            left_ear = eye_aspect_ratio(
                landmarks, LEFT_EYE, width, height
            )

            right_ear = eye_aspect_ratio(
                landmarks, RIGHT_EYE, width, height
            )

            if not calibrated:

                elapsed = time.time() - start_time

                calibration_values.append(
                    (left_ear, right_ear)
                )

                remaining = calibration_time - int(elapsed)

                cv2.putText(
                    frame,
                    "CALIBRATION",
                    (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    3
                )

                cv2.putText(
                    frame,
                    "Keep both eyes OPEN",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Starting in: {max(0, remaining)}",
                    (20, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )

                if elapsed >= calibration_time:

                    left_average = sum(
                        value[0] for value in calibration_values
                    ) / len(calibration_values)

                    right_average = sum(
                        value[1] for value in calibration_values
                    ) / len(calibration_values)

                    left_threshold = left_average * 0.75
                    right_threshold = right_average * 0.75

                    calibrated = True

                    print("Calibration complete")
                    print(f"Left threshold: {left_threshold:.2f}")
                    print(f"Right threshold: {right_threshold:.2f}")

            else:

                cv2.putText(
                    frame,
                    f"Left: {left_ear:.2f}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Right: {right_ear:.2f}",
                    (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                if left_ear < left_threshold and right_ear > right_threshold:
                    cv2.putText(
                        frame,
                        "LEFT BLINK",
                        (20, 125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                elif right_ear < right_threshold and left_ear > left_threshold:
                    cv2.putText(
                        frame,
                        "RIGHT BLINK",
                        (20, 125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                elif left_ear < left_threshold and right_ear < right_threshold:
                    cv2.putText(
                        frame,
                        "BOTH EYES BLINK",
                        (20, 125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        3
                    )

                else:
                    cv2.putText(
                        frame,
                        "READY",
                        (20, 125),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        3
                    )

        cv2.imshow("EyeAssist - Adaptive Blink Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()

            