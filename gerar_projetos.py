"""
Ponto de entrada retrocompatível para a automação de geração de livros e manuais didáticos.

Este arquivo mantém compatibilidade total com invocações existentes de `gerar_projetos.py`,
delegando as operações para o módulo estruturado `gerar_projetos_refatorado.py`.
"""

from gerar_projetos_refatorado import (
    CSS_FILE_NAME,
    FALLBACK_CSS,
    HTMLTemplates,
    LIMITE_LINHAS_PAGINA,
    MAX_LINHAS_BLOCO_CODIGO,
    TEXTO_INTRODUCAO_OFICIAL,
    anexar_header_superior_se_necessario,
    carregar_projetos,
    dividir_codigo_por_comentarios,
    executar_automacao,
    gerar_bloco_github,
    gerar_html_didatica_4_pilares,
    gerar_html_introducao,
    gerar_html_projeto,
    gerar_html_sumario_formal,
    gerar_qr_code_asset,
    gerar_qr_code_html,
    obter_conteudo_css,
    renderizar_blocos_codigo,
    renderizar_desafios,
    renderizar_fluxo_setas,
    renderizar_lista,
    sanitizar_slug,
    tornar_tabelas_modulos_interativas,
)

if __name__ == "__main__":
    executar_automacao(
        arq_origem="Manual.html",
        arq_json="projetos_estruturas.txt",
        arq_destino="Manual.html",
    )