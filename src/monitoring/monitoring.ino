#include <WiFi.h>
#include <WiFiManager.h> // https://github.com/tzapu/WiFiManager
#include <ESP32Servo.h>

// Motor Pins
#define ENA 19 // Left (Motor A, PWM)
#define M1 17
#define M2 16

#define ENB 5  // Right (Motor B, PWM)
#define M3 4
#define M4 2

// Line Sensor Pins
#define S1 34
#define S2 35
#define S3 33
#define S4 32
#define S5 25

#define SERVO_PIN 2

Servo myServo;

// WiFi TCP Server
WiFiServer server(8080); // TCP server on port 8080
WiFiClient client;       // Connected client

// Data variables
String buff; 
const char delimiter[] = ":";
int motor_speed_val, servo_angle_val; 
int sensor1, sensor2, sensor3, sensor4, sensor5;

void setup() {
  Serial.begin(115200); // Serial for debugging

  // Motor pin setup
  pinMode(ENA, OUTPUT); // PWM
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(ENB, OUTPUT); // PWM
  pinMode(M3, OUTPUT);
  pinMode(M4, OUTPUT);

  // Sensor pin setup
  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  pinMode(S3, INPUT); 
  pinMode(S4, INPUT);
  pinMode(S5, INPUT);

  stopMotors(); // Important: Stop motors at startup
  myServo.attach(SERVO_PIN);
  myServo.write(0); // Initial servo position

  // WiFiManager for easy WiFi config
  WiFiManager wm;
  bool res = wm.autoConnect("AutoConnectAP","password"); // Portal if not connected

  if (!res) {
    Serial.println("Failed to connect to WiFi");
  } else {
    Serial.println("WiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP()); 
    server.begin(); 
    Serial.println("TCP server started on port 8080. Waiting for client...");
  }
}

void loop() {
  sensor(); // Read sensors

  // Accept new client
  if (server.hasClient()) {
    if (client && client.connected()) {
        Serial.println("New client trying to connect, disconnecting old client.");
        client.stop();
    }
    client = server.available(); 
    if (client) {
        Serial.println("New client connected!");
        client.flush(); 
    }
  }

  // Handle client commands
  if (client && client.connected()) {
    if (client.available() > 0) {
      buff = client.readStringUntil('\n'); 
      buff.trim(); 
      Serial.print("Received from client: "); 
      Serial.println(buff);

      if (buff.length() > 0) {
        if (buff[0] == 'M') {
          char buff_array[buff.length() + 1]; 
          buff.toCharArray(buff_array, sizeof(buff_array));
          
          char *token = strtok(buff_array, delimiter); 
          if (token != NULL) {
            token = strtok(NULL, delimiter); 
            if (token != NULL) {
              motor_speed_val = atoi(token); 
            } else {
              motor_speed_val = 0; 
            }
          } else {
            motor_speed_val = 0; 
          }

          char *action_token = strtok(NULL, delimiter); 
          if (action_token != NULL && strlen(action_token) > 0) {
            char action = action_token[0];
            if (action == 'F') {
              forward(motor_speed_val);
            } else if (action == 'B') {
              backward(motor_speed_val);
            } else if (action == 'L') {
              turnLeft(motor_speed_val);
            } else if (action == 'R') {
              turnRight(motor_speed_val);
            } else if (action == 'S') {
              stopMotors();
            } else {
              Serial.println("Unknown motor action.");
              stopMotors(); 
            }
          } else {
            Serial.println("No motor action, stopping motors.");
            stopMotors(); 
          }
        } 
        else if (buff[0] == 'S') {
          char buff_array[buff.length() + 1];
          buff.toCharArray(buff_array, sizeof(buff_array));
          
          char *token = strtok(buff_array, delimiter); 
          if (token != NULL) {
            token = strtok(NULL, delimiter); 
            if (token != NULL) {
              servo_angle_val = atoi(token); 
              myServo.write(servo_angle_val);
              Serial.print("Servo set to: "); Serial.println(servo_angle_val);
            }
          }
        } 
        else if (buff.startsWith("GETSENSOR")) {
          String sensorData = "SENSORS:";
          sensorData += String(sensor1) + ",";
          sensorData += String(sensor2) + ",";
          sensorData += String(sensor3) + ","; 
          sensorData += String(sensor4) + ",";
          sensorData += String(sensor5);
          client.println(sensorData); 
          Serial.print("Sent to client: "); 
          Serial.println(sensorData);
        } 
        else {
            Serial.print("Unknown command: ");
            Serial.println(buff);
        }
      }
    }
  } 
}

void sensor() {
  sensor1 = digitalRead(S1);
  sensor2 = digitalRead(S2);
  sensor3 = analogRead(S3); 
  sensor4 = digitalRead(S4);
  sensor5 = digitalRead(S5);
}

// Motor control functions (PWM)
void forward(int speed_val) {
  // Left forward, right forward
  digitalWrite(M1, HIGH); 
  digitalWrite(M2, LOW);
  digitalWrite(M3, HIGH); 
  digitalWrite(M4, LOW);
  analogWrite(ENA, speed_val);
  analogWrite(ENB, speed_val);
  Serial.print("Motor: Forward, Speed: "); Serial.println(speed_val);
}

void backward(int speed_val) {
  // Left backward, right backward
  digitalWrite(M1, LOW);  
  digitalWrite(M2, HIGH);
  digitalWrite(M3, LOW);  
  digitalWrite(M4, HIGH);
  analogWrite(ENA, speed_val);
  analogWrite(ENB, speed_val);
  Serial.print("Motor: Backward, Speed: "); Serial.println(speed_val);
}

void turnLeft(int speed_val) {
  // Left backward, right forward
  digitalWrite(M1, LOW);   // left backward
  digitalWrite(M2, HIGH);
  digitalWrite(M3, HIGH);  // right forward
  digitalWrite(M4, LOW);
  analogWrite(ENA, speed_val);
  analogWrite(ENB, speed_val);
  Serial.print("Motor: Turn Left, Speed: "); Serial.println(speed_val);
}

void turnRight(int speed_val) {
  // Left forward, right backward
  digitalWrite(M1, HIGH);  // left forward
  digitalWrite(M2, LOW);
  digitalWrite(M3, LOW);   // right backward
  digitalWrite(M4, HIGH);
  analogWrite(ENA, speed_val);
  analogWrite(ENB, speed_val);
  Serial.print("Motor: Turn Right, Speed: "); Serial.println(speed_val);
}

void stopMotors() {
  analogWrite(ENA, 0); // Important: Stop motors
  analogWrite(ENB, 0); // Important: Stop motors
  digitalWrite(M1, LOW);
  digitalWrite(M2, LOW);
  digitalWrite(M3, LOW);
  digitalWrite(M4, LOW);
  Serial.println("Motor: Stopped");
}
