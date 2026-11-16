# 🚀 PRJ 2.9 — Pedra, Papel e Tesoura

> **Etapa de Ensino:** Módulo II - Ensino Fundamental I  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Pedra, Papel e Tesoura.png" alt="Pedra, Papel e Tesoura" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Pedra, Papel e Tesoura (PRJ 2.9)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 2.9` |
| **Título do Projeto** | Pedra, Papel e Tesoura |
| **Módulo Curricular** | Módulo II - Ensino Fundamental I |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Conhecer as três jogadas e suas regras, identificar sensor e LCD e comparar distâncias. Distinguir uma resposta sorteada de uma leitura do gesto da mão.

### 💡 Habilidades de Pensamento Computacional:
- Seleção pseudoaleatória em vetor
- Detecção de aproximação
- Controle de novo acionamento
- Exibição de mensagens

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Pedra, papel e tesoura organiza uma disputa curta com três escolhas conhecidas pelos participantes. Uma versão eletrônica permite discutir como uma máquina seleciona uma resposta. A turma mantém a interpretação das regras e compara sua jogada com o texto sorteado, sem atribuir ao sensor a capacidade de reconhecer gestos.
- **Matematica:** Relacionar três escolhas possíveis a índices 0, 1 e 2, contar frequências de sorteio e comparar os limites de aproximação de 200 cm e afastamento de 250 cm.

---

## 📖 Contextualização Histórica e Problema Real

Como solicitar uma jogada da máquina sem apertar um botão? O sensor detecta um objeto entre 2 e 200 cm e o programa sorteia uma das três palavras para o LCD. O texto fica visível por cinco segundos; para repetir, o objeto deve se afastar além de 250 cm ou ocorrer ausência de eco. O circuito não identifica a mão como pedra, papel ou tesoura e não calcula o vencedor.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | LCD 16x2 I2C compatível com Adafruit_LiquidCrystal, configurado com deslocamento 0 em relação a 0x20 |
| 1x | Sensor ultrassônico HC-SR04 |
| 1x | Conjunto de jumpers; quantidade não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- D3 → TRIG; D2 → ECHO do HC-SR04
- A4/SDA → SDA do módulo I2C; A5/SCL → SCL do módulo I2C (Arduino Uno)
- 5V → VCC dos módulos de 5 V; GND → referência comum, conferindo as ligações da montagem

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 2.9 Esquema.png" alt="Esquema elétrico - PRJ 2.9" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 2.9 Esquematico.pdf](./PRJ 2.9 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Mostrar convite no LCD
2. Medir distância com timeout
3. Verificar permissão de jogar
4. Detectar objeto entre 2 e 200 cm
5. Sortear índice de 0 a 2
6. Exibir palavra por 5 s
7. Voltar ao convite
8. Rearmar após afastamento ou ausência de eco

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

Adafruit_LiquidCrystal lcd(0);

const byte trigPin = 3;
const byte echoPin = 2;

const float distanciaParaJogar = 200.0;    // cm
const float distanciaParaRearmar = 250.0;  // cm
const unsigned long tempoResposta = 5000; // ms

const char* const respostas[] = {"Pedra", "Papel", "Tesoura"};

bool podeJogar = true;
bool primeiroSorteio = true;

void mostrarConvite() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Vamos jogar?");
  lcd.setCursor(0, 1);
  lcd.print("Aproxime!");
}

float medirDistancia() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long eco = pulseIn(echoPin, HIGH, 25000UL);

  if (eco == 0) {
    return -1;  // Nenhum eco recebido
  }

  return eco * 0.0343 / 2.0;
}

void mostrarJogada() {
  if (primeiroSorteio) {
    randomSeed(micros());
    primeiroSorteio = false;
  }

  byte escolha = random(3);  // 0, 1 ou 2

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(respostas[escolha]);

  Serial.print("Jogada: ");
  Serial.println(respostas[escolha]);

  delay(tempoResposta);
  mostrarConvite();
}

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  digitalWrite(trigPin, LOW);

  Wire.begin();
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  mostrarConvite();
}

