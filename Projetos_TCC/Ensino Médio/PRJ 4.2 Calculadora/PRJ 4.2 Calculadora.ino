#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

// =======================================
// CONFIGURACAO DO LCD
// =======================================

Adafruit_LiquidCrystal lcd(0);

// =======================================
// CONFIGURACAO DO TECLADO 4X4
// =======================================

const byte linhas[4] = {A0, A1, A2, A3};
const byte colunas[4] = {2, 3, 4, 5};

char teclas[4][4] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

// =======================================
// VARIAVEIS DA CALCULADORA
// =======================================

String numero1 = "";
String numero2 = "";

char operacao = '\0';

bool resultadoPronto = false;

// =======================================
// INICIALIZACAO
// =======================================

void setup() {

  // Inicializa o LCD
  lcd.begin(16, 2);
  lcd.setBacklight(1);
  lcd.clear();

  // Configura as linhas como saidas
  for (int i = 0; i < 4; i++) {
    pinMode(linhas[i], OUTPUT);
    digitalWrite(linhas[i], HIGH);
  }

  // Configura colunas como entradas
  for (int i = 0; i < 4; i++) {
    pinMode(colunas[i], INPUT_PULLUP);
  }

  limparCalculadora();
}

// =======================================
// FUNCAO PARA LER O TECLADO
// =======================================

char lerTeclado() {

  for (int i = 0; i < 4; i++) {

    digitalWrite(linhas[i], LOW);
    delayMicroseconds(10);

    for (int j = 0; j < 4; j++) {

      if (digitalRead(colunas[j]) == LOW) {
        digitalWrite(linhas[i], HIGH);
        return teclas[i][j];
      }
    }

    digitalWrite(linhas[i], HIGH);
  }

  return '\0';
}

// =======================================
// LIMPAR CALCULADORA
// =======================================

void limparCalculadora() {

  numero1 = "";
  numero2 = "";
  operacao = '\0';
  resultadoPronto = false;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("CALCULADORA");

  lcd.setCursor(0, 1);
  lcd.print("Digite um numero");
}

// =======================================
// ATUALIZAR LCD
// =======================================

void atualizarLCD() {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print(numero1);

  if (operacao != '\0') {
    lcd.print(operacao);
    lcd.print(numero2);
  }

  lcd.setCursor(0, 1);
  lcd.print("A+ B- C* D/");
}

// =======================================
// CALCULAR RESULTADO
// =======================================

void calcular() {

  // Verifica se existem dados suficientes
  if (numero1.length() == 0 ||
      numero2.length() == 0 ||
      operacao == '\0') {

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Dados invalidos");
    delay(1000);
    atualizarLCD();
    return;
  }

  float a = numero1.toFloat();
  float b = numero2.toFloat();
  float resultado = 0;

  // Verifica divisao por zero
  if (operacao == '/' && b == 0) {

    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("ERRO");

    lcd.setCursor(0, 1);
    lcd.print("Divisao por zero");

    resultadoPronto = true;
    return;
  }

  // Seleciona a operacao matematica
  switch (operacao) {

    case '+':
      resultado = a + b;
      break;

    case '-':
      resultado = a - b;
      break;

    case '*':
      resultado = a * b;
      break;

    case '/':
      resultado = a / b;
      break;
  }

  // Mostra a operacao e o resultado
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print(numero1);
  lcd.print(operacao);
  lcd.print(numero2);

  lcd.setCursor(0, 1);
  lcd.print("= ");
  lcd.print(resultado, 2);

  resultadoPronto = true;
}

// =======================================
// LOOP PRINCIPAL
// =======================================

void loop() {

  // Ler tecla pressionada
  char tecla = lerTeclado();

  // Nenhuma tecla pressionada
  if (tecla == '\0') {
    return;
  }

  // Eliminar ruido do botao
  delay(30);

  if (lerTeclado() != tecla) {
    return;
  }

  // Esperar soltar o botao
  while (lerTeclado() != '\0') {
    delay(10);
  }

  delay(30);

  // =====================================
  // TECLA * : LIMPAR
  // =====================================

  if (tecla == '*') {
    limparCalculadora();
    return;
  }

  // =====================================
  // TECLAS NUMERICAS
  // =====================================

  if (tecla >= '0' && tecla <= '9') {

    // Comecar novo calculo
    if (resultadoPronto) {
      numero1 = "";
      numero2 = "";
      operacao = '\0';
      resultadoPronto = false;
    }

    // Primeiro numero
    if (operacao == '\0') {

      if (numero1.length() < 7) {
        numero1 += tecla;
      }

    } else {

      // Segundo numero
      if (numero2.length() < 7) {
        numero2 += tecla;
      }
    }

    atualizarLCD();
    return;
  }

  // =====================================
  // TECLAS DAS OPERACOES
  // =====================================

  if (tecla == 'A' ||
      tecla == 'B' ||
      tecla == 'C' ||
      tecla == 'D') {

    // Precisa existir primeiro numero
    if (numero1.length() == 0 ||
        numero2.length() > 0 ||
        resultadoPronto) {
      return;
    }

    if (tecla == 'A') {
      operacao = '+';
    }

    if (tecla == 'B') {
      operacao = '-';
    }

    if (tecla == 'C') {
      operacao = '*';
    }

    if (tecla == 'D') {
      operacao = '/';
    }

    atualizarLCD();
    return;
  }

  // =====================================
  // TECLA # : CALCULAR
  // =====================================

  if (tecla == '#') {

    if (!resultadoPronto) {
      calcular();
    }

    return;
  }
}