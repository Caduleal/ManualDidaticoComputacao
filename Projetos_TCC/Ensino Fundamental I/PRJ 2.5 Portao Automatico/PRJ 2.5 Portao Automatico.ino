#include <Servo.h>

const int echoPin = 3;
const int trigPin = 2;
const int ledPin = 4;     // Alterado para pino 4 (evita conflito com Serial RX/TX)
const int buzzerPin = 5;  // Alterado para pino 5 (evita conflito com Serial RX/TX)

Servo myservo;
int pos = 0;

void setup() {
  myservo.attach(A0);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int dist = CalcDist(trigPin, echoPin);
  Serial.println(dist);
  
  if (dist < 100) {
    // Objeto próximo: Abre o portão (90°)
    pos = 90;
    myservo.write(pos);
    
    // Alerta estilo sirene de garagem (Pi-Pi-Pi com LED piscando)
    digitalWrite(ledPin, HIGH);
    tone(buzzerPin, 1200); // Tom mais agudo simulando o bipe de ré/saída
    delay(150);            // Duração do "pi"
    
    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);
    delay(150);            // Pausa entre os bipes
    
  } else {
    // Objeto afastado: Fecha o portão (0°) e desliga os alertas
    pos = 0;
    myservo.write(pos);
    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);
    delay(15);
  }
}

int CalcDist(int trigPin, int echoPin){
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