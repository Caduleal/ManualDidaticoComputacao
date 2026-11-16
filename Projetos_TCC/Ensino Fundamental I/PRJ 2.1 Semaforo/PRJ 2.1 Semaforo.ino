// ==========================
// Pinos Arduino
// ==========================

const int LED_VERMELHO = 11;
const int LED_AMARELO = 12;
const int LED_VERDE = 13;

void setup() {
  // Configura os pinos dos LEDs como saídas digitais
  pinMode(LED_VERMELHO, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
}

void loop() {
  // Estado 1: Vermelho aceso (Pare)
  digitalWrite(LED_VERMELHO, HIGH);
  digitalWrite(LED_AMARELO, LOW);
  digitalWrite(LED_VERDE, LOW);
  delay(5000); // Mantém por 3 segundos

  // Estado 2: Verde aceso (Siga)
  digitalWrite(LED_VERMELHO, LOW);
  digitalWrite(LED_AMARELO, LOW);
  digitalWrite(LED_VERDE, HIGH);
  delay(5000); // Mantém por 3 segundos

  // Estado 3: Amarelo aceso (Atenção)
  digitalWrite(LED_VERMELHO, LOW);
  digitalWrite(LED_AMARELO, HIGH);
  digitalWrite(LED_VERDE, LOW);
  delay(3000); // Mantém por 1 segundo
}