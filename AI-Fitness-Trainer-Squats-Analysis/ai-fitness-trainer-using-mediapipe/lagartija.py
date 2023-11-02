import time
import cv2
import numpy as np
from utils import find_angle, get_landmark_features, draw_text

class PushUpDetector:
    def __init__(self, thresholds, flip_frame=False):
        self.flip_frame = flip_frame  # Indica si se debe voltear el fotograma
        self.thresholds = thresholds  # Umbral para la inactividad
        self.font = cv2.FONT_HERSHEY_SIMPLEX  # Tipo de fuente para los textos
        self.linetype = cv2.LINE_AA  # Tipo de línea
        # Define landmark features for key body parts
        self.key_features = {
            'nose': 0,
            'left_shoulder': 5,
            'right_shoulder': 2,
            'left_elbow': 6,
            'right_elbow': 3,
            'left_wrist': 7,
            'right_wrist': 4
        }
        # Inicializa el rastreador de estado
        self.state_tracker = {
            'start_inactive_time': time.perf_counter(),  # Tiempo de inicio de inactividad
            'INACTIVE_TIME': 0.0,  # Tiempo de inactividad
            'IN_PUSH_UP_POSITION': False,  # Indica si está en posición de lagartija
            'PUSH_UP_COUNT': 0,  # Contador de lagartijas realizadas
            'IMPROPER_PUSH_UP': 0  # Contador de lagartijas incorrectas
        }

    def _is_push_up_position(self, nose, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist):
        # Implementa la lógica para detectar si la persona está en posición de lagartija
        # Puedes necesitar calcular ángulos entre partes del cuerpo u otros criterios
        # Devuelve True si está en posición de lagartija, False en caso contrario
        pass

    def process(self, frame, pose):
        play_sound = None  # Variable para reproducir sonidos
        frame_height, frame_width, _ = frame.shape  # Dimensiones del fotograma

        keypoints = pose.process(frame)  # Procesa las claves de la pose en el fotograma

        if keypoints.pose_landmarks:
            landmarks = keypoints.pose_landmarks.landmark  # Puntos de referencia de la pose
            nose = get_landmark_features(landmarks, self.key_features, 'nose', frame_width, frame_height)
            left_shoulder = get_landmark_features(landmarks, self.key_features, 'left_shoulder', frame_width, frame_height)
            right_shoulder = get_landmark_features(landmarks, self.key_features, 'right_shoulder', frame_width, frame_height)
            left_elbow = get_landmark_features(landmarks, self.key_features, 'left_elbow', frame_width, frame_height)
            right_elbow = get_landmark_features(landmarks, self.key_features, 'right_elbow', frame_width, frame_height)
            left_wrist = get_landmark_features(landmarks, self.key_features, 'left_wrist', frame_width, frame_height)
            right_wrist = get_landmark_features(landmarks, self.key_features, 'right_wrist', frame_width, frame_height)

            # Comprueba si la persona está en posición de lagartija
            in_push_up_position = self._is_push_up_position(nose, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist)
            self.state_tracker['IN_PUSH_UP_POSITION'] = in_push up_position  # Actualiza el estado de la posición de lagartija

            if in_push_up_position:
                # Incrementa el contador de lagartijas cuando está en posición
                self.state_tracker['PUSH_UP_COUNT'] += 1
                play_sound = str(self.state_tracker['PUSH_UP_COUNT'])
            else:
                # Incrementa el contador de lagartijas incorrectas cuando no está en posición
                self.state_tracker['IMPROPER_PUSH_UP'] += 1
                play_sound = 'incorrect'

            # Dibuja los puntos de referencia y la retroalimentación en el fotograma
            cv2.circle(frame, nose, 7, (255, 255, 255), -1)
            for _, landmark in self.key_features.items():
                cv2.circle(frame, landmarks[landmark], 7, (0, 255, 0), -1)

            draw_text(frame, "Lagartijas: " + str(self.state_tracker['PUSH_UP_COUNT']), pos=(30, 30), text_color=(255, 255, 255))
            draw_text(frame, "Incorrectas: " + str(self.state_tracker['IMPROPER_PUSH_UP']), pos=(30, 80), text_color=(255, 255, 255))

        else:
            # Restablece los contadores si no se detecta una pose
            end_time = time.perf_counter()
            self.state_tracker['INACTIVE_TIME'] += end_time - self.state_tracker['start_inactive_time']
            if self.state_tracker['INACTIVE_TIME'] >= self.thresholds['INACTIVE_THRESH']:
                self.state_tracker['PUSH_UP_COUNT'] = 0
                self.state_tracker['IMPROPER_PUSH_UP'] = 0
                play_sound = 'reset_counters'
                self.state_tracker['start_inactive_time'] = end_time

        if self.flip_frame:
            frame = cv2.flip(frame, 1)  # Voltea el fotograma horizontalmente si es necesario

        return frame, play_sound

# Código principal
if __name__ == '__main__':
    thresholds = {
        'INACTIVE_THRESH': 5.0  # Ajusta según tus necesidades
    }

    detector = PushUpDetector(thresholds)
    # Implementa la configuración de la cámara y la detección de pose aquí
    # Inicializa la cámara y el detector de pose

    while True:
        # Captura un fotograma de la cámara
        # Implementa la captura de fotogramas aquí
        frame = None

        # Procesa el fotograma usando PushUpDetector
        frame, sound = detector.process(frame, pose)
        # Implementa la retroalimentación de sonido (por ejemplo, reproduce un sonido si el sonido no es None)

        # Muestra el fotograma
        cv2.imshow("Detector de Lagartijas", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la cámara y realiza la limpieza
    # Implementa la limpieza de la cámara y la detección de pose aquí
    cv2.destroyAllWindows()
