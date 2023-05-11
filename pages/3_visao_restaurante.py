#Libraries
import os
import pandas as pd
import streamlit as st
from util import util as ut
from graficos.graficos_restaurante import GraficosRestaurante

# ======================================
# Inicio da EStrutura logica do Código
# ======================================

st.set_page_config(
    page_title="Visão Restaurante",
    page_icon="🍽️",
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
restaurante = GraficosRestaurante(df1)

st.header('Marketplace - Visão Restaurante')

with st.container():
    st.title('Overal Metrics')
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        devery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
        col1.metric('Entregadore únicos', devery_unique)

    with col2:
        avg_distance = restaurante.distance()
        col2.metric('Distancia Média das Entregas',avg_distance)
                                     
    with col3:
        df_aux = restaurante.avg_std_time_delivery(festival='Yes', op='avg_time')
        col3.metric('Tempo Médio de Entrega Com Festival',df_aux)

    with col4:
        df_aux = restaurante.avg_std_time_delivery(festival='Yes', op='std_time')
        col4.metric('Desvio Padão Médio de Entrega Com Festival',df_aux)

    with col5:
        df_aux = restaurante.avg_std_time_delivery(festival='No', op='avg_time')
        col5.metric('Tempo medio de Entrega Sem Festival',df_aux)

    with col6:
        df_aux = restaurante.avg_std_time_delivery(festival='No', op='std_time')
        col6.metric('Desvio Padão Médio de Entrega Sem Festival',df_aux)



with st.container():
    st.markdown("""---""")
    st.title('Tempo Médio e o Desvio Padrão de Entrega por Cidade')

    fig = restaurante.avg_std_time_graph()
    st.plotly_chart(fig, use_container_width=True)

   
with st.container():
    st.title('Distribuição do Tempo')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### Distância média dos resturantes dos locais de entrega')
        fig = restaurante.distance_fig()
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('##### Tempo médio de entrega por cidade e tipo de tráfego')
        fig = restaurante.avg_std_time_on_traffic()
        st.plotly_chart(fig, use_container_width=True)  
