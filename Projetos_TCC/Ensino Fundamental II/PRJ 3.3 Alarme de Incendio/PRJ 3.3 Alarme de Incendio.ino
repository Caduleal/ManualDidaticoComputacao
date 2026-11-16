/*
  Projeto 3.3 - Alarme de Incendio | Arduino Uno R3 / Tinkercad
  TMP36: A1 | Gas: A0 | LED: A2 | Piezo: D6
  LCD 16x2 I2C MCP23008: SDA/SCL, endereco 0x20 (32).

  A montagem original foi preservada por solicitacao do usuario.
  ATENCAO: o esquema nao une o negativo da protoboard ao GND do Uno,
  e o resistor de 4,7 kohms do gas termina em +5 V. O software nao
  corrige essas ligacoes: leituras e atuacao podem nao funcionar.
  Consulte as limitacoes e o roteiro de testes no README.md.
*/

#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <stdio.h>
#include <stdlib.h>

const byte PINO_GAS = A0;
const byte PINO_TEMPERATURA = A1;
const byte PINO_LED = A2;
const byte PINO_PIEZO = 6;
const byte ENDERECO_LCD = 0x20;

// O construtor recebe o deslocamento em relacao a 0x20.
// Deslocamento zero corresponde ao endereco confirmado: 0x20.
Adafruit_LiquidCrystal lcd(ENDERECO_LCD - 0x20);

// Valores iniciais didaticos, ajustaveis; nao representam calibracao.
const float TEMPERATURA_DISPARO_C = 50.0;
const float TEMPERATURA_RETORNO_C = 45.0;
const int GAS_DISPARO = 400;
const int GAS_RETORNO = 350;
const float TENSAO_REFERENCIA = 5.0;

const unsigned long INTERVALO_LEITURA_MS = 200;
const unsigned long INTERVALO_EXIBICAO_MS = 500;
const unsigned long INTERVALO_AVISO_MS = 250;
const unsigned int FREQUENCIA_PIEZO_HZ = 2000;

int leituraGas = 0;
int leituraTemperatura = 0;
float temperaturaC = 0.0;
bool alarmeGas = false;
bool alarmeTemperatura = false;
bool avisoLigado = false;
bool lcdDisponivel = false;
unsigned long ultimaLeitura = 0;
unsigned long ultimaExibicao = 0;
unsigned long ultimaAlternancia = 0;

void inicializarLCD() {
  Wire.begin();
#if defined(WIRE_HAS_TIMEOUT)
  // Evita espera indefinida se o barramento ficar preso, quando suportado.
  Wire.setWireTimeout(25000UL, true);
#endif
  Wire.beginTransmission(ENDERECO_LCD);
  lcdDisponivel = (Wire.endTransmission() == 0);

  if (lcdDisponivel) {
    // Nao depende do valor de retorno de begin(), que varia entre versoes.
    lcd.begin(16, 2);
    lcd.setBacklight(1);
  } else {
    Serial.println(F("LCD 0x20 sem resposta. Confira alimentacao e GND."));
  }
}

void lerSensores() {
  leituraGas = analogRead(PINO_GAS);
  leituraTemperatura = analogRead(PINO_TEMPERATURA);

  // TMP36: 500 mV em 0 graus C e incremento de 10 mV/grau C.
  const float tensao = leituraTemperatura * (TENSAO_REFERENCIA / 1023.0);
  temperaturaC = (tensao - 0.5) * 100.0;
}

void atualizarEstadoAlarme() {
  // Histerese: o limite de retorno e menor para evitar oscilacoes.
  if (temperaturaC >= TEMPERATURA_DISPARO_C) {
    alarmeTemperatura = true;
  } else if (temperaturaC <= TEMPERATURA_RETORNO_C) {
    alarmeTemperatura = false;
  }

  if (leituraGas >= GAS_DISPARO) {
    alarmeGas = true;
  } else if (leituraGas <= GAS_RETORNO) {
    alarmeGas = false;
  }
}

