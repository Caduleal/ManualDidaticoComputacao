# 🚀 PRJ 1.1 — Circuito Simples

> **Etapa de Ensino:** Módulo I - Educação Infantil  
> **Nível de Complexidade:** `Básico` | **Tempo Estimado:** `1 h/aula (60 min)`  
> *Manual Didático de Computação — Metodologia e Montagem para Laboratórios Escolares*

---

## 📸 Identidade Visual do Projeto

<div align="center">
  <img src="./Circuito Simples.png" alt="Circuito Simples" width="600px" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
  <p><em>Figura de Capa: Circuito Simples (PRJ 1.1)</em></p>
</div>

---

## 📌 Metadados e Plataformas de Simulação

| Parâmetro | Detalhamento |
| :--- | :--- |
| **Identificador** | `PRJ 1.1` |
| **Título do Projeto** | Circuito Simples |
| **Módulo Curricular** | Módulo I - Educação Infantil |
| **Complexidade Didática** | `Básico` |
| **Duração Estimada** | 1 h/aula (60 min) |

### 🔗 Links para Simulação Online
- 🟦 **Tinkercad Circuits:** [Acessar Modelo no Tinkercad](https://www.tinkercad.com/) *(ou montar cópia virtual do circuito)*
- 🟩 **Wokwi Simulator:** *(Espaço reservado para inclusão do link de simulação no Wokwi)*

---

## 🎯 Objetivos de Aprendizagem e Fundamentação BNCC

**Pré-Requisitos Recomendados:**  
Reconhecer cores, comparar objetos e seguir instruções com o professor. Não exige leitura, programação ou estudo prévio de eletricidade.

### 💡 Habilidades de Pensamento Computacional:
- Sequenciamento de ações de montagem
- Reconhecimento de estados: aceso e apagado
- Previsão e observação de causa e efeito
- Identificação de falhas por comparação com um modelo

### 🌐 Articulação Interdisciplinar:
- **Historia E Sociedade:** A iluminação elétrica mudou como as pessoas usam os espaços quando escurece. Lanternas levam luz a lugares sem tomada. Neste circuito, a turma observa como uma bateria alimenta uma pequena luz e conversa sobre seus usos no cotidiano.
- **Matematica:** Contar bateria, resistor e LED; comparar os terminais do LED e ordenar a montagem com imagens.

---

## 📖 Contextualização Histórica e Problema Real

Como acender uma luz longe de uma tomada? Uma lanterna resolve essa necessidade com uma bateria e um caminho elétrico fechado. A turma monta um modelo com LED e resistor, observando que a luz depende das conexões. Ao abrir esse caminho, o LED apaga, tornando visível a relação entre ligação e funcionamento.

---

## 🛠️ Arquitetura de Hardware e Lista de Materiais (BOM)

### 📋 Componentes e Quantitativos:

| Qtd | Componente / Especificação |
| :---: | :--- |
| 1x | Bateria de 3 V: CR2032 nas imagens; BR2016 no PDF. Usar suporte compatível. |
| 1x | LED, identificado como D1 no esquemático |
| 1x | Resistor de 220 Ω, identificado como R1 no esquemático |
| 1x | Suporte da bateria com terminais positivo e negativo, mostrado nas imagens |
| 1x | Conjunto de fios para unir bateria, resistor e LED; quantidade não especificada |

### 📐 Diagrama Esquemático do Circuito:

<div align="center">
  <img src="./PRJ 1.1 Esquema.png" alt="Esquema elétrico - PRJ 1.1" width="650px" style="border-radius: 6px; border: 1px solid #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,0.08);" />
  <p><em>FIGURA 1: ESQUEMA DO CIRCUITO SIMPLES</em></p>
</div>

📄 **Arquivo Esquemático Vetorial para Impressão:** [PRJ 1.1 Esquematico.pdf](./PRJ 1.1 Esquematico.pdf)

---

## 📝 Roteiro Prático de Execução (Passo a Passo)

1. Mostre as imagens e localize com a turma a bateria, o LED e o resistor. O professor mantém a bateria no suporte, fora do alcance das crianças: sua ingestão é perigosa.
2. Com a bateria desconectada, identifique os terminais do suporte. Confira a bateria: CR2032 de 3 V nas imagens e BR2016 no PDF. Use suporte compatível.
3. Conecte o terminal positivo do suporte a uma extremidade do resistor de 220 Ω e a outra extremidade ao anodo do LED vermelho. O resistor não tem polaridade; a perna maior do LED costuma indicar o anodo.
4. Ligue o catodo do LED ao terminal negativo do suporte. Confira a montagem antes de inserir a bateria. Não una seus polos diretamente; mantenha o resistor em série.
5. O professor conecta a bateria e convida a turma a observar a luz. Se não acender, desconecte a alimentação e confira os contatos e a polaridade do LED. Não há código-fonte nem Arduino nesta pasta; CODIGO_FONTE permanece vazio.
6. Abra uma conexão e peça às crianças que descrevam o resultado; depois reconecte e compare. Registre os estados com desenhos de uma luz acesa e outra apagada. Sem fluxograma fornecido, ARQUIVO permanece vazio. Ao terminar, retire a bateria e guarde as peças.

---

## 🔍 Articulação Teórica e Aprofundamento

1) Caminho Fechado: A bateria fornece energia ao circuito. O LED acende quando as conexões formam um caminho contínuo entre seus terminais, com polaridade correta; abrir um contato interrompe a corrente.

2) Orientação do LED: O LED possui anodo e catodo e precisa ser conectado no sentido indicado. A turma pode comparar suas pernas com ajuda do professor, sem exigir nomes técnicos na fala das crianças.

3) Função do Resistor: O resistor de 220 Ω limita a corrente que atravessa o LED. Ele permanece em série durante toda a experiência; sua função pode ser apresentada como um cuidado para proteger a pequena luz.

4) Sequência e Observação: Não existe software neste projeto. Montar, prever, observar e revisar introduz o pensamento computacional por ações concretas e prepara a turma para atividades futuras com comandos.

---

## 📂 Conteúdo do Diretório

| Arquivo | Finalidade |
| :--- | :--- |
| [`Circuito Simples.png`](./Circuito Simples.png) | Fotografia / Identidade visual de capa do projeto |
| [`PRJ 1.1 Circuito Simples.json`](./PRJ 1.1 Circuito Simples.json) | Estrutura JSON de dados e metadados pedagógicos |
| [`PRJ 1.1 Esquema.png`](./PRJ 1.1 Esquema.png) | Esquema elétrico e montagem gráfica do circuito |
| [`PRJ 1.1 Esquematico.pdf`](./PRJ 1.1 Esquematico.pdf) | Documento esquemático / técnico em PDF de alta resolução |

---
*Manual Didático de Computação — Curso de Tecnologia em Sistemas de Computação (UFF)*
