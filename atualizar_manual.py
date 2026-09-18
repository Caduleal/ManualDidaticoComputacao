import json
import html
from pathlib import Path
from bs4 import BeautifulSoup

def carregar_dados_json(caminho_json):
    """
    Lê e desserializa o arquivo JSON/TXT de dados.
    """
    with open(caminho_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def gerar_html_modulo(modulo):
    """
    Gera a tag <main> HTML correspondente a um módulo de ensino.
    """
    competencias_html = "".join([f"<li>{html.escape(c)}</li>" for c in modulo['competencias']])
    
    linhas_tabela = ""
    for idx, prj in enumerate(modulo['projetos_matriz']):
        bg_class = "bg-white" if idx % 2 == 0 else "bg-brand-50"
        
        nivel_badge = {
    "Básico": '<span class="bg-green-100 text-green-800 px-2 py-0.5 rounded text-[9px] font-bold uppercase">Básico</span>',
    "Intermediário": '<span class="bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded text-[9px] font-bold uppercase">Intermediário</span>',
    "Avançado": '<span class="bg-red-100 text-red-800 px-2 py-0.5 rounded text-[9px] font-bold uppercase">Avançado</span>'
    }.get(prj['nivel'], f'<span>{prj["nivel"]}</span>')

        linhas_tabela += f"""
        <tr class="{bg_class} border-b border-brand-100">
            <td class="p-2.5 font-mono text-brand-500 border border-brand-100">{html.escape(prj['codigo'])}</td>
            <td class="p-2.5 font-medium text-brand-900 border border-brand-100">{html.escape(prj['nome'])}</td>
            <td class="p-2.5 text-brand-800 border border-brand-100 text-[11px]">{html.escape(prj['conceitos'])}</td>
            <td class="p-2.5 border border-brand-100 text-center">{nivel_badge}</td>
        </tr>
        """

    return f"""
    <main class="a4-page page-break">
        <div>
            <section class="mb-8">
                <h2 class="font-heading font-bold text-2xl text-brand-900 mb-6 flex items-center gap-2 border-b border-brand-100 pb-2">
                    Módulo {html.escape(modulo['id'])}
                </h2>

                <div class="bg-brand-50 border border-brand-100 p-5 rounded-lg mb-6 avoid-break relative overflow-hidden">
                    <div class="absolute top-0 right-0 bg-green-500 text-white px-3 py-0.5 font-mono text-[10px] font-bold rounded-bl-lg">
                        {html.escape(modulo['etapa'])}
                    </div>

                    <h3 class="font-heading font-bold text-lg text-brand-900 mb-2">{html.escape(modulo['titulo'])}</h3>
                    <div>
                        <h4 class="font-heading font-semibold text-xs text-brand-800 uppercase tracking-wide mb-2">
                            Competências Globais e Objetivos:
                        </h4>
                        <ul class="list-disc pl-5 text-xs text-brand-800 space-y-1">
                            {competencias_html}
                        </ul>
                    </div>
                </div>

                <div class="avoid-break">
                    <h3 class="font-heading font-semibold text-base text-brand-800 mb-3">Matriz de Projetos do Módulo</h3>
                    <table class="w-full text-left text-xs border-collapse">
                        <thead>
                            <tr class="bg-brand-800 text-white font-heading">
                                <th class="p-2.5 border border-brand-800 w-20">Cód</th>
                                <th class="p-2.5 border border-brand-800">Projeto</th>
                                <th class="p-2.5 border border-brand-800">Conceitos Abordados</th>
                                <th class="p-2.5 border border-brand-800 text-center">Nível</th>
                            </tr>
                        </thead>
                        <tbody>
                            {linhas_tabela}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    </main>
    """

def gerar_html_projeto_detalhado(prj):
    """
    Gera o par de páginas <main> para detalhamento técnico de cada projeto.
    """
    bom_linhas = "".join([
        f'<tr><td class="p-1.5 border border-student/20 text-center font-mono">{html.escape(item["qtd"])}</td>'
        f'<td class="p-1.5 border border-student/20">{html.escape(item["componente"])}</td></tr>'
        for item in prj['bom']
    ])

    pinos_linhas = "".join([f'<li>{html.escape(pino)}</li>' for pino in prj['pinos']])
    roteiro_linhas = "".join([f'<li>{html.escape(step)}</li>' for step in prj['roteiro_pratico']])

    trouble_linhas = "".join([
        f'<tr><td class="p-1.5 border-b border-trouble/10 font-medium text-trouble-dark">{html.escape(t["sintoma"])}</td>'
        f'<td class="p-1.5 border-b border-trouble/10">{html.escape(t["diagnostico"])}</td></tr>'
        for t in prj['troubleshooting']
    ])

    pagina1 = f"""
    <main class="a4-page page-break">
        <div>
            <header class="text-center mb-6 avoid-break border-b-2 border-brand-800 pb-4">
                <h2 class="font-heading font-extrabold text-3xl text-brand-900 mb-1">{html.escape(prj['codigo'])} - {html.escape(prj['titulo'])}</h2>
                <p class="text-brand-500 font-medium text-xs">{html.escape(prj['subtitulo'])}</p>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 avoid-break">
                <div class="bg-teacher-light border border-teacher/20 border-l-4 border-l-teacher p-4 rounded">
                    <h3 class="font-heading font-bold text-teacher-dark flex items-center gap-2 mb-2 text-xs uppercase tracking-wider">
                        <span class="material-symbols-outlined text-[16px]">co_present</span> Dados do Projeto
                    </h3>
                    <ul class="text-xs space-y-1.5 text-teacher-dark/90">
                        <li><strong class="text-teacher-dark">Etapa de Ensino:</strong> {html.escape(prj['metadados']['etapa'])}</li>
                        <li><strong class="text-teacher-dark">Complexidade:</strong> {html.escape(prj['metadados']['complexidade'])}</li>
                        <li><strong class="text-teacher-dark">Tempo Estimado:</strong> {html.escape(prj['metadados']['tempo_estimado'])}</li>
                        <li><strong class="text-teacher-dark">Conceitos Foco:</strong> {html.escape(prj['metadados']['conceitos_foco'])}</li>
                    </ul>
                </div>

                <div class="bg-bncc-light border border-bncc/30 border-t-4 border-t-bncc p-4 rounded shadow-sm relative">
                    <div class="absolute -top-3 right-4 bg-bncc text-white px-2 py-0.5 rounded text-[9px] font-bold shadow">NORMATIVA</div>
                    <h3 class="font-heading font-bold text-bncc-dark flex items-center gap-2 mb-2 text-xs uppercase tracking-wider mt-0.5">
                        <span class="material-symbols-outlined text-[16px]">verified</span> Mapeamento Curricular
                    </h3>
                    <div class="space-y-2 text-xs">
                        <div>
                            <strong class="text-[11px] text-bncc-dark block mb-0.5">Competências Interdisciplinares</strong>
                            <div class="flex items-start gap-1.5">
                                <span class="font-mono text-[9px] bg-white border border-bncc/20 px-1 py-0.5 rounded text-bncc-dark font-bold">{html.escape(prj['bncc']['materia'])}</span>
                                <span class="text-[11px] text-bncc-dark/80 leading-tight">{html.escape(prj['bncc']['descricao'])}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <section class="mb-6 avoid-break">
                <h3 class="font-heading font-bold text-brand-900 text-sm mb-2 flex items-center gap-2 border-b border-brand-100 pb-1">
                    Contextualização e Modelagem
                </h3>
                <div class="pl-3 border-l-2 border-brand-500 text-brand-800 text-xs space-y-2 text-justify">
                    <p><strong>Problematização:</strong> {html.escape(prj['contextualizacao'])}</p>
                </div>
            </section>

            <section class="bg-student-light border border-student/20 rounded-lg overflow-hidden mb-6 avoid-break">
                <div class="bg-student text-white px-4 py-2 flex items-center gap-2">
                    <span class="material-symbols-outlined text-[18px]">engineering</span>
                    <h3 class="font-heading font-bold text-xs uppercase tracking-wide">Arquitetura de Hardware e BOM</h3>
                </div>

                <div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <h4 class="font-heading font-bold text-student-dark text-xs mb-2">Lista de Materiais</h4>
                        <table class="w-full text-[11px] text-left border-collapse border border-student/20 bg-white">
                            <thead class="bg-student/5 text-student-dark">
                                <tr>
                                    <th class="p-1.5 border border-student/20 text-center">Qtd</th>
                                    <th class="p-1.5 border border-student/20">Componente</th>
                                </tr>
                            </thead>
                            <tbody class="text-brand-800">
                                {bom_linhas}
                            </tbody>
                        </table>
                    </div>

                    <div class="space-y-2">
                        <div class="bg-white p-2.5 border border-student/20 rounded shadow-sm">
                            <h4 class="font-heading font-bold text-student-dark text-[11px] mb-1">Mapeamento de Pinos</h4>
                            <ul class="font-mono text-[10px] text-brand-800 space-y-0.5">
                                {pinos_linhas}
                            </ul>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </main>
    """

    pagina2 = f"""
    <main class="a4-page page-break">
        <div>
            <section class="mb-6 avoid-break">
                <h3 class="font-heading font-bold text-brand-900 text-sm mb-2 flex items-center gap-2 border-b border-brand-100 pb-1">
                    Modelagem Lógico-Algorítmica
                </h3>

                <div class="border border-brand-800 rounded-lg overflow-hidden shadow-sm">
                    <div class="bg-brand-800 px-4 py-1.5 flex items-center justify-between">
                        <span class="text-brand-100 font-mono text-[11px] font-semibold">{html.escape(prj['codigo_fonte']['arquivo'])}</span>
                    </div>
                    <div class="bg-brand-50 p-3 overflow-x-auto code-block">
                        <pre class="m-0"><code class="text-brand-900 text-[11px]">{html.escape(prj['codigo_fonte']['codigo'])}</code></pre>
                    </div>
                </div>
            </section>

            <section class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6 avoid-break">
                <div class="bg-student-light border border-student/20 p-4 rounded-lg">
                    <h3 class="font-heading font-bold text-student-dark text-xs uppercase mb-2 border-b border-student/20 pb-1">
                        Roteiro Prático de Execução
                    </h3>
                    <ol class="list-decimal pl-4 space-y-1 text-[11px] text-brand-800">
                        {roteiro_linhas}
                    </ol>
                </div>

                <div class="bg-trouble-light border border-trouble/30 p-4 rounded-lg shadow-sm">
                    <h3 class="font-heading font-bold text-trouble-dark text-xs uppercase mb-2 flex items-center gap-1 border-b border-trouble/20 pb-1">
                        <span class="material-symbols-outlined text-[16px]">build_circle</span> Troubleshooting
                    </h3>
                    <table class="w-full text-left text-[10px] border-collapse bg-white rounded overflow-hidden">
                        <tbody class="text-brand-800">
                            {trouble_linhas}
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    </main>
    """

    return pagina1 + pagina2

def atualizar_manual_html(caminho_html_origem, caminho_json, caminho_html_destino):
    """
    Lê o HTML base, substitui o conteúdo dinâmico do JSON e salva o arquivo final.
    """
    diretorio_base = Path(__file__).parent.resolve()

    caminho_origem = diretorio_base / caminho_html_origem
    caminho_json_file = diretorio_base / caminho_json
    caminho_destino = diretorio_base / caminho_html_destino

    # Carrega dados do arquivo JSON/TXT
    dados = carregar_dados_json(caminho_json_file)

    # Lê o HTML base
    with open(caminho_origem, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    mains = soup.find_all('main')
    
    # Mantém as duas primeiras páginas de capa/apresentação (Capa principal e Capa Interna)
    capas_html = str(mains[0]) + "\n" + str(mains[1]) if len(mains) >= 2 else ""

    # Gera HTML dinâmico dos módulos
    modulos_html = "\n".join([gerar_html_modulo(m) for m in dados['modulos']])

    # Gera HTML dinâmico dos projetos detalhados
    projetos_html = "\n".join([gerar_html_projeto_detalhado(p) for p in dados.get('projetos_detalhados', [])])

    novos_mains = capas_html + "\n" + modulos_html + "\n" + projetos_html

    # Remove os mains antigos
    for m in soup.find_all('main'):
        m.decompose()

    # Injeta os novos elementos no HTML de forma segura
    novos_elementos = BeautifulSoup(novos_mains, 'html.parser')

    if soup.body:
        soup.body.append(novos_elementos)
    else:
        soup.append(novos_elementos)

    # Salva o arquivo final formatado
    with open(caminho_destino, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print(f"[+] Arquivo HTML atualizado com sucesso em: {caminho_destino}")

if __name__ == "__main__":
    atualizar_manual_html(
        caminho_html_origem="Manual.html",
        caminho_json="dados_manual.txt",
        caminho_html_destino="Manual.html"
    )