void loop() {
  float distancia = medirDistancia();

  if (distancia < 0) {
    Serial.println("Sem eco");
    podeJogar = true;
  } else {
    Serial.print("Distancia: ");
    Serial.print(distancia, 1);
    Serial.println(" cm");

    if (distancia > distanciaParaRearmar) {
      podeJogar = true;
    }

    if (podeJogar && distancia >= 2.0 && distancia <= distanciaParaJogar) {
      podeJogar = false;
      mostrarJogada();
    }
  }

  delay(60);  // Intervalo entre medições do HC-SR04
}
```

📁 **Arquivo fonte compilável:** [`PRJ 2.9 Pedra, Papel e Tesoura.ino`](./PRJ 2.9 Pedra, Papel e Tesoura.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Monte com USB desligado, identificando sensor e LCD. Ligue TRIG a D3 e ECHO a D2, além de 5V e GND.
2. Ligue o LCD a SDA/SCL do Uno e confira o retorno comum de alimentação. O projeto não usa câmera ou sensor de reconhecimento de gestos.
3. Instale Adafruit LiquidCrystal, abra o .ino completo com Wire.h e carregue na placa correta. O trecho exibido destaca o sorteio e a mensagem.
4. Abra o Monitor Serial a 9600 baud e aproxime um objeto entre 2 e 200 cm. Leia a palavra e compare-a manualmente com a jogada de um colega. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre sorteio de uma das três respostas; para executar, use PRJ 2.9 Pedra, Papel e Tesoura.ino completo (trecho nas linhas 42–59).
5. Aguarde os cinco segundos de exibição. Afaste o objeto além de 250 cm ou observe o rearme por ausência de eco antes de tentar novamente; em simulação, controle essas condições diretamente.
6. Registre as três respostas em várias tentativas. Discuta por que manter a mão parada não deve produzir uma nova jogada a cada leitura e por que o vencedor ainda depende da comparação feita pelos participantes. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Distância e Presença: medirDistancia() usa pulseIn() com timeout e devolve −1 quando não recebe eco. Essa condição rearma o jogo; o sensor mede a posição de um obstáculo, sem identificar sua forma.

2) Escolha em Vetor: respostas contém Pedra, Papel e Tesoura, e random(3) seleciona um índice válido. O primeiro sorteio inicializa randomSeed() com micros(), usando o instante do evento para variar a sequência.

3) Rearme com Margem: O limite de jogar é 200 cm e o de rearmar é 250 cm. A diferença reduz novos comandos perto da mesma fronteira; podeJogar guarda se a próxima aproximação deve ser aceita.

4) Escopo do Jogo: O LCD mostra a escolha da máquina durante delay(5000), período em que não há novas leituras no loop. Não existe variável para a jogada humana nem regra de vitória implementada no arquivo original.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Contar quantas vezes cada palavra aparece em uma sequência de tentativas.
- **Nível Intermediário:** Reduzir os dois limites para uma maquete de mesa, mantendo afastamento de rearme maior que o limite de jogar.
- **Nível Avançado:** Acrescentar três botões em pinos livres para escolher a jogada humana e comparar as escolhas por uma tabela de regras, em uma cópia do fonte.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`PRJ 2.9 Esquema.png`](./PRJ 2.9 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 2.9 Esquematico.pdf`](./PRJ 2.9 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 2.9 Pedra, Papel e Tesoura.ino`](./PRJ 2.9 Pedra, Papel e Tesoura.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 2.9 Pedra, Papel e Tesoura.json`](./PRJ 2.9 Pedra, Papel e Tesoura.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`Pedra, Papel e Tesoura.png`](./Pedra, Papel e Tesoura.png) | Fotografia / Identidade visual de capa do projeto |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
