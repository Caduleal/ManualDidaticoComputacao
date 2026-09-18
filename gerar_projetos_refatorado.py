"""
Módulo de automação e geração de livros e manuais didáticos de computação em formato HTML/A4.

Este script estrutura uma publicação no formato formal de LIVRO DIDÁTICO, organizando:
1. Capa / Título do Livro
2. Sumário Formal do Livro (Table of Contents - imediatamente após a capa)
3. Introdução e Contexto Histórico (Papert & Paulo Freire, BNCC, tipografia ampliada)
4. Explicação da Estrutura Didática do Módulo (Os 4 Pilares: Esquema, Fluxograma, Tinkercad e GitHub)
5. Módulos Curriculares com Tabelas de Projetos Interativas (com links diretos clicáveis)
6. Lista Sequencial de Projetos (com QR Code GitHub, fluxo de código com setas e cálculo volumétrico A4)
"""

import base64
import html
import io
import json
import re
import urllib.parse
from pathlib import Path
from string import Template
from typing import Any, Dict, List, Optional, Tuple, Union
from bs4 import BeautifulSoup
import atualizar_manual

# ==============================================================================
# CONFIGURAÇÕES E CONSTANTES DE LAYOUT
# ==============================================================================

CSS_FILE_NAME: str = "style.css"
LIMITE_LINHAS_PAGINA: int = 55
MAX_LINHAS_BLOCO_CODIGO: int = 40

TEXTO_INTRODUCAO_OFICIAL: List[str] = [
    (
        "A trajetória da inclusão das Tecnologias de Informação e Comunicação (TIC) no ambiente escolar brasileiro "
        "revela um histórico marcado pela priorização infraestrutural e da aquisição de equipamentos físicos. "
        "Desde as primeiras políticas públicas de informática educativa no final do século XX, grande parte dos esforços "
        "concentrou-se na instalação de laboratórios e no provimento de computadores nas escolas. No entanto, a mera "
        "presença dos recursos tecnológicos não se traduziu na apropriação efetiva dos fundamentos científicos e metodológicos "
        "da Computação. O modelo pedagógico predominante manteve-se instrumental, restringindo o uso das máquinas ao suporte "
        "de atividades tradicionais, como a digitação de textos, a realização de pesquisas na internet e o manuseio de "
        "softwares educativos fechados, o que manteve os princípios operacionais internos da tecnologia velados e distantes "
        "da compreensão dos estudantes."
    ),
    (
        "Com o objetivo de superar essa perspectiva estritamente utilitária e formar sujeitos capacitados a atuar criticamente "
        "na sociedade contemporânea, consolida-se a abordagem da Computação como ciência e o desenvolvimento do Pensamento "
        "Computacional. Formulado como a capacidade de expressar e resolver problemas por meio de conceitos fundamentais da "
        "ciência da computação como decomposição, reconhecimento de padrões, abstração e algoritmo, esse paradigma desloca "
        "o foco do simples uso de aplicações prontas para a capacidade de projetar e compreender o funcionamento dos sistemas "
        "digitais. Essa reorientação educacional encontra sustentação regulatória nos marcos normativos nacionais, especialmente "
        "na Base Nacional Comum Curricular (BNCC) e na Resolução CNE/CEB nº 1/2022, que formalizam a obrigatoriedade da "
        "integração de conceitos computacionais em todas as etapas da Educação Básica."
    ),
    (
        "Apesar dos avanços normativos, a implementação efetiva dessas diretrizes no cotidiano escolar enfrenta barreiras "
        "estruturais significativas. Destacam-se a precariedade de infraestrutura de muitos estabelecimentos, a escassez de "
        "iniciativas continuadas para a formação docente na área e a carência de materiais didáticos estruturados que orientem "
        "a prática pedagógica de forma sistemática. No contexto atual, os dispositivos digitais permanecem frequentemente "
        'tratados como "caixas-pretas", ferramentas cujas interfaces são operadas sem o entendimento dos circuitos, sinais e '
        "lógicas que viabilizam seu funcionamento. Essa desconexão limita o desenvolvimento de habilidades de criação e autoria "
        "tecnológica, mantendo a comunidade escolar restrita à condição de consumidora passiva de tecnologias concebidas por terceiros."
    ),
    (
        "Em resposta a essas limitações, e fundamentado teórica e metodologicamente no construcionismo de Seymour Papert e "
        "nos princípios de emancipação da pedagogia da autonomia de Paulo Freire, este trabalho propõe uma abordagem voltada "
        "à práxis libertadora e ao aprendizado significativo. Parte-se da premissa de que a assimilação de conceitos abstratos "
        "de lógica e programação é potencializada quando mediada pela construção de artefatos concretos no mundo físico. "
        "Assim, a integração de sistemas embarcados, microcontroladores, sensores e atuadores estabelece uma ponte tangível entre "
        "a teoria e a experimentação empírica. Ao manipular circuitos e programar o comportamento de dispositivos físicos, o "
        "estudante observa o impacto direto de seu código no ambiente, o que favorece a identificação e a correção de erros, "
        "a testagem sistemática de hipóteses e a consolidação do raciocínio lógico-algorítmico."
    ),
    (
        "Diante dessas premissas, este trabalho tem como objetivo desenvolver um manual didático modular direcionado a "
        "professores da Educação Básica, fornecendo suporte técnico e pedagógico para a estruturação e a condução de atividades "
        "em laboratórios escolares. A proposta foi desenhada sob a metodologia da pesquisa-ação e pauta-se pelo uso de "
        "metodologias ativas baseadas na resolução de problemas e na interdisciplinaridade. Visando assegurar a viabilidade "
        "financeira e a ampla replicabilidade do material em redes públicas de ensino, prioriza-se o emprego de plataformas "
        "de hardware de código aberto, softwares livres e componentes eletrônicos de baixo custo, reduzindo as barreiras "
        "de acesso ao ensino prático de Ciência da Computação."
    ),
    (
        "A estrutura do manual foi organizada segundo uma progressão cognitiva e didática contínua, abrangendo desde noções "
        "elementares de circuitos elétricos até o desenvolvimento de algoritmos e o controle de sistemas embarcados complexos. "
        "O material divide-se em módulos instrucionais que englobam orientações de infraestrutura, roteiros de montagem, propostas "
        "de articulação curricular com disciplinas como Física e Matemática. Com este recurso, pretende-se oferecer aos docentes "
        "uma ferramenta estruturada para mediar o ensino de Computação, contribuindo para a democratização do conhecimento "
        "científico-tecnológico e para o fortalecimento da autonomia dos estudantes."
    ),
]

FALLBACK_CSS: str = """
@media screen {
    .a4-page {
        width: 210mm !important;
        height: 297mm !important;
        margin: 20px auto !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
        overflow: hidden !important;
        background-color: white !important;
        box-sizing: border-box !important;
        position: relative !important;
        padding: 2.5cm 2cm !important;
    }

    #secao-sumario {
        height: auto !important;
        min-height: 297mm !important;
        max-height: none !important;
        overflow: visible !important;
        padding-bottom: 30mm !important;
    }
}

@media print {
    @page {
        size: A4;
        margin: 20mm 15mm 20mm 15mm;
    }

    html,
    body {
        width: 100%;
        height: auto;
        background-color: #ffffff !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    .a4-page {
        width: 100% !important;
        height: auto !important;
        max-width: 100% !important;
        max-height: none !important;
        margin: 0 !important;
        padding: 15mm 5mm 20mm 5mm !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
        page-break-after: always !important;
        break-after: page !important;
        overflow: visible !important;
        position: relative !important;
        display: block !important;
    }

    .md\\:grid-cols-2 {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }

    .md\\:flex-row {
        flex-direction: row !important;
    }

    .no-print {
        display: none !important;
    }

    .page-break {
        page-break-before: always !important;
        break-before: page !important;
    }

    .avoid-break {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }

    #secao-sumario {
        page-break-before: always !important;
        break-before: page !important;
        page-break-after: always !important;
        break-after: page !important;
        page-break-inside: auto !important;
        break-inside: auto !important;
        height: auto !important;
        max-height: none !important;
        overflow: visible !important;
        padding-bottom: 25mm !important;
    }

    .sumario-lista, ul.sumario {
        page-break-inside: auto !important;
        break-inside: auto !important;
        display: block !important;
        margin-bottom: 20mm !important;
    }

    .sumario-item, li.sumario-item, .toc-row {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        display: flex !important;
    }

    .secao-introducao, #secao-introducao, #introducao {
        page-break-before: always !important;
        break-before: page !important;
    }
}

.code-block {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.5;
}

.icon-align {
    vertical-align: -0.15em;
}

.curriculum-map img {
    width: 100%;
    height: auto;
    border-radius: 0.5rem;
    border: 1px solid #e2e8f0;
}

.page-top-header {
    position: absolute;
    top: 1cm;
    left: 2cm;
    right: 2cm;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    color: #94a3b8;
    letter-spacing: 0.05em;
    pointer-events: none;
    z-index: 10;
}

.page-top-header .page-header-title {
    text-transform: uppercase;
    font-weight: 600;
}

.page-top-header .page-header-number {
    font-weight: 700;
    color: #64748b;
}

.toc-row {
    display: flex;
    align-items: baseline;
    width: 100%;
    text-decoration: none;
    color: inherit;
    transition: opacity 0.2s;
}

.toc-row:hover {
    opacity: 0.8;
}

.toc-leader {
    flex-grow: 1;
    border-bottom: 1px dotted #94a3b8;
    margin: 0 0.5rem;
    position: relative;
    bottom: 0.25rem;
}

.module-project-link {
    color: #0f172a;
    font-weight: 600;
    text-decoration: none;
    transition: color 0.15s ease-in-out;
}

.module-project-link:hover {
    color: #2563eb;
    text-decoration: underline;
}

.code-flow-container {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.4rem;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 0.6rem 0.8rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
}

.code-flow-step {
    display: inline-flex;
    align-items: center;
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 0.375rem;
    padding: 0.25rem 0.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 600;
    color: #1e293b;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.code-flow-arrow {
    color: #64748b;
    font-weight: bold;
    font-size: 11px;
    display: inline-flex;
    align-items: center;
}

.github-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    border-radius: 0.5rem;
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.75rem;
    border: 1px solid #334155;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.08);
}

/* Tipografia Editorial Contínua: Introdução e Aplicação Extracurricular */
.secao-texto-continuo {
    --line-height: 1.45;
}

.secao-texto-continuo p,
#secao-introducao .secao-texto-continuo p,
#secao-didatica .secao-texto-continuo p {
    font-size: 10px;
    line-height: var(--line-height, 1.45);
    margin: 0;
    margin-bottom: 0;
    padding: 0;
    text-align: justify;
    text-justify: inter-word;
    text-indent: 1.5em;
    color: #1e293b;
    font-weight: 400;
}

/* Quebra e controle do Sumário e Introdução (regras globais) */
#secao-sumario {
    page-break-before: always !important;
    break-before: page !important;
    page-break-inside: auto !important;
    break-inside: auto !important;
}

.sumario-lista, ul.sumario {
    page-break-inside: auto !important;
    break-inside: auto !important;
    display: block !important;
}

.sumario-item, li.sumario-item {
    page-break-inside: avoid !important;
    break-inside: avoid !important;
    display: flex !important;
}

.secao-introducao, #secao-introducao, #introducao {
    page-break-before: always !important;
    break-before: page !important;
}
"""

