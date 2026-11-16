#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_LEDBackpack.h>

Adafruit_7segment matrix = Adafruit_7segment();

// Definição de Pinos conforme o esquemático
const int pinoBotao = A3;
const int pinoLedVermelho = 3; // Ajuste o pino PWM/Digital do canal Vermelho do LED RGB
const int pinoLedVerde = 5;    // Ajuste o pino PWM/Digital do canal Verde do LED RGB

// Parâmetros do Jogo
const unsigned long TEMPO_ALVO_MS = 5000;    // 5.0 segundos
const unsigned long TOLERANCIA_MS = 200;     // Tolerância de 0.2 segundos (200 ms)

enum EstadoJogo {
  AGUARDANDO_INICIO,
  PISCAR_INICIAL,
  CRONOMETRO_RODANDO,
  FIM_JOGADA
};

EstadoJogo estadoAtual = AGUARDANDO_INICIO;

unsigned long tempoInicio = 0;
unsigned long tempoFinalParcial = 0;
bool estadoAnteriorBotao = HIGH;

void setup() {
  pinMode(pinoBotao, INPUT);
  pinMode(pinoLedVermelho, OUTPUT);
  pinMode(pinoLedVerde, OUTPUT);

  matrix.begin(0x70);
  matrix.setBrightness(7);
  matrix.clear();
  matrix.writeDisplay();

  // Estado inicial: LED vermelho aceso e display congelado em 00.00
  digitalWrite(pinoLedVermelho, HIGH);
  digitalWrite(pinoLedVerde, LOW);
  matrix.printFloat(0.00, 2);
  matrix.writeDisplay();
}

void loop() {
  bool leituraBotao = digitalRead(pinoBotao);

  switch (estadoAtual) {
    
    case AGUARDANDO_INICIO:
      digitalWrite(pinoLedVermelho, HIGH);
      digitalWrite(pinoLedVerde, LOW);
      
      // Se o botão for pressionado, inicia a sequência de partida
      if (leituraBotao == HIGH && estadoAnteriorBotao == LOW) {
        delay(50); // Debounce
        estadoAtual = PISCAR_INICIAL;
      }
      break;

    case PISCAR_INICIAL:
      // Pisca o LED vermelho 3 vezes
      for (int i = 0; i < 3; i++) {
        digitalWrite(pinoLedVermelho, LOW);
        delay(300);
        digitalWrite(pinoLedVermelho, HIGH);
        delay(300);
      }
      // Mantém o LED vermelho aceso e inicia o cronômetro
      digitalWrite(pinoLedVermelho, HIGH);
      tempoInicio = millis();
      estadoAtual = CRONOMETRO_RODANDO;
      break;

    case CRONOMETRO_RODANDO: {
      unsigned long tempoAtual = millis() - tempoInicio;
      float segundosTotais = tempoAtual / 1000.0;

      // Mantém a contagem atualizada no display
      matrix.printFloat(segundosTotais, 2);
      matrix.writeDisplay();

      // Verifica se o botão foi pressionado para parar a jogada
      if (leituraBotao == HIGH && estadoAnteriorBotao == LOW) {
        delay(50);
        tempoFinalParcial = tempoAtual;
        estadoAtual = FIM_JOGADA;
      }
      break;
    }

    case FIM_JOGADA: {
      // Avalia a tolerância de 0.2s (|t - 5.0| <= 0.2)
      long diferenca = (long)tempoFinalParcial - (long)TEMPO_ALVO_MS;
      
      if (abs(diferenca) <= TOLERANCIA_MS) {
        // Acerta o tempo: LED Verde aceso, Vermelho apagado
        digitalWrite(pinoLedVermelho, LOW);
        digitalWrite(pinoLedVerde, HIGH);
      } else {
        // Erra o tempo: Mantém LED Vermelho aceso, Verde apagado
        digitalWrite(pinoLedVermelho, HIGH);
        digitalWrite(pinoLedVerde, LOW);
      }

      // Mantém o tempo final congelado no display
      float segundosFinais = tempoFinalParcial / 1000.0;
      matrix.printFloat(segundosFinais, 2);
      matrix.writeDisplay();

      // Aguarda um novo clique para reiniciar o ciclo do jogo
      if (leituraBotao == HIGH && estadoAnteriorBotao == LOW) {
        delay(50);
        matrix.clear();
        matrix.printFloat(0.00, 2);
        matrix.writeDisplay();
        estadoAtual = PISCAR_INICIAL; // Reinicia a partida
      }
      break;
    }
  }

  estadoAnteriorBotao = leituraBotao;
}