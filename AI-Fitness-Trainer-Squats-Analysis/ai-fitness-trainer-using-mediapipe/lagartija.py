# Importa las bibliotecas necesarias
import cv2  # OpenCV
import mediapipe as mp  # MediaPipe

# Define una clase llamada 'poseDetector'
class poseDetector():
    
    # Constructor de la clase con parámetros opcionales
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detectionCon=0.5, trackCon=0.5):
        #
        # Inicializa los parámetros de configuración
        self.mode = mode 
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        # Crea instancias de las clases de MediaPipe necesarias
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.detectionCon, self.trackCon)
        
    # Método para encontrar y dibujar la pose en una imagen
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
                
        return img
    
    # Método para encontrar la posición de los landmarks de la pose
    def findPosition(self, img, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                # Obtener la altura, ancho y canales de la imagen
                h, w, c = img.shape
                # Determinar las coordenadas de píxeles de los landmarks
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList

# Función principal
def main():
    # Crear una instancia del detector de pose
    detector = poseDetector()
    
    # Abrir la cámara web (0 es la cámara predeterminada)
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, img = cap.read()  # 'ret' es solo la variable de retorno, no se usa mucho
        if ret:
            # Utilizar el detector para encontrar y dibujar la pose en el marco de video
            img = detector.findPose(img)
            cv2.imshow('Esqueleto completo con nodos', img)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

# Ejecutar la función principal si este script es el punto de entrada
if __name__ == "__main__":
    main()
