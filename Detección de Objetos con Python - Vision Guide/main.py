import cv2 #opencv
import urllib.request #para abrir y leer URL
import numpy as np
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db


#CONEXIÓN A LA BASE DE DATOS FIREBASE

# Configuración de las credenciales de Firebase
firebase_cred = {
  "type": "service_account",
  "project_id": "mandar-notificacion",
  "private_key_id": "a0f6e393f685b4e04c9c32e35b452310cac0fd7e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDOj3+KsLbOQvG8\nEU6ZTTzxFHV5dlSA4gYiFlGRRMt+jiwgk6cgLX++/LgjUUuGqYNrzoqarrJduTPh\nxOl870ZlTchpoSGNAaJDIxkF1N5AmAV2l+CiZfdl77JzOfL2rn8FOKud3ueg6lip\n806Uqr3V6Q/CSQfwFEIeEUPCgZn3mrZ0Cu1BjKuUkslUWKIon4KfjJRC7KnkvXaS\nyY0osgN43MwYiXjLxOuIu4QD47T+y8vgT+fnhiG6p+A/JionJAl0N1Gfj9yV4qRs\nyIH1sCUN1oeDY+PKaZ0ynY6iZncxOJWYsLOqmwmJCtxWOH7ibvu4mocG1iH590JC\nHU+vlwoLAgMBAAECggEADypPh0bMhRdt8nLXpHKC3bUbOUNL/PjOa0SpBGz0Mi+m\nybvnDBO+SnvF2sHzNS9o3xdkHoTI9g/M4VYfSY7mFwK/V6uYcDPSGyYoH8EUxQVK\nqv3t/iS78mRgygwgUtm8D0DgrxyLp2LNOhA+kRrgCSTghVEhuUMJ5g86b4nFKUqB\n3wmbNxQQNgxvd0I86tYt4xRbOpbcdWf0melARM4SkJv7ggTPUs5OmE88kjWQFv5c\n90O8AzCFJgqjUSWhRJGIiOwn/ygDQui7xIaBQYDiktpO+LBBUXXN3TsERzw4dYz8\nC03sQDOsSvxqen5Wf86zgTnEN1bWMo7RWGNqTeXzMQKBgQD8SYYOB+AxAKP9+j4e\nK5uQG2CCvf04b3/otNHQhceRF3NZdknUnbioWjHtNwqRtKQ6JQp4DV+l78enXCge\n0C0gtU1KLr4/wGFjzg9WNOT+qXedZDz/fWYFPMwkq+6bIR+USESR4hgiU2sklsio\ncLbrtJkR+lln1P1kg4NILgbelQKBgQDRmbPDiy3jqXT7Nb+h6tifFo6xkp1jZc9w\n87nGknJdgl6m0SMSzWe4qur4g3t7SDGd0XPI6QplDggYl5qiv/gmDlKfjsiAxylC\nIL3CFoflImntN+a/bzfa9uYrKvGxiFPUHgdSbVKLrvpoO5g4cIxoS/+iqTGVh3p/\nyNyVYvI+HwKBgQCzoYoQnWz0lxcs9CucgcIu1j9ed/Y/Y6x4PZ8S0N4qob7g2Qdy\nmqZrQGVCGKmu2yb/u3X7ytHqrZLDyCtM3T70hgK1KhkN/WWakZJ7+AeAh5uCdme0\nJk4otoRILB8lV21LwDUKhihW8HxePfo7bJ3hr+I5Wb6k3pNZKQalsxfzDQKBgQCW\nW2E2RFA+AaDWWH9IwvR0YzUnsxpOZImD6IL7LLD33X7SwjIb2devBIUckw1wqaBW\nKxuZI3t+dKtgINkgKP/1JM8mgMHah4RUWLJnWcxQlfhQ4IoaB8mUvQruKpdJGJey\nEXyFJ8FQTMx7G00eJ7bBVstiP2c/cflxU4DRdTJ7VwKBgQC9jazR7mIaySY/DF7U\nyr5x2RPcQdQnPgzD3JC356ljAcCQ2oKhDeH1Iw5WW3nsPwv4hmlMmiYdEN6DX39q\nUMj0KC4/fxWmQ+eV0Jlq9wsUevPeFDMQErULM7CcNOpHbhWD4Ox85QFFQfPuxcuv\nt1TFugiQVZfaT1EJAvKj6j3rQQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-royll@mandar-notificacion.iam.gserviceaccount.com",
  "client_id": "110485824900783183320",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-royll%40mandar-notificacion.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Configura las credenciales de Firebase
cred = credentials.Certificate(firebase_cred)

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
