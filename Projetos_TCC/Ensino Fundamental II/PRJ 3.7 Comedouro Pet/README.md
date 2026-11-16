# 🚀 PRJ 3.7 — Comedouro Pet

> **Etapa de Ensino:** Módulo III - Ensino Fundamental II  
> **Nível de Complexidade:** `Avançado` | **Tempo Estimado:** `3 h/aula (180 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Comedouro Pet.png" alt="Comedouro Pet" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Comedouro Pet (PRJ 3.7)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 3.7` |
| **Título do Projeto** | Comedouro Pet |
| **Módulo Curricular** | Módulo III - Ensino Fundamental II |
| **Complexidade Didática** | `Avançado` |
| **Duração Estimada** | 3 h/aula (180 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Sensor ultrassônico, servo, botão com polarização externa e LCD. Compreender contagem limitada, temporização e necessidade de calibrar uma referência de distância.

### 💡 Habilidades de Pensamento Computacional:
- Calibração de referência
- Detecção de chegada e ausência
- Contagem limitada de eventos
- Debounce e temporização com millis()

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Dispositivos automáticos podem executar tarefas repetitivas quando alguém se aproxima. Um alimentador precisa considerar quantidade, intervalos e supervisão, além do movimento de uma tampa. A maquete permite estudar esses controles com materiais inertes, sem usar a contagem do programa como orientação para alimentar um animal real.
- **Matematica:** Contar de zero a cinco porções, comparar distância com uma referência de fundo e relacionar abertura de 1 s com o movimento entre 0° e 60°.

---

## 📖 Contextualização Histórica e Problema Real

Como liberar uma dose de demonstração uma vez por aproximação? O programa observa o fundo ao iniciar e detecta uma mudança de distância de pelo menos 3 cm. Uma chegada abre o servo por um segundo e soma uma porção, com limite de cinco; é preciso detectar ausência para aceitar outra visita. O botão zera a contagem, e o LCD mostra o estado, mas a massa liberada não é medida.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | LCD 16x2 I2C compatível com Adafruit_LiquidCrystal, configurado com deslocamento 0 em relação a 0x20 |
| 1x | Sensor HC-SR04 |
| 1x | Microservo |
| 1x | Botão de pressão |
| 1x | Resistor de 220 Ω para a rede do botão, conforme o PDF |
| 1x | Conjunto de jumpers; quantidade não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- D3 → TRIG; D2 → ECHO do HC-SR04
- D4 → sinal do servo da tampa
- A0 → botão com resistor externo para GND, pressionado = HIGH
- A4/SDA → SDA do módulo I2C; A5/SCL → SCL do módulo I2C (Arduino Uno)
- 5V → VCC dos módulos de 5 V; GND → referência comum, conferindo as ligações da montagem

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 3.7 Esquema.png" alt="Esquema elétrico - PRJ 3.7" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 3.7 Esquematico.pdf](./PRJ 3.7 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Ler fundo durante inicialização
2. Disparar sensor a cada 65 ms
3. Comparar distância com referência
4. Detectar nova presença
5. Abrir servo a 60° por 1 s
6. Somar até cinco porções
7. Aguardar ausência por 350 ms
8. Tratar botão com debounce de 30 ms
9. Mostrar estado no LCD

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>

const byte TRIG = 3, ECHO = 2, PINO_SERVO = 4, BOTAO = A0;
const byte LIMITE_PORCOES = 5;
const byte ANGULO_FECHADO = 0, ANGULO_ABERTO = 60;
const unsigned long TEMPO_ABERTO_MS = 1000;
const unsigned long INTERVALO_SENSOR_MS = 65;
const unsigned long AUSENCIA_MS = 350;
const float MARGEM_CM = 3.0; // Variacao em relacao ao fundo para indicar chegada.

Adafruit_LiquidCrystal lcd(0);
Servo tampa;
byte porcoes = 0;
bool confirmarReset = false;
unsigned long instanteReset = 0;
bool aberto = false, presente = false;
bool sensorPronto = false;
float fundoCm = 0;
unsigned long inicioCalibracao = 0, ultimoRetorno = 0;
unsigned long inicioAbertura = 0, ultimoDisparo = 0, ultimoEco = 0;

void mostrar() {
  lcd.clear();
  lcd.print("Porcoes: ");
  lcd.print(porcoes);
  lcd.print("/");
  lcd.print(LIMITE_PORCOES);
  lcd.setCursor(0, 1);
  if (confirmarReset) lcd.print("Contagem zerada");
  else if (!sensorPronto) lcd.print("Lendo o fundo");
  else if (aberto) lcd.print("Servindo...");
  else if (porcoes == LIMITE_PORCOES) lcd.print("Aperte o botao");
  else if (presente) lcd.print("Aguarde a saida");
  else lcd.print("Aguardando pet");
}

void verificarBotao() {
  static bool anterior = LOW, estavel = LOW;
  static unsigned long mudouEm = 0;
  bool leitura = digitalRead(BOTAO);
  unsigned long agora = millis();
  if (leitura != anterior) {
    anterior = leitura;
    mudouEm = agora;
  }
  if (leitura != estavel && agora - mudouEm >= 30) {
    estavel = leitura;
    if (estavel == HIGH) {
      porcoes = 0;
      instanteReset = agora;
      confirmarReset = true;
      mostrar();
    }
  }
}

void verificarPet() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  unsigned long pulso = pulseIn(ECHO, HIGH, 30000UL);
  float cm = pulso * 0.0343f / 2;
  unsigned long agora = millis();
  if (pulso) ultimoRetorno = agora;
  else if (agora - ultimoRetorno >= AUSENCIA_MS) fundoCm = 0;
  // Memoriza o fundo ao ligar e acompanha o alvo se ele for afastado.
  if ((!sensorPronto || !presente) && fundoCm > 0 && cm > fundoCm) fundoCm = cm;
  if (!sensorPronto) {
    if (pulso && fundoCm == 0) fundoCm = cm;
    if (agora - inicioCalibracao >= AUSENCIA_MS) {
      sensorPronto = true;
      mostrar();
    }
    return;
  }
  float margem = presente ? MARGEM_CM / 2 : MARGEM_CM;
  if (pulso && (fundoCm == 0 || fundoCm - cm >= margem)) {
    ultimoEco = agora;
    if (presente) return;
    presente = true;
    if (!aberto && porcoes < LIMITE_PORCOES) {
      confirmarReset = false;
      if (!tampa.attached()) tampa.attach(PINO_SERVO);
      tampa.write(ANGULO_ABERTO);
      inicioAbertura = agora;
      aberto = true;
      ++porcoes;
      mostrar();
    }
  } else if (presente && agora - ultimoEco >= AUSENCIA_MS) {
    presente = false;
    mostrar();
  }
}

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(BOTAO, INPUT); // Resistor externo para GND; pressionado = HIGH.
  // Manter o sinal em LOW, sem pulsos de servo, ate a primeira visita.
  digitalWrite(PINO_SERVO, LOW);
  pinMode(PINO_SERVO, OUTPUT);
  Wire.begin();
  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);
  mostrar();
  inicioCalibracao = millis();
}

