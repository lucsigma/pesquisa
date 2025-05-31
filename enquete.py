
import streamlit as st
import sqlite3
import pandas as pd
import io

# Conexão com o banco SQLite
conn = sqlite3.connect('enquete.db')
cursor = conn.cursor()

# Criar tabela, se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    resposta TEXT NOT NULL
)
''')
conn.commit()

st.title("🔮 Enquete ")
st.write("*Pergunta:* Se você fosse Deus, o que você eternizaria?")

# Formulário para envio de resposta
with st.form("formulario_enquete"):
    nome = st.text_input("Seu nome:")
    resposta = st.text_area("Sua resposta:")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        if nome.strip() == "" or resposta.strip() == "":
            st.warning("Por favor, preencha o nome e a resposta.")
        else:
            cursor.execute("INSERT INTO respostas (nome, resposta) VALUES (?, ?)", (nome.strip(), resposta.strip()))
            conn.commit()
            st.success("Resposta registrada com sucesso!")

# Consultar os dados
cursor.execute("SELECT nome, resposta FROM respostas")
dados = cursor.fetchall()

# Exibir os dados organizadamente
st.subheader("📋 Respostas dos Participantes")
if dados:
    df = pd.DataFrame(dados, columns=["Nome", "Resposta"])
    st.table(df)

    # Gerar conteúdo do TXT
    conteudo_txt = ""
    for nome, resposta in dados:
        conteudo_txt += f"Nome: {nome}\nResposta: {resposta}\n{'-'*40}\n"

    # Senha para download
    st.markdown("---")
    st.subheader("🔐 Área de Download Protegida por Senha")

    senha = st.text_input("Digite a senha para baixar o arquivo:", type="password")
    if senha:
        if senha == "deus123":
            buffer = io.StringIO(conteudo_txt)
            st.download_button(
                label="📄 Baixar respostas em TXT",
                data=buffer.getvalue(),
                file_name="respostas_enquete.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ Senha incorreta.")

    # Área de exclusão protegida
    st.markdown("---")
    st.subheader("🔴 Área de Exclusão")

    senha_exclusao = st.text_input("Digite a senha para excluir todas as respostas:", type="password", key="exclusao")
    if senha_exclusao:
        if senha_exclusao == "deus123":
            if st.button("🗑 Excluir todas as respostas"):
                cursor.execute("DELETE FROM respostas")
                conn.commit()
                st.success("Todas as respostas foram excluídas!")
        else:
            st.error("❌ Senha de exclusão incorreta.")
else:
    st.info("Nenhuma resposta registrada ainda.")

# Fechar conexão
conn.close()