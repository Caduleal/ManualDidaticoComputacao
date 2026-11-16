# 🚀 PRJ 3.4 — Lixeira Automática

> **Etapa de Ensino:** Módulo III - Ensino Fundamental II  
> **Nível de Complexidade:** `Avançado` | **Tempo Estimado:** `3 h/aula (180 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Lixeira Automática.png" alt="Lixeira Automática" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Lixeira Automática (PRJ 3.4)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 3.4` |
| **Título do Projeto** | Lixeira Automática |
| **Módulo Curricular** | Módulo III - Ensino Fundamental II |
| **Complexidade Didática** | `Avançado` |
| **Duração Estimada** | 3 h/aula (180 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Controle de servo, leitura ultrassônica, saídas digitais e funções. Compreender alimentação compartilhada e testar um conjunto antes de repetir a montagem.

### 💡 Habilidades de Pensamento Computacional:
- Repetição de módulos de controle
- Função parametrizada de distância
- Associação entre sensor e atuador
- Diagnóstico de limitações de leitura

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Recipientes identificados ajudam a organizar a separação de materiais em um espaço coletivo. Abrir uma tampa por aproximação pode reduzir a necessidade de tocá-la. A maquete permite discutir sinalização e hábitos de descarte, lembrando que o circuito não reconhece o material colocado e depende da escolha feita pela pessoa.
- **Matematica:** Associar quatro sensores a quatro tampas, comparar distâncias com 100 cm e relacionar posições de 0° e 90° ao movimento das alavancas.

---

## 📖 Contextualização Histórica e Problema Real

Como abrir a tampa correspondente à aproximação de uma mão? O projeto possui quatro canais, cada um formado por sensor ultrassônico, servo e LED. Para uma distância menor que 100 cm, o programa abre o respectivo servo a 90° e acende seu LED; nos demais casos volta a 0°. O conjunto modela quatro recipientes de uma estação de descarte, sem classificar automaticamente os resíduos.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 4x | Sensores ultrassônicos HC-SR04 |
| 4x | Microservos |
| 4x | LEDs amarelo, verde, azul e vermelho |
| 4x | Resistores de 220 Ω para os LEDs |
| 1x | Protoboard, conforme a imagem da montagem |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- Canal 1: D2 TRIG, D3 ECHO, D10 LED amarelo, A0 sinal do servo
- Canal 2: D4 TRIG, D5 ECHO, D11 LED verde, A1 sinal do servo
- Canal 3: D6 TRIG, D7 ECHO, D12 LED azul, A2 sinal do servo
- Canal 4: D8 TRIG, D9 ECHO, D13 LED vermelho, A3 sinal do servo
- LEDs via resistores de 220 Ω; catodos → GND
- Sensores → 5V/GND; servos precisam de fonte de 5 V dimensionada para o conjunto e GND comum com o Uno

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 3.4 Esquema.png" alt="Esquema elétrico - PRJ 3.4" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 3.4 Esquematico.pdf](./PRJ 3.4 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Inicializar quatro servos a 0°
2. Apagar os quatro LEDs
3. Medir distância do canal 1
4. Comparar com 100 cm e acionar servo/LED
5. Repetir para canais 2, 3 e 4
6. Registrar distâncias na serial
7. Reiniciar ciclo sequencial

### 📊 Diagrama de Fluxo Lógico (Fluxograma):

<div align="center">
  <img src="./PRJ 3.4 Fluxograma.jpg" alt="Fluxograma Lógico - PRJ 3.4" width="550px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 2: FLUXOGRAMA LÓGICO-ALGORÍTMICO DO FIRMWARE</em></p>
</div>

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Servo.h>

// Sensores ultrassônicos
const int echoPin1 = 3;
const int trigPin1 = 2;

const int echoPin2 = 5;
const int trigPin2 = 4;

const int echoPin3 = 7;
const int trigPin3 = 6;

const int echoPin4 = 9;
const int trigPin4 = 8;

// LEDs
const int ledPin1 = 10;
const int ledPin2 = 11;
const int ledPin3 = 12;
const int ledPin4 = 13;

// Servomotores
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

int pos = 0;

void setup() {
  servo1.attach(A0);
  servo2.attach(A1);
  servo3.attach(A2);
  servo4.attach(A3);

  pinMode(echoPin1, INPUT);
  pinMode(trigPin1, OUTPUT);

  pinMode(echoPin2, INPUT);
  pinMode(trigPin2, OUTPUT);

  pinMode(echoPin3, INPUT);
  pinMode(trigPin3, OUTPUT);

  pinMode(echoPin4, INPUT);
  pinMode(trigPin4, OUTPUT);

  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(ledPin4, OUTPUT);

  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);

  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  digitalWrite(ledPin4, LOW);

  Serial.begin(9600);
}

