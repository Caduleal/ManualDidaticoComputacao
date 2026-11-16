#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <math.h>

Adafruit_LiquidCrystal lcd(0);
const byte trigPin[] = {3, 4};
const byte echoPin[] = {2, 5};
const float velocidadeSom = 0.0343;
const float distanciaMinima = 2.0;
const float distanciaMaxima = 300.0;
const float velocidadeMinima = 0.10;

const unsigned long intervaloLeitura = 30000UL;
const unsigned long pausaEntreMovimentos = 800UL;
const unsigned long tempoExibicao = 3000UL;

float distanciaAnterior[2];
unsigned long tempoAnterior[2];
bool primeiraLeitura[] = {true, true};
byte sensor = 0;
unsigned long ultimaLeitura = 0;
unsigned long ultimoMovimento = 0;
unsigned long inicioExibicao = 0;
unsigned long pessoas = 0;
enum Estado { LIVRE, ESPERA_S1, ESPERA_S2, FINALIZADA };
Estado estado = LIVRE;
unsigned long inicioSequencia = 0;
const unsigned long prazoSequencia = 20000UL;
bool exibindo = false;
float medirDistancia(byte i) {
  digitalWrite(trigPin[i], LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin[i], HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin[i], LOW);
  unsigned long duracao = pulseIn(echoPin[i], HIGH, 20000UL);
  float distancia = duracao * velocidadeSom / 2.0;
  if (duracao == 0 || distancia < distanciaMinima || distancia > distanciaMaxima) {
    return -1;
  }
  return distancia;
}

void mostrarTotal(const char* mensagem) {
  lcd.clear();
  lcd.print("Total:");
  lcd.print(pessoas);
  lcd.setCursor(0, 1);
  lcd.print(mensagem);
}

void registrarAproximacao(byte i) {
  ultimoMovimento = millis();
  if (estado == LIVRE) {
    inicioSequencia = ultimoMovimento;
    estado = (i == 0) ? ESPERA_S2 : ESPERA_S1;
    exibindo = false;
    mostrarTotal(i == 0 ? "Aguardando S2" : "Aguardando S1");
  } else if (estado == ESPERA_S2 && i == 1) {
    ++pessoas;
    mostrarTotal("Entrada");
    estado = FINALIZADA;
  } else if (estado == ESPERA_S1 && i == 0) {
    if (pessoas > 0) --pessoas;
    mostrarTotal("Saida");
    estado = FINALIZADA;
  } else {
    return;
  }
  if (estado == FINALIZADA) {
    exibindo = true;
    inicioExibicao = ultimoMovimento;
  }
}

void verificarMovimento(byte i, float distancia) {
  if (distancia < 0) {
    primeiraLeitura[i] = true;
    return;
  }

  unsigned long instante = micros();
  if (!primeiraLeitura[i]) {
    float segundos = (instante - tempoAnterior[i]) / 1000000.0;
    if (segundos > 0) {
      float velocidade = ((distancia - distanciaAnterior[i]) / 100.0) / segundos;
      Serial.print("DIST");
      Serial.print(i + 1);
      Serial.print(" | cm: ");
      Serial.print(distancia, 2);
      Serial.print(" | m/s: ");
      Serial.println(velocidade, 3);

      if (velocidade < 0 && fabs(velocidade) >= velocidadeMinima) {
        registrarAproximacao(i);
      }
    }
  }
  primeiraLeitura[i] = false;
  distanciaAnterior[i] = distancia;
  tempoAnterior[i] = instante;
}
void setup() {
  Serial.begin(115200);
  for (byte i = 0; i < 2; ++i) {
    pinMode(trigPin[i], OUTPUT);
    pinMode(echoPin[i], INPUT);
    digitalWrite(trigPin[i], LOW);
  }
  Wire.begin();
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  mostrarTotal("Monitorando...");
}
void loop() {
  unsigned long agoraMs = millis();
  if (estado == FINALIZADA && agoraMs - ultimoMovimento >= pausaEntreMovimentos) {
    estado = LIVRE;
  }
  if ((estado == ESPERA_S1 || estado == ESPERA_S2) && agoraMs - inicioSequencia >= prazoSequencia) {
    estado = LIVRE;
    mostrarTotal("Monitorando...");
  }
  if (exibindo && agoraMs - inicioExibicao >= tempoExibicao) {
    exibindo = false;
    mostrarTotal("Monitorando...");
  }

  unsigned long agora = micros();
  if (agora - ultimaLeitura < intervaloLeitura) return;
  ultimaLeitura = agora;
  verificarMovimento(sensor, medirDistancia(sensor));
  sensor = 1 - sensor;
}