# ==============================================================================
# TEMPLATES HTML DEDICADOS
# ==============================================================================

class HTMLTemplates:
    """Catálogo estruturado de templates HTML utilizados na renderização."""

    BOTAO_IMPRESSAO_PDF = Template("""
    <div class="no-print fixed top-4 right-4 z-50">
        <button onclick="window.print()" class="bg-brand-800 hover:bg-brand-900 text-white font-bold py-2.5 px-4 rounded-lg shadow-xl flex items-center gap-2 cursor-pointer transition-all border border-brand-700 active:scale-95">
            <span class="material-symbols-outlined text-[20px]">print</span>
            <span class="text-xs font-sans">Gerar PDF / Imprimir</span>
        </button>
    </div>
    """)

    HEADER_PAGINACAO_SUPERIOR = Template("""
    <div class="page-top-header">
        <span class="page-header-title">${titulo_secao}</span>
        <span class="page-header-number">Página ${num_pagina}</span>
    </div>
    """)

    PAGINA_SUMARIO_FORMAL_A4 = Template("""
    <main class="a4-page page-break" id="secao-sumario">
        ${header_superior}
        <div class="w-full">
            <header class="border-b-2 border-brand-800 pb-1.5 mb-2.5 avoid-break">
                <h2 class="font-heading font-bold text-xl text-brand-900 leading-tight text-center">
                    Sumário
                </h2>
            </header>

            <div class="sumario-lista">
                ${itens_sumario}
            </div>
        </div>
    </main>
    """)

    SUMARIO_ITEM_LINHA = Template("""
    <a href="${link_ancora}" class="toc-row sumario-item group">
        <span class="font-mono text-brand-500 font-bold min-w-[62px] whitespace-nowrap shrink-0">${prefixo}</span>
        <span class="text-brand-900 font-medium group-hover:text-accent-blue truncate">${titulo}</span>
        <span class="toc-leader"></span>
        <span class="font-mono text-brand-600 font-bold shrink-0">${pagina}</span>
    </a>
    """)

    PAGINA_INTRODUCAO_A4 = Template("""
    <main class="a4-page page-break secao-introducao" id="secao-introducao">
        ${header_superior}
        <div>
            <header class="border-b-4 border-brand-800 pb-1.5 mb-2 avoid-break">
                <h2 class="font-heading font-bold text-2xl text-brand-900 leading-tight">
                    Introdução e Contexto Histórico
                </h2>
            </header>

            <section class="mb-2 avoid-break ">
                <div class="bg-white p-3 rounded-lg border border-brand-200 shadow-2xs secao-texto-continuo">
                    ${paragrafos_html}
                </div>
            </section>

            <!-- Tópicos em Bloco Vertical Estrito (um abaixo do outro) -->
            <div class="flex flex-col space-y-1 block avoid-break">
                <div class="block w-full bg-white border border-slate-200 border-l-4 border-l-brand-800 p-1.5 px-2.5 rounded-sm">
                    <div class="mb-0.5 text-slate-900 font-bold text-xs uppercase">
                        <span>Marco Regulatório: BNCC e Resolução CNE/CEB nº 1/2022</span>
                    </div>
                    <p class="text-[9px] text-slate-700 leading-snug m-0">
                        Superação do uso meramente instrumental dos computadores, consolidando a Computação como ciência e o desenvolvimento do Pensamento Computacional.
                    </p>
                </div>

                <div class="block w-full bg-white border border-slate-200 border-l-4 border-l-brand-800 p-1.5 px-2.5 rounded-sm">
                    <div class="mb-0.5 text-slate-900 font-bold text-xs uppercase">
                        <span>Bases Epistemológicas: Seymour Papert e Paulo Freire</span>
                    </div>
                    <p class="text-[9px] text-slate-700 leading-snug m-0">
                        Integração do construcionismo com a pedagogia da autonomia para promover a emancipação tecnológica dos estudantes como criadores ativos.
                    </p>
                </div>

                <div class="block w-full bg-white border border-slate-200 border-l-4 border-l-brand-800 p-1.5 px-2.5 rounded-sm">
                    <div class="mb-0.5 text-slate-900 font-bold text-xs uppercase">
                        <span>Viabilidade Pública: Hardware Aberto e Baixo Custo</span>
                    </div>
                    <p class="text-[9px] text-slate-700 leading-snug m-0">
                        Soluções modulares, plataformas de código aberto e componentes acessíveis para viabilizar laboratórios escolares em redes públicas.
                    </p>
                </div>
                <div class="block w-full bg-white border border-slate-200 border-l-4 border-l-brand-800 p-1.5 px-2.5 rounded-sm">
                    <div class="mb-0.5 text-slate-900 font-bold text-xs uppercase">
                        <span>
                            Interdisciplinaridade
                        </span>
                    </div>
                    <p class="text-[9px] text-slate-700 leading-snug m-0">
                        Suguestões de temas a serem abordados que vão além dos projetos como tecnologia e sociedade, matemática, física e
                        lógica.
                    </p>
                </div>
            </div>
        </div>
    </main>
    """)

    PAGINA_DIDATICA_4_PILARES_A4 = Template("""
    <main class="a4-page page-break" id="secao-didatica">
        ${header_superior}
        <div>
            <header class="border-b-4 border-brand-800 pb-2 mb-3 avoid-break">
                <h2 class="font-heading font-bold text-2xl text-brand-900 leading-tight">
                    Estrutura didática dos Projetos
                </h2>
            </header>

            <!-- Texto Introdutório: Atividades Extracurriculares e Autonomia -->
            <section class="mb-3 avoid-break">
                <div class="bg-white p-3 rounded-lg border border-brand-200 shadow-2xs secao-texto-continuo">
                    <h3 class="font-heading font-bold text-brand-900 text-xs uppercase tracking-wider mb-2">
                        Aplicação Extracurricular e Autonomia Estudantil
                    </h3>
                    <p class="text-brand-800 text-justify indent-4 font-normal">
                        Este manual foi concebido para extrapolar os limites do ensino curricular convencional, posicionando-se como um guia prático, flexível e dinâmico para a estruturação de atividades extracurriculares, tais como feiras de ciências, clubes de robótica, mostras tecnológicas, olimpíadas do conhecimento e oficinas de invenção. A proposta metodológica visa fomentar o protagonismo e a autonomia investigativa do estudante, encorajando-o a agir como um verdadeiro agente de criação tecnológica. Ao interagir diretamente com os componentes físicos e os ambientes de simulação, o aluno é incentivado a formular suas próprias hipóteses, diagnosticar falhas de circuitos e algoritmos, e projetar soluções de forma independente. Dessa forma, articula-se a criatividade com os pilares do pensamento computacional e da engenharia, transformando a curiosidade científica em projetos funcionais de impacto real.
                    </p>
                    <p class="text-brand-800 text-justify indent-4 font-normal">
                        Além disso, o ecossistema educacional contemporâneo beneficia-se enormemente do acesso facilitado a plataformas
                        digitais, simuladores online e ambientes virtuais de aprendizagem. Essa flexibilidade tecnológica garante que a prática
                        não fique restrita ao espaço ou ao tempo da sala de aula física: atividades que eventualmente não possam ser concluídas
                        durante o horário regular podem ser facilmente desdobradas como tarefas de casa, desafios de expansão ou projetos para
                        clubes de tecnologia. Dessa forma, as ferramentas virtuais democratizam o contato com a computação, permitindo que o
                        estudante continue explorando, criando e aprimorando seus projetos no seu próprio ritmo e de qualquer lugar.
                    </p>
                </div>
            </section>

            <!-- Modelagem Prévia de Engenharia: Esquema e Fluxograma -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3.5 avoid-break">
                <div class="bg-white p-3 rounded-lg border border-brand-200 shadow-2xs">
                    <div class="mb-1 text-brand-900 font-bold text-xs">
                        <span>Esquema Elétrico de Circuito</span>
                    </div>
                    <p class="text-[10px] text-brand-700 leading-relaxed m-0">
                        Diagramas completos de conexão na protoboard com especificação de pinagem, polaridades e resistores de proteção.
                    </p>
                </div>
                <div class="bg-white p-3 rounded-lg border border-brand-200 shadow-2xs">
                    <div class="mb-1 text-brand-900 font-bold text-xs">
                        <span>Fluxograma Lógico-Algorítmico</span>
                    </div>
                    <p class="text-[10px] text-brand-700 leading-relaxed m-0">
                        Mapeamento visual do algoritmo antes da programação, estruturando tomadas de decisão (if/else) e laços (loop).
                    </p>
                </div>
            </div>

            <!-- Apresentação Vertical das Ferramentas Digitais -->
            <section class="space-y-2.5 mb-3.5 avoid-break">
                <h3 class="font-heading font-bold text-brand-900 text-xs uppercase tracking-wider mb-1">
                    Ecossistema de Ferramentas Digitais
                </h3>

                <!-- Tinkercad -->
                <div class="bg-white p-2.5 rounded-lg border border-brand-200 shadow-2xs flex items-center gap-3">
                    <img src="https://cdn.simpleicons.org/tinkercad/005F9E" alt="Logo Tinkercad" class="w-10 h-10 object-contain shrink-0 p-1 bg-slate-50 border border-slate-200 rounded-md" />
                    <div>
                        <h4 class="font-heading font-bold text-brand-900 text-xs mb-0.5">
                            Tinkercad: Simulação Virtual e Prototipagem em Nuvem
                        </h4>
                        <p class="text-[10px] text-brand-700 leading-snug m-0">
                            Ambiente online e gratuito da Autodesk para modelagem e simulação interativa de circuitos e códigos C++ no navegador. Permite ao estudante experimentar, testar sensores/atuadores e depurar hipóteses sem risco de queima de componentes, viabilizando o estudo autônomo e a preparação prévia antes do laboratório físico.
                        </p>
                    </div>
                </div>

                <!-- Wokwi -->
                <div class="bg-white p-2.5 rounded-lg border border-brand-200 shadow-2xs flex items-center gap-3">
                    <img src="https://avatars.githubusercontent.com/u/56967200?s=280&v=4" alt="Logo Wokwi" class="w-10 h-10 object-contain shrink-0 p-1 bg-slate-50 border border-slate-200 rounded-md" />
                    <div>
                        <h4 class="font-heading font-bold text-brand-900 text-xs mb-0.5">
                            Wokwi: Simulação Avançada e Prototipagem de Microcontroladores ESP
                        </h4>
                        <p class="text-[10px] text-brand-700 leading-snug m-0">
                            Plataforma de simulação em nuvem voltada para o desenvolvimento de projetos baseados na arquitetura ESP (como ESP32 e ESP8266). Permite a validação de circuitos, integração com protocolos de conectividade Wi-Fi/IoT e execução de firmwares diretamente no navegador, eliminando a necessidade de hardware físico na etapa de testes e garantindo a prototipagem ágil desses microcontroladores.
                        </p>
                    </div>
                </div>

                <!-- GitHub -->
                <div class="bg-white p-2.5 rounded-lg border border-brand-200 shadow-2xs flex items-center gap-3">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="Logo GitHub" class="w-10 h-10 object-contain shrink-0 p-1 bg-slate-50 border border-slate-200 rounded-md" />
                    <div>
                        <h4 class="font-heading font-bold text-brand-900 text-xs mb-0.5">
                            GitHub: Repositório Aberto e Versionamento de Código
                        </h4>
                        <p class="text-[10px] text-brand-700 leading-snug m-0">
                            Plataforma de hospedagem e compartilhamento comunitário onde todos os códigos-fonte (.ino), esquemas elétricos e arquivos dos projetos estão organizados. Garante transparência pedagógica, histórico de versões e acesso rápido via QR Code para que alunos e professores possam baixar, estudar e expandir os códigos.
                        </p>
                    </div>
                </div>

                <!-- Arduino IDE -->
                <div class="bg-white p-2.5 rounded-lg border border-brand-200 shadow-2xs flex items-center gap-3">
                    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/arduino/arduino-original.svg" alt="Logo Arduino IDE" class="w-10 h-10 object-contain shrink-0 p-1 bg-slate-50 border border-slate-200 rounded-md" />
                    <div>
                        <h4 class="font-heading font-bold text-brand-900 text-xs mb-0.5">
                            Arduino IDE: Compilação, Upload e Monitoramento Serial
                        </h4>
                        <p class="text-[10px] text-brand-700 leading-snug m-0">
                            Software oficial de desenvolvimento utilizado na bancada para validar sintaxe, compilar e transferir o firmware via USB para a placa física. Disponibiliza o Monitor Serial como recurso essencial para leitura de variáveis, telemetria em tempo real e verificação dos estados operacionais do circuito.
                        </p>
                    </div>
                </div>
            </section>

            <!-- Diagrama Geral do Fluxo de Código em C++ -->
            <div class="bg-white p-2.5 rounded-lg border border-brand-200 shadow-2xs avoid-break">
                <h4 class="font-heading font-bold text-brand-900 text-xs uppercase tracking-wider mb-1.5">
                    Diagrama Geral do Fluxo de Código em C++
                </h4>
                <div class="code-flow-container m-0">
                    <span class="code-flow-step">Bibliotecas</span>
                    <span class="code-flow-arrow">&rarr;</span>
                    <span class="code-flow-step">Pinos e Constantes</span>
                    <span class="code-flow-arrow">&rarr;</span>
                    <span class="code-flow-step">setup()</span>
                    <span class="code-flow-arrow">&rarr;</span>
                    <span class="code-flow-step">Funções Auxiliares</span>
                    <span class="code-flow-arrow">&rarr;</span>
                    <span class="code-flow-step">loop()</span>
                </div>
            </div>
        </div>
    </main>
    """)

    PAGINA_FLUXOGRAMA_GERAL_A4 = Template("""
    <main class="a4-page page-break" id="secao-fluxograma-geral">
        ${header_superior}
        <div>
            <header class="border-b-4 border-brand-800 pb-2 mb-3.5 avoid-break">
                <h2 class="font-heading font-bold text-2xl text-brand-900 leading-tight">
                    Fluxograma Geral Integrado dos Projetos
                </h2>
            </header>

            <!-- Card Pedagógico: Aplicação Multinível e Aprofundamento -->
            <section class="mb-3.5 avoid-break">
                <div class="bg-white p-3.5 rounded-lg border border-brand-200 shadow-2xs">
                    <p class="text-[10.5px] text-brand-800 leading-relaxed text-justify indent-4 m-0 font-normal">
                        A progressão pedagógica apresentada neste fluxograma organiza as competências de forma modular e contínua. Os projetos propostos para etapas e anos anteriores podem ser plenamente aplicados em anos mais avançados sem a necessidade de simplificar os conteúdos ou reduzir os desafios técnicos. A diferenciação reside essencialmente no nível de aprofundamento investigativo, na sofisticação da modelagem algorítmica e na autonomia dos estudantes na prototipagem física. Teoricamente, todas as crianças e jovens são plenamente capazes de desenvolver as atividades práticas aqui delineadas, respeitando-se suas trajetórias singulares, seus conhecimentos prévios e o ritmo de aprendizagem de cada faixa etária.
                    </p>
                    <p class="text-[10.5px] text-brand-800 leading-relaxed text-justify indent-4 m-0 font-normal">
                        Para garantir a máxima eficácia dessa abordagem, é fundamental que a seleção dos projetos seja adaptada à realidade, aos
                        recursos e ao nível de maturidade de cada turma. A sequência de atividades apresentada neste manual não exige uma
                        execução estritamente linear, permitindo que o educador priorize os temas que melhor se conectem com o contexto local
                        dos estudantes. Contudo, é indispensável atentar para a progressão dos conceitos fundamentais envolvidos: ainda que a
                        ordem dos projetos seja flexibilizada, os requisitos conceituais e lógicos de cada etapa devem ser devidamente abordados
                        e consolidados antes do avanço para estruturas de maior complexidade, assegurando uma aprendizagem sólida e integrada.
                    </p>
                    <p class="text-[10.5px] text-brand-800 leading-relaxed text-justify indent-4 m-0 font-normal">
                        No que tange à Educação Infantil, é imperativo respeitar o tempo de desenvolvimento cognitivo, a fase de alfabetização e
                        a maturação motora dos estudantes. Nessa etapa, a inserção dos fundamentos computacionais não deve envolver a escrita de
                        códigos ou o uso de telas digitais; pelo contrário, deve ser pautada exclusivamente pela computação desplugada. O
                        aprendizado deve ocorrer por meio de dinâmicas lúdicas, brincadeiras corporais, jogos de mesa, circuitos motores e
                        manipulação de materiais concretos. Essa abordagem garante a construção do raciocínio lógico, do reconhecimento de
                        padrões e da espacialidade de forma saudável, promovendo uma relação equilibrada e pedagógica com a tecnologia desde os
                        primeiros anos.
                    </p>
                </div>
            </section>

            <!-- Fluxograma Panorâmico com Borda e Legenda Técnica em Fundo Cinza -->
            <div class="bg-slate-100 border border-slate-200 rounded-xl p-3 text-center avoid-break shadow-2xs">
                <img src="${img_src}" alt="Fluxograma Geral dos Projetos" class="w-full max-h-[165mm] object-contain mx-auto rounded mb-1.5" />
                <span class="font-mono text-[9px] font-bold text-slate-500 uppercase tracking-wider block">
                    FIGURA GERAL: FLUXOGRAMA DE INTEGRAÇÃO DOS PROJETOS E NÍVEIS DE ENSINO
                </span>
            </div>
        </div>
    </main>
    """)

    BLOCO_GITHUB = Template("""
    <div class="github-box avoid-break">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-white text-[20px]">code</span>
            </div>
            <div>
                <span class="text-[11px] font-bold tracking-wide uppercase block text-brand-200">Repositório GitHub</span>
                <p class="text-[10px] text-brand-100 leading-snug m-0">
                    Acesse o código-fonte C++ completo e atualizado escaneando o QR Code ao lado ou acessando o repositório no GitHub.
                </p>
            </div>
        </div>
        <div class="flex flex-col items-center justify-center bg-white p-1 rounded shadow-xs shrink-0">
            <a href="${link_github}" target="_blank" rel="noopener noreferrer" title="Acessar repositório no GitHub">
                <img src="${qr_github_src}" alt="QR Code GitHub" class="w-11 h-11 object-contain" />
            </a>
            <span class="text-[6.5px] font-bold text-brand-900 uppercase font-mono mt-0.5">GitHub</span>
        </div>
    </div>
    """)

    FLUXO_CODIGO_SETAS = Template("""
    <div class="bg-brand-50/70 border border-brand-200 p-2.5 rounded-lg mb-3 avoid-break">
        <span class="font-mono text-[9px] font-bold text-brand-700 uppercase tracking-wider block mb-1.5">
            Sequência de Estruturação do Código
        </span>
        <div class="code-flow-container m-0">
            ${passos_html}
        </div>
    </div>
    """)

    QR_CODE_TINKERCAD = Template("""
    <div class="flex flex-col items-center justify-center border border-brand-200 bg-white p-1 rounded shadow-xs shrink-0 avoid-break">
        <a href="${link}" target="_blank" rel="noopener noreferrer" title="Acessar no Tinkercad">
            <img src="${src}" alt="QR Code Tinkercad" class="w-12 h-12 object-contain" />
        </a>
        <span class="text-[7px] font-bold text-brand-800 uppercase tracking-tighter mt-0.5">Tinkercad</span>
    </div>
    """)

    DESAFIO_ITEM_COM_BADGE = Template("""
    <div class="flex items-center justify-between gap-3 bg-white p-2.5 rounded-md border border-slate-200/80 shadow-2xs avoid-break mb-2">
        <p class="text-[10px] text-slate-800 leading-snug m-0 font-medium flex-1">${desc}</p>
        <div class="flex items-center justify-center text-[9px] font-bold uppercase px-3 py-1.5 rounded-md shrink-0 min-w-[90px] text-center ${badge_class}">
            ${nivel}
        </div>
    </div>
    """)

    DESAFIO_ITEM_SIMPLES = Template("""
    <div class="bg-white p-2.5 rounded-md border border-slate-200/80 text-[10px] text-slate-800 font-medium avoid-break mb-2">
        ${desc}
    </div>
    """)

    DESAFIOS_DE_EXPANSAO = Template("""
    <section class="bg-slate-100 border border-slate-200 p-3.5 rounded-lg avoid-break mb-3.5">
        <h3 class="font-heading font-bold text-slate-800 text-[11.5px] uppercase tracking-wide mb-2 pb-1 border-b border-slate-300">
            DESAFIOS DE EXPANSÃO
        </h3>
        ${desafios_html}
    </section>
    """)

    DESAFIOS_CONTAINER = DESAFIOS_DE_EXPANSAO

    ESTIMULO_POS_FLUXOGRAMA = Template("""
    <div class="bg-emerald-50/80 border border-emerald-200 border-l-4 border-l-emerald-600 p-2.5 rounded-sm mb-3 avoid-break">
        <div class="flex items-start gap-2">
            <span class="text-sm shrink-0 leading-none mt-0.5"></span>
            <div>
                <span class="font-heading font-bold text-emerald-950 text-[10.5px] uppercase tracking-wide block mb-0.5">
                    Explore e Modifique
                </span>
                <p class="text-[10px] text-emerald-900 leading-relaxed m-0">
                    O fluxograma e o código fornecidos são a base do projeto. Incentive os estudantes a alterarem trechos do algoritmo (como intervalos de tempo, frequências sonoras, padrões de repetição e limites lógicos) e a proporem novas funcionalidades, estimulando a criatividade, a experimentação ativa e a autonomia investigativa.
                </p>
            </div>
        </div>
    </div>
    """)

    SECAO_TRECHO_CODIGO = Template("""
    <section class="mb-3.5 avoid-break">
        <h3 class="font-heading font-bold text-slate-900 text-[11.5px] uppercase tracking-wide mb-2 pb-1 border-b border-slate-200">
            TRECHO DO CÓDIGO-FONTE
        </h3>
        <div class="border border-brand-900 rounded-lg overflow-hidden shadow-xs mb-2">
            <div class="bg-brand-900 px-3.5 py-1.5 flex items-center justify-between">
                <span class="text-brand-100 font-mono text-[10px] font-semibold tracking-wide">${subtitulo}</span>
                <span class="text-[9px] font-mono text-brand-300 font-medium">C++ / Arduino</span>
            </div>
            ${html_exp}
            <div class="bg-white p-3 overflow-x-auto code-block">
                <pre class="m-0"><code class="text-black text-[9.5px] font-mono leading-relaxed whitespace-pre-wrap break-words">${codigo}</code></pre>
            </div>
        </div>
        <div class="bg-amber-50/90 border border-amber-200 rounded-md p-2.5 flex items-start gap-2 text-amber-950">
            <span class="text-sm shrink-0 leading-none mt-0.5"></span>
            <p class="text-[9.5px] leading-relaxed m-0 font-normal">
                <strong>Nota:</strong> Por motivos didáticos e de síntese visual, exibimos acima apenas o trecho principal da lógica do algoritmo. O código-fonte integral em C++ (com todas as rotinas auxiliares, mapeamentos de pinos e laço de setup) está disponível para consulta e download via QR Code do Repositório GitHub.
            </p>
        </div>
    </section>
    """)

    EXPLICACAO_CODIGO = Template(
        '<div class="bg-brand-100/50 p-2 border-b border-brand-200 text-[10px] text-brand-900 leading-relaxed italic">'
        '<strong>Explicação:</strong> ${exp}</div>'
    )

    BLOCO_CODIGO = Template("""
    <div class="border border-brand-800 rounded-lg overflow-hidden shadow-sm mb-4">
        <div class="bg-brand-800 px-3 py-1 flex items-center justify-between">
            <span class="text-brand-100 font-mono text-[10px] font-semibold">${nome}</span>
        </div>
        ${html_exp}
        <div class="bg-brand-50 p-2.5 overflow-x-auto code-block">
            <pre class="m-0"><code class="text-brand-900 text-[10px] font-mono whitespace-pre-wrap break-words">${codigo}</code></pre>
        </div>
    </div>
    """)

    DIAGRAMA_ESQUEMA = Template("""
    <div class="bg-slate-100 rounded-xl p-3 text-center avoid-break mb-3">
        <img src="${img_src}" alt="Esquema do Circuito" class="max-h-60 mx-auto object-contain rounded mb-1.5" />
        <span class="font-mono text-[9px] font-bold text-slate-500 uppercase tracking-wider block">FIGURA 1: ESQUEMA DO CIRCUITO ELETRÔNICO</span>
    </div>
    """)

    DIAGRAMA_FLUXOGRAMA = Template("""
    <div class="bg-slate-100 rounded-xl p-3 text-center avoid-break mb-3">
        <img src="${img_src}" alt="Fluxograma Lógico" class="max-h-100 mx-auto object-contain rounded mb-1.5" />
        <span class="font-mono text-[9px] font-bold text-slate-500 uppercase tracking-wider block">FIGURA 2: FLUXOGRAMA LÓGICO-ALGORÍTMICO</span>
    </div>
    """)

    HEADER_DETALHAMENTO = Template("""
    <header class="mb-3 avoid-break border-b-2 border-brand-800 pb-1.5">
        <h3 class="font-heading font-extrabold text-base text-brand-900">${codigo} - Detalhamento e Prática</h3>
    </header>
    """)

    ROTEIRO_PRATICO = Template("""
    <section class="bg-sky-50/70 border border-sky-200 p-3.5 rounded-lg avoid-break mb-3.5">
        <h3 class="font-heading font-bold text-sky-950 text-[11.5px] uppercase tracking-wide mb-2 pb-1 border-b border-sky-200">
            ROTEIRO PRÁTICO DE EXECUÇÃO
        </h3>
        <ol class="list-decimal pl-4 space-y-2 text-[10px] text-slate-800 leading-[1.6]">${roteiro_lis}</ol>
    </section>
    """)

    ARTICULACAO_APROFUNDAMENTO = Template("""
    <section class="bg-emerald-50/70 border border-emerald-200 p-3.5 rounded-lg mb-3.5 avoid-break">
        <h3 class="font-heading font-bold text-emerald-950 text-[11.5px] uppercase tracking-wide mb-2 pb-1 border-b border-emerald-200">
            ARTICULAÇÃO E APROFUNDAMENTO TEÓRICO
        </h3>
        <div class="pl-4 space-y-2 text-[10px] text-slate-800 leading-[1.6] m-0">
            ${articulacao}
        </div>
    </section>
    """)

    PAGINA_CAPA_A4 = Template("""
    <main class="a4-page page-break" id="${id_ancora}">
        ${header_superior}
        <div>
            <header class="flex items-start justify-between mb-3.5 avoid-break border-b-2 border-brand-800 pb-2.5 gap-4">
                <div class="flex-1">
                    <span class="font-mono text-brand-500 text-[10px] font-bold tracking-widest uppercase block mb-0.5">${modulo}</span>
                    <h2 class="font-heading font-extrabold text-xl text-brand-900 mb-0.5 leading-tight">${codigo} - ${titulo}</h2>
                </div>
                ${qr_code}
            </header>

            <div class="flex flex-col gap-2.5 mb-3 avoid-break">
                <!-- Especificações Técnicas: barra verde sinalizando orientação pedagógica -->
                <div class="bg-white border border-slate-200 border-l-4 border-l-emerald-600 p-2.5 rounded-sm">
                    <h3 class="font-heading font-bold text-brand-900 mb-1 text-[10.5px] uppercase tracking-wider">
                        Especificações Técnicas
                    </h3>
                    <ul class="text-[10.5px] space-y-0.5 text-slate-800">
                        <li><strong class="text-slate-900">Complexidade:</strong> ${complexidade}</li>
                        <li><strong class="text-slate-900">Tempo Estimado:</strong> ${tempo}</li>
                        <li><strong class="text-slate-900">Pré-requisitos:</strong> ${prereq}</li>
                    </ul>
                </div>

                <!-- Articulação Curricular: barra verde sinalizando orientação pedagógica -->
                <div class="bg-white border border-slate-200 border-l-4 border-l-emerald-600 p-2.5 rounded-sm">
                    <h3 class="font-heading font-bold text-brand-900 mb-1 text-[10.5px] uppercase tracking-wider">
                        Articulação Curricular
                    </h3>
                    <p class="text-[10px] text-slate-800 leading-snug mb-1">
                        <strong class="text-slate-900">Interdisciplinaridade:</strong> ${inter_texto}
                    </p>
                    <strong class="text-[10px] text-slate-900 block mb-0.5">Habilidades de Computação:</strong>
                    <ul class="list-disc pl-4 text-[10px] text-slate-700 space-y-0.5">${habilidades_lis}</ul>
                </div>
            </div>

            <section class="mb-3 avoid-break">
                <h3 class="font-heading font-bold text-brand-900 text-xs mb-1.5 pb-0.5 border-b border-slate-200 uppercase tracking-wide">
                    Contextualização e Modelagem do Problema Real
                </h3>
                <div class="pl-3 border-l-2 border-slate-400 text-slate-800 text-[10.5px] space-y-1 text-justify leading-relaxed">
                    <p class="m-0">${contexto}</p>
                </div>
            </section>

            <section class="border border-sky-200 rounded-lg overflow-hidden mb-3 avoid-break bg-sky-50/60">
                <div class="bg-brand-900 text-white px-3.5 py-1.5">
                    <h3 class="font-heading font-bold text-[11px] uppercase tracking-wider m-0">
                        Arquitetura de Hardware e Lista de Materiais
                    </h3>
                </div>
                <div class="p-3">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <h4 class="font-heading font-bold text-slate-900 text-[10.5px] uppercase tracking-wide mb-1.5 pb-0.5 border-b border-sky-200">
                                Lista de Materiais (BOM)
                            </h4>
                            <table class="w-full text-left border-collapse">
                                <thead>
                                    <tr class="border-b-2 border-slate-700 text-slate-900 text-[10px]">
                                        <th class="py-1 px-2 font-bold text-center w-14">Qtd</th>
                                        <th class="py-1 px-2 font-bold">Componente</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${bom_rows}
                                </tbody>
                            </table>
                        </div>
                        <div>
                            <h4 class="font-heading font-bold text-slate-900 text-[10.5px] uppercase tracking-wide mb-1.5 pb-0.5 border-b border-sky-200">
                                Mapeamento de Pinos
                            </h4>
                            <div class="bg-white/80 p-2.5 rounded-md border border-sky-200/80">
                                <ul class="font-mono text-[9.5px] text-slate-800 space-y-1">${pinos_lis}</ul>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </main>
    """)

    PAGINA_DINAMICA_A4 = Template("""
    <main class="a4-page page-break">
        ${header_superior}
        <div>
            ${header_continuidade}
            <section>
                ${html_chunk}
            </section>
        </div>
    </main>
    """)


