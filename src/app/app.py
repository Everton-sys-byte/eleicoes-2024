import pandas as pd
import sqlalchemy

# importando utils
from utils import make_scatter, make_clusters

# streamlit
import streamlit as st

engine = sqlalchemy.create_engine("sqlite:///../../data/database.db")

with open("./etl_partidos.sql", 'r') as open_file:
    query = open_file.read()

data = pd.read_sql(query, engine)

data.head()

welcome = """ 
# TSE Analytics - Eleições 2024

Análise de dados dos partidos que disputaram a eleição de 2024.

"""

st.markdown(welcome)

# estados
uf_options = data['SG_UF'].unique().tolist()
uf_options.remove("BR")
uf_options = ["BR"] + uf_options

# cargos
cargos_options = data['DS_CARGO'].unique().tolist()
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

data = data[(data['SG_UF'] == selected_estado) & (data['DS_CARGO'] == selected_cargo)]


totalCandidaturas = data['totalCandidatos'].sum()
st.markdown(f"Total de candidaturas: {totalCandidaturas}")

# análise 
if (cluster):
    data = make_clusters(data=data, n=n_clusters)

fig = make_scatter(data=data, size=size, cluster=cluster)

st.pyplot(fig)