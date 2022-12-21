#Libraries
import os
import pandas as pd
import streamlit as st
from util import util as ut
from graficos.graficos_empresa import GraficosEmpresa

# ======================================
# Inicio da EStrutura logica do Código
# ======================================

st.set_page_config(
    page_title="Visão Empresa",
    page_icon="📈",
    layout='wide'
)

home_path = os.getcwd()
df = pd.read_csv(os.path.join(home_path, 'datasets', 'train.csv'))

# Limpando os dados
df = ut.clean_code(df)

date_slider, traffic_options = ut.sidebar()

# Filtros de Data
linhas_selecionadas = df['Order_Date'] < date_slider
df = df.loc[linhas_selecionadas, :]

# Filtro de Transito
linhas_selecionadas = df['Road_traffic_density'].isin(traffic_options)
df = df.loc[linhas_selecionadas, :]

# ====================================
# Layout no Streamlit
# ====================================

empresa = GraficosEmpresa(df)
st.header('Marketplace - Visão Empresa')

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geografica'])

with tab1:
    with st.container():
        st.markdown('# Orders by Day')
        fig = empresa.order_metric()
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.header('Traffic Order Share')
            fig = empresa.traffic_order_share()
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.header('Traffic Order City Share')
            fig = empresa.traffic_order_city()
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    with st.container():
        st.markdown('# Order by Week')
        fig = empresa.order_by_week()
        st.plotly_chart(fig, use_container_width=True)

    with st.container():
        st.markdown('# Order Share by Week')
        fig = empresa.order_share_by_week()
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header('Country Maps')
    empresa.country_maps()