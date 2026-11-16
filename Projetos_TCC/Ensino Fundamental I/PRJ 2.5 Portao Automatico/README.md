# 🚀 PRJ 2.5 — Portão Automático

> **Etapa de Ensino:** Módulo II - Ensino Fundamental I  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Portão Automatico.png" alt="Portão Automático" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Portão Automático (PRJ 2.5)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 2.5` |
| **Título do Projeto** | Portão Automático |
| **Módulo Curricular** | Módulo II - Ensino Fundamental I |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
LEDs com resistor, leitura de distância e comparação de números. Reconhecer que um servo recebe um comando de posição e precisa de alimentação adequada.

### 💡 Habilidades de Pensamento Computacional:
- Funções com parâmetros
- Decisão if/else
- Conversão do tempo de eco em distância
- Controle coordenado de servo, LED e buzzer

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Portões automatizados combinam movimento e avisos para indicar quando uma passagem está sendo aberta. Luz e som ajudam as pessoas a perceber uma mudança no ambiente. Uma maquete permite observar essas funções e discutir por que um mecanismo real precisa de proteções que vão além de um único sensor.
- **Matematica:** Comparar distâncias com o limite de 100 cm, reconhecer posições de 0° e 90° e relacionar bipes de 150 ms com pausas de igual duração.

---

## 📖 Contextualização Histórica e Problema Real

Como abrir uma passagem quando um objeto se aproxima? O sensor mede a distância e o programa compara o resultado com 100 cm. Abaixo desse limite, o servo vai a 90° e LED e buzzer alternam avisos; caso contrário, o servo volta a 0°. O modelo representa um portão de papelão e não incorpora as proteções de uma instalação real.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | Sensor ultrassônico HC-SR04 |
| 1x | Microservo |
| 1x | LED amarelo |
| 1x | Resistor de 220 Ω |
| 1x | Buzzer ou piezo |
| 1x | Protoboard, conforme a imagem da montagem |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- D2 → TRIG; D3 → ECHO do HC-SR04
- D4 → anodo do LED via resistor de 220 Ω
- D5 → positivo do buzzer/piezo
- A0 → sinal do servo, usado como saída digital
- 5V → alimentação dos módulos compatíveis; GND → referência comum, catodo do LED e negativo do piezo

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 2.5 Esquema.png" alt="Esquema elétrico - PRJ 2.5" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 2.5 Esquematico.pdf](./PRJ 2.5 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Inicializar servo e pinos
2. Medir o tempo de eco
3. Calcular distância em centímetros
4. Comparar distância com 100 cm
5. Abrir a 90° e emitir avisos
6. Alternar sinal a cada 150 ms
7. Fechar a 0° quando afastado
8. Repetir a leitura

### 📊 Diagrama de Fluxo Lógico (Fluxograma):

<div align="center">
  <img src="./PRJ 2.5 Fluxograma.png" alt="Fluxograma Lógico - PRJ 2.5" width="550px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 2: FLUXOGRAMA LÓGICO-ALGORÍTMICO DO FIRMWARE</em></p>
</div>

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Servo.h>

const int echoPin = 3;
const int trigPin = 2;
const int ledPin = 4;     // Alterado para pino 4 (evita conflito com Serial RX/TX)
const int buzzerPin = 5;  // Alterado para pino 5 (evita conflito com Serial RX/TX)

Servo myservo;
int pos = 0;

void setup() {
  myservo.attach(A0);
  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int dist = CalcDist(trigPin, echoPin);
  Serial.println(dist);
  
  if (dist < 100) {
    // Objeto próximo: Abre o portão (90°)
    pos = 90;
    myservo.write(pos);
    
    // Alerta estilo sirene de garagem (Pi-Pi-Pi com LED piscando)
    digitalWrite(ledPin, HIGH);
    tone(buzzerPin, 1200); // Tom mais agudo simulando o bipe de ré/saída
    delay(150);            // Duração do "pi"
    
    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);
    delay(150);            // Pausa entre os bipes
    
  } else {
    // Objeto afastado: Fecha o portão (0°) e desliga os alertas
    pos = 0;
    myservo.write(pos);
    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);
    delay(15);
  }
}

int CalcDist(int trigPin, int echoPin){
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

📁 **Arquivo fonte compilável:** [`PRJ 2.5 Portao Automatico.ino`](./PRJ 2.5 Portao Automatico.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Fixe o microservo a uma pequena cancela de papelão, sem carga pesada. Com USB desligado, identifique os três fios do servo e os quatro pinos do sensor.
2. Conecte TRIG a D2, ECHO a D3 e sinal do servo a A0. Confira a alimentação do servo e o GND comum; use fonte de 5 V adequada se a alimentação da placa for insuficiente.
3. Ligue o LED amarelo a D4 por resistor de 220 Ω e o piezo a D5, com retornos ao GND. Não use os pinos RX/TX para esses avisos.
4. Abra o .ino completo, que utiliza Servo.h, selecione Uno e carregue. O trecho do JSON destaca a abertura com avisos, sem substituir o programa completo. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre abertura com avisos e fechamento por distância; para executar, use PRJ 2.5 Portao Automatico.ino completo (trecho nas linhas 24–45).
5. Abra o Monitor Serial a 9600 baud e mova um objeto para distâncias abaixo e acima de 100 cm. Observe 90° na abertura e 0° no fechamento.
6. Teste também ausência de eco e registre o comportamento: pulseIn() não recebe timeout explícito e um retorno zero pode ser interpretado como distância próxima. Mantenha mãos fora do mecanismo.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Distância por Eco: CalcDist() gera um pulso de disparo e mede o retorno com pulseIn(). O fator de conversão considera a viagem de ida e volta do som; o resultado inteiro em centímetros alimenta a decisão.

2) Posição do Servo: Servo.h produz o sinal de controle no pino A0. Os comandos de 0° e 90° representam posições da maquete, mas a geometria da alavanca e o esforço mecânico precisam ser conferidos antes de prender a cancela.

3) Avisos Coordenados: Na abertura, digitalWrite() e tone() ligam LED e piezo por 150 ms, seguidos de uma pausa igual. Esses delays também limitam a frequência com que o programa consegue realizar novas medições.

4) Limitação da Leitura: O código original não distingue explicitamente a falta de eco de um objeto muito próximo. Esse ponto deve ser observado nos testes; acrescentar validação é uma expansão, não uma característica já existente.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Alterar o limite de distância para uma maquete menor e prever a nova região de acionamento.
- **Nível Intermediário:** Modificar a frequência e a duração dos bipes, mantendo LED e servo nos mesmos pinos.
- **Nível Avançado:** Em uma cópia do fonte, acrescentar timeout e validação de eco e substituir as pausas dos avisos por millis().

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`PRJ 2.5 Esquema.png`](./PRJ 2.5 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 2.5 Esquematico.pdf`](./PRJ 2.5 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 2.5 Fluxograma.png`](./PRJ 2.5 Fluxograma.png) | Fluxograma lógico-algorítmico do firmware |
| [`PRJ 2.5 Portao Automatico.ino`](./PRJ 2.5 Portao Automatico.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 2.5 Portao Automatico.json`](./PRJ 2.5 Portao Automatico.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`Portão Automatico.png`](./Portão Automatico.png) | Fotografia / Identidade visual de capa do projeto |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
