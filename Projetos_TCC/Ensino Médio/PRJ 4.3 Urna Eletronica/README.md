# 🚀 PRJ 4.3 — Urna Eletrônica

> **Etapa de Ensino:** Módulo IV - Ensino Médio  
> **Nível de Complexidade:** `Avançado` | **Tempo Estimado:** `3 h/aula (180 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Urna Eletrônica.png" alt="Urna Eletrônica" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Urna Eletrônica (PRJ 4.3)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 4.3` |
| **Título do Projeto** | Urna Eletrônica |
| **Módulo Curricular** | Módulo IV - Ensino Médio |
| **Complexidade Didática** | `Avançado` |
| **Duração Estimada** | 3 h/aula (180 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Teclado matricial, strings, contadores, funções e porcentagens. Distinguir uma simulação de votação escolar de um sistema eleitoral com requisitos de segurança e sigilo.

### 💡 Habilidades de Pensamento Computacional:
- Validação e classificação de entradas
- Contagem por categorias
- Controle de encerramento
- Cálculo e apresentação de porcentagens

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Uma votação coletiva precisa de regras para registrar escolhas e conferir totais. A contagem eletrônica permite acompanhar categorias, mas também exige discutir transparência e privacidade. Nesta simulação, os estudantes podem organizar uma escolha fictícia da turma e observar que o próprio programa imprime na serial a categoria de cada voto, sem garantir sigilo.
- **Matematica:** Somar categorias de votos e calcular percentual como quantidade × 100 ÷ total. Comparar contagem absoluta, porcentagem e proteção contra divisão por zero.

---

## 📖 Contextualização Histórica e Problema Real

Como registrar votos e apresentar uma apuração por categoria? O teclado recebe 20 para Cadu, 10 para Ana, A para branco e outros números para nulo; # confirma e * corrige. A tecla D encerra quando há votos e nenhuma entrada pendente, passando a exibir porcentagens. Os dados ficam em RAM e o protótipo não controla identidade, voto único nem sigilo, servindo apenas como simulação.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | LCD 16x2 I2C compatível com Adafruit_LiquidCrystal, configurado com deslocamento 0 em relação a 0x20 |
| 1x | Teclado matricial 4x4 |
| 1x | Buzzer/piezo |
| 1x | Conjunto de jumpers; quantidade não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- A0–A3 → linhas 1–4 do teclado
- D2–D5 → colunas 1–4, INPUT_PULLUP
- D6 → buzzer/piezo; negativo → GND
- A4/SDA → SDA do módulo I2C; A5/SCL → SCL do módulo I2C (Arduino Uno)
- 5V → VCC dos módulos de 5 V; GND → referência comum, conferindo as ligações da montagem

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 4.3 Esquema.png" alt="Esquema elétrico - PRJ 4.3" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 4.3 Esquematico.pdf](./PRJ 4.3 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Inicializar contadores zerados
2. Varrer teclado
3. Receber número ou voto branco
4. Corrigir com * ou confirmar com #
5. Classificar e incrementar contadores
6. Mostrar confirmação e total na serial
7. Encerrar com D nas condições válidas
8. Alternar porcentagens no LCD

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

// =======================================
// CONFIGURACAO DO LCD
// =======================================

Adafruit_LiquidCrystal lcd(0);

// =======================================
// CONFIGURACAO DO TECLADO 4X4
// =======================================

const byte linhas[4] = {A0, A1, A2, A3};
const byte colunas[4] = {2, 3, 4, 5};

char teclas[4][4] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

// =======================================
// BUZZER
// =======================================

const int buzzer = 6;

// =======================================
// CONTADORES
// =======================================

int votosCadu = 0;
int votosAna = 0;
int votosBrancos = 0;
int votosNulos = 0;
int totalVotos = 0;

String numero = "";
bool encerrada = false;

// =======================================
// SONS
// =======================================

void somTecla() {
  tone(buzzer, 1200, 70);
  delay(90);
}

void somCorrecao() {
  tone(buzzer, 700, 100);
  delay(150);
  tone(buzzer, 700, 100);
  delay(150);
}

void somConfirmacao() {
  tone(buzzer, 1000, 150);
  delay(180);
  tone(buzzer, 1500, 400);
  delay(450);
}

// =======================================
// FUNCAO PARA LER O TECLADO
// MESMA LOGICA DA CALCULADORA
// =======================================

char lerTeclado() {

  for (int i = 0; i < 4; i++) {

    digitalWrite(linhas[i], LOW);
    delayMicroseconds(10);

    for (int j = 0; j < 4; j++) {

      if (digitalRead(colunas[j]) == LOW) {
        digitalWrite(linhas[i], HIGH);
        return teclas[i][j];
      }
    }

    digitalWrite(linhas[i], HIGH);
  }

  return '\0';
}

// =======================================
// TELA PARA PROXIMO ELEITOR
// =======================================

void mostrarInicio() {

  numero = "";

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Digite seu voto");

  lcd.setCursor(0, 1);
  lcd.print("Numero: ");
}

// =======================================
// MOSTRAR CONTAGEM NO SERIAL
// =======================================

void mostrarContagem() {

  Serial.println("--------------------");

  Serial.print("Cadu: ");
  Serial.println(votosCadu);

  Serial.print("Ana: ");
  Serial.println(votosAna);

  Serial.print("Brancos: ");
  Serial.println(votosBrancos);

  Serial.print("Nulos: ");
  Serial.println(votosNulos);

  Serial.print("Total: ");
  Serial.println(totalVotos);

  Serial.println("--------------------");
}

// =======================================
// REGISTRAR VOTO
// =======================================

void registrarVoto() {

  lcd.clear();

  if (numero == "20") {

    votosCadu++;
    lcd.print("Voto: CADU");
    Serial.println("Voto registrado: CADU");

  } else if (numero == "10") {

    votosAna++;
    lcd.print("Voto: ANA");
    Serial.println("Voto registrado: ANA");

  } else if (numero == "A") {

    votosBrancos++;
    lcd.print("Voto BRANCO");
    Serial.println("Voto registrado: BRANCO");

  } else {

    // 00 e outros numeros invalidos
    votosNulos++;
    lcd.print("Voto NULO");
    Serial.println("Voto registrado: NULO");
  }

  totalVotos++;

  lcd.setCursor(0, 1);
  lcd.print("CONFIRMADO!");

  somConfirmacao();

  mostrarContagem();

  delay(1000);

  mostrarInicio();
}

// =======================================
// ENCERRAR VOTACAO
// =======================================

void apurarVotos() {

  encerrada = true;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("VOTACAO");

  lcd.setCursor(0, 1);
  lcd.print("ENCERRADA!");

  tone(buzzer, 900, 300);

  Serial.println();
  Serial.println("===== RESULTADO FINAL =====");

  mostrarContagem();

  delay(2000);
}

// =======================================
// MOSTRAR PORCENTAGENS
// =======================================

void mostrarResultados() {

  float pCadu = 0;
  float pAna = 0;
  float pBranco = 0;
  float pNulo = 0;

  if (totalVotos > 0) {

    pCadu = votosCadu * 100.0 / totalVotos;
    pAna = votosAna * 100.0 / totalVotos;
    pBranco = votosBrancos * 100.0 / totalVotos;
    pNulo = votosNulos * 100.0 / totalVotos;
  }

  // CANDIDATOS
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("CADU: ");
  lcd.print(pCadu, 1);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("ANA: ");
  lcd.print(pAna, 1);
  lcd.print("%");

  delay(3000);

  // BRANCOS E NULOS
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("BRANCO: ");
  lcd.print(pBranco, 1);
  lcd.print("%");

  lcd.setCursor(0, 1);
  lcd.print("NULO: ");
  lcd.print(pNulo, 1);
  lcd.print("%");

  delay(3000);
}

// =======================================
// INICIALIZACAO
// =======================================

void setup() {

  Serial.begin(9600);

  lcd.begin(16, 2);
  lcd.setBacklight(1);
  lcd.clear();

  pinMode(buzzer, OUTPUT);

  // MESMA CONFIGURACAO DA CALCULADORA

  for (int i = 0; i < 4; i++) {
    pinMode(linhas[i], OUTPUT);
    digitalWrite(linhas[i], HIGH);
  }

  for (int i = 0; i < 4; i++) {
    pinMode(colunas[i], INPUT_PULLUP);
  }

  // ZERESIMA
  lcd.setCursor(0, 0);
  lcd.print("Cadu:0  Ana:0");

  lcd.setCursor(0, 1);
  lcd.print("Total votos: 0");

  Serial.println("=== URNA ELETRONICA ===");

  mostrarContagem();

  delay(3000);

  mostrarInicio();
}

// =======================================
// LOOP PRINCIPAL
// MESMA LEITURA DA CALCULADORA
// =======================================

void loop() {

  // Votacao encerrada
  if (encerrada) {
    mostrarResultados();
    return;
  }

  // Ler tecla
  char tecla = lerTeclado();

  if (tecla == '\0') {
    return;
  }

  // Eliminar ruido
  delay(30);

  if (lerTeclado() != tecla) {
    return;
  }

  // Esperar soltar a tecla
  while (lerTeclado() != '\0') {
    delay(10);
  }

  delay(30);

  // =====================================
  // TECLA D - ENCERRAR
  // =====================================

  if (tecla == 'D') {

    // Evita encerrar com numero incompleto
    if (numero.length() > 0) {
      lcd.clear();
      lcd.print("Corrija ou");
      lcd.setCursor(0, 1);
      lcd.print("confirme voto");
      delay(1200);
      mostrarInicio();
      return;
    }

    // Exige pelo menos um voto
    if (totalVotos == 0) {
      lcd.clear();
      lcd.print("Nenhum voto!");
      delay(1200);
      mostrarInicio();
      return;
    }

    apurarVotos();
    return;
  }

  // =====================================
  // TECLA * - CORRIGIR
  // =====================================

  if (tecla == '*') {

    somCorrecao();
    mostrarInicio();
    return;
  }

  // =====================================
  // TECLA # - CONFIRMAR
  // =====================================

  if (tecla == '#') {

    if (numero.length() > 0) {
      registrarVoto();
    }

    return;
  }

  // =====================================
  // TECLA A - VOTO BRANCO
  // =====================================

  if (tecla == 'A') {

    somTecla();

    numero = "A";

    lcd.setCursor(8, 1);
    lcd.print("BRANCO  ");

    return;
  }

  // =====================================
  // TECLAS NUMERICAS
  // =====================================

  if (tecla >= '0' && tecla <= '9') {

    if (numero == "A") {
      numero = "";
    }

    if (numero.length() < 2) {

      numero += tecla;

      somTecla();

      lcd.setCursor(8, 1);
      lcd.print("        ");

      lcd.setCursor(8, 1);
      lcd.print(numero);
    }

    return;
  }
}
```

📁 **Arquivo fonte compilável:** [`PRJ 4.3 Urna Eletronica.ino`](./PRJ 4.3 Urna Eletronica.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Identifique teclado, LCD e buzzer. Com USB desligado, ligue linhas do teclado a A0–A3 e colunas a D2–D5, respeitando o conector do modelo usado.
2. Ligue buzzer a D6 e GND e LCD ao barramento I2C, 5V e GND. Instale Adafruit LiquidCrystal e abra o .ino completo.
3. Carregue e confira os contadores zerados no início. Abra o Monitor Serial a 9600 baud e use apenas votos fictícios, pois a categoria registrada é impressa na serial.
4. Teste 20 e # para Cadu, 10 e # para Ana, A e # para branco e 00 e # para nulo. Use * para corrigir uma entrada antes da confirmação. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre classificação dos votos e atualização do total; para executar, use PRJ 4.3 Urna Eletronica.ino completo (trecho nas linhas 144–170).
5. Com pelo menos um voto e entrada vazia, pressione D. Observe a alternância dos percentuais dos candidatos e de brancos/nulos a cada três segundos.
6. Compare a soma dos contadores com totalVotos e calcule percentuais manualmente. Reiniciar a placa apaga a votação; não há cadastro de eleitores, bloqueio de voto repetido nem armazenamento persistente. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Classificação do Voto: registrarVoto() compara a string com 20, 10 e A; os demais conteúdos confirmados vão para nulos. O total é incrementado uma vez após essa escolha, e as mensagens ajudam a acompanhar a categoria registrada.

2) Apuração Percentual: Cada categoria é dividida pelo total e multiplicada por 100. A rotina verifica total maior que zero antes de dividir e alterna duas telas porque quatro resultados não cabem simultaneamente no LCD 16x2.

3) Estado Encerrado: encerrada desvia o loop para a apresentação contínua dos resultados. A tecla D exige ao menos um voto e ausência de entrada pendente; a operação não pode ser reaberta por uma tecla no programa atual.

4) Limites da Simulação: Os contadores estão na RAM e não resistem ao desligamento. A serial revela categorias de votos, não há autenticação e a mesma pessoa pode votar várias vezes; essas limitações devem orientar o uso exclusivamente didático.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Simular uma votação fictícia e conferir contagens e porcentagens com uma tabela manual.
- **Nível Intermediário:** Criar um conjunto de testes para entrada incompleta, correção, branco, nulo e encerramento sem votos.
- **Nível Avançado:** Em uma cópia do fonte, usar EEPROM para guardar apenas totais com estratégia de gravação controlada e discutir o que essa melhoria ainda não resolve sobre sigilo e voto único.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`PRJ 4.3 Esquema.png`](./PRJ 4.3 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 4.3 Esquematico.pdf`](./PRJ 4.3 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 4.3 Urna Eletronica.ino`](./PRJ 4.3 Urna Eletronica.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 4.3 Urna Eletronica.json`](./PRJ 4.3 Urna Eletronica.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`Urna Eletrônica.png`](./Urna Eletrônica.png) | Fotografia / Identidade visual de capa do projeto |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
