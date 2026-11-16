# 🚀 PRJ 3.3 — Alarme de Incêndio

> **Etapa de Ensino:** Módulo III - Ensino Fundamental II  
> **Nível de Complexidade:** `Avançado` | **Tempo Estimado:** `3 h/aula (180 min), incluindo revisão da montagem`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Alarme de Incêndio .png" alt="Alarme de Incêndio" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Alarme de Incêndio (PRJ 3.3)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 3.3` |
| **Título do Projeto** | Alarme de Incêndio |
| **Módulo Curricular** | Módulo III - Ensino Fundamental II |
| **Complexidade Didática** | `Avançado` |
| **Duração Estimada** | 3 h/aula (180 min), incluindo revisão da montagem |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Leitura analógica, conversão do TMP36, operadores lógicos e temporização com millis(). Distinguir um protótipo didático de um equipamento de proteção certificado.

### 💡 Habilidades de Pensamento Computacional:
- Histerese em decisões
- Combinação lógica de sensores
- Temporização sem delay() no ciclo principal
- Diagnóstico de disponibilidade I2C

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Alertas visuais e sonoros ajudam a chamar atenção para uma condição que precisa ser verificada. A automação permite acompanhar mais de uma variável ao mesmo tempo. O projeto escolar usa esse princípio para discutir responsabilidade ao interpretar sensores, sem atribuir ao protótipo a confiabilidade de um sistema real de proteção contra incêndio.
- **Matematica:** Comparar limiares de disparo e retorno, converter leitura do TMP36 em graus Celsius e relacionar intervalos de 200, 250 e 500 ms com tarefas diferentes.

---

## 📖 Contextualização Histórica e Problema Real

Como sinalizar quando uma medida ultrapassa uma faixa escolhida? O programa combina leitura bruta de gás e temperatura, acionando luz e som se qualquer alarme estiver ativo. Limiares diferentes de disparo e retorno evitam alternância perto da fronteira. O próprio fonte informa problemas de GND e do resistor do sensor de gás; a montagem deve ser revisada antes de interpretar resultados.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | LCD 16x2 I2C compatível com Adafruit_LiquidCrystal, configurado com deslocamento 0 em relação a 0x20 |
| 1x | Sensor TMP36 |
| 1x | Sensor de gás da montagem; modelo não confirmado no PDF |
| 1x | LED vermelho |
| 1x | Resistor de 220 Ω para o LED |
| 1x | Resistor de 4,7 kΩ indicado no circuito de gás |
| 1x | Piezo/buzzer |
| 1x | Protoboard, conforme a imagem da montagem |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- A0 → leitura de gás (PINO_GAS)
- A1 → VOUT do TMP36 (PINO_TEMPERATURA)
- A2 → LED vermelho via resistor de 220 Ω (PINO_LED, saída digital)
- D6 → piezo (PINO_PIEZO)
- A4/SDA e A5/SCL → LCD MCP23008, endereço 0x20
- 5V/GND → alimentação e referência a revisar: o fonte avisa ausência de GND comum e resistor de 4,7 kΩ ligado ao +5V

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 3.3 Esquema.png" alt="Esquema elétrico - PRJ 3.3" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 3.3 Esquematico.pdf](./PRJ 3.3 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Consultar LCD em 0x20
2. Ler gás A0 e TMP36 A1
3. Converter temperatura
4. Aplicar histerese dos dois sensores
5. Combinar alarmes com OU lógico
6. Alternar LED e piezo a cada 250 ms
7. Atualizar LCD e serial a cada 500 ms
8. Repetir leitura a cada 200 ms

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
/*
  Projeto 3.3 - Alarme de Incendio | Arduino Uno R3 / Tinkercad
  TMP36: A1 | Gas: A0 | LED: A2 | Piezo: D6
  LCD 16x2 I2C MCP23008: SDA/SCL, endereco 0x20 (32).

  A montagem original foi preservada por solicitacao do usuario.
  ATENCAO: o esquema nao une o negativo da protoboard ao GND do Uno,
  e o resistor de 4,7 kohms do gas termina em +5 V. O software nao
  corrige essas ligacoes: leituras e atuacao podem nao funcionar.
  Consulte as limitacoes e o roteiro de testes no README.md.
*/

#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <stdio.h>
#include <stdlib.h>

const byte PINO_GAS = A0;
const byte PINO_TEMPERATURA = A1;
const byte PINO_LED = A2;
const byte PINO_PIEZO = 6;
const byte ENDERECO_LCD = 0x20;

// O construtor recebe o deslocamento em relacao a 0x20.
// Deslocamento zero corresponde ao endereco confirmado: 0x20.
Adafruit_LiquidCrystal lcd(ENDERECO_LCD - 0x20);