void loop() {
  unsigned long agora = millis();
  if (confirmarReset && agora - instanteReset >= 1000UL) {
    confirmarReset = false;
    mostrar();
  }
  if (aberto && agora - inicioAbertura >= TEMPO_ABERTO_MS) {
    tampa.write(ANGULO_FECHADO);
    aberto = false;
    mostrar();
  }
  verificarBotao();
  if (agora - ultimoDisparo >= INTERVALO_SENSOR_MS) {
    ultimoDisparo = agora;
    verificarPet();
  }
}
```

📁 **Arquivo fonte compilável:** [`PRJ 3.7 Comedouro Pet.ino`](./PRJ 3.7 Comedouro Pet.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Monte uma pequena tampa ou comporta de papelão com peças leves, usando bolinhas de papel para representar a dose. Não teste o protótipo diretamente com animais.
2. Com alimentação desligada, ligue TRIG em D3, ECHO em D2, sinal do servo em D4 e botão em A0 com polarização externa para GND.
3. Ligue LCD a SDA/SCL e confira alimentação e GND comum. Instale Adafruit LiquidCrystal e abra o .ino completo com Servo.h.
4. Coloque um fundo estável diante do sensor e deixe a área sem aproximações ao ligar. O programa aprende uma referência inicial e não fixa um alcance absoluto de acionamento. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre limite de porções e abertura por evento; para executar, use PRJ 3.7 Comedouro Pet.ino completo (trecho nas linhas 85–93).
5. Aproxime um objeto o suficiente para reduzir a distância em pelo menos 3 cm. Observe uma abertura de 60° por um segundo; afaste o objeto e aguarde a confirmação de ausência para repetir.
6. Repita até cinco porções e confirme o bloqueio; pressione o botão para zerar. O fonte só associa o servo na primeira visita, sem comandar fechamento em setup(), portanto confira manualmente a posição inicial da comporta. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Referência de Fundo: fundoCm guarda uma distância observada e pode acompanhar um alvo afastado. A comparação usa variação relativa, diferente de projetos que acionam apenas abaixo de uma distância fixa.

2) Uma Visita por Evento: presente impede nova dose enquanto o mesmo objeto permanece detectado. A ausência por 350 ms permite rearmar; uma margem menor durante a presença ajuda a manter o estado sem alternância imediata.

3) Porções e Temporização: O limite é cinco eventos de abertura e não uma massa de ração. millis() fecha o servo após um segundo e permite verificar o botão durante o funcionamento, sem pausa longa bloqueante.

4) Inicialização Mecânica: O sinal começa em LOW e o servo só recebe attach() na primeira visita. Assim, não existe comando inicial para levar a tampa a 0°; a posição da maquete precisa ser conferida antes do teste.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Registrar aproximações, aberturas e porções no LCD até alcançar o limite de cinco.
- **Nível Intermediário:** Alterar o tempo de abertura em uma cópia do fonte e comparar a quantidade de bolinhas de papel liberadas.
- **Nível Avançado:** Adicionar um fechamento controlado na inicialização e testar perda de eco e reset durante uma abertura, mantendo os mesmos componentes.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Comedouro Pet.png`](./Comedouro Pet.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 3.7 Comedouro Pet.ino`](./PRJ 3.7 Comedouro Pet.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 3.7 Comedouro Pet.json`](./PRJ 3.7 Comedouro Pet.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`PRJ 3.7 Esquema.png`](./PRJ 3.7 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 3.7 Esquematico.pdf`](./PRJ 3.7 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
