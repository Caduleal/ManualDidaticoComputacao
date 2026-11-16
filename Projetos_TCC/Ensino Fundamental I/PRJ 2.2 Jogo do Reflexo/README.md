# 🚀 PRJ 2.2 — Jogo do Reflexo

> **Etapa de Ensino:** Módulo II - Ensino Fundamental I  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Jogo do Reflexo.png" alt="Jogo do Reflexo" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Jogo do Reflexo (PRJ 2.2)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 2.2` |
| **Título do Projeto** | Jogo do Reflexo |
| **Módulo Curricular** | Módulo II - Ensino Fundamental I |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Botões, LEDs e estados ligado/desligado. Comparar intervalos de tempo e acompanhar a leitura de um mostrador com apoio do professor.

### 💡 Habilidades de Pensamento Computacional:
- Máquina de estados
- Medição de tempo com millis()
- Detecção de transição do botão
- Comparação com uma margem de tolerância

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Jogos com cronômetros transformam a percepção de tempo em um desafio compartilhado. Mostradores eletrônicos permitem comparar tentativas usando a mesma regra. A turma pode alternar jogadores e discutir que um resultado depende da atenção, da prática e também do modo como o botão responde.
- **Matematica:** Converter milissegundos em segundos e comparar a tentativa com 5,0 s. A margem de 200 ms aceita resultados entre 4,8 s e 5,2 s, incluindo os limites.

---

## 📖 Contextualização Histórica e Problema Real

Como parar uma contagem o mais perto possível de cinco segundos? O primeiro comando inicia três piscadas e depois o cronômetro; outro comando congela o tempo. O programa compara a diferença com uma margem de 0,2 segundo e usa vermelho ou verde para mostrar o resultado. O projeto exercita estimativa temporal, embora o nome sugira uma medição de reflexo a um estímulo surpresa.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | Mostrador de quatro dígitos e sete segmentos com backpack HT16K33, I2C 0x70 |
| 1x | LED RGB de catodo comum |
| 1x | Botão de pressão |
| 4x | Resistores de 220 Ω indicados no PDF: três canais RGB e circuito do botão |
| 1x | Protoboard, conforme a imagem da montagem |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- A3 → leitura do botão (pinoBotao, INPUT)
- D3 → canal vermelho do LED RGB via resistor (pinoLedVermelho)
- D5 → canal verde do LED RGB via resistor (pinoLedVerde)
- D4 → canal azul via resistor na imagem; o programa não controla esse canal
- A4/SDA e A5/SCL → mostrador HT16K33, endereço 0x70
- 5V e GND → alimentação do mostrador e circuito; comum do RGB → GND

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 2.2 Esquema.png" alt="Esquema elétrico - PRJ 2.2" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 2.2 Esquematico.pdf](./PRJ 2.2 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Inicializar mostrador I2C
2. Aguardar botão
3. Piscar vermelho
4. Guardar início
5. Atualizar tempo
6. Congelar na próxima transição
7. Comparar diferença com 200 ms
8. Acerto em verde
9. Erro em vermelho
10. Aguardar nova jogada

### 📊 Diagrama de Fluxo Lógico (Fluxograma):

<div align="center">
  <img src="./PRJ 2.2 Fluxograma.png" alt="Fluxograma Lógico - PRJ 2.2" width="550px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 2: FLUXOGRAMA LÓGICO-ALGORÍTMICO DO FIRMWARE</em></p>
</div>

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
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
```

📁 **Arquivo fonte compilável:** [`PRJ 2.2 Jogo do Reflexo.ino`](./PRJ 2.2 Jogo do Reflexo.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Confira o mostrador HT16K33, o botão e o RGB. Faça as ligações com USB desligado, usando um resistor em cada canal do LED.
2. Ligue os canais vermelho e verde a D3 e D5. O canal azul aparece em D4 na imagem, mas não é usado no .ino; mantenha essa distinção ao explicar a montagem.
3. Ligue o sinal do botão a A3 e confira a rede resistiva antes do teste. A imagem mostra resistor ao positivo e botão ao GND; o código detecta LOW para HIGH, podendo registrar a soltura.
4. Ligue VCC/GND e SDA/SCL do mostrador. Instale Adafruit GFX Library e Adafruit LED Backpack Library e suas dependências; abra o fonte original com Wire.h. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre tolerância de acerto e resultado congelado; para executar, use PRJ 2.2 Jogo do Reflexo.ino completo (trecho nas linhas 95–110).
5. Carregue no Uno e observe qual movimento do botão gera o comando. Após as três piscadas, tente congelar a contagem perto de 5,00 s; o display registra o resultado.
6. Compare tentativas dentro e fora de 4,8–5,2 s. A transição usada pelo programa foi preservada; registre a diferença entre apertar e soltar antes de interpretar o desempenho dos jogadores.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Estados do Jogo: AGUARDANDO_INICIO, PISCAR_INICIAL, CRONOMETRO_RODANDO e FIM_JOGADA separam as fases. Isso evita misturar a atualização do tempo com a decisão de acerto e torna o fluxo mais fácil de acompanhar.

2) Tempo e Tolerância: millis() marca o início e a subtração fornece o tempo decorrido. O valor absoluto da diferença para 5000 ms precisa ser menor ou igual a 200 ms; não se exige um resultado exatamente igual a cinco segundos.

3) Botão e Transição: O programa procura a passagem de LOW para HIGH e usa delay(50) como espera de estabilização. Como a imagem apresenta polarização ao positivo, o evento pode corresponder à soltura, aspecto que deve ser testado e explicado.

4) Mostrador I2C: O backpack recebe os números pelo barramento em 0x70, em vez de exigir um fio por segmento. O resultado fica congelado até um novo comando, permitindo registrar as tentativas sem depender apenas da memória do jogador.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Alterar TEMPO_ALVO_MS e TOLERANCIA_MS.
- **Nível Intermediário:** Anotar cinco tentativas e identificar a mais próxima de 5 segundos.
- **Nível Avançado:** Contabiliza três tentativas seguidas antes de encerrar a partida, exibindo a média de precisão do jogador no final.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Jogo do Reflexo.png`](./Jogo do Reflexo.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 2.2 Esquema.png`](./PRJ 2.2 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 2.2 Esquematico.pdf`](./PRJ 2.2 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 2.2 Fluxograma.png`](./PRJ 2.2 Fluxograma.png) | Fluxograma lógico-algorítmico do firmware |
| [`PRJ 2.2 Jogo do Reflexo.ino`](./PRJ 2.2 Jogo do Reflexo.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 2.2 Jogo do Reflexo.json`](./PRJ 2.2 Jogo do Reflexo.json) | Estrutura JSON de dados e metadados pedagógicos |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
