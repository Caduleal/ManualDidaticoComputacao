
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <math.h>

// LCD I2C
Adafruit_LiquidCrystal lcd(0);

// SENSOR HC-SR04
const int trigPin = 3;
const int echoPin = 2;

// CONFIGURACOES
const float velocidadeSom = 0.0343; // cm/us
const float distanciaMinima = 2.0;  // cm
const float distanciaMaxima = 300.0; // cm

// INTERVALO ENTRE LEITURAS
const unsigned long intervaloLeitura = 30000UL; // 30 ms

// TEMPO DE EXIBICAO
const unsigned long tempoExibicao = 3000UL; // 3 segundos

// LIMIAR DE MOVIMENTO
const float velocidadeMinima = 0.10; // m/s

// VARIAVEIS
float distanciaAtual = 0;
float distanciaAnterior = 0;

float velocidade = 0;
float velocidadeCapturada = 0;

unsigned long tempoAnterior = 0;
unsigned long ultimaLeitura = 0;
unsigned long inicioExibicao = 0;

bool primeiraLeitura = true;

// ESTADOS
// 0 = Monitorando
// 1 = Exibindo resultado
int estado = 0;

// MEDIR DISTANCIA
float medirDistancia() {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long duracao =
      pulseIn(echoPin, HIGH, 20000UL);

  if (duracao == 0) {
    return -1;
  }

  float distancia =
      duracao * velocidadeSom / 2.0;

  if (distancia < distanciaMinima ||
      distancia > distanciaMaxima) {
    return -1;
  }

  return distancia;
}

// MOSTRAR VELOCIDADE
void mostrarVelocidade(float v) {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("V: ");
  lcd.print(v, 2);
  lcd.print(" m/s");

  lcd.setCursor(0, 1);
  lcd.print("Km/h: ");
  lcd.print(v * 3.6, 2);
}

// CONFIGURACAO
void setup() {

  Serial.begin(115200);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  digitalWrite(trigPin, LOW);

  Wire.begin();

  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);

  lcd.setCursor(0, 0);
  lcd.print("MEDIDOR DE");

  lcd.setCursor(0, 1);
  lcd.print("VELOCIDADE");

  delay(1500);

  lcd.clear();
  lcd.print("Monitorando...");
}

// PROGRAMA
void loop() {

  unsigned long agora = micros();

  // ESTADO 1: EXIBIR VELOCIDADE POR 3 SEGUNDOS
  if (estado == 1) {

    if (millis() - inicioExibicao >= tempoExibicao) {

      estado = 0;
      primeiraLeitura = true;

      ultimaLeitura = micros();

      lcd.clear();
      lcd.print("Monitorando...");
    }

    return;
  }

  // CONTROLAR FREQUENCIA
  if (agora - ultimaLeitura < intervaloLeitura) {
    return;
  }

  ultimaLeitura = agora;

  // LER SENSOR
  distanciaAtual = medirDistancia();

  unsigned long instante = micros();

  // VERIFICAR OBJETO
  if (distanciaAtual < 0) {

    primeiraLeitura = true;

    return;
  }

  // PRIMEIRA LEITURA VALIDA
  if (primeiraLeitura) {

    distanciaAnterior = distanciaAtual;
    tempoAnterior = instante;

    primeiraLeitura = false;

    return;
  }

  // CALCULAR DIFERENCAS
  float deltaDistancia =
      distanciaAtual - distanciaAnterior;

  float deltaTempo =
      (instante - tempoAnterior) / 1000000.0;

  // VELOCIDADE
  if (deltaTempo > 0) {

    velocidade =
      (deltaDistancia / 100.0) / deltaTempo;
  }

  // ATUALIZAR LEITURAS
  distanciaAnterior = distanciaAtual;
  tempoAnterior = instante;

  // MONITOR SERIAL
  Serial.print("Distancia: ");
  Serial.print(distanciaAtual, 2);

  Serial.print(" cm | Velocidade: ");
  Serial.print(velocidade, 3);
  Serial.println(" m/s");

  // DETECTAR MOVIMENTO
  if (fabs(velocidade) >= velocidadeMinima) {

    velocidadeCapturada = fabs(velocidade);

    // MOSTRAR RESULTADO
    mostrarVelocidade(velocidadeCapturada);

    Serial.println("OBJETO DETECTADO!");

    Serial.print("Velocidade capturada: ");
    Serial.print(velocidadeCapturada, 3);
    Serial.println(" m/s");

    // INICIAR EXIBICAO
    inicioExibicao = millis();
    estado = 1;
  }
}
