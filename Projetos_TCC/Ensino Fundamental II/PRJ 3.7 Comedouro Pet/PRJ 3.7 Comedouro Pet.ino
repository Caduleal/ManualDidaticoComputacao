#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>

const byte TRIG = 3, ECHO = 2, PINO_SERVO = 4, BOTAO = A0;
const byte LIMITE_PORCOES = 5;
const byte ANGULO_FECHADO = 0, ANGULO_ABERTO = 60;
const unsigned long TEMPO_ABERTO_MS = 1000;
const unsigned long INTERVALO_SENSOR_MS = 65;
const unsigned long AUSENCIA_MS = 350;
const float MARGEM_CM = 3.0; // Variacao em relacao ao fundo para indicar chegada.

Adafruit_LiquidCrystal lcd(0);
Servo tampa;
byte porcoes = 0;
bool confirmarReset = false;
unsigned long instanteReset = 0;
bool aberto = false, presente = false;
bool sensorPronto = false;
float fundoCm = 0;
unsigned long inicioCalibracao = 0, ultimoRetorno = 0;
unsigned long inicioAbertura = 0, ultimoDisparo = 0, ultimoEco = 0;

void mostrar() {
  lcd.clear();
  lcd.print("Porcoes: ");
  lcd.print(porcoes);
  lcd.print("/");
  lcd.print(LIMITE_PORCOES);
  lcd.setCursor(0, 1);
  if (confirmarReset) lcd.print("Contagem zerada");
  else if (!sensorPronto) lcd.print("Lendo o fundo");
  else if (aberto) lcd.print("Servindo...");
  else if (porcoes == LIMITE_PORCOES) lcd.print("Aperte o botao");
  else if (presente) lcd.print("Aguarde a saida");
  else lcd.print("Aguardando pet");
}

void verificarBotao() {
  static bool anterior = LOW, estavel = LOW;
  static unsigned long mudouEm = 0;
  bool leitura = digitalRead(BOTAO);
  unsigned long agora = millis();
  if (leitura != anterior) {
    anterior = leitura;
    mudouEm = agora;
  }
  if (leitura != estavel && agora - mudouEm >= 30) {
    estavel = leitura;
    if (estavel == HIGH) {
      porcoes = 0;
      instanteReset = agora;
      confirmarReset = true;
      mostrar();
    }
  }
}

void verificarPet() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  unsigned long pulso = pulseIn(ECHO, HIGH, 30000UL);
  float cm = pulso * 0.0343f / 2;
  unsigned long agora = millis();
  if (pulso) ultimoRetorno = agora;
  else if (agora - ultimoRetorno >= AUSENCIA_MS) fundoCm = 0;
  // Memoriza o fundo ao ligar e acompanha o alvo se ele for afastado.
  if ((!sensorPronto || !presente) && fundoCm > 0 && cm > fundoCm) fundoCm = cm;
  if (!sensorPronto) {
    if (pulso && fundoCm == 0) fundoCm = cm;
    if (agora - inicioCalibracao >= AUSENCIA_MS) {
      sensorPronto = true;
      mostrar();
    }
    return;
  }
  float margem = presente ? MARGEM_CM / 2 : MARGEM_CM;
  if (pulso && (fundoCm == 0 || fundoCm - cm >= margem)) {
    ultimoEco = agora;
    if (presente) return;
    presente = true;
    if (!aberto && porcoes < LIMITE_PORCOES) {
      confirmarReset = false;
      if (!tampa.attached()) tampa.attach(PINO_SERVO);
      tampa.write(ANGULO_ABERTO);
      inicioAbertura = agora;
      aberto = true;
      ++porcoes;
      mostrar();
    }
  } else if (presente && agora - ultimoEco >= AUSENCIA_MS) {
    presente = false;
    mostrar();
  }
}

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(BOTAO, INPUT); // Resistor externo para GND; pressionado = HIGH.
  // Manter o sinal em LOW, sem pulsos de servo, ate a primeira visita.
  digitalWrite(PINO_SERVO, LOW);
  pinMode(PINO_SERVO, OUTPUT);
  Wire.begin();
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  mostrar();
  inicioCalibracao = millis();
}

void loop() {
  unsigned long agora = millis();
  if (confirmarReset && agora - instanteReset >= 1000UL) {
    confirmarReset = false;
    mostrar();
  }
  if (aberto && agora - inicioAbertura >= TEMPO_ABERTO_MS) {
    tampa.write(ANGULO_FECHADO);
    aberto = false;
    mostrar();
  }
  verificarBotao();
  if (agora - ultimoDisparo >= INTERVALO_SENSOR_MS) {
    ultimoDisparo = agora;
    verificarPet();
  }
}
