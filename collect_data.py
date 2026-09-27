import cv2
import mediapipe as mp
import csv
import os
import math

mp_face_mesh = mp.solutions.face_mesh

LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

DATA_FILE = "eye_gesture_data.csv"

GESTURES = {
    "1": "normal",
    "2": "left_blink",
    "3": "right_blink",
    "4": "both_blink",
    "5": "look_left",
    "6": "look_right",
    "7": "look_up",
    "8": "look_down"
}


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
    ]


if not os.path.exists(DATA_FILE):

    with open(DATA_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "left_ear",
            "right_ear",
            "iris_x",
            "iris_y",
            "gaze_x",
            "gaze_y",
            "left_ratio_x",
            "right_ratio_x",
            "left_ratio_y",
            "right_ratio_y",
            "label"
        ])


camera = cv2.VideoCapture(0)

current_gesture = None
sample_count = 0

print()
print("EyeAssist ML Data Collection")
print("----------------------------")
print("1 = Normal")
print("2 = Left Blink")
print("3 = Right Blink")
print("4 = Both Blink")
print("5 = Look Left")
print("6 = Look Right")
print("7 = Look Up")
print("8 = Look Down")
print("Q = Quit")
print()

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

            features = get_features(
                landmarks,
                width,
                height
            )

            if current_gesture:

                with open(
                    DATA_FILE,
                    "a",
                    newline=""
                ) as file:

                    writer = csv.writer(file)

                    writer.writerow(
                        features + [current_gesture]
                    )

                sample_count += 1

            cv2.putText(
                frame,
                f"Gesture: {current_gesture}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Samples: {sample_count}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

        cv2.imshow(
            "EyeAssist - Data Collection",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("1"):
            current_gesture = "normal"
            print("Collecting NORMAL")

        elif key == ord("2"):
            current_gesture = "left_blink"
            print("Collecting LEFT BLINK")

        elif key == ord("3"):
            current_gesture = "right_blink"
            print("Collecting RIGHT BLINK")

        elif key == ord("4"):
            current_gesture = "both_blink"
            print("Collecting BOTH BLINK")

        elif key == ord("5"):
            current_gesture = "look_left"
            print("Collecting LOOK LEFT")

        elif key == ord("6"):
            current_gesture = "look_right"
            print("Collecting LOOK RIGHT")

        elif key == ord("7"):
            current_gesture = "look_up"
            print("Collecting LOOK UP")

        elif key == ord("8"):
            current_gesture = "look_down"
            print("Collecting LOOK DOWN")

        elif key == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()

print()
print("Data collection stopped.")
print(f"Total samples collected: {sample_count}")
print(f"Saved to: {DATA_FILE}")