void loop() {

  // Sensor e motor 1
  int dist1 = CalcDist(trigPin1, echoPin1);
  Serial.print("Distancia 1: ");
  Serial.println(dist1);

  if (dist1 < 100) {
    pos = 90;
    servo1.write(pos);
    digitalWrite(ledPin1, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo1.write(pos);
    digitalWrite(ledPin1, LOW);
    delay(15);
  }

  // Sensor e motor 2
  int dist2 = CalcDist(trigPin2, echoPin2);
  Serial.print("Distancia 2: ");
  Serial.println(dist2);

  if (dist2 < 100) {
    pos = 90;
    servo2.write(pos);
    digitalWrite(ledPin2, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo2.write(pos);
    digitalWrite(ledPin2, LOW);
    delay(15);
  }

  // Sensor e motor 3
  int dist3 = CalcDist(trigPin3, echoPin3);
  Serial.print("Distancia 3: ");
  Serial.println(dist3);

  if (dist3 < 100) {
    pos = 90;
    servo3.write(pos);
    digitalWrite(ledPin3, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo3.write(pos);
    digitalWrite(ledPin3, LOW);
    delay(15);
  }

  // Sensor e motor 4
  int dist4 = CalcDist(trigPin4, echoPin4);
  Serial.print("Distancia 4: ");
  Serial.println(dist4);

  if (dist4 < 100) {
    pos = 90;
    servo4.write(pos);
    digitalWrite(ledPin4, HIGH);
    delay(15);
  } else {
    pos = 0;
    servo4.write(pos);
    digitalWrite(ledPin4, LOW);
    delay(15);
  }
}

// Mesma função do código original
int CalcDist(int trigPin, int echoPin) {
  long duration, distanceCm;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);

  distanceCm = duration * 343 / 10000 / 2;

  return distanceCm;
}
```

📁 **Arquivo fonte compilável:** [`PRJ 3.4 Lixeira Automatica.ino.ino`](./PRJ 3.4 Lixeira Automatica.ino.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Monte uma estação de papelão com tampas leves, identificando os quatro canais. Com alimentação desligada, teste primeiro um sensor, servo e LED antes de repetir o circuito.
2. Ligue os pares TRIG/ECHO D2/D3, D4/D5, D6/D7 e D8/D9. Posicione os sensores para reduzir a leitura de ecos de recipientes vizinhos.
3. Conecte sinais dos servos a A0–A3 e LEDs com resistores a D10–D13. Confira a correspondência de cada conjunto antes de prender as alavancas.
4. Use alimentação de servos dimensionada para quatro motores, com GND comum; não presuma que a saída de 5V do Uno sustenta todos. Abra o .ino completo com Servo.h e carregue. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre um canal de sensor, servo e led; para executar, use PRJ 3.4 Lixeira Automatica.ino.ino completo (trecho nas linhas 70–84).
5. Observe o Monitor Serial a 9600 baud e aproxime um objeto de cada canal. Confira abertura a 90°, retorno a 0° e LED do mesmo recipiente.
6. Teste a ausência de eco: CalcDist() usa pulseIn() sem timeout explícito e pode retornar distância zero. Registre essa limitação e mantenha mãos longe das articulações durante o movimento.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Canal Repetido: Cada sensor comanda seu próprio servo e LED. O trecho do JSON apresenta o primeiro conjunto; o programa completo repete a mesma decisão para os outros três canais, com seus respectivos pinos.

2) Leitura Sequencial: As quatro medidas são feitas uma após outra e incluem pulseIn() e pausas. A resposta do conjunto não é simultânea, e um canal sem retorno pode atrasar o processamento dos seguintes.

3) Alimentação dos Servos: Quatro motores podem exigir corrente significativa, especialmente ao iniciar ou travar. A montagem física precisa de fonte adequada e GND comum, além de tampas leves que não forcem a mecânica.

4) Alcance e Limitações: O limiar de 100 cm pode ser grande para uma maquete de mesa. A função não valida ausência de eco, e o circuito não reconhece plástico, papel ou metal; a separação depende da identificação dos recipientes.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Criar placas de identificação para os quatro recipientes e conferir o canal que abre cada tampa.
- **Nível Intermediário:** Ajustar o limite de distância em uma cópia do fonte e testar acionamentos indesejados entre canais próximos.
- **Nível Avançado:** Substituir a repetição por vetores e uma função por canal, incluindo timeout e rejeição de eco inválido, sem adicionar sensores ou servos.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Lixeira Automática.png`](./Lixeira Automática.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 3.4 Esquema.png`](./PRJ 3.4 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 3.4 Esquematico.pdf`](./PRJ 3.4 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 3.4 Fluxograma.jpg`](./PRJ 3.4 Fluxograma.jpg) | Fluxograma lógico-algorítmico do firmware |
| [`PRJ 3.4 Lixeira Automatica.ino.ino`](./PRJ 3.4 Lixeira Automatica.ino.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 3.4 Lixeira Automatica.json`](./PRJ 3.4 Lixeira Automatica.json) | Estrutura JSON de dados e metadados pedagógicos |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
