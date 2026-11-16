# 🚀 PRJ 2.8 — Dado Eletrônico

> **Etapa de Ensino:** Módulo II - Ensino Fundamental I  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Dado Eletrônico.png" alt="Dado Eletrônico" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Dado Eletrônico (PRJ 2.8)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 2.8` |
| **Título do Projeto** | Dado Eletrônico |
| **Módulo Curricular** | Módulo II - Ensino Fundamental I |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Contagem de 1 a 6, uso de botão e identificação de LEDs. Apresentar o display de sete segmentos e a ideia de um padrão que forma cada número.

### 💡 Habilidades de Pensamento Computacional:
- Vetores de padrões
- Laços de repetição
- Sorteio pseudoaleatório
- Estabilização do botão e detecção de soltura

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Dados são usados em jogos para produzir resultados que os participantes não escolhem diretamente. Uma versão eletrônica troca as faces físicas por números luminosos. A turma pode comparar sequências de lançamentos e discutir que obter resultados diferentes não significa que cada número aparecerá a mesma quantidade em poucas tentativas.
- **Matematica:** Contar frequências de 1 a 6, comparar quantidades e representar resultados em um gráfico simples. Identificar sete segmentos que formam diferentes algarismos.

---

## 📖 Contextualização Histórica e Problema Real

Como sortear um número de um a seis usando um botão? O programa aguarda um comando, anima os segmentos e apresenta um resultado gerado por random(1, 7). A primeira jogada usa o instante do acionamento para iniciar a sequência pseudoaleatória. Outra jogada só é permitida depois que o botão for solto, evitando vários sorteios pelo mesmo aperto.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | Display de sete segmentos de anodo comum |
| 1x | Botão |
| 1x | Resistor de 220 kΩ identificado como R1 no PDF, na rede do botão |
| 1x | Resistor de 100 Ω identificado como R2 no PDF, no comum do display |
| 1x | Protoboard, conforme a imagem da montagem |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- A0 → botão, INPUT com resistor externo para GND; pressionado = HIGH
- D6 → segmento a; D5 → b; D4 → c; D2 → d
- D3 → segmento e; D1 → f; D0 → g (ordem do vetor PINOS_SEGMENTOS)
- Comum do display → positivo via resistor conforme a imagem; segmentos acendem em LOW
- 5V/GND → rede de alimentação; D0 e D1 também são RX/TX do Uno

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 2.8 Esquema.png" alt="Esquema elétrico - PRJ 2.8" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 2.8 Esquematico.pdf](./PRJ 2.8 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Configurar os sete segmentos
2. Mostrar zero por 1 s
3. Aguardar botão em HIGH
4. Confirmar estado após 25 ms
5. Semear o primeiro sorteio com micros()
6. Sortear de 1 a 6
7. Executar animação
8. Mostrar resultado
9. Aguardar soltura estável

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
const byte PINO_BOTAO = A0;

// Pinos dos segmentos na ordem a, b, c, d, e, f, g.
const byte PINOS_SEGMENTOS[] = {6, 5, 4, 2, 3, 1, 0};

// Display de ânodo comum: um bit 0 acende o segmento.
// O índice de cada padrão corresponde ao número exibido.
const byte DIGITOS[] = {
  0x40,  // 0
  0x79,  // 1
  0x24,  // 2
  0x30,  // 3
  0x19,  // 4
  0x12,  // 5
  0x02   // 6
};

// Mesma sequência visual do código original.
const byte SEQUENCIA_ANIMACAO[] = {6, 1, 2, 3, 4, 5};
bool primeiraJogada = true;

void mostrarNumero(byte numero) {
  for (byte segmento = 0; segmento < 7; segmento++) {
    digitalWrite(PINOS_SEGMENTOS[segmento], bitRead(DIGITOS[numero], segmento));
  }
}

void animarDado() {
  for (byte volta = 0; volta < 10; volta++) {
    for (byte numero : SEQUENCIA_ANIMACAO) {
      mostrarNumero(numero);
      delay(50);
    }
  }
}

