import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]

LEFT_EYE_CORNERS = [362, 263]
RIGHT_EYE_CORNERS = [33, 133]

LEFT_EYE_TOP_BOTTOM = [386, 374]
RIGHT_EYE_TOP_BOTTOM = [159, 145]

camera = cv2.VideoCapture(0)

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

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:

            landmarks = results.multi_face_landmarks[0].landmark

            left_iris_x = sum(landmarks[i].x for i in LEFT_IRIS) / 5
            left_iris_y = sum(landmarks[i].y for i in LEFT_IRIS) / 5

            right_iris_x = sum(landmarks[i].x for i in RIGHT_IRIS) / 5
            right_iris_y = sum(landmarks[i].y for i in RIGHT_IRIS) / 5

            left_min_x = landmarks[362].x
            left_max_x = landmarks[263].x

            right_min_x = landmarks[33].x
            right_max_x = landmarks[133].x

            left_min_y = landmarks[386].y
            left_max_y = landmarks[374].y

            right_min_y = landmarks[159].y
            right_max_y = landmarks[145].y

            left_ratio_x = (
                (left_iris_x - left_min_x) /
                (left_max_x - left_min_x)
            )

            right_ratio_x = (
                (right_iris_x - right_min_x) /
                (right_max_x - right_min_x)
            )

            left_ratio_y = (
                (left_iris_y - left_min_y) /
                (left_max_y - left_min_y)
            )

            right_ratio_y = (
                (right_iris_y - right_min_y) /
                (right_max_y - right_min_y)
            )

            gaze_x = (left_ratio_x + right_ratio_x) / 2
            gaze_y = (left_ratio_y + right_ratio_y) / 2

            horizontal_difference = abs(gaze_x - 0.5)
            vertical_difference = abs(gaze_y - 0.5)

            if horizontal_difference > vertical_difference:

                if gaze_x < 0.35:
                    gaze = "GAZE LEFT"

                elif gaze_x > 0.65:
                    gaze = "GAZE RIGHT"

                else:
                    gaze = "GAZE CENTER"

            else:

                if gaze_y < 0.35:
                    gaze = "GAZE UP"

                elif gaze_y > 0.65:
                    gaze = "GAZE DOWN"

                else:
                    gaze = "GAZE CENTER"

            cv2.putText(
                frame,
                gaze,
                (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )

        cv2.imshow("EyeAssist - Gaze Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()