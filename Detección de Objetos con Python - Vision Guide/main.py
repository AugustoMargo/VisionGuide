import cv2 #opencv
import urllib.request #para abrir y leer URL
import numpy as np
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db


#CONEXIÓN A LA BASE DE DATOS FIREBASE

# Configura las credenciales de Firebase 
cred = credentials.Certificate("Detección de Objetos con Python - Vision Guide\mandar-notificacion-firebase-adminsdk-royll-a0f6e393f6.json")

# Inicializa la base de datos de Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mandar-notificacion-default-rtdb.firebaseio.com/'
})

config = {
  "apiKey": "AIzaSyCFQrKa4D56ZPZhVjQ3CZuRM8rGJVOWvt4",
  "authDomain": "mandar-notificacion.firebaseapp.com",
  "databaseURL": "https://mandar-notificacion-default-rtdb.firebaseio.com",
  "projectId": "mandar-notificacion",
  "storageBucket": "mandar-notificacion.appspot.com",
  "messagingSenderId": "49457625336",
  "appId": "1:49457625336:web:3b5d7a1c0c04711f96e30d"
}


# Inicializa la base de datos de Firebase
firebase_db = db.reference()


#PROGRAMA DE CLASIFICACION DE OBJETOS PARA VIDEO EN DIRECCION IP 

url = 'http://192.168.2.114/800x600.jpg'
#url = 'http://192.168.1.6/'
# winName = 'ESP32 CAMERA'
# cv2.namedWindow(winName,cv2.WINDOW_AUTOSIZE)
#scale_percent = 80 # percent of original size    #para procesamiento de imagen

classNames = []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
#net.setInputSize(480,480)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while(1):
    imgResponse = urllib.request.urlopen (url) #abrimos el URL
    imgNp = np.array(bytearray(imgResponse.read()),dtype=np.uint8)
    img = cv2.imdecode (imgNp,-1) #decodificamos

    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # vertical
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #black and white

    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    print(classNames[classIds.flatten()[0] - 1]) if len(classIds) != 0 else None  # Imprime el nombre del objeto si se detecta

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            print(f'Objeto detectado: {className}')

            # Crear un diccionario con los datos de detección de objetos
            detection_data = {
                "object_name": className,
            }

            # Enviar los datos de detección de objetos a Firebase
            firebase_db.child('detections').set(detection_data)

    # Para mostrar la camara y lo que esta detectando
    # if len(classIds) != 0:
    #     for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
    #         cv2.rectangle(img, box, color=(0, 255, 0), thickness=3)  # mostramos en rectangulo lo que se encuentra
    #         cv2.putText(img, classNames[classId - 1], (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
    #                     (0, 255, 0), 2)


    # cv2.imshow(winName,img) # mostramos la imagen

    #esperamos a que se presione ESC para terminar el programa
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
cv2.destroyAllWindows()
firebase_admin.delete_app(firebase_admin.get_app()) 
