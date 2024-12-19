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



st.title("Processador de PDF Listagem de Documentos GedAcervo")
st.write("Faça upload de um arquivo PDF de algum serviço para extrair informações dos nomes dos 'arquivos.pdf' e em seguida, sera gerado um arquivo txt para copiar e colar no aplicativo 'WinSCP'.")
st.write('1º Passo: Entrar na pasta devida do serviço dentro da AWS onde sera ira pegar os PDFs')
st.write('2º Passo: Utilizar ctrl + alt + f')
st.write('3º Passo: Ira abrir uma janela então você clica em EDITAR')
st.write('4º Passo: Copie tudo do arquivo txt gerado e cole dentro de: *Incluir Arquivos* e em seguida OK e depois mais uma vez clicar em OK. ')
st.write('5º Conferir se o número de arquivos filtrados batem com o numero de registros encontrados no PDF')
st.write('6º Dar um ctrl+a e arrastar pro lado esquerdo do WinSCP para baixar todos os documentos filtrados do PDF.')

uploaded_pdf = st.file_uploader("Envie seu arquivo PDF", type=["pdf"])

if uploaded_pdf is not None:
    if st.button("Iniciar processamento"):
        resultados, contador = extrair_e_salvar_arquivos_pdf(uploaded_pdf)
        resultados_por_pagina = extrair_e_salvar_arquivos_pdf_pagina(uploaded_pdf)
        
        txt_todos = "\n".join(resultados)
        txt_por_pagina = "\n".join(resultados_por_pagina)

        st.success(f"Processamento concluído! Foram encontrados {contador} arquivos.")

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
