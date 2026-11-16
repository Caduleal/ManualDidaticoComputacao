# 🚀 PRJ 4.6 — Radar de Velocidade

> **Etapa de Ensino:** Módulo IV - Ensino Médio  
> **Nível de Complexidade:** `Avançado` | **Tempo Estimado:** `3 h/aula (180 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Radar de Velocidade.png" alt="Radar de Velocidade" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Radar de Velocidade (PRJ 4.6)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 4.6` |
| **Título do Projeto** | Radar de Velocidade |
| **Módulo Curricular** | Módulo IV - Ensino Médio |
| **Complexidade Didática** | `Avançado` |
| **Duração Estimada** | 3 h/aula (180 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Leitura ultrassônica, diferença entre distância e deslocamento, unidades de tempo, ponto flutuante e uso de micros()/millis(). Interpretar resultados de um sensor com incerteza.

### 💡 Habilidades de Pensamento Computacional:
- Amostragem de grandezas
- Cálculo por diferenças sucessivas
- Validação de faixa e timeout
- Controle de estados de medição e exibição

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Medir movimento permite estudar deslocamentos e comparar experiências com critérios comuns. Equipamentos profissionais usam métodos e calibração apropriados à aplicação. O nome radar aproxima o tema do cotidiano, mas este protótipo usa ultrassom e serve para investigar movimento na direção do sensor, sem equivaler a um instrumento de fiscalização.
- **Matematica:** Calcular velocidade como Δdistância/Δtempo, converter centímetros em metros e microssegundos em segundos e multiplicar m/s por 3,6 para obter km/h.

---

## 📖 Contextualização Histórica e Problema Real

Como estimar a rapidez de um objeto que se aproxima ou se afasta? O sensor mede duas distâncias em instantes sucessivos e o programa divide a variação pelo tempo decorrido. Ao atingir módulo de pelo menos 0,10 m/s, congela uma estimativa e a mostra por três segundos no LCD. A medição representa a componente radial do movimento e pode sofrer variações por ecos e posicionamento do alvo.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | LCD 16x2 I2C compatível com Adafruit_LiquidCrystal, configurado com deslocamento 0 em relação a 0x20 |
| 1x | Sensor HC-SR04 |
| 1x | Conjunto de jumpers; quantidade não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- D3 → TRIG; D2 → ECHO do HC-SR04
- A4/SDA → SDA do módulo I2C; A5/SCL → SCL do módulo I2C (Arduino Uno)
- 5V → VCC dos módulos de 5 V; GND → referência comum, conferindo as ligações da montagem

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 4.6 Esquema.png" alt="Esquema elétrico - PRJ 4.6" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 4.6 Esquematico.pdf](./PRJ 4.6 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Disparar HC-SR04
2. Validar eco entre 2 e 300 cm
3. Guardar primeira leitura válida
4. Calcular intervalo entre instantes
5. Calcular velocidade em m/s
6. Comparar módulo com 0,10 m/s
7. Mostrar m/s e km/h
8. Aguardar 3 s sem novas medições
9. Retomar monitoramento

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <math.h>

// LCD I2C
Adafruit_LiquidCrystal lcd(0);

// SENSOR HC-SR04
const int trigPin = 3;
const int echoPin = 2;

// CONFIGURACOES
const float velocidadeSom = 0.0343; // cm/us
const float distanciaMinima = 2.0;  // cm
const float distanciaMaxima = 300.0; // cm

// INTERVALO ENTRE LEITURAS
const unsigned long intervaloLeitura = 30000UL; // 30 ms

// TEMPO DE EXIBICAO
const unsigned long tempoExibicao = 3000UL; // 3 segundos

// LIMIAR DE MOVIMENTO
const float velocidadeMinima = 0.10; // m/s

// VARIAVEIS
float distanciaAtual = 0;
float distanciaAnterior = 0;

float velocidade = 0;
float velocidadeCapturada = 0;

unsigned long tempoAnterior = 0;
unsigned long ultimaLeitura = 0;
unsigned long inicioExibicao = 0;

bool primeiraLeitura = true;

// ESTADOS
// 0 = Monitorando
// 1 = Exibindo resultado
int estado = 0;

// MEDIR DISTANCIA
float medirDistancia() {

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long duracao =
      pulseIn(echoPin, HIGH, 20000UL);

  if (duracao == 0) {
    return -1;
  }

  float distancia =
      duracao * velocidadeSom / 2.0;

  if (distancia < distanciaMinima ||
      distancia > distanciaMaxima) {
    return -1;
  }

  return distancia;
}

// MOSTRAR VELOCIDADE
void mostrarVelocidade(float v) {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("V: ");
  lcd.print(v, 2);
  lcd.print(" m/s");

  lcd.setCursor(0, 1);
  lcd.print("Km/h: ");
  lcd.print(v * 3.6, 2);
}

// CONFIGURACAO
void setup() {

  Serial.begin(115200);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  digitalWrite(trigPin, LOW);

  Wire.begin();

  lcd.begin(16, 2);
  lcd.setBacklight(HIGH);

  lcd.setCursor(0, 0);
  lcd.print("MEDIDOR DE");

  lcd.setCursor(0, 1);
  lcd.print("VELOCIDADE");

  delay(1500);

  lcd.clear();
  lcd.print("Monitorando...");
}

// PROGRAMA
void loop() {

  unsigned long agora = micros();

  // ESTADO 1: EXIBIR VELOCIDADE POR 3 SEGUNDOS
  if (estado == 1) {

    if (millis() - inicioExibicao >= tempoExibicao) {

      estado = 0;
      primeiraLeitura = true;

      ultimaLeitura = micros();

      lcd.clear();
      lcd.print("Monitorando...");
    }

    return;
  }

  // CONTROLAR FREQUENCIA
  if (agora - ultimaLeitura < intervaloLeitura) {
    return;
  }

  ultimaLeitura = agora;

  // LER SENSOR
  distanciaAtual = medirDistancia();

  unsigned long instante = micros();

  // VERIFICAR OBJETO
  if (distanciaAtual < 0) {

    primeiraLeitura = true;

    return;
  }

  // PRIMEIRA LEITURA VALIDA
  if (primeiraLeitura) {

    distanciaAnterior = distanciaAtual;
    tempoAnterior = instante;

    primeiraLeitura = false;

    return;
  }

  // CALCULAR DIFERENCAS
  float deltaDistancia =
      distanciaAtual - distanciaAnterior;

  float deltaTempo =
      (instante - tempoAnterior) / 1000000.0;

  // VELOCIDADE
  if (deltaTempo > 0) {

    velocidade =
      (deltaDistancia / 100.0) / deltaTempo;
  }

  // ATUALIZAR LEITURAS
  distanciaAnterior = distanciaAtual;
  tempoAnterior = instante;

  // MONITOR SERIAL
  Serial.print("Distancia: ");
  Serial.print(distanciaAtual, 2);

  Serial.print(" cm | Velocidade: ");
  Serial.print(velocidade, 3);
  Serial.println(" m/s");

  // DETECTAR MOVIMENTO
  if (fabs(velocidade) >= velocidadeMinima) {

    velocidadeCapturada = fabs(velocidade);

    // MOSTRAR RESULTADO
    mostrarVelocidade(velocidadeCapturada);

    Serial.println("OBJETO DETECTADO!");

    Serial.print("Velocidade capturada: ");
    Serial.print(velocidadeCapturada, 3);
    Serial.println(" m/s");

    // INICIAR EXIBICAO
    inicioExibicao = millis();
    estado = 1;
  }
}
```

📁 **Arquivo fonte compilável:** [`PRJ 4.6 Radar de Velocidade.ino`](./PRJ 4.6 Radar de Velocidade.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Prepare um alvo plano que possa ser movido lentamente sobre a mesa na direção do sensor. Evite interpretar movimento lateral como deslocamento radial.
2. Com USB desligado, conecte TRIG a D3, ECHO a D2 e alimentação do sensor a 5V/GND. Ligue o LCD ao barramento I2C do Uno.
3. Instale Adafruit LiquidCrystal e abra o .ino completo com Wire.h e math.h. O trecho no JSON mostra o cálculo de diferenças, não toda a aquisição necessária.
4. Carregue e abra o Monitor Serial a 115200 baud. Mantenha o alvo na faixa de 2 a 300 cm e observe o sinal da velocidade ao aproximar e afastar. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre velocidade por diferença de distância e tempo; para executar, use PRJ 4.6 Radar de Velocidade.ino completo (trecho nas linhas 169–184).
5. Movimente o alvo até superar o limiar de 0,10 m/s. O LCD mostra o módulo em m/s e a conversão para km/h durante três segundos, sem realizar novas medidas nesse estado.
6. Compare várias tentativas com um deslocamento e tempo conhecidos. Registre dispersão e ecos inválidos; não use a estimativa para fiscalização, controle de veículos ou decisões que exijam instrumento calibrado. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Distância e Tempo: O eco é convertido em centímetros e validado antes do cálculo. O instante de cada leitura é obtido com micros(); o intervalo de 30000 µs organiza as amostras sem garantir um período perfeitamente constante.

2) Velocidade por Diferença: A expressão divide a variação de distância em metros pelo tempo em segundos. Aproximação pode produzir sinal negativo e afastamento positivo; fabs() remove o sinal quando o valor é capturado para exibição.

3) Unidades e Apresentação: mostrarVelocidade() apresenta m/s e multiplica por 3,6 para km/h. O limiar de 0,10 m/s dispara o estado de exibição, que dura três segundos antes de reiniciar a referência de leitura.

4) Limites do Método: O sensor observa apenas a mudança de distância ao alvo e não toda a trajetória no espaço. Pequenas diferenças de eco podem aumentar o erro do cálculo, por isso o trabalho deve comparar repetibilidade e não prometer precisão profissional.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Conferir manualmente a conversão de três velocidades entre m/s e km/h.
- **Nível Intermediário:** Registrar leituras com o alvo parado e em movimento e comparar dispersão e falsos disparos.
- **Nível Avançado:** Em uma cópia do fonte, calcular velocidade por uma janela de várias amostras e comparar ruído e atraso da resposta com o método de duas leituras.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`PRJ 4.6 Esquema.png`](./PRJ 4.6 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 4.6 Esquematico.pdf`](./PRJ 4.6 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 4.6 Radar de Velocidade.ino`](./PRJ 4.6 Radar de Velocidade.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 4.6 Radar de Velocidade.json`](./PRJ 4.6 Radar de Velocidade.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`Radar de Velocidade.png`](./Radar de Velocidade.png) | Fotografia / Identidade visual de capa do projeto |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
