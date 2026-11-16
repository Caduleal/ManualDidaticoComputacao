
#include <Servo.h>

// Sensores ultrassônicos
const int echoPin1 = 3;
const int trigPin1 = 2;

const int echoPin2 = 5;
const int trigPin2 = 4;

const int echoPin3 = 7;
const int trigPin3 = 6;

const int echoPin4 = 9;
const int trigPin4 = 8;

// LEDs
const int ledPin1 = 10;
const int ledPin2 = 11;
const int ledPin3 = 12;
const int ledPin4 = 13;

// Servomotores
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

int pos = 0;

void setup() {
  servo1.attach(A0);
  servo2.attach(A1);
  servo3.attach(A2);
  servo4.attach(A3);

  pinMode(echoPin1, INPUT);
  pinMode(trigPin1, OUTPUT);

  pinMode(echoPin2, INPUT);
  pinMode(trigPin2, OUTPUT);

  pinMode(echoPin3, INPUT);
  pinMode(trigPin3, OUTPUT);

  pinMode(echoPin4, INPUT);
  pinMode(trigPin4, OUTPUT);

  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);

  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);

  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  digitalWrite(ledPin4, LOW);

  Serial.begin(9600);
}

void loop() {

  // Sensor e motor 1
  int dist1 = CalcDist(trigPin1, echoPin1);
  Serial.print("Distancia 1: ");
  Serial.println(dist1);

  if (dist1 < 100) {
    pos = 90;
    servo1.write(pos);
    digitalWrite(ledPin1, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo1.write(pos);
    digitalWrite(ledPin1, LOW);
    delay(15);
  }

  // Sensor e motor 2
  int dist2 = CalcDist(trigPin2, echoPin2);
  Serial.print("Distancia 2: ");
  Serial.println(dist2);

  if (dist2 < 100) {
    pos = 90;
    servo2.write(pos);
    digitalWrite(ledPin2, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo2.write(pos);
    digitalWrite(ledPin2, LOW);
    delay(15);
  }

  // Sensor e motor 3
  int dist3 = CalcDist(trigPin3, echoPin3);
  Serial.print("Distancia 3: ");
  Serial.println(dist3);

  if (dist3 < 100) {
    pos = 90;
    servo3.write(pos);
    digitalWrite(ledPin3, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo3.write(pos);
    digitalWrite(ledPin3, LOW);
    delay(15);
  }

  // Sensor e motor 4
  int dist4 = CalcDist(trigPin4, echoPin4);
  Serial.print("Distancia 4: ");
  Serial.println(dist4);

  if (dist4 < 100) {
    pos = 90;
    servo4.write(pos);
    digitalWrite(ledPin4, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo4.write(pos);
    digitalWrite(ledPin4, LOW);
    delay(15);
  }
}

// Mesma função do código original
int CalcDist(int trigPin, int echoPin) {
  long duration, distanceCm;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  distanceCm = duration * 343 / 10000 / 2;

  return distanceCm;
}
