import os
import pandas as pd
# importando utils
from utils import make_scatter, make_clusters

# streamlit
import streamlit as st

prepare_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(prepare_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, "data")

# o arquivo data_partidos.parquet vai ser utilizado
@st.cache_data(ttl=60*60*24)
def create_df():
    filename = os.path.join(data_path, "data_partidos.parquet")
    return pd.read_parquet(filename)

df = create_df()

welcome = """ 
# TSE Analytics - Eleições 2024

Análise de dados dos partidos que disputaram a eleição de 2024.

"""

st.markdown(welcome)

# estados
uf_options = df['SG_UF'].unique().tolist()
uf_options.remove("BR")
uf_options = ["BR"] + uf_options

# cargos
cargos_options = df['DS_CARGO'].unique().tolist()
cargos_options.sort()
cargos_options.remove("GERAL")
cargos_options = ["GERAL"]  + cargos_options

# GRID
col1, col2 = st.columns(2)

with col1:
    selected_estado = st.selectbox(label="Estado", placeholder="Selecione o estado para filtro", options=uf_options)

with col2:
    selected_cargo = st.selectbox(label="Cargo", placeholder="Selecione um cargo", options=cargos_options)


size = st.checkbox("Tamanho das bolhas?")
cluster = st.checkbox("Definir cluster?")

if (cluster):
    n_clusters = st.number_input("Quantidade de clusters", value=6, format="%d", max_value=10, min_value=1)

data = df[(df['SG_UF'] == selected_estado) & (df['DS_CARGO'] == selected_cargo)]


totalCandidaturas = data['totalCandidatos'].sum()
st.markdown(f"Total de candidaturas: {totalCandidaturas}")

# análise 
if (cluster):
    data = make_clusters(data=data, n=n_clusters)

x = "txGenFeminino"
y = "txCorRacaPreta"

fig = make_scatter(data=data, x=x, y=y, size=size, cluster=cluster)

st.pyplot(fig)