
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

// ===== LCD I2C =====
Adafruit_LiquidCrystal lcd(0);

// ===== PINOS =====
const int sensorPin = A0;

const int ledVermelho = 2;
const int ledAzul = 3;
const int ledVerde = 4;

float temperatura = 0;

// ===== SIMBOLO DE GRAU PERSONALIZADO =====
byte simboloGrau[8] = {
  B00110,
  B01001,
  B01001,
  B00110,
  B00000,
  B00000,
  B00000,
  B00000
};

// ===== CONTROLE DO LED RGB =====
void controlarLED(bool vermelho, bool verde, bool azul) {
  digitalWrite(ledVermelho, vermelho ? HIGH : LOW);
  digitalWrite(ledVerde, verde ? HIGH : LOW);
  digitalWrite(ledAzul, azul ? HIGH : LOW);
}

void setup() {

  // Inicializa o Monitor Serial
  Serial.begin(9600);

  // Configuracao dos LEDs
  pinMode(ledVermelho, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAzul, OUTPUT);

  controlarLED(false, false, false);

  // ===== INICIALIZACAO DO LCD =====
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);

  // Cria o simbolo de grau na posicao 0
  lcd.createChar(0, simboloGrau);

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("TERMOMETRO");

  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");

  Serial.println("Sistema iniciado!");

  delay(2000);
  lcd.clear();
}

void loop() {

  // ===== LEITURA DA TEMPERATURA =====
  int leitura = analogRead(sensorPin);

  float tensao = leitura * (5.0 / 1023.0);

  // Conversao para graus Celsius (TMP36)
  temperatura = (tensao - 0.5) * 100.0;

  const char* cor;
  const char* estado;

  // ===== MAQUINA DE ESTADOS =====

  if (temperatura < 20.0) {

    // ESTADO FRIO - LED AZUL
    controlarLED(false, false, true);

    cor = "AZUL";
    estado = "FRIO";

  }
  else if (temperatura <= 30.0) {

    // ESTADO NORMAL - LED AMARELO
    controlarLED(true, true, false);

    cor = "AMARELO";
    estado = "NORMAL";

  }
  else {

    // ESTADO QUENTE - LED VERMELHO
    controlarLED(true, false, false);

    cor = "VERMELHO";
    estado = "QUENTE";
  }

  // ===== MONITOR SERIAL =====
  Serial.print("Temperatura: ");
  Serial.print(temperatura, 1);
  Serial.print(" C | Estado: ");
  Serial.print(estado);
  Serial.print(" | LED: ");
  Serial.println(cor);

  // ===== DISPLAY LCD =====

  // Primeira linha: Temperatura
  lcd.setCursor(0, 0);
  lcd.print("                ");

  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperatura, 1);

  // Exibe o simbolo de grau personalizado
  lcd.write((byte)0);
  lcd.print("C");

  // Segunda linha: Estado
  lcd.setCursor(0, 1);
  lcd.print("                ");

  lcd.setCursor(0, 1);
  lcd.print("Sensacao: ");
  lcd.print(estado);

  // Atualiza a cada 1 segundo
  delay(1000);
}