# ==============================================================================
# FUNÇÕES DE TRATAMENTO DE DADOS E FORMATAÇÃO
# ==============================================================================

def carregar_projetos(caminho_json: Path) -> List[Dict[str, Any]]:
    """Carrega e valida o arquivo JSON/TXT contendo a lista de projetos."""
    if not caminho_json.exists():
        print(f"[ERRO] Arquivo não encontrado: {caminho_json.resolve()}")
        return []

    with open(caminho_json, "r", encoding="utf-8") as f:
        try:
            dados = json.load(f)
            print(f"[OK] {len(dados)} projeto(s) carregado(s) de '{caminho_json.name}'.")
            return dados
        except json.JSONDecodeError as err:
            print(f"[ERRO] Falha ao ler o formato JSON em '{caminho_json.name}': {err}")
            return []


def sanitizar_slug(texto: str) -> str:
    """Gera um slug HTML seguro a partir de um código ou título."""
    limpo = re.sub(r"[^\w\s-]", "", texto.lower())
    return re.sub(r"[-\s]+", "-", limpo).strip("-")


def gerar_qr_code_asset(link: str, output_path: Optional[Path] = None) -> str:
    """
    Gera o QR Code para uma URL, salvando opcionalmente no disco e retornando data URI base64.
    """
    if not link or not str(link).strip():
        return ""

    link_str = str(link).strip()

    try:
        import qrcode

        qr = qrcode.QRCode(version=1, box_size=3, border=1)
        qr.add_data(link_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(output_path), format="PNG")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{img_b64}"
    except ImportError:
        encoded_url = urllib.parse.quote(link_str, safe="")
        return f"https://api.qrserver.com/v1/create-qr-code/?size=120x120&data={encoded_url}"


