# 🚀 PRJ 3.1 — Lâmpada Automática

> **Etapa de Ensino:** Módulo III - Ensino Fundamental II  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min), com revisão do acionamento`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Lampada Automatica.png" alt="Lâmpada Automática" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Lâmpada Automática (PRJ 3.1)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 3.1` |
| **Título do Projeto** | Lâmpada Automática |
| **Módulo Curricular** | Módulo III - Ensino Fundamental II |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min), com revisão do acionamento |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Entradas e saídas digitais, uso de if/else e diferença entre circuito de controle e circuito da carga. Ler um esquema com sensor PIR e relé.

### 💡 Habilidades de Pensamento Computacional:
- Leitura de presença em nível digital
- Decisão condicional
- Acionamento de saída
- Diagnóstico pela comunicação serial

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** A iluminação automática aparece em passagens e locais de uso eventual. Detectar movimento pode reduzir o tempo em que uma luz permanece ligada sem necessidade. A atividade permite discutir economia de energia e as limitações de inferir ocupação apenas pela resposta de um sensor de movimento.
- **Matematica:** Comparar tempos ligado e desligado, registrar eventos em uma tabela e estimar a diferença de tempo de uso em dois cenários de circulação.

---

## 📖 Contextualização Histórica e Problema Real

Como acender uma luz quando há movimento em uma passagem? O PIR fornece um sinal digital ao Arduino, que comanda o relé conforme HIGH ou LOW. A imagem representa uma lâmpada alimentada por bateria de 9 V, sem rede elétrica. O desenho do relé precisa de revisão do acionamento antes da montagem física, pois o código sozinho não fornece a etapa de potência.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | Sensor PIR |
| 1x | Relé K1 mostrado sem módulo de acionamento na imagem |
| 1x | Lâmpada de baixa tensão compatível com a fonte de 9 V, a conferir |
| 1x | Bateria de 9 V BAT1 |
| 1x | Conjunto de fios de ligação |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- A0 → OUT do PIR (pinoPir); PIR VCC/GND → 5V/GND
- D13 → comando do relé (pinoRele); imagem mostra relé avulso, sem driver
- Contatos do relé → circuito separado com bateria de 9 V e lâmpada, conforme imagem
- Acionamento da bobina e proteção precisam de revisão; não ligar a bobina diretamente ao pino nem usar rede elétrica

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 3.1 Esquema.png" alt="Esquema elétrico - PRJ 3.1" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 3.1 Esquematico.pdf](./PRJ 3.1 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Configurar D13 como saída e A0 como entrada
2. Ler sinal do PIR
3. Se HIGH, acionar D13
4. Registrar movimento na serial
5. Aguardar 100 ms
6. Se LOW, desligar D13
7. Aguardar 300 ms
8. Repetir

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

### 💻 Firmware / Código-Fonte em C++ (Arduino IDE):

```cpp
int pinoRele = 13;  // Fio amarelo conectado ao módulo relé
int pinoPir = A0;   // Fio verde conectado ao sinal do sensor PIR
int val = 0;        // Variável para armazenar a leitura do sensor

void setup() { 
  pinMode(pinoRele, OUTPUT);
  pinMode(pinoPir, INPUT);        
  Serial.begin(9600);                 
} 

void loop() { 
  val = digitalRead(pinoPir); // Lê o estado digital do sensor PIR
  
  if (val == HIGH) { 
    digitalWrite(pinoRele, HIGH); // Aciona o relé, ligando a lâmpada
    Serial.println("Movimento detectado - Lampada LIGADA");
    delay(100); 
  } else { 
    digitalWrite(pinoRele, LOW);  // Desaciona o relé, desligando a lâmpada
    delay(300);   
  } 
}
```

📁 **Arquivo fonte compilável:** [`PRJ 3.1 Lampada Automatica.ino`](./PRJ 3.1 Lampada Automatica.ino)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Compare o esquema e o .ino. Identifique PIR, relé, bateria de 9 V e lâmpada; use somente uma carga de baixa tensão nesta atividade.
2. Com tudo desligado, conecte OUT do PIR a A0 e confira VCC e GND. Aguarde a estabilização do sensor antes de interpretar os testes.
3. Não reproduza o comando direto de bobina do desenho. O professor deve selecionar módulo de relé ou driver com proteção adequado ao comando D13; esses itens são adequações, não materiais confirmados na imagem.
4. Mantenha os contatos do relé no circuito de bateria de 9 V e lâmpada compatível, conforme revisão do professor. Não conecte este projeto a uma tomada. O campo CODIGO_FONTE é um recorte didático de até 20 linhas, sobre presença comanda a saída do relé; para executar, use PRJ 3.1 Lampada Automatica.ino completo (trecho nas linhas 11–22).
5. Abra o .ino completo, selecione Uno e carregue. Observe no Monitor Serial a 9600 baud o sinal de movimento e confira se o módulo escolhido responde ao nível HIGH esperado pelo programa.
6. Compare movimento e repouso do PIR com o estado da luz. Registre o tempo de resposta do sensor; não há temporização prolongada de permanência implementada além das pausas de 100/300 ms. Não há fluxograma fornecido; ARQUIVO permanece vazio.

---

## 🔍 Articulação Teórica e Aprofundamento

1) PIR como Entrada: A0 é lido por digitalRead(), portanto funciona como entrada digital neste projeto. O resultado indica o estado do módulo PIR e não uma medida numérica de distância ou uma identificação de pessoas.

2) Regra de Acionamento: O if/else escreve HIGH em D13 quando a entrada está HIGH e LOW no caso contrário. Um módulo ativo em nível baixo produziria comportamento diferente, razão para conferir sua compatibilidade antes do teste.

3) Relé e Carga: Os contatos comutam o circuito da lâmpada de 9 V. A bobina exige acionamento apropriado e proteção contra retorno indutivo; o relé avulso mostrado na imagem não deve ser tratado como um módulo pronto.

4) Limite da Automação: O programa depende do sinal de movimento e não garante detectar alguém parado. O estudo pode comparar luz acesa e uso do espaço, deixando claro que economia depende da situação e da configuração do sensor.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Contar acionamentos do PIR em diferentes posições na sala, usando apenas sinalização de baixa tensão.
- **Nível Intermediário:** Adicionar um intervalo de permanência após o último movimento, com millis(), em uma cópia do programa.
- **Nível Avançado:** Acrescentar um LDR em pino livre para permitir acionamento somente no escuro, mantendo o circuito de carga em baixa tensão e com driver adequado.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Lampada Automatica.png`](./Lampada Automatica.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 3.1 Esquema.png`](./PRJ 3.1 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 3.1 Esquematico.pdf`](./PRJ 3.1 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 3.1 Lampada Automatica.ino`](./PRJ 3.1 Lampada Automatica.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 3.1 Lampada Automatica.json`](./PRJ 3.1 Lampada Automatica.json) | Estrutura JSON de dados e metadados pedagógicos |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