// Valores iniciais didaticos, ajustaveis; nao representam calibracao.
const float TEMPERATURA_DISPARO_C = 50.0;
const float TEMPERATURA_RETORNO_C = 45.0;
const int GAS_DISPARO = 400;
const int GAS_RETORNO = 350;
const float TENSAO_REFERENCIA = 5.0;

const unsigned long INTERVALO_LEITURA_MS = 200;
const unsigned long INTERVALO_EXIBICAO_MS = 500;
const unsigned long INTERVALO_AVISO_MS = 250;
const unsigned int FREQUENCIA_PIEZO_HZ = 2000;

int leituraGas = 0;
int leituraTemperatura = 0;
float temperaturaC = 0.0;
bool alarmeGas = false;
bool alarmeTemperatura = false;
bool avisoLigado = false;
bool lcdDisponivel = false;
unsigned long ultimaLeitura = 0;
unsigned long ultimaExibicao = 0;
unsigned long ultimaAlternancia = 0;

void inicializarLCD() {
  Wire.begin();
#if defined(WIRE_HAS_TIMEOUT)
  // Evita espera indefinida se o barramento ficar preso, quando suportado.
  Wire.setWireTimeout(25000UL, true);
#endif
  Wire.beginTransmission(ENDERECO_LCD);
  lcdDisponivel = (Wire.endTransmission() == 0);

  if (lcdDisponivel) {
    // Nao depende do valor de retorno de begin(), que varia entre versoes.
    lcd.begin(16, 2);
    lcd.setBacklight(1);
  } else {
    Serial.println(F("LCD 0x20 sem resposta. Confira alimentacao e GND."));
  }
}

void lerSensores() {
  leituraGas = analogRead(PINO_GAS);
  leituraTemperatura = analogRead(PINO_TEMPERATURA);

  // TMP36: 500 mV em 0 graus C e incremento de 10 mV/grau C.
  const float tensao = leituraTemperatura * (TENSAO_REFERENCIA / 1023.0);
  temperaturaC = (tensao - 0.5) * 100.0;
}

void atualizarEstadoAlarme() {
  // Histerese: o limite de retorno e menor para evitar oscilacoes.
  if (temperaturaC >= TEMPERATURA_DISPARO_C) {
    alarmeTemperatura = true;
  } else if (temperaturaC <= TEMPERATURA_RETORNO_C) {
    alarmeTemperatura = false;
  }

  if (leituraGas >= GAS_DISPARO) {
    alarmeGas = true;
  } else if (leituraGas <= GAS_RETORNO) {
    alarmeGas = false;
  }
}

void aplicarAviso(bool ligar) {
  digitalWrite(PINO_LED, ligar ? HIGH : LOW);
  if (ligar) {
    tone(PINO_PIEZO, FREQUENCIA_PIEZO_HZ);
  } else {
    noTone(PINO_PIEZO);
  }
}

void atualizarAvisos(unsigned long agora) {
  static bool alarmeAnterior = false;
  const bool alarmeAtual = alarmeGas || alarmeTemperatura;

  if (alarmeAtual != alarmeAnterior) {
    // Comeca a sinalizar imediatamente quando o alarme dispara.
    avisoLigado = alarmeAtual;
    ultimaAlternancia = agora;
    aplicarAviso(avisoLigado);
    alarmeAnterior = alarmeAtual;
  }

  if (alarmeAtual && agora - ultimaAlternancia >= INTERVALO_AVISO_MS) {
    ultimaAlternancia = agora;
    avisoLigado = !avisoLigado;
    aplicarAviso(avisoLigado);
  }
}

const char* obterEstado() {
  if (alarmeGas && alarmeTemperatura) return "ALARME: GAS/TEMP";
  if (alarmeGas) return "ALARME: GAS";
  if (alarmeTemperatura) return "ALARME: TEMP";
  return "NORMAL";
}

void escreverLinhaLCD(byte linha, const char* texto) {
  lcd.setCursor(0, linha);
  byte coluna = 0;
  while (coluna < 16 && texto[coluna] != '\0') {
    lcd.print(texto[coluna]);
    ++coluna;
  }
  // Apaga caracteres antigos sem executar clear() a cada atualizacao.
  while (coluna < 16) {
    lcd.print(' ');
    ++coluna;
  }
}

void atualizarExibicao() {
  if (lcdDisponivel) {
    char textoTemperatura[10];
    char linha[17];
    // AVR nao habilita %f no snprintf por padrao; dtostrf faz a conversao.
    dtostrf(temperaturaC, 5, 1, textoTemperatura);
    snprintf(linha, sizeof(linha), "T:%s G:%4d", textoTemperatura, leituraGas);
    escreverLinhaLCD(0, linha);
    escreverLinhaLCD(1, obterEstado());
  }

  // Os valores brutos ajudam a diagnosticar a montagem original.
  Serial.print(F("A0="));
  Serial.print(leituraGas);
  Serial.print(F(" | A1="));
  Serial.print(leituraTemperatura);
  Serial.print(F(" | TMP36="));
  Serial.print(temperaturaC, 1);
  Serial.print(F(" C | "));
  Serial.println(obterEstado());
}