def gerar_qr_code_html(link: Optional[str]) -> str:
    """Gera o HTML do QR Code para o Tinkercad."""
    if not link or not str(link).strip():
        return ""

    link_str = str(link).strip()
    src = gerar_qr_code_asset(link_str)
    return HTMLTemplates.QR_CODE_TINKERCAD.substitute(
        link=html.escape(link_str),
        src=src
    )


def gerar_bloco_github(prj: Dict[str, Any], slug: str, base_dir: Path) -> str:
    """Gera o bloco de aviso e QR Code do repositório GitHub para o projeto."""
    link_github = (
        prj.get("LINK_GITHUB")
        or prj.get("GITHUB")
        or prj.get("REPOSITORIO")
        or f"https://github.com/cadu-leal/manual-computacao-escolar/tree/main/{slug}"
    )

    qr_path = base_dir / "projetos" / f"{slug}_github_qr.png"
    qr_src = gerar_qr_code_asset(link_github, output_path=qr_path)

    return HTMLTemplates.BLOCO_GITHUB.substitute(
        link_github=html.escape(link_github),
        qr_github_src=qr_src
    )


def renderizar_fluxo_setas(prj: Dict[str, Any], secoes_codigo: List[Dict[str, str]]) -> str:
    """Renderiza a sequência do código interligada por setas direcionais."""
    fluxo = (
        prj.get("FLUXO_ESTRUTURA_CODIGO")
        or prj.get("FLUXO_CODIGO")
        or prj.get("SEQUENCIA_CODIGO")
    )

    if isinstance(fluxo, list) and len(fluxo) > 0:
        passos = [str(p).strip() for p in fluxo]
    elif secoes_codigo:
        passos = [s.get("nome", "").strip() for s in secoes_codigo if s.get("nome")]
    else:
        passos = [
            "Definição de Pinos",
            "Setup",
            "Liga LED",
            "Desligar LED",
            "Sequenciar LEDs",
            "Start",
            "Game Over",
            "Loop"
        ]

    elementos_html = []
    for idx, passo in enumerate(passos):
        elementos_html.append(f'<span class="code-flow-step">{html.escape(passo)}</span>')
        if idx < len(passos) - 1:
            elementos_html.append('<span class="code-flow-arrow">&rarr;</span>')

    return HTMLTemplates.FLUXO_CODIGO_SETAS.substitute(passos_html=" ".join(elementos_html))


