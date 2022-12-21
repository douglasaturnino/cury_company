#Libraries
import os
import pandas as pd
import streamlit as st
from util import util as ut
from graficos.graficos_entregadores import GraficosEntregadores

# ======================================
# Inicio da EStrutura logica do Código
# ======================================

st.set_page_config(
    page_title="Visão Entregadores",
    page_icon="🚚",
    layout='wide'
)

home_path = os.getcwd()
df = pd.read_csv(os.path.join(home_path, 'datasets', 'train.csv'))

df1 = df.copy()
# Limpando os dados
df1 = ut.clean_code(df1)

date_slider, traffic_options = ut.sidebar()

# Filtros de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ====================================
# Layout no Streamlit
# ====================================
entregadores = GraficosEntregadores(df1)

st.header('Marketplace - Visão Entregadores')

with st.container():
    st.title('Overroll Metrics')
    
    col1, col2, col3, col4 = st.columns(4, gap='large')

    with col1:
        # A maior idade dos entregadores
        maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
        col1.metric('Maior idade', maior_idade)

    with col2:
        # A menor idade dos entregadores
        menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
        col2.metric('Menor idade', menor_idade)

    with col3:
        # A melhor condição de veiculo
        melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
        col3.metric( 'Melhor condição de veículo', melhor_condicao)

    with col4:
        # A pior condição de veiculo
        pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
        col4.metric( 'Pior condição de veículo', pior_condicao)

with st.container():

    st.markdown("""___""")
    st.title('Avaliações')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Avaliação medias por entregador')
        df_avg_ratings_per_delivery = entregadores.ratings_per_delivery()
        st.dataframe(df_avg_ratings_per_delivery)

    with col2:
        st.markdown('#### Avaliação media por transito')
        df_avg_std_ranting_by_traffic = entregadores.ranting_by_traffic()
        st.dataframe(df_avg_std_ranting_by_traffic)

        st.markdown('#### Avaliação media por clima')
        df_avg_std_ranting_by_weather = entregadores.ranting_by_weather()
        st.dataframe(df_avg_std_ranting_by_weather)

with st.container():
    st.markdown("""___""")
    st.title('A velocidade de entrega')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('##### Top Entregadores mais rapidos')
        df3 = entregadores.top_delivers(top_asc=True)
        st.dataframe(df3)

    with col2:
        st.markdown('##### Top entregadores mais lentos')
        df3 = entregadores.top_delivers(top_asc=False)
        st.dataframe(df3)