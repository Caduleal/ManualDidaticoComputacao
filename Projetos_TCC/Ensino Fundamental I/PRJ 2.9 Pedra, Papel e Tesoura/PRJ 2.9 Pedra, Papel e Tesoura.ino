#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

Adafruit_LiquidCrystal lcd(0);

const byte trigPin = 3;
const byte echoPin = 2;

const float distanciaParaJogar = 200.0;    // cm
const float distanciaParaRearmar = 250.0;  // cm
const unsigned long tempoResposta = 5000; // ms

const char* const respostas[] = {"Pedra", "Papel", "Tesoura"};

bool podeJogar = true;
bool primeiroSorteio = true;

void mostrarConvite() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Vamos jogar?");
  lcd.setCursor(0, 1);
  lcd.print("Aproxime!");
}

float medirDistancia() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long eco = pulseIn(echoPin, HIGH, 25000UL);

  if (eco == 0) {
    return -1;  // Nenhum eco recebido
  }

  return eco * 0.0343 / 2.0;
}

void mostrarJogada() {
  if (primeiroSorteio) {
    randomSeed(micros());
    primeiroSorteio = false;
  }

  byte escolha = random(3);  // 0, 1 ou 2

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(respostas[escolha]);

  Serial.print("Jogada: ");
  Serial.println(respostas[escolha]);

  delay(tempoResposta);
  mostrarConvite();
}

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite(trigPin, LOW);

  Wire.begin();
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  mostrarConvite();
}

void loop() {
  float distancia = medirDistancia();

  if (distancia < 0) {
    Serial.println("Sem eco");
    podeJogar = true;
  } else {
    Serial.print("Distancia: ");
    Serial.print(distancia, 1);
    Serial.println(" cm");

    if (distancia > distanciaParaRearmar) {
      podeJogar = true;
    }

    if (podeJogar && distancia >= 2.0 && distancia <= distanciaParaJogar) {
      podeJogar = false;
      mostrarJogada();
    }
  }

  delay(60);  // Intervalo entre medições do HC-SR04
}