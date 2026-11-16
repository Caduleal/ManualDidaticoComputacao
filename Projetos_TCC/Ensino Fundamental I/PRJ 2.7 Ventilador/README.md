# 🚀 PRJ 2.7 — Ventilador

> **Etapa de Ensino:** Módulo II - Ensino Fundamental I  
> **Nível de Complexidade:** `Intermediário` | **Tempo Estimado:** `2 h/aula (120 min), após revisão técnica`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Ventilador Automatico.png" alt="Ventilador" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Ventilador (PRJ 2.7)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 2.7` |
| **Título do Projeto** | Ventilador |
| **Módulo Curricular** | Módulo II - Ensino Fundamental I |
| **Complexidade Didática** | `Intermediário` |
| **Duração Estimada** | 2 h/aula (120 min), após revisão técnica |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Comparar temperaturas, reconhecer LED RGB e sensor TMP36 e compreender que motores precisam de alimentação e acionamento adequados. O professor deve revisar o circuito antes da montagem física.

### 💡 Habilidades de Pensamento Computacional:
- Identificação de entradas e saídas
- Modelagem de uma regra de controle
- Leitura de um esquema de conexões
- Distinção entre circuito desenhado e software implementado

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Ventiladores ajudam a movimentar o ar em ambientes ocupados. O acionamento automático associa uma medida a uma decisão, em vez de depender apenas de uma chave. A imagem deste projeto permite discutir essa ideia, mas a turma precisa distinguir o que está desenhado do que ainda depende de programa e revisão elétrica.
- **Matematica:** Proposta de exploração: comparar temperaturas e representar uma regra por faixas. Não há limiar de acionamento, fórmula executada ou intervalo de atualização definidos no arquivo vazio.

---

## 📖 Contextualização Histórica e Problema Real

Como relacionar a temperatura ao funcionamento de um pequeno ventilador? A imagem reúne Arduino, sensor TMP36, RGB e motor, sugerindo um indicador e um acionamento por temperatura. Entretanto, o .ino está vazio e não confirma nenhuma regra de controle. Além disso, o motor aparece ligado a A1 por resistor, sem estágio de potência, o que exige revisão antes de um teste físico.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Placa Arduino Uno R3 |
| 1x | Cabo USB compatível |
| 1x | Sensor TMP36 mostrado na imagem |
| 1x | LED RGB de catodo comum |
| 1x | Motor CC com hélice, especificação não informada |
| 4x | Resistores de 220 Ω indicados no PDF |
| 1x | Protoboard, conforme a imagem da montagem |
| 1x | Conjunto de jumpers; quantidade individual não especificada |

### 🔌 Mapeamento de Pinos e Conexões Elétricas:

- Mapeamento visual, sem confirmação por código: arquivo .ino vazio
- A0 → saída central do TMP36; alimentação do sensor em 5V/GND
- D2, D3 e D4 → três canais do RGB por resistores de 220 Ω; comum → GND
- A1 → resistor de 220 Ω → motor → GND, conforme a imagem; ligação não validada para montagem física
- 5V/GND → barramentos da protoboard; não há driver de motor visível

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 2.7 Esquema.png" alt="Esquema elétrico - PRJ 2.7" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 2.7 Esquematico.pdf](./PRJ 2.7 Esquematico.pdf)

---

## 🧠 Modelagem Lógica e Algorítmica

### 🔄 Sequência de Operação e Lógica de Controle:

1. Ler a imagem e identificar TMP36, RGB e motor
2. Confirmar que o .ino está vazio
3. Revisar o acionamento elétrico do motor
4. Definir a regra somente após receber o programa
5. Validar entradas e saídas antes do teste

### 📊 Diagrama de Fluxo (Fluxograma):

*(Fluxograma em processo de elaboração gráfica — a modelagem lógica completa está descrita no fluxo passo a passo acima).*

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Identifique na imagem o sensor de temperatura, o RGB e o motor. Confirme que o .ino tem zero bytes e não há programa para carregar.
2. Com a alimentação desligada, registre as conexões visíveis do TMP36 em A0 e do RGB nos pinos D2, D3 e D4.
3. Marque a ligação de A1 ao motor como pendência técnica. Não conecte o motor diretamente à saída do Uno, mesmo que haja resistor em série.
4. Antes de montar fisicamente, o professor deve definir um driver ou transistor, proteção contra retorno indutivo e fonte compatível; esses itens são adequações necessárias, não componentes confirmados nos arquivos.
5. Aguarde o programa para confirmar temperaturas, cores e condições de partida e parada. Discuta essas escolhas como proposta, sem inventar valores para preencher o código.
6. Após receber o fonte e revisar o hardware, teste primeiro sensor e RGB e depois o motor com acionamento adequado. CODIGO_FONTE e fluxograma ficam vazios nesta versão.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Entrada Analógica: O TMP36 aparece conectado a A0. Essa ligação sugere uma medida de temperatura, mas não confirma a fórmula ou os limites que seriam usados por um programa, pois o arquivo fornecido não contém instruções.

2) Sinalização RGB: Três pinos digitais chegam ao LED por resistores individuais. Sem fonte, não é possível afirmar qual cor representa frio, normal ou quente; essas associações precisam ser explicitadas quando o projeto for completado.

3) Motor e Potência: Um pino de sinal não substitui um estágio de acionamento de motor. A imagem não apresenta transistor, driver ou diodo de proteção; o resistor de 220 Ω desenhado não resolve essa lacuna de projeto.

4) Regra Pendente: Comparar temperatura com um limiar seria uma possibilidade didática. A versão documentada não implementa essa comparação, portanto os testes funcionais e o trecho de código dependem de arquivos adicionais e revisão da montagem.

---

## 🌟 Desafios de Expansão Pedagógica

- **Nível Fácil:** Identificar em um desenho quais componentes medem, indicam e produzem movimento.
- **Nível Intermediário:** Escrever uma tabela de faixas de temperatura como proposta a validar quando houver código.
- **Nível Avançado:** Depois da revisão do acionamento e do fornecimento do fonte, testar dois limiares de ligar e desligar para evitar alternância perto de uma mesma temperatura.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`PRJ 2.7 Esquema.png`](./PRJ 2.7 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 2.7 Esquematico.pdf`](./PRJ 2.7 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 2.7 Ventilador.ino`](./PRJ 2.7 Ventilador.ino) | Firmware em código C++ para carregar no Arduino |
| [`PRJ 2.7 Ventilador.json`](./PRJ 2.7 Ventilador.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`Ventilador Automatico.png`](./Ventilador Automatico.png) | Fotografia / Identidade visual de capa do projeto |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
