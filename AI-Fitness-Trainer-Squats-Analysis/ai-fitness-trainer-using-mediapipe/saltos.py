import cv2
import mediapipe as mp

# PRUEBAS DE CONTADOR DE SALTO DE CUERDA INTENTO No.14
# INICIALIZAR LAS VARIABLES
inicio = 0
contador = 0
piso = 2848
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture('output_sample.mp4')#no detecta la camara esta mamada

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        success, img = cap.read()
        if not success:
            break

        img.flags.writeable = False
        results = pose.process(img)
        image_height, image_width, _ = img.shape

        # Dentro del bucle principal
        if results.pose_landmarks:
            left_foot_index = (int(results.pose_landmarks.landmark[31].x * image_width),
                               int(results.pose_landmarks.landmark[31].y * image_height))
            right_foot_index = (int(results.pose_landmarks.landmark[32].x * image_width),
                                int(results.pose_landmarks.landmark[32].y * image_height))
            left_heel = (int(results.pose_landmarks.landmark[29].x * image_width),
                         int(results.pose_landmarks.landmark[29].y * image_height))
            right_heel = (int(results.pose_landmarks.landmark[30].x * image_width),
                          int(results.pose_landmarks.landmark[30].y * image_height))

            cv2.circle(img, left_foot_index, 15, (0, 0, 255), 15)
            cv2.circle(img, right_foot_index, 15, (0, 0, 255), 15)

            if piso - left_foot_index[1] > 80:
                inicio = 1
            elif inicio and piso - left_foot_index[1] < 10:
                contador = contador + 1
                inicio = 0
        else:
            # Manejo cuando no se detectan landmarks
            left_foot_index = (0, 0)  # Establecer un valor predeterminado o realizar alguna acción adecuada
            # O simplemente omitir esta iteración usando 'continue'

        mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        img = cv2.putText(img, "Numero de saltos: " + str(contador), (50, 650),
                          cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 10, cv2.LINE_AA)

        cv2.imshow('Contador de saltos', img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
