import PyPDF2
import re
import streamlit as st

def extrair_e_salvar_arquivos_pdf(pdf_bytes):
    """Extrai os nomes dos arquivos de um PDF e gera o conteúdo para salvar no TXT."""
    contador = 0
    resultados = []
    pdf_reader = PyPDF2.PdfReader(pdf_bytes)
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        texto_pagina = page.extract_text()

        padrao = r"Arquivo:\s+(\S+?)\."
        correspondencias = re.findall(padrao, texto_pagina)

        for nome in correspondencias:
            resultados.append(f"*{nome}*")
            contador += 1

    return resultados, contador


def extrair_e_salvar_arquivos_pdf_pagina(pdf_bytes):
    """Extrai os nomes dos arquivos de um PDF, organizados por página, e gera o conteúdo para salvar no TXT."""
    resultados_por_pagina = []
    pdf_reader = PyPDF2.PdfReader(pdf_bytes)
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        texto_pagina = page.extract_text()

        padrao = r"Arquivo:\s+(\S+?)\."
        correspondencias = re.findall(padrao, texto_pagina)
        nomes_formatados = ";".join(f"*{nome}*" for nome in correspondencias)

        resultados_por_pagina.append(f"Página {page_num + 1}: {nomes_formatados}")

    return resultados_por_pagina


# Streamlit App
st.title("Processador de Arquivos PDF")
st.write("Faça upload de um arquivo PDF para extrair informações e gerar arquivos TXT.")

# Upload do PDF
uploaded_pdf = st.file_uploader("Envie seu arquivo PDF", type=["pdf"])

if uploaded_pdf is not None:
    # Botão para processar
    if st.button("Iniciar processamento"):
        # Processar o PDF
        resultados, contador = extrair_e_salvar_arquivos_pdf(uploaded_pdf)
        resultados_por_pagina = extrair_e_salvar_arquivos_pdf_pagina(uploaded_pdf)

        # Criar os arquivos TXT em memória
        txt_todos = "\n".join(resultados)
        txt_por_pagina = "\n".join(resultados_por_pagina)

        # Exibir mensagem de sucesso
        st.success(f"Processamento concluído! Foram encontrados {contador} arquivos.")

        # Botões de download
        st.download_button(
            label="Baixar resultados (todos juntos)",
            data=txt_todos,
            file_name="resultados.txt",
            mime="text/plain",
        )
        st.download_button(
            label="Baixar resultados (por página)",
            data=txt_por_pagina,
            file_name="resultados_por_pagina.txt",
            mime="text/plain",
        )
