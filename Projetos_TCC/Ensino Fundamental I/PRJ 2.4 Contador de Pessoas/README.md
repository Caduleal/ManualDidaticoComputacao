# 🚀 PRJ 2.4 — Contador de Pessoas

> **Etapa de Ensino:** Módulo II - Ensino Fundamental I  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Contador de Pessoas.png" alt="Contador de Pessoas" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Contador de Pessoas (PRJ 2.4)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 2.4` |
| **Título do Projeto** | Contador de Pessoas |
| **Módulo Curricular** | Módulo II - Ensino Fundamental I |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Contagem, comparação de distâncias e noção de entrada e saída. Retomar sensores como entradas e mostradores como saídas, com leitura do código mediada pelo professor.

### 💡 Habilidades de Pensamento Computacional:
- Leitura alternada de sensores
- Contagem condicionada por sequência
- Máquina de estados
- Medição de intervalos com micros() e millis()

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Bibliotecas e salas de atividades precisam saber quantas pessoas estão presentes. Uma contagem manual pode perder eventos quando entradas e saídas acontecem rapidamente. O modelo permite discutir por que a ordem de passagem importa e por que uma leitura isolada não descreve todo o movimento de alguém.
- **Matematica:** Somar entradas, subtrair saídas sem permitir total negativo e comparar distâncias sucessivas. Explorar velocidade como variação de posição por intervalo, com apoio de exemplos concretos.

---

## 📖 Contextualização Histórica e Problema Real

Como atualizar a quantidade de pessoas quando alguém atravessa uma passagem? Dois sensores observam aproximações em sequência: S1 seguido de S2 soma uma entrada; a ordem inversa registra uma saída. O LCD mostra o total e o estado da passagem. Trata-se de uma maquete que exige posicionamento e testes, pois movimentos simultâneos não são identificados individualmente.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | LCD 16x2 I2C compatível com Adafruit_LiquidCrystal, configurado com deslocamento 0 em relação a 0x20 |
| 2x | Sensores ultrassônicos HC-SR04 |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- D3 → TRIG de S1; D2 → ECHO de S1 (índice 0)
- D4 → TRIG de S2; D5 → ECHO de S2 (índice 1)
- A4/SDA → SDA do módulo I2C; A5/SCL → SCL do módulo I2C (Arduino Uno)
- 5V → VCC dos módulos de 5 V; GND → referência comum, conferindo as ligações da montagem

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 2.4 Esquema.png" alt="Esquema elétrico - PRJ 2.4" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 2.3 Esquematico.pdf](./PRJ 2.3 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Inicializar LCD e dois sensores
2. Alternar medições a cada 30000 µs
3. Descartar distância inválida
4. Comparar distância com leitura anterior
5. Detectar aproximação de pelo menos 0,10 m/s
6. Aguardar o segundo sensor
7. Somar entrada ou subtrair saída
8. Exibir resultado e liberar nova sequência

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <math.h>

Adafruit_LiquidCrystal lcd(0);
const byte trigPin[] = {3, 4};
const byte echoPin[] = {2, 5};
const float velocidadeSom = 0.0343;
const float distanciaMinima = 2.0;
const float distanciaMaxima = 300.0;
const float velocidadeMinima = 0.10;

const unsigned long intervaloLeitura = 30000UL;
const unsigned long pausaEntreMovimentos = 800UL;
const unsigned long tempoExibicao = 3000UL;

float distanciaAnterior[2];
unsigned long tempoAnterior[2];
bool primeiraLeitura[] = {true, true};
byte sensor = 0;
unsigned long ultimaLeitura = 0;
unsigned long ultimoMovimento = 0;
unsigned long inicioExibicao = 0;
unsigned long pessoas = 0;
enum Estado { LIVRE, ESPERA_S1, ESPERA_S2, FINALIZADA };
Estado estado = LIVRE;
unsigned long inicioSequencia = 0;
const unsigned long prazoSequencia = 20000UL;
bool exibindo = false;
float medirDistancia(byte i) {
  digitalWrite(trigPin[i], LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin[i], HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin[i], LOW);
  unsigned long duracao = pulseIn(echoPin[i], HIGH, 20000UL);
  float distancia = duracao * velocidadeSom / 2.0;
  if (duracao == 0 || distancia < distanciaMinima || distancia > distanciaMaxima) {
    return -1;
  }
  return distancia;
}

void mostrarTotal(const char* mensagem) {
  lcd.clear();
  lcd.print("Total:");
  lcd.print(pessoas);
  lcd.setCursor(0, 1);
  lcd.print(mensagem);
}

void registrarAproximacao(byte i) {
  ultimoMovimento = millis();
  if (estado == LIVRE) {
    inicioSequencia = ultimoMovimento;
    estado = (i == 0) ? ESPERA_S2 : ESPERA_S1;
    exibindo = false;
    mostrarTotal(i == 0 ? "Aguardando S2" : "Aguardando S1");
  } else if (estado == ESPERA_S2 && i == 1) {
    ++pessoas;
    mostrarTotal("Entrada");
    estado = FINALIZADA;
  } else if (estado == ESPERA_S1 && i == 0) {
    if (pessoas > 0) --pessoas;
    mostrarTotal("Saida");
    estado = FINALIZADA;
  } else {
    return;
  }
  if (estado == FINALIZADA) {
    exibindo = true;
    inicioExibicao = ultimoMovimento;
  }
}

