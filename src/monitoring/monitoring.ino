#include <Servo.h>

// Pin untuk Motor
#define ENA 9
#define IN1 2
#define IN2 3

#define ENB 6
#define IN3 5
#define IN4 11

// Pin untuk Sensor Garis
#define S1 13
#define S2 12
#define S3 8
#define S4 7
#define S5 4

// Pin untuk Servo
#define SERVO_PIN 10

Servo myServo;

// Variabel untuk menyimpan data dari Serial
String buff, buff_motor, buff_servo;
const char delimiter[] = ":";
int motor, servo;
int sensor1, sensor2, sensor3, sensor4, sensor5;

// Variabel untuk tracking aksi dan PWM terakhir
String lastAction = "";
int lastPwm = -1;

void setup() {
  Serial.begin(115200);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(S1, INPUT);
  pinMode(S2, INPUT);
  pinMode(S3, INPUT);
  pinMode(S4, INPUT);
  pinMode(S5, INPUT);

  stopMotors();
  myServo.attach(SERVO_PIN);
  myServo.write(0);
}

void loop() {
  sensor();  // Baca sensor garis

  if (Serial.available() > 0) { // Jika ada data dari Serial
    buff = Serial.readStringUntil('\n'); // Baca data hingga newline

    if (buff[0] == 'M') { // Jika data adalah perintah motor
      buff_motor = buff;
      char buff_motor_array[buff_motor.length() + 1];
      buff_motor.toCharArray(buff_motor_array, sizeof(buff_motor_array));
      char *token = strtok(buff_motor_array, delimiter);
      int newPwm = -1;
      String newAction = "";
      if (token != NULL) {
        token = strtok(NULL, delimiter);
        if (token != NULL) {
          newPwm = atoi(token); // Ambil nilai motor dari string
        }
      }
      char *action = strtok(NULL, delimiter); // Ambil aksi motor
      if (action != NULL) {
        newAction = String(action[0]);
      } else {
        newAction = "F";
      }

      // Jika aksi berubah atau PWM berubah, update motor
      if (newAction != lastAction || newPwm != lastPwm) {
        if (newAction == "F") {
          forward(newPwm);
        } else if (newAction == "B") {
          backward(newPwm);
        } else if (newAction == "L") {
          turnLeft(newPwm);
        } else if (newAction == "R") {
          turnRight(newPwm);
        } else if (newAction == "S") {
          stopMotors();
        }
        lastAction = newAction;
        lastPwm = newPwm;
      } else if (newAction == lastAction && newPwm != lastPwm) {
        // Jika hanya PWM berubah, update PWM saja tanpa ubah arah
        if (newAction == "F") {
          analogWrite(ENA, newPwm);
          analogWrite(ENB, newPwm);
        } else if (newAction == "B") {
          analogWrite(ENA, newPwm);
          analogWrite(ENB, newPwm);
        } else if (newAction == "L") {
          analogWrite(ENA, newPwm);
          analogWrite(ENB, 0);
        } else if (newAction == "R") {
          analogWrite(ENA, 0);
          analogWrite(ENB, newPwm);
        }
        lastPwm = newPwm;
      }
    }
    else if (buff[0] == 'S') { // Jika data adalah perintah servo
      buff_servo = buff;
      char buff_servo_array[buff_servo.length() + 1];
      buff_servo.toCharArray(buff_servo_array, sizeof(buff_servo_array));
      char *token = strtok(buff_servo_array, delimiter);
      if (token != NULL) {
        token = strtok(NULL, delimiter);
        if (token != NULL) {
          servo = atoi(token); // Ambil nilai sudut servo
        }
      }
      myServo.write(servo);
    }
    else if (buff.startsWith("GETSENSOR")) { // Jika minta data sensor
      Serial.print("SENSORS:");
      Serial.print(sensor1); Serial.print(",");
      Serial.print(sensor2); Serial.print(",");
      Serial.print(sensor3); Serial.print(",");
      Serial.print(sensor4); Serial.print(",");
      Serial.println(sensor5);
    }
  }
}

void sensor() {
  sensor1 = digitalRead(S1);
  sensor2 = digitalRead(S2);
  sensor3 = digitalRead(S3);
  sensor4 = digitalRead(S4);
  sensor5 = digitalRead(S5);
}

void forward(int num) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, num);
  analogWrite(ENB, num);
}

void backward(int num) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, num);
  analogWrite(ENB, num);
}

void turnLeft(int num) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, num);
  analogWrite(ENB, 0);
}

void turnRight(int num) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, num);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}