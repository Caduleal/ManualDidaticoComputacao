
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>

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
// CONFIGURACAO DO SERVO MOTOR
// =======================================

Servo servoCofre;

const int servoPin = 13;

const int posicaoFechado = 0;
const int posicaoAberto = 90;

bool cofreAberto = false;

// =======================================
// CONFIGURACAO DA SENHA
// =======================================

String senhaCorreta = "1234";
String senhaDigitada = "";

// =======================================
// INICIALIZACAO
// =======================================

void setup() {

  // Inicializa o LCD
  lcd.begin(16, 2);
  lcd.setBacklight(1);
  lcd.clear();

  // Configura as linhas do teclado
  for (int i = 0; i < 4; i++) {
    pinMode(linhas[i], OUTPUT);
    digitalWrite(linhas[i], HIGH);
  }

  // Configura as colunas do teclado
  for (int i = 0; i < 4; i++) {
    pinMode(colunas[i], INPUT_PULLUP);
  }

  // Inicializa o servo motor
  servoCofre.attach(servoPin);

  // Cofre inicia fechado
  servoCofre.write(posicaoFechado);

  mostrarTelaInicial();
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
// MOSTRAR TELA INICIAL
// =======================================

void mostrarTelaInicial() {

  senhaDigitada = "";

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("COFRE DIGITAL");

  lcd.setCursor(0, 1);
  lcd.print("Digite a senha");
}

// =======================================
// ATUALIZAR SENHA NO LCD
// =======================================

void atualizarLCD() {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("DIGITE A SENHA:");

  lcd.setCursor(0, 1);

  // Mostra asteriscos no lugar dos numeros
  for (int i = 0; i < senhaDigitada.length(); i++) {
    lcd.print("*");
  }
}

// =======================================
// ABRIR COFRE
// =======================================

void abrirCofre() {

  servoCofre.write(posicaoAberto);

  cofreAberto = true;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("ACESSO LIBERADO");

  lcd.setCursor(0, 1);
  lcd.print("COFRE ABERTO");

  senhaDigitada = "";
}

// =======================================
// FECHAR COFRE
// =======================================

void fecharCofre() {

  servoCofre.write(posicaoFechado);

  cofreAberto = false;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("COFRE FECHADO");

  lcd.setCursor(0, 1);
  lcd.print("Aguarde...");

  delay(1500);

  mostrarTelaInicial();
}

// =======================================
// VERIFICAR SENHA
// =======================================

void verificarSenha() {

  if (cofreAberto) {
    return;
  }

  if (senhaDigitada == senhaCorreta) {

    abrirCofre();

  } else {

    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("SENHA INVALIDA");

    lcd.setCursor(0, 1);
    lcd.print("TENTE NOVAMENTE");

    delay(2000);

    mostrarTelaInicial();
  }
}

// =======================================
// LOOP PRINCIPAL
// =======================================

void loop() {

  // Leitura do teclado
  char tecla = lerTeclado();

  if (tecla == '\0') {
    return;
  }

  // Elimina ruido do botao
  delay(30);

  if (lerTeclado() != tecla) {
    return;
  }

  // Espera soltar o botao
  while (lerTeclado() != '\0') {
    delay(10);
  }

  delay(30);

  // =====================================
  // TECLA A : FECHAR COFRE
  // =====================================

  if (tecla == 'A') {

    fecharCofre();
    return;
  }

  // =====================================
  // TECLA * : LIMPAR SENHA
  // =====================================

  if (tecla == '*') {

    if (!cofreAberto) {
      mostrarTelaInicial();
    }

    return;
  }

  // =====================================
  // TECLAS NUMERICAS
  // =====================================

  if (tecla >= '0' && tecla <= '9') {

    if (!cofreAberto) {

      if (senhaDigitada.length() < 8) {
        senhaDigitada += tecla;
      }

      atualizarLCD();
    }

    return;
  }

  // =====================================
  // TECLA D : CONFIRMAR SENHA
  // =====================================

  if (tecla == 'D') {

    verificarSenha();
    return;
  }
}