void setup() {
  pinMode(PINO_GAS, INPUT);
  pinMode(PINO_TEMPERATURA, INPUT);
  pinMode(PINO_LED, OUTPUT);
  pinMode(PINO_PIEZO, OUTPUT);
  aplicarAviso(false);
  Serial.begin(9600);
  Serial.println(F("Alarme 3.3: montagem original, sem alteracoes."));
  Serial.println(F("Verifique no README as limitacoes de GND e do divisor de gas."));
  inicializarLCD();

  lerSensores();
  atualizarEstadoAlarme();
  const unsigned long agora = millis();
  ultimaLeitura = agora;
  ultimaExibicao = agora;
  atualizarAvisos(agora);
  atualizarExibicao();
}

void loop() {
  const unsigned long agora = millis();

  // Subtracoes unsigned mantem a temporizacao valida apos o rollover.
  if (agora - ultimaLeitura >= INTERVALO_LEITURA_MS) {
    ultimaLeitura = agora;
    lerSensores();
    atualizarEstadoAlarme();
  }

  atualizarAvisos(agora);

  if (agora - ultimaExibicao >= INTERVALO_EXIBICAO_MS) {
    ultimaExibicao = agora;
    atualizarExibicao();
  }
}
```

📁 **Arquivo fonte compilável:** [`PRJ 3.3 Alarme de Incendio.ino`](./PRJ 3.3 Alarme de Incendio.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Leia os avisos iniciais do .ino. Ele informa que a montagem original não une o negativo da protoboard ao GND e que o resistor de gás termina em +5V; não considere as leituras validadas.
2. Antes de alimentar, peça ao professor que revise GND comum e circuito de leitura do gás. O README citado pelo fonte não existe na pasta recebida; as limitações conhecidas estão registradas aqui.
3. Confira os sinais A0 gás, A1 TMP36, A2 LED por resistor e D6 piezo. Ligue LCD a SDA/SCL e verifique o endereço 0x20 e a alimentação.
4. Instale Adafruit LiquidCrystal e abra o .ino completo. O recorte no JSON mostra a histerese; ele não inclui toda a inicialização, leitura e exibição necessárias para executar. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre histerese de temperatura e gás; para executar, use PRJ 3.3 Alarme de Incendio.ino completo (trecho nas linhas 78–91).
5. Carregue e use Monitor Serial a 9600 baud. Em simulação, teste temperatura de disparo em 50 °C e retorno em 45 °C, gás em 400 e retorno em 350; esses valores não representam calibração.
6. Compare alarmes separados e simultâneos e observe o aviso intermitente. Não use fogo, fumaça ou liberação de gás para testar; trabalhe com os controles do simulador e mantenha o protótipo restrito ao estudo. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Histerese: Temperatura liga em 50 °C e desliga em 45 °C; gás liga em leitura 400 e desliga em 350. Entre esses limites o estado anterior é mantido, reduzindo oscilações sem exigir novos componentes.

2) Tarefas Temporizadas: millis() organiza leitura em 200 ms, alternância do aviso em 250 ms e exibição em 500 ms. A leitura de sensores, a sinalização e a atualização do LCD são tratadas em funções diferentes.

3) Diagnóstico do LCD: O programa consulta 0x20 e só escreve no LCD se houver resposta. O Monitor Serial continua apresentando dados para diagnóstico, o que ajuda a separar uma falha do mostrador de uma condição dos sensores.

4) Limites Documentados: A leitura bruta do gás não equivale a concentração calibrada. As falhas de GND e da rede resistiva são avisadas no fonte, e nenhum software corrige uma ligação elétrica incorreta; o protótipo não é um dispositivo de proteção.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Em simulação, registrar os estados ao subir e descer a temperatura pelos dois limiares.
- **Nível Intermediário:** Criar uma tabela com as quatro combinações dos alarmes e conferir o resultado do OU lógico.
- **Nível Avançado:** Após revisão elétrica, acrescentar registro serial dos instantes de transição sem bloquear as tarefas, comparando leituras e eventos no simulador.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Alarme de Incêndio .png`](./Alarme de Incêndio .png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 3.3 Alarme de Incendio.ino`](./PRJ 3.3 Alarme de Incendio.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 3.3 Alarme de Incendio.json`](./PRJ 3.3 Alarme de Incendio.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`PRJ 3.3 Esquema.png`](./PRJ 3.3 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 3.3 Esquematico.pdf`](./PRJ 3.3 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
