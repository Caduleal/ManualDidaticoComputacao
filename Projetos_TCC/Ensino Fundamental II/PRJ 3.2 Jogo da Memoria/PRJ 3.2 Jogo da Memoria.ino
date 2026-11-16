#define MAX_NIVEL 100
// ==========================
// Pinos Arduino
// ==========================
const uint8_t LED_VERMELHO = 5;
const uint8_t BOTAO_VERMELHO = 8;

const uint8_t LED_AMARELO = 4;
const uint8_t BOTAO_AMARELO = 9;

const uint8_t LED_AZUL = 3;
const uint8_t BOTAO_AZUL = 10;

const uint8_t LED_VERDE = 2;
const uint8_t BOTAO_VERDE = 11;

const uint8_t BUZZER_PIN = 12;

// ==========================
// Arrays de Hardware
// ==========================
const uint8_t leds[] = {LED_VERMELHO, LED_AMARELO, LED_AZUL, LED_VERDE};
const uint8_t botoes[] = {BOTAO_VERMELHO, BOTAO_AMARELO, BOTAO_AZUL, BOTAO_VERDE};
const uint8_t numPares = 4;

const uint16_t simonTones[] = {262, 330, 392, 523};
const uint8_t failTone = 150;

uint8_t filaOriginal[MAX_NIVEL];
uint16_t nivel = 1;

bool jogoInciado = false;

// ==========================
// Abstração de Hardware
// ==========================
void ligarLed(uint8_t pino) {
  digitalWrite(pino, HIGH); // Todos os LEDs acendem em HIGH
}

void desligarLed(uint8_t pino) {
  digitalWrite(pino, LOW);  // Todos os LEDs apagam em LOW
}

// ==========================
// Setup
// ==========================
void setup() {
  Serial.begin(9600);

  for (uint8_t i = 0; i < numPares; i++) {
    pinMode(leds[i], OUTPUT);
    // Configura como INPUT comum para respeitar os resistores de pull-down externos
    pinMode(botoes[i], INPUT); 
    
    // Força estado inicial desligado
    desligarLed(leds[i]); 
  }
}

void gameOver() {
  tone(BUZZER_PIN, failTone);
  
  for (int i = 0; i < 3; i++) {
    // Acende todos os LEDs simultaneamente, respeitando a lógica individual
    for (int j = 0; j < numPares; j++) {
      ligarLed(leds[j]);
    }
    delay(150);
    
    // Apaga todos os LEDs
    for (int j = 0; j < numPares; j++) {
      desligarLed(leds[j]);
    }
    delay(150);
  }
  
  noTone(BUZZER_PIN);
  delay(1000);

  nivel = 1;
  jogoInciado = false;
  memset(filaOriginal, 0, sizeof(filaOriginal));
}

void start() {
  for (int j = 0; j < 3; j++) {
    for (int i = 0; i < numPares; i++) {
      ligarLed(leds[i]);
      tone(BUZZER_PIN, simonTones[i]);
      delay(50);
      
      desligarLed(leds[i]);
      noTone(BUZZER_PIN);
      delay(50);
    }
    delay(700);
  }
}

int espelharBotoesNosLeds() {
  for (int i = 0; i < numPares; i++) { 
    int estadoBotao = digitalRead(botoes[i]);
    
    // Validação Active-High para os botões via resistores de pull-down
    if (estadoBotao == HIGH) { 
      ligarLed(leds[i]);
      tone(BUZZER_PIN, simonTones[i]);
      return i;
    } else {
      desligarLed(leds[i]); 
      noTone(BUZZER_PIN);
    }
  }
  return -1;
}

void reproduzirSequencia(){
    for(uint16_t i = 0; i < nivel; i++){
        uint8_t indice = filaOriginal[i];
    
      ligarLed(leds[indice]);
      tone(BUZZER_PIN, simonTones[indice]);
      delay(300);

      desligarLed(leds[indice]);
      noTone(BUZZER_PIN);
      delay(250);
    }

}

// ==========================
// Loop Principal
// ==========================
void loop() {
    if (jogoInciado == false){
        start();
        randomSeed(analogRead(A0));
        jogoInciado = true;
        delay(500);
    }
    filaOriginal[nivel - 1] = random(0,numPares);
    reproduzirSequencia();
    delay(100);
    Serial.print("Fila atual (Nivel ");
    Serial.print(nivel);
    Serial.print("): ");
    for (uint16_t i = 0; i < nivel; i++) {
        Serial.print(filaOriginal[i]);
        Serial.print(" ");
    }
    Serial.println(); // Quebra de linha após a leitura do array
    
    for(uint16_t i = 0; i < nivel; i++){
        int botaoPressionado = -1;
        while (botaoPressionado == -1){
            botaoPressionado = espelharBotoesNosLeds();
        }
        Serial.print("Posicao ");
        Serial.print(i);
        Serial.print(" | Digitado: ");
        Serial.println(botaoPressionado);

        if (botaoPressionado != filaOriginal[i]){
            Serial.println("-> Erro: Game Over");
            gameOver();
            return;
        }
        while(espelharBotoesNosLeds() != -1){
            delay(10);
        }
    }
    Serial.println("-> Sequencia correta. Proximo nivel.");
    nivel++;
    delay(2000);
}