void verificarMovimento(byte i, float distancia) {
  if (distancia < 0) {
    primeiraLeitura[i] = true;
    return;
  }

  unsigned long instante = micros();
  if (!primeiraLeitura[i]) {
    float segundos = (instante - tempoAnterior[i]) / 1000000.0;
    if (segundos > 0) {
      float velocidade = ((distancia - distanciaAnterior[i]) / 100.0) / segundos;
      Serial.print("DIST");
      Serial.print(i + 1);
      Serial.print(" | cm: ");
      Serial.print(distancia, 2);
      Serial.print(" | m/s: ");
      Serial.println(velocidade, 3);

      if (velocidade < 0 && fabs(velocidade) >= velocidadeMinima) {
        registrarAproximacao(i);
      }
    }
  }
  primeiraLeitura[i] = false;
  distanciaAnterior[i] = distancia;
  tempoAnterior[i] = instante;
}
void setup() {
  Serial.begin(115200);
  for (byte i = 0; i < 2; ++i) {
    pinMode(trigPin[i], OUTPUT);
    pinMode(echoPin[i], INPUT);
    digitalWrite(trigPin[i], LOW);
  }
  Wire.begin();
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  mostrarTotal("Monitorando...");
}
void loop() {
  unsigned long agoraMs = millis();
  if (estado == FINALIZADA && agoraMs - ultimoMovimento >= pausaEntreMovimentos) {
    estado = LIVRE;
  }
  if ((estado == ESPERA_S1 || estado == ESPERA_S2) && agoraMs - inicioSequencia >= prazoSequencia) {
    estado = LIVRE;
    mostrarTotal("Monitorando...");
  }
  if (exibindo && agoraMs - inicioExibicao >= tempoExibicao) {
    exibindo = false;
    mostrarTotal("Monitorando...");
  }

  unsigned long agora = micros();
  if (agora - ultimaLeitura < intervaloLeitura) return;
  ultimaLeitura = agora;
  verificarMovimento(sensor, medirDistancia(sensor));
  sensor = 1 - sensor;
}
```

📁 **Arquivo fonte compilável:** [`PRJ 2.4 Contador de Pessoas.ino`](./PRJ 2.4 Contador de Pessoas.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Organize os dois sensores em uma passagem de maquete, identificando S1 e S2. Monte com o USB desligado e evite apontar os sensores diretamente um para o outro.
2. Ligue S1 com TRIG em D3 e ECHO em D2; ligue S2 com TRIG em D4 e ECHO em D5. Compartilhe 5V e GND conforme os módulos.
3. Ligue o LCD I2C ao barramento SDA/SCL do Uno. O PDF está nomeado PRJ 2.3, mas foi encontrado nesta pasta 2.4; use os pinos do .ino como referência funcional.
4. Instale Adafruit LiquidCrystal e abra o .ino completo da pasta. Selecione Uno e a porta correta; o trecho no JSON destaca apenas a decisão de entrada e saída. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre ordem dos sensores determina entrada ou saída; para executar, use PRJ 2.4 Contador de Pessoas.ino completo (trecho nas linhas 54–69).
5. Carregue e abra o Monitor Serial a 115200 baud. Aproxime um objeto de S1 e depois de S2; repita na ordem inversa e observe a atualização do total.
6. Teste uma sequência incompleta e uma saída com total zero. Registre que o programa usa prazo de 20 s, pausa de 800 ms após o movimento final e não deixa a contagem ficar negativa. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Direção por Ordem: A função registrarAproximacao() guarda qual sensor iniciou a passagem. O segundo evento define entrada ou saída; usar dois pontos de observação diferencia esse projeto de um simples detector de presença.

2) Movimento Calculado: O programa compara duas distâncias e o intervalo entre elas. Apenas aproximações com módulo de velocidade de pelo menos 0,10 m/s acionam o registro, portanto colocar um objeto parado diante do sensor não equivale a atravessar.

3) Estados e Prazos: LIVRE, ESPERA_S1, ESPERA_S2 e FINALIZADA organizam a sequência. Um prazo de 20 segundos cancela a espera incompleta, e a pausa após o movimento reduz a repetição imediata de uma mesma passagem.

4) Limites da Contagem: O total fica na memória RAM e é perdido ao reiniciar. Duas pessoas lado a lado ou leituras com eco ruim podem gerar resultados incorretos; a turma deve comparar o LCD com uma contagem manual durante os testes.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Criar uma tabela com a ordem dos sensores e a mudança esperada no total.
- **Nível Intermediário:** Testar diferentes posições dos sensores e comparar os acertos com uma contagem manual.
- **Nível Avançado:** Adicionar, em uma cópia do programa e com pino livre, um botão para zerar a contagem, evitando que um botão mantido pressionado gere comandos repetidos.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Contador de Pessoas.png`](./Contador de Pessoas.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 2.3 Esquematico.pdf`](./PRJ 2.3 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 2.4 Contador de Pessoas.ino`](./PRJ 2.4 Contador de Pessoas.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 2.4 Contador de Pessoas.json`](./PRJ 2.4 Contador de Pessoas.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`PRJ 2.4 Esquema.png`](./PRJ 2.4 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
