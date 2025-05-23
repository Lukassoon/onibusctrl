import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Cadastro de Funcionários", layout="centered")
st.title("📋 Cadastro de Funcionários - Bairro e Ônibus")

# Caminho do arquivo
ARQUIVO_DADOS = "funcionarios.csv"
COLUNAS_PADRAO = ["Nome", "Matrícula", "Bairro", "Ônibus"]

# Carrega ou inicializa os dados
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        try:
            df = pd.read_csv(ARQUIVO_DADOS)
            for col in COLUNAS_PADRAO:
                if col not in df.columns:
                    df[col] = ""
            return df[COLUNAS_PADRAO]
        except Exception:
            st.warning("⚠️ Erro ao carregar o arquivo. Um novo será iniciado.")
    return pd.DataFrame(columns=COLUNAS_PADRAO)

# Salva dados no CSV
def salvar_dados(df):
    df.to_csv(ARQUIVO_DADOS, index=False)

# Inicializa dados
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
                "Nome": nome.strip().title(),
                "Matrícula": matricula.strip(),
                "Bairro": bairro.strip().upper(),
                "Ônibus": onibus.strip().upper()
            }
            st.session_state.funcionarios = pd.concat(
                [st.session_state.funcionarios, pd.DataFrame([novo_dado])],
                ignore_index=True
            )
            salvar_dados(st.session_state.funcionarios)
            st.success("Funcionário cadastrado com sucesso!")
        else:
            st.warning("⚠️ Preencha todos os campos antes de cadastrar.")

# Recarrega dados após cadastro
st.session_state.funcionarios = carregar_dados()

# Filtros
st.subheader("🔍 Filtros")
col1, col2 = st.columns(2)

with col1:
    bairros_unicos = (
        st.session_state.funcionarios["Bairro"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .unique()
        .tolist()
    )
    bairro_filtro = st.selectbox("Filtrar por Bairro", options=["Todos"] + sorted(bairros_unicos))

with col2:
    onibus_unicos = (
        st.session_state.funcionarios["Ônibus"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
        .unique()
        .tolist()
    )
    onibus_filtro = st.selectbox("Filtrar por Ônibus", options=["Todos"] + sorted(onibus_unicos))

# Aplica filtros
df_filtrado = st.session_state.funcionarios.copy()

if bairro_filtro != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Bairro"].astype(str).str.strip().str.upper() == bairro_filtro
    ]

if onibus_filtro != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["Ônibus"].astype(str).str.strip().str.upper() == onibus_filtro
    ]

# Exibe funcionários
st.subheader("📄 Funcionários Cadastrados")

# Garante que matrícula e ônibus sejam exibidos como texto puro
df_mostrar = df_filtrado.copy()
df_mostrar["Matrícula"] = df_mostrar["Matrícula"].astype(str)
df_mostrar["Ônibus"] = df_mostrar["Ônibus"].astype(str)

st.dataframe(df_mostrar, use_container_width=True)


# Download CSV
st.download_button(
    "⬇️ Baixar dados filtrados (CSV)",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="funcionarios_filtrados.csv",
    mime="text/csv"
)

# Estatísticas
# Estatísticas
st.subheader("📊 Estatísticas")

col3, col4 = st.columns(2)

with col3:
    st.write("**Funcionários por Bairro**")
    df_bairro = (
        st.session_state.funcionarios["Bairro"]
        .astype(str)
        .str.strip()
        .str.upper()
        .value_counts()
        .rename_axis("Bairro")
        .reset_index(name="Quantidade")
    )
    st.dataframe(df_bairro)

with col4:
    st.write("**Funcionários por Ônibus**")
    df_onibus = (
        st.session_state.funcionarios["Ônibus"]
        .astype(str)
        .str.strip()
        .str.upper()
        .value_counts()
        .rename_axis("Ônibus")
        .reset_index(name="Quantidade")
    )
    st.dataframe(df_onibus)