void setup() {
  for (byte pino : PINOS_SEGMENTOS) {
    pinMode(pino, OUTPUT);
  }

  // O resistor externo entre A0 e GND mantém o botão solto em LOW.
  pinMode(PINO_BOTAO, INPUT);
  mostrarNumero(0);
  delay(1000);
}

void loop() {
  if (digitalRead(PINO_BOTAO) == LOW) return;

  // Confirma o aperto depois que o contato estabilizar.
  delay(25);
  if (digitalRead(PINO_BOTAO) == LOW) return;

  if (primeiraJogada) {
    randomSeed(micros());
    primeiraJogada = false;
  }

  byte resultado = random(1, 7);  // Sorteia de 1 a 6.
  animarDado();
  mostrarNumero(resultado);

  // Só libera outra jogada depois que o botão estiver solto por 25 ms.
  do {
    while (digitalRead(PINO_BOTAO) == HIGH) {
      delay(1);
    }
    delay(25);
  } while (digitalRead(PINO_BOTAO) == HIGH);
}
```

📁 **Arquivo fonte compilável:** [`PRJ 2.8 Dado Eletronico.ino`](./PRJ 2.8 Dado Eletronico.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Identifique o display de anodo comum e os segmentos a até g. Confira no PDF os valores R1 = 220 kΩ e R2 = 100 Ω antes de comparar com o material físico.
2. Com USB desligado, siga a ordem do vetor: a em D6, b em D5, c em D4, d em D2, e em D3, f em D1 e g em D0.
3. Conecte o botão a A0 com polarização externa para GND e acionamento em HIGH. O desenho usa resistor no comum do display; antes da montagem física, revise a limitação de corrente por segmento.
4. Abra o .ino completo e carregue no Uno. Como D0 e D1 estão conectados ao display, se houver conflito no carregamento, desligue o USB, desconecte esses sinais, carregue e reconecte com a alimentação desligada. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre semente inicial e sorteio de 1 a 6; para executar, use PRJ 2.8 Dado Eletronico.ino completo (trecho nas linhas 55–62).
5. Pressione o botão, observe a animação e registre o resultado. Mantenha-o pressionado e verifique que o programa aguarda a soltura para aceitar outra jogada.
6. Faça uma série de lançamentos e conte os resultados. Não use Monitor Serial com D0 e D1 ligados aos segmentos; o programa original não inicializa a serial. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Codificação dos Dígitos: DIGITOS guarda padrões de bits para os números. Como o display é de anodo comum, um bit zero acende o segmento; mostrarNumero() percorre os sete pinos e aplica o padrão correspondente.

2) Sorteio e Animação: random(1, 7) produz valores inteiros de 1 a 6. A animação apenas percorre uma sequência visual fixa; ela não altera o resultado que já foi sorteado antes de ser exibido.

3) Botão Estável: Duas verificações separadas por 25 ms ajudam a confirmar o aperto. Depois do resultado, a rotina espera uma soltura estável, evitando que um acionamento longo seja contado como várias jogadas.

4) Conferência Elétrica: O PDF especifica 220 kΩ e 100 Ω, e a imagem limita o display pelo comum. A distribuição de corrente merece revisão física; D0 e D1 ainda compartilham funções com a serial e exigem cuidado na carga do programa.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Registrar 30 resultados e montar um gráfico de quantas vezes cada número apareceu.
- **Nível Intermediário:** Modificar a duração da animação e comparar a percepção dos jogadores sem mudar o intervalo do sorteio.
- **Nível Avançado:** Em uma cópia do programa, remapear os segmentos de D0/D1 para pinos livres e revisar a proteção por segmento, liberando a serial para registrar resultados.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Dado Eletrônico.png`](./Dado Eletrônico.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 2.8 Dado Eletronico.ino`](./PRJ 2.8 Dado Eletronico.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 2.8 Dado Eletronico.json`](./PRJ 2.8 Dado Eletronico.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`PRJ 2.8 Esquema.png`](./PRJ 2.8 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 2.8 Esquematico.pdf`](./PRJ 2.8 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