void aplicarAviso(bool ligar) {
  digitalWrite(PINO_LED, ligar ? HIGH : LOW);
  if (ligar) {
    tone(PINO_PIEZO, FREQUENCIA_PIEZO_HZ);
  } else {
    noTone(PINO_PIEZO);
  }
}

void atualizarAvisos(unsigned long agora) {
  static bool alarmeAnterior = false;
  const bool alarmeAtual = alarmeGas || alarmeTemperatura;

  if (alarmeAtual != alarmeAnterior) {
    // Comeca a sinalizar imediatamente quando o alarme dispara.
    avisoLigado = alarmeAtual;
    ultimaAlternancia = agora;
    aplicarAviso(avisoLigado);
    alarmeAnterior = alarmeAtual;
  }

  if (alarmeAtual && agora - ultimaAlternancia >= INTERVALO_AVISO_MS) {
    ultimaAlternancia = agora;
    avisoLigado = !avisoLigado;
    aplicarAviso(avisoLigado);
  }
}

const char* obterEstado() {
  if (alarmeGas && alarmeTemperatura) return "ALARME: GAS/TEMP";
  if (alarmeGas) return "ALARME: GAS";
  if (alarmeTemperatura) return "ALARME: TEMP";
  return "NORMAL";
}

void escreverLinhaLCD(byte linha, const char* texto) {
  lcd.setCursor(0, linha);
  byte coluna = 0;
  while (coluna < 16 && texto[coluna] != '\0') {
    lcd.print(texto[coluna]);
    ++coluna;
  }
  // Apaga caracteres antigos sem executar clear() a cada atualizacao.
  while (coluna < 16) {
    lcd.print(' ');
    ++coluna;
  }
}

void atualizarExibicao() {
  if (lcdDisponivel) {
    char textoTemperatura[10];
    char linha[17];
    // AVR nao habilita %f no snprintf por padrao; dtostrf faz a conversao.
    dtostrf(temperaturaC, 5, 1, textoTemperatura);
    snprintf(linha, sizeof(linha), "T:%s G:%4d", textoTemperatura, leituraGas);
    escreverLinhaLCD(0, linha);
    escreverLinhaLCD(1, obterEstado());
  }

  // Os valores brutos ajudam a diagnosticar a montagem original.
  Serial.print(F("A0="));
  Serial.print(leituraGas);
  Serial.print(F(" | A1="));
  Serial.print(leituraTemperatura);
  Serial.print(F(" | TMP36="));
  Serial.print(temperaturaC, 1);
  Serial.print(F(" C | "));
  Serial.println(obterEstado());
}

void setup() {
  pinMode(PINO_GAS, INPUT);
  pinMode(PINO_TEMPERATURA, INPUT);
  pinMode(PINO_LED, OUTPUT);
  pinMode(PINO_PIEZO, OUTPUT);
  aplicarAviso(false);
  Serial.begin(9600);
  Serial.println(F("Alarme 3.3: montagem original, sem alteracoes."));
  Serial.println(F("Verifique no README as limitacoes de GND e do divisor de gas."));
  inicializarLCD();

  lerSensores();
  atualizarEstadoAlarme();
  const unsigned long agora = millis();
  ultimaLeitura = agora;
  ultimaExibicao = agora;
  atualizarAvisos(agora);
  atualizarExibicao();
}

void loop() {
  const unsigned long agora = millis();

  // Subtracoes unsigned mantem a temporizacao valida apos o rollover.
  if (agora - ultimaLeitura >= INTERVALO_LEITURA_MS) {
    ultimaLeitura = agora;
    lerSensores();
    atualizarEstadoAlarme();
  }

  atualizarAvisos(agora);

  if (agora - ultimaExibicao >= INTERVALO_EXIBICAO_MS) {
    ultimaExibicao = agora;
    atualizarExibicao();
  }
}
