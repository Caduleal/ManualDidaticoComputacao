
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
// BUZZER
// =======================================

const int buzzer = 6;

// =======================================
// CONTADORES
// =======================================

int votosCadu = 0;
int votosAna = 0;
int votosBrancos = 0;
int votosNulos = 0;
int totalVotos = 0;

String numero = "";
bool encerrada = false;

// =======================================
// SONS
// =======================================

void somTecla() {
  tone(buzzer, 1200, 70);
  delay(90);
}

void somCorrecao() {
  tone(buzzer, 700, 100);
  delay(150);
  tone(buzzer, 700, 100);
  delay(150);
}

void somConfirmacao() {
  tone(buzzer, 1000, 150);
  delay(180);
  tone(buzzer, 1500, 400);
  delay(450);
}

// =======================================
// FUNCAO PARA LER O TECLADO
// MESMA LOGICA DA CALCULADORA
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
// TELA PARA PROXIMO ELEITOR
// =======================================

void mostrarInicio() {

  numero = "";

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Digite seu voto");

  lcd.setCursor(0, 1);
  lcd.print("Numero: ");
}

// =======================================
// MOSTRAR CONTAGEM NO SERIAL
// =======================================

void mostrarContagem() {

  Serial.println("--------------------");

  Serial.print("Cadu: ");
  Serial.println(votosCadu);

  Serial.print("Ana: ");
  Serial.println(votosAna);

  Serial.print("Brancos: ");
  Serial.println(votosBrancos);

  Serial.print("Nulos: ");
  Serial.println(votosNulos);

  Serial.print("Total: ");
  Serial.println(totalVotos);

  Serial.println("--------------------");
}

// =======================================
// REGISTRAR VOTO
// =======================================

void registrarVoto() {

  lcd.clear();

  if (numero == "20") {

    votosCadu++;
    lcd.print("Voto: CADU");
    Serial.println("Voto registrado: CADU");

  } else if (numero == "10") {

    votosAna++;
    lcd.print("Voto: ANA");
    Serial.println("Voto registrado: ANA");

  } else if (numero == "A") {

    votosBrancos++;
    lcd.print("Voto BRANCO");
    Serial.println("Voto registrado: BRANCO");

  } else {

    // 00 e outros numeros invalidos
    votosNulos++;
    lcd.print("Voto NULO");
    Serial.println("Voto registrado: NULO");
  }

  totalVotos++;

  lcd.setCursor(0, 1);
  lcd.print("CONFIRMADO!");

  somConfirmacao();

  mostrarContagem();

  delay(1000);

  mostrarInicio();
}

// =======================================
// ENCERRAR VOTACAO
// =======================================

void apurarVotos() {

  encerrada = true;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("VOTACAO");

  lcd.setCursor(0, 1);
  lcd.print("ENCERRADA!");

  tone(buzzer, 900, 300);

  Serial.println();
  Serial.println("===== RESULTADO FINAL =====");

  mostrarContagem();

  delay(2000);
}

// =======================================
// MOSTRAR PORCENTAGENS
// =======================================

void mostrarResultados() {

  float pCadu = 0;
  float pAna = 0;
  float pBranco = 0;
  float pNulo = 0;

  if (totalVotos > 0) {

    pCadu = votosCadu * 100.0 / totalVotos;
    pAna = votosAna * 100.0 / totalVotos;
    pBranco = votosBrancos * 100.0 / totalVotos;
    pNulo = votosNulos * 100.0 / totalVotos;
  }

  // CANDIDATOS
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("CADU: ");
  lcd.print(pCadu, 1);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("ANA: ");
  lcd.print(pAna, 1);
  lcd.print("%");

  delay(3000);

  // BRANCOS E NULOS
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("BRANCO: ");
  lcd.print(pBranco, 1);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("NULO: ");
  lcd.print(pNulo, 1);
  lcd.print("%");

  delay(3000);
}

// =======================================
// INICIALIZACAO
// =======================================

void setup() {

  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.setBacklight(1);
  lcd.clear();

  pinMode(buzzer, OUTPUT);

  // MESMA CONFIGURACAO DA CALCULADORA

  for (int i = 0; i < 4; i++) {
    pinMode(linhas[i], OUTPUT);
    digitalWrite(linhas[i], HIGH);
  }

  for (int i = 0; i < 4; i++) {
    pinMode(colunas[i], INPUT_PULLUP);
  }

  // ZERESIMA
  lcd.setCursor(0, 0);
  lcd.print("Cadu:0  Ana:0");

  lcd.setCursor(0, 1);
  lcd.print("Total votos: 0");

  Serial.println("=== URNA ELETRONICA ===");

  mostrarContagem();

  delay(3000);

  mostrarInicio();
}

// =======================================
// LOOP PRINCIPAL
// MESMA LEITURA DA CALCULADORA
// =======================================

void loop() {

  // Votacao encerrada
  if (encerrada) {
    mostrarResultados();
    return;
  }

  // Ler tecla
  char tecla = lerTeclado();

  if (tecla == '\0') {
    return;
  }

  // Eliminar ruido
  delay(30);

  if (lerTeclado() != tecla) {
    return;
  }

  // Esperar soltar a tecla
  while (lerTeclado() != '\0') {
    delay(10);
  }

  delay(30);

  // =====================================
  // TECLA D - ENCERRAR
  // =====================================

  if (tecla == 'D') {

    // Evita encerrar com numero incompleto
    if (numero.length() > 0) {
      lcd.clear();
      lcd.print("Corrija ou");
      lcd.setCursor(0, 1);
      lcd.print("confirme voto");
      delay(1200);
      mostrarInicio();
      return;
    }

    // Exige pelo menos um voto
    if (totalVotos == 0) {
      lcd.clear();
      lcd.print("Nenhum voto!");
      delay(1200);
      mostrarInicio();
      return;
    }

    apurarVotos();
    return;
  }

  // =====================================
  // TECLA * - CORRIGIR
  // =====================================

  if (tecla == '*') {

    somCorrecao();
    mostrarInicio();
    return;
  }

  // =====================================
  // TECLA # - CONFIRMAR
  // =====================================

  if (tecla == '#') {

    if (numero.length() > 0) {
      registrarVoto();
    }

    return;
  }

  // =====================================
  // TECLA A - VOTO BRANCO
  // =====================================

  if (tecla == 'A') {

    somTecla();

    numero = "A";

    lcd.setCursor(8, 1);
    lcd.print("BRANCO  ");

    return;
  }

  // =====================================
  // TECLAS NUMERICAS
  // =====================================

  if (tecla >= '0' && tecla <= '9') {

    if (numero == "A") {
      numero = "";
    }

    if (numero.length() < 2) {

      numero += tecla;

      somTecla();

      lcd.setCursor(8, 1);
      lcd.print("        ");

      lcd.setCursor(8, 1);
      lcd.print(numero);
    }

    return;
  }
}