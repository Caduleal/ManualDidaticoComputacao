# 🚀 PRJ 4.4 — Cofre Digital

> **Etapa de Ensino:** Módulo IV - Ensino Médio  
> **Nível de Complexidade:** `Avançado` | **Tempo Estimado:** `3 h/aula (180 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Cofre Digital.png" alt="Cofre Digital" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Cofre Digital (PRJ 4.4)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 4.4` |
| **Título do Projeto** | Cofre Digital |
| **Módulo Curricular** | Módulo IV - Ensino Médio |
| **Complexidade Didática** | `Avançado` |
| **Duração Estimada** | 3 h/aula (180 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Varredura de teclado, comparação de strings, funções e controle de servo. Compreender a diferença entre esconder caracteres na interface e proteger uma credencial.

### 💡 Habilidades de Pensamento Computacional:
- Validação de senha
- Controle de estados aberto/fechado
- Limitação do tamanho da entrada
- Integração de interface e atuador

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Fechaduras com senha relacionam uma informação digitada a uma autorização. A interface precisa comunicar se a entrada foi aceita e qual é o estado da porta. Uma maquete ajuda a discutir privacidade e segurança, percebendo que esconder os dígitos no LCD não protege uma senha que permanece escrita no próprio programa.
- **Matematica:** Comparar sequências de dígitos, contar posições até o limite de oito caracteres e relacionar comandos de 0° e 90° ao deslocamento de uma trava leve.

---

## 📖 Contextualização Histórica e Problema Real

Como liberar uma trava depois de conferir uma sequência digitada? O teclado recebe até oito dígitos e o LCD mostra asteriscos; D compara a entrada com a senha fixa 1234. Se corresponder, o servo vai a 90° e o estado muda para aberto; A fecha a 0° e * limpa a digitação quando fechado. O modelo demonstra uma autorização simples, sem resistência mecânica ou proteção de credenciais de um cofre real.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | LCD 16x2 I2C compatível com Adafruit_LiquidCrystal, configurado com deslocamento 0 em relação a 0x20 |
| 1x | Teclado matricial 4x4 |
| 1x | Microservo |
| 1x | Conjunto de jumpers; quantidade não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- A0–A3 → linhas 1–4 do teclado
- D2–D5 → colunas 1–4, INPUT_PULLUP
- D13 → sinal do servo (servoPin)
- Servo → alimentação compatível com o modelo; GND comum com o Uno
- A4/SDA → SDA do módulo I2C; A5/SCL → SCL do módulo I2C (Arduino Uno)
- 5V → VCC dos módulos de 5 V; GND → referência comum, conferindo as ligações da montagem

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 4.4 Esquema.png" alt="Esquema elétrico - PRJ 4.4" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Inicializar servo fechado a 0°
2. Varrer teclado e estabilizar tecla
3. Acumular até oito dígitos
4. Mostrar asteriscos no LCD
5. Receber D para comparar senha
6. Abrir a 90° se válida
7. Mostrar erro se inválida
8. Fechar com A ou limpar com *

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>
#include <Servo.h>

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
// CONFIGURACAO DO SERVO MOTOR
// =======================================

Servo servoCofre;

const int servoPin = 13;

const int posicaoFechado = 0;
const int posicaoAberto = 90;

bool cofreAberto = false;

// =======================================
// CONFIGURACAO DA SENHA
// =======================================

String senhaCorreta = "1234";
String senhaDigitada = "";

// =======================================
// INICIALIZACAO
// =======================================

void setup() {

  // Inicializa o LCD
  lcd.begin(16, 2);
  lcd.setBacklight(1);
  lcd.clear();

  // Configura as linhas do teclado
  for (int i = 0; i < 4; i++) {
    pinMode(linhas[i], OUTPUT);
    digitalWrite(linhas[i], HIGH);
  }

  // Configura as colunas do teclado
  for (int i = 0; i < 4; i++) {
    pinMode(colunas[i], INPUT_PULLUP);
  }

  // Inicializa o servo motor
  servoCofre.attach(servoPin);

  // Cofre inicia fechado
  servoCofre.write(posicaoFechado);

  mostrarTelaInicial();
}

// =======================================
// FUNCAO PARA LER O TECLADO
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
// MOSTRAR TELA INICIAL
// =======================================

void mostrarTelaInicial() {

  senhaDigitada = "";

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("COFRE DIGITAL");

  lcd.setCursor(0, 1);
  lcd.print("Digite a senha");
}

// =======================================
// ATUALIZAR SENHA NO LCD
// =======================================

void atualizarLCD() {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("DIGITE A SENHA:");

  lcd.setCursor(0, 1);

  // Mostra asteriscos no lugar dos numeros
  for (int i = 0; i < senhaDigitada.length(); i++) {
    lcd.print("*");
  }
}

// =======================================
// ABRIR COFRE
// =======================================

void abrirCofre() {

  servoCofre.write(posicaoAberto);

  cofreAberto = true;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("ACESSO LIBERADO");

  lcd.setCursor(0, 1);
  lcd.print("COFRE ABERTO");

  senhaDigitada = "";
}

// =======================================
// FECHAR COFRE
// =======================================

void fecharCofre() {

  servoCofre.write(posicaoFechado);

  cofreAberto = false;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("COFRE FECHADO");

  lcd.setCursor(0, 1);
  lcd.print("Aguarde...");

  delay(1500);

  mostrarTelaInicial();
}

// =======================================
// VERIFICAR SENHA
// =======================================

void verificarSenha() {

  if (cofreAberto) {
    return;
  }

  if (senhaDigitada == senhaCorreta) {

    abrirCofre();

  } else {

    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print("SENHA INVALIDA");

    lcd.setCursor(0, 1);
    lcd.print("TENTE NOVAMENTE");

    delay(2000);

    mostrarTelaInicial();
  }
}

// =======================================
// LOOP PRINCIPAL
// =======================================

void loop() {

  // Leitura do teclado
  char tecla = lerTeclado();

  if (tecla == '\0') {
    return;
  }

  // Elimina ruido do botao
  delay(30);

  if (lerTeclado() != tecla) {
    return;
  }

  // Espera soltar o botao
  while (lerTeclado() != '\0') {
    delay(10);
  }

  delay(30);

  // =====================================
  // TECLA A : FECHAR COFRE
  // =====================================

  if (tecla == 'A') {

    fecharCofre();
    return;
  }

  // =====================================
  // TECLA * : LIMPAR SENHA
  // =====================================

  if (tecla == '*') {

    if (!cofreAberto) {
      mostrarTelaInicial();
    }

    return;
  }

  // =====================================
  // TECLAS NUMERICAS
  // =====================================

  if (tecla >= '0' && tecla <= '9') {

    if (!cofreAberto) {

      if (senhaDigitada.length() < 8) {
        senhaDigitada += tecla;
      }

      atualizarLCD();
    }

    return;
  }

  // =====================================
  // TECLA D : CONFIRMAR SENHA
  // =====================================

  if (tecla == 'D') {

    verificarSenha();
    return;
  }
}
```

📁 **Arquivo fonte compilável:** [`PRJ 4.4 Cofre Digital.ino`](./PRJ 4.4 Cofre Digital.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Construa uma porta de papelão com trava leve, sem guardar objetos de valor. Identifique os fios do servo e os terminais do teclado com alimentação desligada.
2. Ligue linhas a A0–A3 e colunas a D2–D5. Conecte o sinal do servo a D13 e confira fonte e GND comum antes de fixar a alavanca.
3. Conecte LCD a SDA/SCL, 5V e GND. Instale Adafruit LiquidCrystal e abra o .ino completo com Servo.h; o trecho no JSON destaca a comparação da senha.
4. Carregue e confirme a posição inicial de 0°. Digite 1234 e pressione D; observe a abertura a 90° e a mensagem de acesso liberado. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre verificação da senha e mensagem de acesso inválido; para executar, use PRJ 4.4 Cofre Digital.ino completo (trecho nas linhas 186–210).
5. Pressione A para fechar. Teste senha diferente, * para limpar e mais de oito dígitos, observando as regras do programa sem forçar o servo mecanicamente.
6. Discuta que a senha está visível no fonte, não há limite de tentativas e o servo só move uma maquete. Não apresente o circuito como proteção física ou digital de bens. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Comparação de Sequências: senhaDigitada é comparada com senhaCorreta somente quando o cofre está fechado. A igualdade entre strings exige a mesma ordem de caracteres; uma permutação com os mesmos dígitos não é aceita.

2) Estado Mecânico e Lógico: abrirCofre() e fecharCofre() enviam ângulos e alteram cofreAberto. O programa não possui sensor de posição, portanto o estado lógico indica o comando enviado, não uma confirmação física da porta.

3) Interface Limitada: O LCD substitui cada dígito por asterisco e a entrada é limitada a oito caracteres. Isso evita mostrar a sequência a quem olha a tela, mas não cifra nem remove a senha armazenada no código.

4) Segurança do Modelo: A senha 1234 é fixa e não existe bloqueio por tentativas. Melhorias podem ser estudadas no mesmo kit, porém autenticação robusta e resistência da trava ultrapassam o que este protótipo demonstra.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Trocar a senha em uma cópia do fonte e elaborar testes de aceitação e rejeição.
- **Nível Intermediário:** Adicionar contador de erros e espera temporária com millis(), permitindo reinício do teste sem travar a interface.
- **Nível Avançado:** Acrescentar um botão ou fim de curso em pino livre para comparar a posição física da porta com o estado cofreAberto, mantendo a trava de papelão.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Cofre Digital.png`](./Cofre Digital.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 4.4 Cofre Digital.ino`](./PRJ 4.4 Cofre Digital.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 4.4 Cofre Digital.json`](./PRJ 4.4 Cofre Digital.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`PRJ 4.4 Esquema.png`](./PRJ 4.4 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 4.4 Esquemático.pdf`](./PRJ 4.4 Esquemático.pdf) | Documento esquemático / técnico em PDF de alta resolução |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
