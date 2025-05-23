import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Cadastro de Funcionários", layout="centered")
st.title("📋 Cadastro de Funcionários - Bairro e Ônibus")

# Caminho do arquivo para salvar os dados
ARQUIVO_DADOS = "funcionarios.csv"

# Função para carregar dados do CSV (se existir)
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        return pd.read_csv(ARQUIVO_DADOS)
    else:
        return pd.DataFrame(columns=["Nome", "Matrícula", "Bairro", "Ônibus"])

# Função para salvar dados no CSV
def salvar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

# Inicializa os dados
if "funcionarios" not in st.session_state:
    st.session_state.funcionarios = carregar_dados()

# Formulário de cadastro
with st.form("form_cadastro"):
    nome = st.text_input("Nome do Funcionário")
    matricula = st.text_input("Matrícula")
    bairro = st.text_input("Bairro")
    onibus = st.text_input("Ônibus")

    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if nome and matricula and bairro and onibus:
            novo_dado = {
                "Nome": nome,
                "Matrícula": matricula,
                "Bairro": bairro,
                "Ônibus": onibus
            }
            st.session_state.funcionarios = pd.concat(
                [st.session_state.funcionarios, pd.DataFrame([novo_dado])],
                ignore_index=True
            )
            salvar_dados(st.session_state.funcionarios)
            st.success("Funcionário cadastrado com sucesso!")
        else:
            st.warning("⚠️ Preencha todos os campos antes de cadastrar.")

# Filtros
st.subheader("🔍 Filtros")

col1, col2 = st.columns(2)
with col1:
    bairro_filtro = st.selectbox(
        "Filtrar por Bairro", 
        options=["Todos"] + sorted(st.session_state.funcionarios["Bairro"].dropna().unique().tolist())
    )
with col2:
    onibus_filtro = st.selectbox(
        "Filtrar por Ônibus", 
        options=["Todos"] + sorted(st.session_state.funcionarios["Ônibus"].dropna().unique().tolist())
    )

# Aplicar filtros
df_filtrado = st.session_state.funcionarios.copy()

if bairro_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Bairro"] == bairro_filtro]

if onibus_filtro != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Ônibus"] == onibus_filtro]

# Exibe a tabela filtrada
st.subheader("📄 Funcionários Cadastrados")
st.dataframe(df_filtrado, use_container_width=True)

# Botão de download
st.download_button(
    "⬇️ Baixar dados em CSV",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="funcionarios_filtrados.csv",
    mime="text/csv"
)

# Estatísticas
st.subheader("📊 Estatísticas")

col3, col4 = st.columns(2)
with col3:
    st.write("**Funcionários por Bairro**")
    st.dataframe(st.session_state.funcionarios["Bairro"].value_counts().rename_axis("Bairro").reset_index(name="Quantidade"))

with col4:
    st.write("**Funcionários por Ônibus**")
    st.dataframe(st.session_state.funcionarios["Ônibus"].value_counts().rename_axis("Ônibus").reset_index(name="Quantidade"))
