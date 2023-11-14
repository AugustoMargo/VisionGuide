#include <Arduino.h>
#include <WiFi.h>
// #include <FirebaseESP32.h>
#include <Firebase_ESP_Client.h>
#include <Wire.h>
#include <WiFiUdp.h>
#include "WifiCam.hpp"
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

// Define the WiFi credentials
#define WIFI_SSID "saltayroca"
#define WIFI_PASSWORD "escuela2043+"

// Define the Firebase project API Key
#define API_KEY "AIzaSyCFQrKa4D56ZPZhVjQ3CZuRM8rGJVOWvt4"

// Define RTDB URL
#define DATABASE_URL "https://mandar-notificacion-default-rtdb.firebaseio.com/"

IPAddress local_IP(192, 168, 2, 116); // Desired Static IP Address
IPAddress subnet(255, 255, 255, 0);
IPAddress gateway(192, 168, 1, 1);

// Define Firebase objects
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// Variable to save USER UID
String uid;

// Database main path (to be updated in setup with the user UID)
String databasePath;
String distancePath = "/distancia";  // Define the path to store distance data

// Parent Node (to be updated in every loop)
String parentPath;

esp32cam::Resolution initialResolution;

WebServer server(80);

// Sensor pins
const int triggerPin1 = 4;
const int echoPin1 = 2;
const int triggerPin2 = 14;
const int echoPin2 = 15;

const int umbral = 12;
const int distanciaMaxima = 200;

// Timer variables (send new readings every three minutes)
unsigned long sendDataPrevMillis = 0;
unsigned long timerDelay = 3000;  
bool signupOK = false;
int count = 0;

// Función para medir la distancia usando HC-SR04
float medirDistancia(int triggerPin, int echoPin) {
  // Establece el pin TRIGGER como salida
  pinMode(triggerPin, OUTPUT);
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);

  // Genera un pulso corto en el pin TRIGGER
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  // Lee la duración del pulso en el pin ECHO
  pinMode(echoPin, INPUT);
  long duracion = pulseIn(echoPin, HIGH);

  // Calcula la distancia en centímetros (usando la velocidad del sonido en el aire)
  float distancia = (duracion / 2) * 0.0343;  // Dividido por 2 porque el pulso va de ida y vuelta

  return distancia;
}


void setup() {
  Serial.begin(115200);

  if (!WiFi.config(local_IP, gateway, subnet)) {
  Serial.println("STA Failed to configure");
  }

  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("WiFi failure");
    delay(5000);
    ESP.restart();
  }

  Serial.println("WiFi connected");

  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("camera initialize failure");
      delay(5000);
      ESP.restart();
    }
    Serial.println("camera initialize success");
  }

  Serial.println("Conectado a WiFi");
  Serial.println(WiFi.localIP());

  // Inicializa la conexión WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }

  /* Assign the api key (required) */
  config.api_key = API_KEY;

  /* Assign the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }

  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
  addRequestHandlers();
  server.begin();
}

void loop() {
  // Envía nuevas lecturas de distancia a la base de datos
  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 5000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();

    // Medir distancias con sensores HC-SR04
    float distancia1 = medirDistancia(triggerPin1, echoPin1);
    float distancia2 = medirDistancia(triggerPin2, echoPin2);

    // Comparar distancias y detectar objetos
    String estadoObjeto;
    if (distancia1 > distanciaMaxima && distancia2 > distanciaMaxima) {
      estadoObjeto = "Ningún objeto detectado";
    } else if (distancia1 - distancia2 > umbral) {
      estadoObjeto = "a la izquierda";
    } else if (distancia2 - distancia1 > umbral) {
      estadoObjeto = "a la derecha";
    } else {
      float distanciaPromedio = (distancia1 + distancia2) / 2;
      estadoObjeto = String(distanciaPromedio) + " cm";
    }

    distancePath = "/detections/distancia";
    if (Firebase.RTDB.setString(&fbdo, distancePath, estadoObjeto.c_str())) {
      Serial.println("Dato enviado a Firebase: " + estadoObjeto);
    }

    // Firebase.setString(&fbdo, distancePath, estadoObjeto.c_str());
    // Serial.println("Dato enviado a Firebase: " + estadoObjeto);
    // parentPath = distancePath;

    // Firebase.setString(fbdo, parentPath.c_str(), estadoObjeto.c_str());

    // Serial.println("Datos enviados a Firebase: " + estadoObjeto);
    
    server.handleClient();
  }
}
