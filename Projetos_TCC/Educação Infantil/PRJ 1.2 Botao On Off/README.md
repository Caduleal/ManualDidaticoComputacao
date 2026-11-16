# 🚀 PRJ 1.2 — Botão On Off

> **Etapa de Ensino:** Módulo I - Educação Infantil  
> **Nível de Complexidade:** `Básico` | **Tempo Estimado:** `1 h/aula (60 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Botão on_off.png" alt="Botão On Off" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Botão On Off (PRJ 1.2)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 1.2` |
| **Título do Projeto** | Botão On Off |
| **Módulo Curricular** | Módulo I - Educação Infantil |
| **Complexidade Didática** | `Básico` |
| **Duração Estimada** | 1 h/aula (60 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Reconhecer cores e acompanhar uma sequência curta com o professor. Retomar a experiência de circuito aberto e fechado do projeto 1.1; não exige leitura ou programação.

### 💡 Habilidades de Pensamento Computacional:
- Sequenciamento de ações
- Reconhecimento dos estados ligado e desligado
- Relação de causa e efeito
- Previsão e verificação de resultados

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Interruptores permitem que as pessoas controlem quando uma luz fica acesa. Esse comando aparece em luminárias e brinquedos que as crianças conhecem. Ao experimentar duas posições de uma chave, a turma percebe que um pequeno gesto pode mudar o funcionamento de um objeto.
- **Matematica:** Comparar duas posições da chave, contar os componentes e representar os estados com pares de cartões: ligado/desligado e aberto/fechado.

---

## 📖 Contextualização Histórica e Problema Real

Como ligar e desligar uma luz sem retirar sua bateria? O circuito acrescenta uma chave deslizante ao caminho entre bateria, resistor e LED verde. Em uma posição a passagem de corrente é interrompida; na outra, o caminho se fecha e a luz pode acender. A experiência modela o comando manual de uma pequena luminária.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Bateria tipo moeda de 3 V: CR2032 na imagem e BR2016 no PDF; conferir o modelo |
| 1x | Suporte compatível com a bateria mostrada na imagem |
| 1x | Resistor R1 de 220 Ω |
| 1x | Conjunto de fios de ligação |
| 1x | LED verde D1 |
| 1x | Chave deslizante S1 de três terminais, usando comum e um contato lateral |

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 1.2 Esquema.png" alt="Esquema elétrico - PRJ 1.2" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 1.2 Esquenatico.pdf](./PRJ 1.2 Esquenatico.pdf)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Mostre os componentes e retome a ideia de caminho fechado. O professor manipula a bateria tipo moeda e a mantém protegida no suporte, pois sua ingestão é perigosa.
2. Com a bateria retirada, identifique o terminal comum da chave e o contato lateral indicado na imagem. Não una diretamente os polos da bateria.
3. Ligue o positivo do suporte ao comum da chave. Ligue o contato lateral ao resistor de 220 Ω e o resistor ao anodo do LED verde.
4. Ligue o catodo do LED ao negativo do suporte. Confira a orientação do LED e as conexões com a imagem antes de alimentar.
5. O professor insere a bateria. Mova a chave entre as duas posições e peça que as crianças expliquem quando o caminho está fechado.
6. Registre os estados com desenhos. Não há código-fonte, Arduino nem fluxograma fornecidos; esses campos ficam vazios. Retire e guarde a bateria ao terminar.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Chave e Continuidade: A chave deslizante une seu terminal comum a um dos contatos laterais. Usar apenas um contato lateral produz uma posição ligada e outra desligada, tornando a decisão física fácil de observar.

2) Proteção do LED: O resistor de 220 Ω permanece em série com o LED verde e limita a corrente. A chave controla o contato, mas não substitui a função do resistor nem permite retirar essa proteção.

3) Polaridade e Fonte: O LED precisa de orientação correta. A imagem mostra CR2032 e o PDF nomeia BR2016; a escolha da bateria e do suporte deve ser conferida pelo professor, sem tratar os modelos como uma peça idêntica.

4) Pensamento Sequencial: Antes de mover a chave, a criança prevê o estado da luz e depois compara sua previsão com o resultado. O controle é elétrico e manual; não existe programa escondido nesta montagem.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Botão on_off.png`](./Botão on_off.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 1.2 Botao On Off.json`](./PRJ 1.2 Botao On Off.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`PRJ 1.2 Esquema.png`](./PRJ 1.2 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 1.2 Esquenatico.pdf`](./PRJ 1.2 Esquenatico.pdf) | Documento esquemático / técnico em PDF de alta resolução |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
