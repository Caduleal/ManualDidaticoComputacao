# 🚀 PRJ 1.4 — Ventilador

> **Etapa de Ensino:** Módulo I - Educação Infantil  
> **Nível de Complexidade:** `Básico` | **Tempo Estimado:** `1 h/aula (60 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Ventilador .png" alt="Ventilador" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Ventilador (PRJ 1.4)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 1.4` |
| **Título do Projeto** | Ventilador |
| **Módulo Curricular** | Módulo I - Educação Infantil |
| **Complexidade Didática** | `Básico` |
| **Duração Estimada** | 1 h/aula (60 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Comparar objetos parados e em movimento, reconhecer o comando de uma chave e acompanhar a montagem demonstrativa do professor. Não exige programação.

### 💡 Habilidades de Pensamento Computacional:
- Sequência de acionamento
- Identificação de entrada e efeito
- Comparação entre previsão e observação
- Representação dos estados parado e girando

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** Ventiladores movimentam o ar para melhorar a sensação de conforto. Diferentes objetos usam motores para transformar energia elétrica em movimento. A turma observa um modelo pequeno e conversa sobre onde encontra hélices, percebendo que movimento e luz são efeitos diferentes da eletricidade.
- **Matematica:** Contar as pás visíveis e os componentes, comparar parado e girando e ordenar as ações necessárias para ligar e desligar a chave.

---

## 📖 Contextualização Histórica e Problema Real

Como produzir movimento com uma pequena fonte de energia? O material mostra bateria, chave, resistor e motor com hélice em um circuito em série. Quando a chave fecha o caminho, o motor recebe energia, mas a bateria e o resistor podem limitar a corrente e impedir a partida. A atividade deve começar pela observação do modelo e pela verificação do professor.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Bateria tipo moeda de 3 V: CR2032 na imagem e BR2016 no PDF; conferir o modelo |
| 1x | Suporte compatível com a bateria mostrada na imagem |
| 1x | Resistor R1 de 220 Ω |
| 1x | Conjunto de fios de ligação |
| 1x | Motor CC M1 com hélice, modelo e corrente não informados |
| 1x | Chave deslizante S1 |

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 1.4 Esquema.png" alt="Esquema elétrico - PRJ 1.4" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 1.4 Esquematico.pdf](./PRJ 1.4 Esquematico.pdf)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Apresente o circuito como modelo de movimento. O professor mantém a bateria no suporte e a hélice afastada de mãos, cabelos e rosto.
2. Com a bateria retirada, confira a chave, o resistor de 220 Ω e os dois terminais do motor. A imagem mostra CR2032 e o PDF identifica BR2016.
3. Reproduza apenas a sequência documentada entre positivo, chave, resistor e motor; ligue o outro terminal do motor ao negativo do suporte.
4. Antes do teste físico, confira a compatibilidade do motor com a fonte. O resistor de 220 Ω e a bateria tipo moeda podem não fornecer corrente de partida; não elimine o resistor para forçar o funcionamento.
5. Faça um acionamento breve sob controle do professor e observe se há rotação. Se o motor não partir, desligue e registre a limitação, sem afirmar que a montagem foi validada.
6. Compare as posições da chave e desenhe o que foi observado. Não há código nem fluxograma; os campos ficam vazios. Desconecte a bateria ao encerrar.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Energia e Movimento: O motor transforma parte da energia elétrica em movimento de rotação. A turma pode comparar esse efeito com a luz do LED dos projetos anteriores, usando apenas observações concretas.

2) Circuito em Série: A chave, o resistor e o motor estão no mesmo caminho da corrente. Abrir uma conexão interrompe o circuito; a presença de uma bateria, por si só, não garante que o motor consiga iniciar o movimento.

3) Limite da Montagem: Os arquivos mostram resistor de 220 Ω e bateria tipo moeda, mas não especificam o consumo do motor. Essa combinação exige verificação antes do uso físico e pode ser trabalhada inicialmente como simulação.

4) Controle Manual: O comando ocorre na chave e não em software. Registrar parado, tentando partir e girando ajuda a distinguir o resultado esperado do resultado realmente observado durante a experiência.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`PRJ 1.4 Esquema.png`](./PRJ 1.4 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 1.4 Esquematico.pdf`](./PRJ 1.4 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |
| [`PRJ 1.4 Ventilador.json`](./PRJ 1.4 Ventilador.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`Ventilador .png`](./Ventilador .png) | Fotografia / Identidade visual de capa do projeto |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