def renderizar_lista(val: Union[List[Any], str, None], remover_numeracao: bool = False) -> str:
    """Converte listas e textos para itens <li> HTML higienizados."""
    if isinstance(val, list) and len(val) > 0:
        items = []
        for item in val:
            if isinstance(item, dict):
                nivel = html.escape(str(item.get("nivel", "")))
                desc = str(item.get("descricao", ""))
                if remover_numeracao:
                    desc = re.sub(r"^\s*\d+[\.\)\-]\s*", "", desc)
                desc = html.escape(desc)
                prefix = f"<strong>[{nivel}]</strong> " if nivel else ""
                items.append(f"<li>{prefix}{desc}</li>")
            else:
                texto = str(item)
                if remover_numeracao:
                    texto = re.sub(r"^\s*\d+[\.\)\-]\s*", "", texto)
                items.append(f"<li>{html.escape(texto)}</li>")
        return "".join(items)
    elif isinstance(val, str) and val.strip():
        texto = val
        if remover_numeracao:
            texto = re.sub(r"^\s*\d+[\.\)\-]\s*", "", texto)
        return f"<li>{html.escape(texto)}</li>"

    return "<li class='text-gray-400 italic'>A preencher</li>"


def renderizar_desafios(val: Union[List[Any], str, None]) -> str:
    """Renderiza os Desafios de Expansão com a dificuldade centralizada à direita."""
    if not val:
        return "<p class='text-gray-400 italic text-[10px]'>Nenhum desafio cadastrado.</p>"

    if isinstance(val, str):
        return f"<p class='text-[10px] text-slate-700'>{html.escape(val)}</p>"

    items_html = []
    for item in val:
        if isinstance(item, dict):
            nivel = str(item.get("nivel", "")).strip()
            desc = html.escape(str(item.get("descricao", "")).strip())

            badge_class = "bg-slate-200 text-slate-700"
            if any(k in nivel for k in ["Fácil", "Facil", "Básico", "Basico"]):
                badge_class = "bg-emerald-100 text-emerald-800 border border-emerald-300"
            elif any(k in nivel for k in ["Intermediário", "Intermediario"]):
                badge_class = "bg-amber-100 text-amber-800 border border-amber-300"
            elif any(k in nivel for k in ["Avançado", "Avancado", "Hardware", "Interrupção"]):
                badge_class = "bg-red-100 text-red-800 border border-red-300"

            item_str = HTMLTemplates.DESAFIO_ITEM_COM_BADGE.substitute(
                desc=desc,
                badge_class=badge_class,
                nivel=html.escape(nivel),
            )
            items_html.append(item_str)
        else:
            desc = html.escape(str(item).strip())
            item_str = HTMLTemplates.DESAFIO_ITEM_SIMPLES.substitute(desc=desc)
            items_html.append(item_str)

    return '<div class="space-y-1.5">' + "".join(items_html) + "</div>"


def dividir_codigo_por_comentarios(codigo: str) -> List[Dict[str, str]]:
    """Divide código C++/Arduino em seções lógicas baseando-se em comentários de separação."""
    if not codigo or not codigo.strip():
        return []

    pattern = re.compile(r"//\s*={3,}\s*\n//\s*(.*?)\s*\n//\s*={3,}")
    matches = list(pattern.finditer(codigo))

    if not matches:
        return [{"nome": "Código Fonte (sketch.ino)", "codigo": codigo, "explicacao": ""}]

    blocos = []
    if matches[0].start() > 0:
        codigo_inicial = codigo[:matches[0].start()].strip()
        if codigo_inicial:
            blocos.append({"nome": "Definições e Bibliotecas", "codigo": codigo_inicial})

    for i in range(len(matches)):
        titulo = matches[i].group(1).strip()
        inicio_codigo = matches[i].end()
        fim_codigo = matches[i + 1].start() if i + 1 < len(matches) else len(codigo)

        trecho_codigo = codigo[inicio_codigo:fim_codigo].strip()
        if trecho_codigo:
            blocos.append({"nome": titulo, "codigo": trecho_codigo, "explicacao": ""})

    return blocos


def formatar_articulacao_teorica(art_raw: str) -> str:
    """
    Formata os tópicos da articulação teórica com recuo pl-4, space-y-2 e tópicos em negrito.
    """
    if not art_raw or not art_raw.strip():
        return "<p class='text-gray-400 italic text-[10px] m-0'>A preencher</p>"

    paragrafos = [p.strip() for p in art_raw.split("\n\n") if p.strip()]
    items_html = []
    for p in paragrafos:
        p_esc = html.escape(p)
        # Identifica tópicos no formato "1) Título: resto" ou "1. Título: resto"
        match = re.match(r"^\d+[\)\.]\s*([^:]+:)(.*)$", p_esc, re.DOTALL)
        if match:
            topico, resto = match.group(1), match.group(2)
            items_html.append(f'<p class="m-0"><strong class="font-bold text-slate-900">{topico}</strong>{resto}</p>')
        else:
            items_html.append(f'<p class="m-0">{p_esc}</p>')

    return "\n".join(items_html)


