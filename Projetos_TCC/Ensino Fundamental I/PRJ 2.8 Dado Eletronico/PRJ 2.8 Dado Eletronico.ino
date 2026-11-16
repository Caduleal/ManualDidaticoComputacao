const byte PINO_BOTAO = A0;

// Pinos dos segmentos na ordem a, b, c, d, e, f, g.
const byte PINOS_SEGMENTOS[] = {6, 5, 4, 2, 3, 1, 0};

// Display de ânodo comum: um bit 0 acende o segmento.
// O índice de cada padrão corresponde ao número exibido.
const byte DIGITOS[] = {
  0x40,  // 0
  0x79,  // 1
  0x24,  // 2
  0x30,  // 3
  0x19,  // 4
  0x12,  // 5
  0x02   // 6
};

// Mesma sequência visual do código original.
const byte SEQUENCIA_ANIMACAO[] = {6, 1, 2, 3, 4, 5};
bool primeiraJogada = true;

void mostrarNumero(byte numero) {
  for (byte segmento = 0; segmento < 7; segmento++) {
    digitalWrite(PINOS_SEGMENTOS[segmento], bitRead(DIGITOS[numero], segmento));
  }
}

void animarDado() {
  for (byte volta = 0; volta < 10; volta++) {
    for (byte numero : SEQUENCIA_ANIMACAO) {
      mostrarNumero(numero);
      delay(50);
    }
  }
}

void setup() {
  for (byte pino : PINOS_SEGMENTOS) {
    pinMode(pino, OUTPUT);
  }

  // O resistor externo entre A0 e GND mantém o botão solto em LOW.
  pinMode(PINO_BOTAO, INPUT);
  mostrarNumero(0);
  delay(1000);
}

void loop() {
  if (digitalRead(PINO_BOTAO) == LOW) return;

  // Confirma o aperto depois que o contato estabilizar.
  delay(25);
  if (digitalRead(PINO_BOTAO) == LOW) return;

  if (primeiraJogada) {
    randomSeed(micros());
    primeiraJogada = false;
  }

  byte resultado = random(1, 7);  // Sorteia de 1 a 6.
  animarDado();
  mostrarNumero(resultado);

  // Só libera outra jogada depois que o botão estiver solto por 25 ms.
  do {
    while (digitalRead(PINO_BOTAO) == HIGH) {
      delay(1);
    }
    delay(25);
  } while (digitalRead(PINO_BOTAO) == HIGH);
}