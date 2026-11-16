#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>

Adafruit_LiquidCrystal lcd(0);
Servo cancela;
const byte TRIG[] = {3, 4};
const byte ECHO[] = {2, 5};
const byte SERVO = 6, BUZZER = 7, LED = 8;
const byte CAPACIDADE = 10;
const byte FECHADA = 0, ABERTA = 90;
const int DETECTAR_CM = 100, LIBERAR_CM = 115;
const unsigned long INTERVALO_MS = 65;
const unsigned long TEMPO_DESISTENCIA_MS = 8000;
const unsigned long TEMPO_LIBERACAO_MS = 1000;

enum Estado { PRONTO, ENTRANDO, SAINDO, CONFIRMADO, LOTADO };
Estado estado = PRONTO;
byte ocupadas = 0;
bool presente[2] = {};
bool livre[2] = {};
byte pertoSeguido[2] = {};
byte longeSeguido[2] = {};
byte sensor = 0;
unsigned long ultimoDisparo = 0, inicioLivre = 0;
bool contandoTempoLivre = false;

void mostrar(const char* mensagem) {
  lcd.clear();
  lcd.print("Vagas: ");
  lcd.print(CAPACIDADE - ocupadas);
  lcd.print("/");
  lcd.print(CAPACIDADE);
  lcd.setCursor(0, 1);
  lcd.print(mensagem);
}
// Retorna true apenas quando um carro acaba de chegar ao sensor.
bool detectarChegada(byte i) {
  digitalWrite(TRIG[i], LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG[i], HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG[i], LOW);
  unsigned long eco = pulseIn(ECHO[i], HIGH, 25000UL);
  float cm = eco * 0.0343f / 2;
  bool perto = eco > 0 && cm >= 2 && cm < DETECTAR_CM;
  bool longe = cm >= LIBERAR_CM && cm <= 400;
  if (!perto) pertoSeguido[i] = 0;
  else if (pertoSeguido[i] < 2) ++pertoSeguido[i];
  if (!longe) longeSeguido[i] = 0;
  else if (longeSeguido[i] < 2) ++longeSeguido[i];
  livre[i] = longeSeguido[i] == 2;
  if (livre[i]) presente[i] = false;
  if (!presente[i] && pertoSeguido[i] == 2) {
    presente[i] = true;
    return true;
  }
  return false;
}

void registrar(byte i) {
  if (estado == PRONTO) {
    if (i == 0 && ocupadas == CAPACIDADE) {
      estado = LOTADO;
      mostrar("Lotado");
      return;
    }
    estado = i == 0 ? ENTRANDO : SAINDO;
    cancela.write(ABERTA);
    mostrar(i == 0 ? "Aguardando S2" : "Aguardando S1");
  } else if (estado == ENTRANDO && i == 1) {
    ++ocupadas;
    estado = CONFIRMADO;
    mostrar("Carro entrou");
  } else if (estado == SAINDO && i == 0) {
    if (ocupadas > 0) --ocupadas;
    estado = CONFIRMADO;
    mostrar("Carro saiu");
  }
}

void verificarLiberacao(unsigned long agora) {
  if (estado == PRONTO || !livre[0] || !livre[1]) {
    contandoTempoLivre = false;
    return;
  }
  if (!contandoTempoLivre) {
    inicioLivre = agora;
    contandoTempoLivre = true;
  }
  bool aguardando = estado == ENTRANDO || estado == SAINDO;
  unsigned long espera = aguardando ? TEMPO_DESISTENCIA_MS : TEMPO_LIBERACAO_MS;
  if (agora - inicioLivre >= espera) {
    cancela.write(FECHADA);
    estado = PRONTO;
    contandoTempoLivre = false;
    mostrar(ocupadas == CAPACIDADE ? "Lotado" : "Aguardando carro");
  }
}

void atualizarAlerta(unsigned long agora) {
  static bool ligado = false;
  bool aberto = estado == ENTRANDO || estado == SAINDO || estado == CONFIRMADO;
  bool pulso = aberto && (agora / 150UL) % 2 == 0;
  if (pulso == ligado) return;
  ligado = pulso;
  digitalWrite(LED, ligado ? HIGH : LOW);
  if (ligado) tone(BUZZER, 1200);
  else noTone(BUZZER);
}

void setup() {
  for (byte i = 0; i < 2; ++i) {
    pinMode(TRIG[i], OUTPUT);
    pinMode(ECHO[i], INPUT);
    digitalWrite(TRIG[i], LOW);
  }
  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  cancela.attach(SERVO);
  cancela.write(FECHADA);
  Wire.begin();
  Serial.begin(9600);
  Wire.beginTransmission(0x20);
  if (Wire.endTransmission() == 0) {
    Serial.println("LCD: resposta I2C em 0x20");
  } else {
    Serial.println("LCD: sem resposta I2C em 0x20");
  }
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  mostrar("Aguardando carro");
}

void loop() {
  unsigned long agora = millis();
  if (agora - ultimoDisparo >= INTERVALO_MS) {
    ultimoDisparo = agora;
    if (detectarChegada(sensor)) registrar(sensor);
    sensor = 1 - sensor;
    verificarLiberacao(millis());
  }
  atualizarAlerta(millis());
}