def renderizar_trecho_codigo_fonte(logica_data: Optional[Dict[str, Any]]) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    """
    Renderiza com precisão editorial apenas o trecho central/mais relevante da lógica (Loop Principal),
    com título padronizado 'TRECHO DO CÓDIGO-FONTE', subtítulo descritivo no header escuro
    e caixa de aviso pedagógica com QR Code logo abaixo.
    """
    if not isinstance(logica_data, dict):
        logica_data = {}

    fontes = (
        logica_data.get("CODIGOS")
        or logica_data.get("ARQUIVOS_CODIGO")
        or logica_data.get("CODIGO_FONTE")
    )
    lista_codigos = []

    if isinstance(fontes, str):
        lista_codigos = dividir_codigo_por_comentarios(fontes)
    elif isinstance(fontes, list):
        for idx, item in enumerate(fontes, start=1):
            if isinstance(item, dict):
                nome = item.get("nome") or item.get("arquivo") or f"Seção {idx}"
                code = item.get("codigo") or item.get("conteudo") or ""
                exp = item.get("explicacao") or item.get("descricao") or ""
                lista_codigos.append({"nome": nome, "codigo": code, "explicacao": exp})
            elif isinstance(item, str):
                lista_codigos.extend(dividir_codigo_por_comentarios(item))

    # Seleciona preferencialmente o trecho que contém o Loop Principal ou void loop
    trecho_escolhido = None
    for item in lista_codigos:
        nome_l = str(item.get("nome", "")).lower()
        code_l = str(item.get("codigo", "")).lower()
        if "loop" in nome_l or "void loop" in code_l or "principal" in nome_l:
            trecho_escolhido = item
            break

    if not trecho_escolhido:
        trecho_escolhido = lista_codigos[0] if lista_codigos else {
            "nome": "Loop Principal",
            "codigo": "// Loop Principal a ser preenchido",
            "explicacao": ""
        }

    nome_orig = str(trecho_escolhido.get("nome", "Loop Principal")).strip()
    codigo_str = str(trecho_escolhido.get("codigo", "")).strip()
    exp_str = str(trecho_escolhido.get("explicacao", "")).strip()

    # Subtítulo preciso da função
    if "loop" in nome_orig.lower():
        subtitulo = "Loop Principal - Lógica de Controle do Jogo"
    else:
        subtitulo = f"{nome_orig} - Lógica de Controle"

    linhas = codigo_str.split("\n")
    if len(linhas) > 35:
        linhas = linhas[:35]
        codigo_str = "\n".join(linhas) + "\n\n// ... (código completo disponível no GitHub)"

    html_exp = (
        HTMLTemplates.EXPLICACAO_CODIGO.substitute(exp=html.escape(exp_str))
        if exp_str
        else ""
    )

    html_bloco = HTMLTemplates.SECAO_TRECHO_CODIGO.substitute(
        subtitulo=html.escape(subtitulo),
        html_exp=html_exp,
        codigo=html.escape(codigo_str)
    )

    linhas_peso = min(len(linhas), 35) + 8

    bloco_resultado = {
        "html": html_bloco,
        "linhas_peso": linhas_peso
    }

    return bloco_resultado, lista_codigos


