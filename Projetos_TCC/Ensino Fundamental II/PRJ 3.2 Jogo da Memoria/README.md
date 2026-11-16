# 🚀 PRJ 3.2 — Jogo da Memória

> **Etapa de Ensino:** Módulo III - Ensino Fundamental II  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Jogo da Memoria.png" alt="Jogo da Memória" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Jogo da Memória (PRJ 3.2)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 3.2` |
| **Título do Projeto** | Jogo da Memória |
| **Módulo Curricular** | Módulo III - Ensino Fundamental II |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Vetores, índices, repetição, botões com polarização externa e LEDs com resistor. Ler sequências de cores e reproduzi-las em ordem.

### 💡 Habilidades de Pensamento Computacional:
- Armazenamento e comparação de sequências
- Laços com índices
- Abstração em funções
- Sinais sonoros associados a eventos

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Jogos de repetição de cores e sons oferecem um desafio de atenção e memória em regras curtas. Uma mesma sequência pode ser observada por todos e depois reproduzida individualmente. Na turma, o resultado permite conversar sobre estratégias de agrupamento e prática, sem tratar o desempenho em um jogo como medida geral de capacidade.
- **Matematica:** Relacionar posições e índices, comparar sequências e representar o aumento de um elemento por rodada. Contar acertos e observar a progressão do nível.

---

## 📖 Contextualização Histórica e Problema Real

Como verificar se alguém repetiu corretamente uma sequência luminosa? O programa acrescenta um índice sorteado ao vetor e apresenta as cores com tons associados. Cada botão recebido é comparado com a posição esperada; um erro produz aviso e reinício. Ao acertar toda a sequência, o nível aumenta e a próxima rodada exige lembrar mais um elemento.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 4x | LEDs: vermelho, amarelo, azul e verde |
| 4x | Botões de pressão |
| 8x | Resistores de 220 Ω no PDF: quatro para LEDs e quatro para as redes dos botões |
| 1x | Buzzer/piezo |
| 1x | Protoboard, conforme a imagem da montagem |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- D5 → LED vermelho; D8 → botão vermelho
- D4 → LED amarelo; D9 → botão amarelo
- D3 → LED azul; D10 → botão azul
- D2 → LED verde; D11 → botão verde
- D12 → buzzer/piezo; LEDs com resistores individuais e catodos ao GND
- Botões: INPUT com resistores externos para GND; pressionado = HIGH
- A0 → leitura para randomSeed(), sem sensor declarado; 5V/GND → alimentação comum

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 3.2 Esquema.png" alt="Esquema elétrico - PRJ 3.2" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 3.2 Esquematico.pdf](./PRJ 3.2 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Executar animação inicial
2. Semear sorteio com analogRead(A0)
3. Acrescentar cor ao vetor
4. Reproduzir sequência com luz e som
5. Aguardar cada botão
6. Comparar índice com posição esperada
7. Reiniciar após erro
8. Aumentar nível após acerto

### 📊 Diagrama de Fluxo Lógico (Fluxograma):

<div align="center">
  <img src="./PRJ 3.2 Fluxograma.png" alt="Fluxograma Lógico - PRJ 3.2" width="550px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 2: FLUXOGRAMA LÓGICO-ALGORÍTMICO DO FIRMWARE</em></p>
</div>

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
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
```

📁 **Arquivo fonte compilável:** [`PRJ 3.2 Jogo da Memoria.ino`](./PRJ 3.2 Jogo da Memoria.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Com USB desligado, organize quatro pares de botão e LED por cor. Confira os resistores de 220 Ω documentados no esquema e as conexões da protoboard.
2. Conecte LEDs vermelho D5, amarelo D4, azul D3 e verde D2, sempre com resistor em série e retorno ao GND.
3. Conecte os botões nas entradas D8, D9, D10 e D11, na mesma ordem de cores, com polarização externa para GND. Ligue o piezo em D12 e GND.
4. Abra o .ino completo e carregue no Uno. Não há bibliotecas externas; A0 é lido para iniciar o sorteio e não corresponde a um componente de jogo confirmado. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre comparação da sequência e tratamento do erro; para executar, use PRJ 3.2 Jogo da Memoria.ino completo (trecho nas linhas 155–173).
5. Observe a sequência e pressione os botões na ordem exibida, soltando cada um antes do próximo. Use o Monitor Serial a 9600 baud para comparar índices e nível.
6. Provoque um erro e observe o reinício. O vetor possui 100 posições, mas não existe condição de encerramento no nível máximo; limite a exploração a rodadas curtas até revisar essa fronteira.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Sequência em Memória: filaOriginal armazena índices de zero a três. O índice seleciona tanto o LED como o tom no vetor correspondente, separando a regra do jogo dos números físicos dos pinos.

2) Comparação Passo a Passo: O programa aguarda uma entrada em cada posição e compara o botão com filaOriginal[i]. Um resultado diferente chama gameOver(); somente uma sequência inteira correta permite incrementar nivel.

3) Som e Resposta: tone() associa uma frequência a cada cor, e a rotina de erro combina som e piscadas. A espera pela soltura evita que um botão mantido pressionado preencha imediatamente todas as posições seguintes.

4) Fronteira do Vetor: MAX_NIVEL define 100 posições, mas nivel continua crescendo após o acerto. Acessar uma posição além desse limite é uma lacuna do fonte original; acrescentar vitória ou reinício no limite deve ser feito como melhoria separada.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Mudar os tempos de exibição e comparar a dificuldade sem alterar a ordem das cores.
- **Nível Intermediário:** Criar uma tabela com os índices e as frequências dos quatro sons e experimentar outros tons.
- **Nível Avançado:** Adicionar condição de vitória no limite do vetor e uma etapa de reinício, testando primeiro com MAX_NIVEL pequeno em uma cópia do código.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Jogo da Memoria.png`](./Jogo da Memoria.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 3.2 Esquema.png`](./PRJ 3.2 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 3.2 Esquematico.pdf`](./PRJ 3.2 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 3.2 Fluxograma.png`](./PRJ 3.2 Fluxograma.png) | Fluxograma lógico-algorítmico do firmware |
| [`PRJ 3.2 Jogo da Memoria.ino`](./PRJ 3.2 Jogo da Memoria.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 3.2 Jogo da Memoria.json`](./PRJ 3.2 Jogo da Memoria.json) | Estrutura JSON de dados e metadados pedagógicos |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