def renderizar_blocos_codigo(logica_data: Optional[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    """Função de compatibilidade retroativa que delega para renderizar_trecho_codigo_fonte."""
    bloco, lista = renderizar_trecho_codigo_fonte(logica_data)
    return [bloco], lista


# ==============================================================================
# GERAÇÃO DAS PÁGINAS EDITORIAIS
# ==============================================================================

def gerar_html_sumario_formal(projetos_info: List[Dict[str, Any]], num_pagina: int = 2) -> str:
    """
    Gera o Sumário Formal do Livro (Table of Contents) imediatamente após a Capa.
    """
    header_sup = HTMLTemplates.HEADER_PAGINACAO_SUPERIOR.substitute(
        titulo_secao="Manual Didático de Computação • Sumário",
        num_pagina=f"{num_pagina:02d}"
    )

    # 1. Fundamentos e Estrutura
    fundamentos = [
        {"prefixo": "01.", "titulo": "Introdução e Contexto Histórico da Computação Escolar", "pagina": "Pág. 03", "link": "#secao-introducao"},
        {"prefixo": "02.", "titulo": "Estrutura didática dos Projetos", "pagina": "Pág. 04", "link": "#secao-didatica"},
        {"prefixo": "03.", "titulo": "Fluxograma Geral Integrado dos Projetos", "pagina": "Pág. 05", "link": "#secao-fluxograma-geral"},
    ]
    html_fund = []
    for item in fundamentos:
        html_fund.append(
            HTMLTemplates.SUMARIO_ITEM_LINHA.substitute(
                prefixo=item["prefixo"],
                titulo=item["titulo"],
                link_ancora=item["link"],
                pagina=item["pagina"]
            )
        )

    # 2. Módulos Curriculares
    modulos = [
        {"prefixo": "MÓD. I", "titulo": "Interação Lúdica e Pensamento Desplugado (Educação Infantil)", "pagina": "Pág. 06", "link": "#modulo-1"},
        {"prefixo": "MÓD. II", "titulo": "Introdução à Programação e Controle (Ensino Fundamental I)", "pagina": "Pág. 07", "link": "#modulo-2"},
        {"prefixo": "MÓD. III", "titulo": "Sistemas Embarcados, Sensores e Lógica Formal (Ensino Fundamental II)", "pagina": "Pág. 08", "link": "#modulo-3"},
        {"prefixo": "MÓD. IV", "titulo": "Integração de Sistemas, IoT e Soluções Complexas (Ensino Médio)", "pagina": "Pág. 09", "link": "#modulo-4"},
    ]
    html_mod = []
    for item in modulos:
        html_mod.append(
            HTMLTemplates.SUMARIO_ITEM_LINHA.substitute(
                prefixo=item["prefixo"],
                titulo=item["titulo"],
                link_ancora=item["link"],
                pagina=item["pagina"]
            )
        )

    # 3. Projetos Práticos Dinâmicos
    html_prj = []
    for prj in projetos_info:
        codigo = prj["codigo"]
        titulo = prj["titulo"]
        pagina_num = prj["pagina_inicio"]
        slug = prj["slug"]

        html_prj.append(
            HTMLTemplates.SUMARIO_ITEM_LINHA.substitute(
                prefixo=html.escape(codigo),
                titulo=html.escape(titulo),
                link_ancora=f"#{slug}",
                pagina=f"Pág. {pagina_num:02d}"
            )
        )

    if not html_prj:
        html_prj.append("<p class='text-gray-400 italic text-[11px] pl-1'>Nenhum projeto cadastrado.</p>")

    itens_todos = html_fund + html_mod + html_prj

    return HTMLTemplates.PAGINA_SUMARIO_FORMAL_A4.substitute(
        header_superior=header_sup,
        itens_sumario="\n".join(itens_todos)
    )


def gerar_html_introducao(num_pagina: int = 3) -> str:
    """
    Gera a página de Introdução oficial com os 6 novos parágrafos e tópicos verticais.
    """
    header_sup = HTMLTemplates.HEADER_PAGINACAO_SUPERIOR.substitute(
        titulo_secao="Manual Didático de Computação • Introdução",
        num_pagina=f"{num_pagina:02d}"
    )

    paragrafos = []
    for p in TEXTO_INTRODUCAO_OFICIAL:
        paragrafos.append(
            f'<p class="text-brand-800 text-justify indent-6 font-normal">'
            f'{html.escape(p)}'
            f'</p>'
        )

    return HTMLTemplates.PAGINA_INTRODUCAO_A4.substitute(
        header_superior=header_sup,
        paragrafos_html="\n".join(paragrafos)
    )


def gerar_html_didatica_4_pilares(num_pagina: int = 4) -> str:
    """
    Gera a página explicativa da Estrutura Didática dos Projetos e Ferramentas Digitais.
    """
    header_sup = HTMLTemplates.HEADER_PAGINACAO_SUPERIOR.substitute(
        titulo_secao="Manual Didático de Computação • Estrutura didática dos Projetos",
        num_pagina=f"{num_pagina:02d}"
    )

    return HTMLTemplates.PAGINA_DIDATICA_4_PILARES_A4.substitute(
        header_superior=header_sup
    )


def gerar_html_fluxograma_geral(num_pagina: int = 5, img_nome: str = "Projetos.png") -> str:
    """
    Gera a página A4 dedicada ao Fluxograma Geral Integrado dos Projetos com explicação de progressão e aprofundamento.
    """
    header_sup = HTMLTemplates.HEADER_PAGINACAO_SUPERIOR.substitute(
        titulo_secao="Manual Didático de Computação • Fluxograma Geral",
        num_pagina=f"{num_pagina:02d}"
    )

    return HTMLTemplates.PAGINA_FLUXOGRAMA_GERAL_A4.substitute(
        header_superior=header_sup,
        img_src=img_nome
    )


# ==============================================================================
# PIPELINE DE GERAÇÃO E PAGINAÇÃO VOLUMÉTRICA A4 DO PROJETO
# ==============================================================================

def gerar_html_projeto(
    prj: Dict[str, Any],
    slug_id: Optional[str] = None,
    pagina_inicial: int = 10,
    base_dir: Optional[Path] = None
) -> Tuple[str, int]:
    """
    Gera as páginas do projeto distribuindo o conteúdo harmonicamente no formato A4:
    - Página 1: Header de paginação, Informações Gerais, Competências, Modelagem Real, BOM e Mapeamento de Pinos
    - Páginas seguintes: Detalhamento Técnico (Diagramas, Fluxograma, Código C++, Roteiro, Articulação e Desafios)
    """
    if base_dir is None:
        base_dir = Path(__file__).parent.resolve()

    codigo = html.escape(str(prj.get("PROJETO", "PRJ X.X")))
    modulo = html.escape(str(prj.get("MODULO", "Módulo")))
    titulo = html.escape(str(prj.get("TITULO", "Sem título")))
    complexidade = html.escape(str(prj.get("COMPLEXIDADE", "Básico")))
    tempo = html.escape(str(prj.get("TEMPO_ESTIMADO", "50 min")))
    prereq = html.escape(str(prj.get("PRE_REQUISITOS", "Nenhum")))

    if not slug_id:
        slug_id = sanitizar_slug(str(prj.get("PROJETO", "prj")))

    hw_data = prj.get("ARQUITETURA_DE_HARDWARE_E_LISTA_DE_MATERIAIS", {})
    if not isinstance(hw_data, dict):
        hw_data = {}

    link_tinkercad = (
        prj.get("LINK")
        or prj.get("LINK_THINKERCAD")
        or prj.get("LINK_TINKERCAD")
        or hw_data.get("LINK_THINKERCAD")
        or hw_data.get("LINK_TINKERCAD")
        or ""
    )
    html_qr_code = gerar_qr_code_html(link_tinkercad)
    habilidades_lis = renderizar_lista(prj.get("HABILIDADES_DE_COMPUTACAO", []))

    inter_info = prj.get("COMPETENCIA_INTERDISCIPLINARES", {})
    if isinstance(inter_info, dict):
        inter_texto = " | ".join([f"{k}: {v}" for k, v in inter_info.items()])
    else:
        inter_texto = str(inter_info)
    inter_texto = html.escape(inter_texto)

    contexto = html.escape(str(prj.get("CONTEXTUALIZACAO_E_MODELAGEM_DO_PROBLEMA_REAL", "A preencher")))
    bom_items = hw_data.get("BOM", [])
    pinos_items = hw_data.get("MAPEAMENTO_PINOS", [])
    img_esquema = html.escape(str(hw_data.get("IMAGEM_ESQUEMA", "")))

    bom_rows = ""
    for item in bom_items:
        qtd = html.escape(str(item.get("qtd", "")))
        comp = html.escape(str(item.get("componente", "")))
        bom_rows += (
            f'<tr class="border-b border-sky-200/60"><td class="py-1.5 px-2 text-center font-mono font-medium text-slate-800 text-[9.5px]">{qtd}</td>'
            f'<td class="py-1.5 px-2 text-slate-800 text-[10px]">{comp}</td></tr>'
        )
    if not bom_rows:
        bom_rows = '<tr class="border-b border-sky-200/60"><td colspan="2" class="py-1.5 px-2 text-center text-slate-400 text-[10px]">A preencher</td></tr>'

    pinos_lis = renderizar_lista(pinos_items)
    logica_data = prj.get("MODELAGEM_LOGICO_ALGORITMA", {})
    img_fluxograma = (
        html.escape(str(logica_data.get("ARQUIVO", "")))
        if isinstance(logica_data, dict)
        else ""
    )

    roteiro_items = prj.get("ROTEIRO_PRATICO_DE_EXECUCAO", [])
    roteiro_lis = renderizar_lista(roteiro_items, remover_numeracao=True)

    art_raw = str(prj.get("ARTICULACAO_E_APROFUNDAMENTO", "A preencher"))
    articulacao = formatar_articulacao_teorica(art_raw)

    desafios_items = prj.get("DESAFIOS_DE_EXPANSAO", [])
    html_desafios = renderizar_desafios(desafios_items)

    html_img_esquema = (
        HTMLTemplates.DIAGRAMA_ESQUEMA.substitute(img_src=img_esquema)
        if img_esquema
        else ""
    )
    html_img_fluxograma = (
        HTMLTemplates.DIAGRAMA_FLUXOGRAMA.substitute(img_src=img_fluxograma)
        if img_fluxograma
        else ""
    )

    # Processamento do trecho central de código e fluxo em setas
    bloco_codigo, secoes_raw = renderizar_trecho_codigo_fonte(logica_data if isinstance(logica_data, dict) else {})
    html_fluxo_setas = renderizar_fluxo_setas(prj, secoes_raw)
    bloco_github = gerar_bloco_github(prj, slug_id, base_dir)

    # --------------------------------------------------------------------------
    # PÁGINA 1 DO PROJETO: Header + Informações Gerais + BOM + Mapeamento de Pinos
    # --------------------------------------------------------------------------
    header_p1 = HTMLTemplates.HEADER_PAGINACAO_SUPERIOR.substitute(
        titulo_secao=f"{codigo} • Visão Geral e Materiais",
        num_pagina=f"{pagina_inicial:02d}"
    )

    p1 = HTMLTemplates.PAGINA_CAPA_A4.substitute(
        header_superior=header_p1,
        id_ancora=slug_id,
        modulo=modulo,
        codigo=codigo,
        titulo=titulo,
        qr_code=html_qr_code,
        complexidade=complexidade,
        tempo=tempo,
        prereq=prereq,
        inter_texto=inter_texto,
        habilidades_lis=habilidades_lis,
        contexto=contexto,
        bom_rows=bom_rows,
        pinos_lis=pinos_lis
    )

    # --------------------------------------------------------------------------
    # ELEMENTOS DINÂMICOS DAS PÁGINAS SEGUINTES
    # --------------------------------------------------------------------------
    elementos_dinamicos: List[Dict[str, Any]] = [
        {"html": HTMLTemplates.HEADER_DETALHAMENTO.substitute(codigo=codigo), "linhas_peso": 4}
    ]

    if html_img_esquema:
        elementos_dinamicos.append({"html": html_img_esquema, "linhas_peso": 14})

    if html_img_fluxograma:
        elementos_dinamicos.append({"html": html_img_fluxograma, "linhas_peso": 15})

    if html_fluxo_setas:
        elementos_dinamicos.append({"html": html_fluxo_setas, "linhas_peso": 5})

    elementos_dinamicos.append({"html": bloco_github, "linhas_peso": 5})

    if roteiro_items:
        html_roteiro = HTMLTemplates.ROTEIRO_PRATICO.substitute(roteiro_lis=roteiro_lis)
        peso_roteiro = 4 + (len(roteiro_items) * 2)
        elementos_dinamicos.append({"html": html_roteiro, "linhas_peso": peso_roteiro})

    if articulacao:
        html_art = HTMLTemplates.ARTICULACAO_APROFUNDAMENTO.substitute(articulacao=articulacao)
        peso_articulacao = 4 + (len(art_raw) // 130)
        elementos_dinamicos.append({"html": html_art, "linhas_peso": peso_articulacao})

    if desafios_items:
        html_des = HTMLTemplates.DESAFIOS_DE_EXPANSAO.substitute(desafios_html=html_desafios)
        peso_desafios = 4 + (len(desafios_items) * 3)
        elementos_dinamicos.append({"html": html_des, "linhas_peso": peso_desafios})

    if html_img_fluxograma:
        elementos_dinamicos.append({"html": HTMLTemplates.ESTIMULO_POS_FLUXOGRAMA.substitute(), "linhas_peso": 4})

    if bloco_codigo:
        elementos_dinamicos.append(bloco_codigo)

    # --------------------------------------------------------------------------
    # ALGORITMO DE DISTRIBUIÇÃO EM PÁGINAS A4
    # --------------------------------------------------------------------------
    paginas: List[List[str]] = []
    pagina_atual: List[str] = []
    linhas_acumuladas: int = 0

    for elem in elementos_dinamicos:
        peso = elem["linhas_peso"]

        if pagina_atual and (linhas_acumuladas + peso > LIMITE_LINHAS_PAGINA):
            paginas.append(pagina_atual)
            pagina_atual = [elem["html"]]
            linhas_acumuladas = peso
        else:
            pagina_atual.append(elem["html"])
            linhas_acumuladas += peso

    if pagina_atual:
        paginas.append(pagina_atual)

    # --------------------------------------------------------------------------
    # RENDERIZAÇÃO DAS PÁGINAS DINÂMICAS COM HEADER DE PAGINAÇÃO SUPERIOR
    # --------------------------------------------------------------------------
    html_paginas_dinamicas = ""
    for idx, pag_htmls in enumerate(paginas):
        num_pag_atual = pagina_inicial + 1 + idx
        header_sup_pag = HTMLTemplates.HEADER_PAGINACAO_SUPERIOR.substitute(
            titulo_secao=f"{codigo} • Detalhamento Prático",
            num_pagina=f"{num_pag_atual:02d}"
        )

        html_chunk = "\n".join(pag_htmls)
        header_continuidade = ""

        html_paginas_dinamicas += HTMLTemplates.PAGINA_DINAMICA_A4.substitute(
            header_superior=header_sup_pag,
            header_continuidade=header_continuidade,
            html_chunk=html_chunk
        )

    total_paginas = 1 + len(paginas)
    return p1 + html_paginas_dinamicas, total_paginas


def obter_conteudo_css(base_dir: Path) -> str:
    """Carrega o CSS a partir do arquivo style.css ou utiliza a constante fallback."""
    caminho_css = base_dir / CSS_FILE_NAME
    if caminho_css.exists():
        try:
            with open(caminho_css, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[AVISO] Não foi possível ler '{caminho_css.name}': {e}. Usando fallback.")
    return FALLBACK_CSS


def anexar_header_superior_se_necessario(main_tag: Any, titulo: str, num_pagina: int) -> None:
    """Injeta o cabeçalho de paginação superior no início de uma tag <main> existente."""
    header_html = HTMLTemplates.HEADER_PAGINACAO_SUPERIOR.substitute(
        titulo_secao=titulo,
        num_pagina=f"{num_pagina:02d}"
    )
    header_soup = BeautifulSoup(header_html, "html.parser")
    main_tag.insert(0, header_soup)


def tornar_tabelas_modulos_interativas(mains_modulos: List[Any], projetos_map: Dict[str, str]) -> None:
    """
    1. Remove o título 'Matriz de Projetos do Módulo' situado acima de cada tabela.
    2. Insere no <thead> um cabeçalho único integrado com o identificador do módulo
       (ex: MÓDULO III - ENSINO FUNDAMENTAL II).
    3. Percorre as tabelas dos Módulos I a IV e transforma as células de código e nome
       de cada projeto em links clicáveis com âncoras para #id-do-projeto.
    """
    titulos_modulos_header = [
        "MÓDULO I - EDUCAÇÃO INFANTIL",
        "MÓDULO II - ENSINO FUNDAMENTAL I",
        "MÓDULO III - ENSINO FUNDAMENTAL II",
        "MÓDULO IV - ENSINO MÉDIO",
    ]

    for idx_mod, main in enumerate(mains_modulos):
        # 1. Remove qualquer título 'Matriz de Projetos' situado antes da tabela
        for elem in list(main.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "span"])):
            txt = elem.get_text()
            if txt and "matriz de projetos" in txt.lower():
                elem.decompose()

        identificador = (
            titulos_modulos_header[idx_mod]
            if idx_mod < len(titulos_modulos_header)
            else f"MÓDULO {idx_mod + 1}"
        )

        # Suaviza a margem inferior dos cards de competências para garantir encaixe perfeito em páginas A4 densas
        for card in main.find_all("div", class_="rounded-lg"):
            classes = card.get("class", [])
            if "mb-6" in classes:
                card["class"] = [c if c != "mb-6" else "mb-3.5" for c in classes]

        tabelas = main.find_all("table")
        for tabela in tabelas:
            # 1. Envolve a tabela em um container com bordas arredondadas e overflow-hidden
            parent = tabela.parent
            if parent and "rounded-lg" not in parent.get("class", []):
                wrapper = BeautifulSoup(
                    '<div class="rounded-lg overflow-hidden border border-slate-300 shadow-2xs bg-white mb-0"></div>',
                    "html.parser"
                ).div
                tabela.wrap(wrapper)

            # 2. Cabeçalho único integrado no <thead> com o identificador do módulo
            thead = tabela.find("thead")
            if thead:
                primeiro_tr = thead.find("tr")
                primeiro_th = primeiro_tr.find("th") if primeiro_tr else None
                if not (primeiro_th and primeiro_th.has_attr("colspan") and int(primeiro_th["colspan"]) >= 4):
                    tr_head_html = (
                        f'<tr class="bg-slate-200 text-brand-900 font-heading border-b border-slate-300">'
                        f'<th colspan="4" class="p-2.5 text-center font-heading font-bold text-xs uppercase tracking-wider bg-slate-200 text-brand-900 border-b border-slate-300">'
                        f'{identificador}'
                        f'</th>'
                        f'</tr>'
                    )
                    tr_soup = BeautifulSoup(tr_head_html, "html.parser")
                    thead.insert(0, tr_soup)
                else:
                    primeiro_tr["class"] = ["bg-slate-200", "text-brand-900", "font-heading", "border-b", "border-slate-300"]
                    primeiro_th["class"] = ["p-2.5", "text-center", "font-heading", "font-bold", "text-xs", "uppercase", "tracking-wider", "bg-slate-200", "text-brand-900", "border-b", "border-slate-300"]
                    primeiro_th.string = identificador

                # Subtítulo (Cód, Projeto, etc.) em azul escuro (bg-brand-800 com texto branco) como estava anteriormente
                trs_head = thead.find_all("tr")
                if len(trs_head) >= 2:
                    segundo_tr = trs_head[1]
                    segundo_tr["class"] = ["bg-brand-800", "text-white", "font-heading"]
                    ths = segundo_tr.find_all("th")
                    for i, th in enumerate(ths):
                        th_classes = ["p-2.5", "border", "border-brand-800", "text-white", "font-semibold", "text-[11px]"]
                        if i == 0:
                            th_classes.append("w-20")
                        th["class"] = th_classes

            linhas = tabela.find_all("tr")
            for tr in linhas:
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    cod_texto = tds[0].get_text(strip=True)
                    nome_texto = tds[1].get_text(strip=True)

                    # Verifica se o código corresponde a algum projeto mapeado
                    slug_alvo = None
                    for cod_key, slug_val in projetos_map.items():
                        if cod_key.lower() == cod_texto.lower() or cod_texto.lower() in cod_key.lower():
                            slug_alvo = slug_val
                            break

                    if not slug_alvo:
                        slug_alvo = f"prj-{sanitizar_slug(cod_texto)}"

                    # Transforma a coluna de código em link
                    if not tds[0].find("a"):
                        tds[0].string = ""
                        a_cod = BeautifulSoup(f'<a href="#{slug_alvo}" class="font-mono font-bold text-accent-blue hover:underline">{cod_texto}</a>', "html.parser")
                        tds[0].append(a_cod)

                    # Transforma a coluna de nome em link
                    if not tds[1].find("a"):
                        tds[1].string = ""
                        a_nome = BeautifulSoup(f'<a href="#{slug_alvo}" class="module-project-link">{nome_texto}</a>', "html.parser")
                        tds[1].append(a_nome)


# ==============================================================================
# PROCESSO PRINCIPAL DE ORQUESTRAÇÃO (LIVRO DIDÁTICO)
# ==============================================================================

def executar_automacao(
    arq_origem: str = "Manual.html",
    arq_json: str = "projetos_estruturas.txt",
    arq_destino: str = "Manual.html"
) -> None:
    """
    Executa a automação estruturando a publicação em formato formal de Livro Didático:
    1. Capa / Título do Livro (Pág. 01)
    2. Sumário Formal do Livro (Pág. 02 - antes da introdução)
    3. Introdução e Contexto Histórico (Pág. 03 - Papert & Paulo Freire)
    4. Explicação da Estrutura Didática dos 4 Pilares (Pág. 04)
    5. Módulos I a IV com Tabelas de Projetos Interativas (Págs. 05 a 08)
    6. Lista Sequencial de Projetos Práticos com QR Code GitHub e Fluxo em Setas (Págs. 09+)
    """
    base_dir = Path(__file__).parent.resolve()
    path_origem = base_dir / arq_origem
    path_json = base_dir / arq_json
    path_destino = base_dir / arq_destino

    print("=" * 50)
    print("      INICIANDO PROCESSO DE AUTOMAÇÃO HTML        ")
    print("=" * 50)

    print("\n[INFO] Pré-processando módulos via atualizar_manual.py...")
    try:
        atualizar_manual.atualizar_manual_html(
            caminho_html_origem=arq_origem,
            caminho_json="dados_manual.txt",
            caminho_html_destino=arq_destino
        )
    except Exception as e:
        print(f"[ERRO] Falha ao pré-processar atualizar_manual_html: {e}")

    path_processado = Path(arq_destino)

    projetos = carregar_projetos(path_json)
    if not projetos:
        print("[CANCELADO] Nenhum dado válido encontrado.")
        return

    if not path_processado.exists():
        print(f"[ERRO] Arquivo HTML de trabalho não foi encontrado: {path_processado.name}")
        return

    with open(path_processado, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Injeção de CSS desacoplado na tag <head>
    conteudo_css = obter_conteudo_css(base_dir)
    tag_existente = soup.head.find("style", id="print-fix") if soup.head else None
    if tag_existente:
        tag_existente.string = conteudo_css
    elif soup.head:
        estilo = soup.new_tag("style", id="print-fix")
        estilo.string = conteudo_css
        soup.head.append(estilo)

    mains = soup.find_all("main")
    if len(mains) < 6:
        print("[ERRO] O arquivo base não possui as 6 páginas estruturais necessárias.")
        return

    # 1. Capa (Página 01 - sem paginação superior)
    capa_preservada = mains[0]
    capa_preservada["id"] = "secao-capa"

    # Garante que a imagem da capa continue centralizada e com tamanho harmônico
    img_capa = capa_preservada.find("img", src=lambda s: s and "Capa" in s)
    if img_capa:
        img_capa["class"] = ["cover", "object-contain", "mx-auto", "max-h-[120mm]", "bg-transparent"]
        parent = img_capa.parent
        if parent and "bg-slate-100" in parent.get("class", []):
            parent["class"] = [c for c in parent.get("class", []) if c != "bg-slate-100"]

    # 2. Pré-cálculo dos projetos para a paginação do Sumário
    PAGINA_INICIAL_PROJETOS = 10
    pagina_corrente = PAGINA_INICIAL_PROJETOS

    projetos_info: List[Dict[str, Any]] = []
    novos_htmls: List[str] = []
    projetos_slug_map: Dict[str, str] = {}

    for prj in projetos:
        cod = str(prj.get("PROJETO", "PRJ X.X"))
        tit = str(prj.get("TITULO", "Sem título"))
        comp = str(prj.get("COMPLEXIDADE", "Básico"))
        modulo_nome = str(prj.get("MODULO", "Módulo Não Especificado"))

        slug_base = sanitizar_slug(cod)
        if slug_base.startswith("prj-"):
            slug = slug_base
        else:
            slug = f"prj-{slug_base}"

        projetos_slug_map[cod] = slug

        html_prj, total_pags = gerar_html_projeto(
            prj,
            slug_id=slug,
            pagina_inicial=pagina_corrente,
            base_dir=base_dir
        )
        novos_htmls.append(html_prj)

        projetos_info.append({
            "codigo": cod,
            "titulo": tit,
            "complexidade": comp,
            "modulo": modulo_nome,
            "pagina_inicio": pagina_corrente,
            "slug": slug,
        })
        pagina_corrente += total_pags

    # 3. Sumário Formal do Livro (Página 02 - imediatamente após a Capa)
    html_sumario = gerar_html_sumario_formal(projetos_info, num_pagina=2)

    # 4. Introdução e Contexto Histórico (Página 03)
    html_introducao = gerar_html_introducao(num_pagina=3)

    # 5. Explicação da Estrutura Didática dos Projetos (Página 04)
    html_didatica = gerar_html_didatica_4_pilares(num_pagina=4)

    # 6. Fluxograma Geral Integrado dos Projetos (Página 05)
    html_fluxograma = gerar_html_fluxograma_geral(num_pagina=5, img_nome="Projetos.png")

    # 7. Módulos Curriculares I a IV (Páginas 06 a 09) com Tabelas Interativas
    modulos_preservados = mains[2:6]
    titulos_modulos = [
        "Diretrizes Curriculares • Módulo I (Educação Infantil)",
        "Diretrizes Curriculares • Módulo II (Ensino Fundamental I)",
        "Diretrizes Curriculares • Módulo III (Ensino Fundamental II)",
        "Diretrizes Curriculares • Módulo IV (Ensino Médio)",
    ]

    for idx_mod, m_mod in enumerate(modulos_preservados):
        pag_mod = 6 + idx_mod
        m_mod["id"] = f"modulo-{idx_mod + 1}"
        anexar_header_superior_se_necessario(
            m_mod,
            titulo=titulos_modulos[idx_mod],
            num_pagina=pag_mod
        )

    # Torna os títulos de projetos nas matrizes dos módulos clicáveis para #prj-X-X
    tornar_tabelas_modulos_interativas(modulos_preservados, projetos_slug_map)

    # Botão Flutuante de PDF
    html_botao_pdf = HTMLTemplates.BOTAO_IMPRESSAO_PDF.substitute()

    # Reconstrução na sequência estrita de LIVRO DIDÁTICO:
    # 1. Capa (Pág. 01)
    # 2. Sumário Formal (Pág. 02)
    # 3. Introdução (Pág. 03)
    # 4. Estrutura Didática dos Projetos (Pág. 04)
    # 5. Fluxograma Geral Integrado com Progressão Multinível (Pág. 05)
    # 6. Módulos I a IV com tabelas interativas (Páginas 06 a 09)
    # 7. Projetos Práticos Sequenciais (Páginas 10+)
    elementos_ordenados = [
        html_botao_pdf,
        str(capa_preservada),
        html_sumario,
        html_introducao,
        html_didatica,
        html_fluxograma,
        "\n".join(str(m) for m in modulos_preservados),
        "\n".join(novos_htmls)
    ]

    conteudo_reconstruido = "\n".join(elementos_ordenados)

    if soup.body:
        soup.body.clear()
        novos_elementos = BeautifulSoup(conteudo_reconstruido, "html.parser")
        soup.body.append(novos_elementos)
    else:
        print("[ERRO] Tag <body> não encontrada no HTML base.")
        return

    with open(path_destino, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

    print(f"[SUCESSO] Processo concluído com sucesso no formato de Livro Didático!")
    print(f" -> 1. Capa / Título: OK (Página 01)")
    print(f" -> 2. Sumário Formal do Livro: OK (Página 02)")
    print(f" -> 3. Introdução Oficial (Papert & Freire): OK (Página 03)")
    print(f" -> 4. Estrutura Didática dos Projetos: OK (Página 04)")
    print(f" -> 5. Fluxograma Geral Integrado (Projetos.png): OK (Página 05)")
    print(f" -> 6. Módulos I a IV com Tabelas Interativas: OK (Páginas 06 a 09)")
    print(f" -> 7. Lista Sequencial de Projetos: OK (Início na Página {PAGINA_INICIAL_PROJETOS:02d})")
    print(f" -> Bloco GitHub e Fluxo com Setas gerados em cada projeto.")
    print(f" -> Arquivo consolidado gerado: '{path_destino.name}'")


if __name__ == "__main__":
    executar_automacao(
        arq_origem="Manual.html",
        arq_json="projetos_estruturas.txt",
        arq_destino="Manual.html"
    )
