#Libraries
import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
import streamlit as st
from datetime import datetime
from haversine import haversine
from PIL import Image
from streamlit_folium import folium_static

# ==================================
# Funções
# ==================================

def sidebar():
    image_path = 'logo.png'
    image = Image.open(image_path)
    st.sidebar.image(image,width=120)
    
    st.sidebar.markdown('# Cury Company')
    st.sidebar.markdown('## Fastest Delivery un Town')
    st.sidebar.markdown("""---""")

    st.sidebar.markdown("## Selecione uma data limite")

    date_slider = st.sidebar.slider(
                    'Até qual valor?',
                    value=datetime(2022,4,6),
                    min_value=datetime(2022,2,11),
                    max_value=datetime(2022,4,13),
                    format='DD-MM-YYYY')

    st.sidebar.markdown("""---""")

    traffic_options = st.sidebar.multiselect(
                        'Quais as condiçoes de trânsito',
                        ['Low', 'Medium', 'High', 'Jam'], 
                        default=['Low', 'Medium', 'High', 'Jam'])

    st.sidebar.markdown("""---""")
    st.sidebar.markdown('### Powered by Comunidade DS')
    
    return date_slider, traffic_options

def clean_code(df1):
    """Esta função tem a responsabilidadede limpar o dataframe 

        Tips de Limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços da variaveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da culuna de tempo (remoção do texto da variável numérica)

        Input: Dataframe
        Output: Dataframe
    """

    # 1. convertendo a coluna Age de texto para numero
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # 2. convertendo a coluna Ratings de texto para numero decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 3. convertendo a coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')

    # 4. convertendo multiple_deliveries de texto para numero inteiro (int)
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)


    # 5. Removendo os espacos dentro de strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    # 6. Removend do NaN
    df1 = df1.loc[df1['Road_traffic_density'] != 'NaN', :].copy()
    df1 = df1.loc[df1['City'] != 'NaN', :].copy()
    df1 = df1.loc[df1['Festival'] != 'NaN ', :].copy()

    # 7. Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1


def distance(df1):
    df1['distance'] = distance_havesine(df1)
    avg_distance = np.round(df1['distance'].mean(),2)

    return avg_distance

def distance_havesine(df1):
    cols = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
    df1['distance'] = df1.loc[:, cols].apply(lambda x: 
                                            haversine(
                                                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
                                            ),axis=1)
    return df1['distance']

def avg_std_time_delivery(df1, festival, op ):
    """ 
        Esta função calcula o tempo médio e o desvio padrão do tempo de entrega.
        Parâmetros:
            Input:
                - df: Dataframe com os dados necessarios para os cálculos.
                - op: Tipo de operação que precisa ser calculado.
                    'avg_time': Calcula o tempo médio.
                    'std_time': Calcula o desvio padrão do tempo.
            Output:
                - df: Dataframe com 2 colunas e uma linha.
    """   
        
    cols = ['Time_taken(min)', 'Festival']
    df_aux = df1.loc[:, cols].groupby('Festival').agg({'Time_taken(min)':['mean','std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    linhas_selecionadas = df_aux['Festival'] == festival
    df_aux = np.round(df_aux.loc[linhas_selecionadas, op],2)
    
    return df_aux

def avg_std_time_graph(df1):
    cols = ['City','Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)':['mean','std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Control',
                         x=df_aux['City'],
                         y=df_aux['avg_time'],
                         error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    
    return fig

def distance_fig(df1):
    df1['distance'] = distance_havesine(df1)
    avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0,0.1,0])])
    
    return fig 

def avg_std_time_on_traffic(df1):
    cols = ['City','Time_taken(min)', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':['mean','std']})
    df_aux.columns = ['avg_time', 'std_time']

    df_aux = df_aux.reset_index()

    fig =px.sunburst(df_aux,path=['City', 'Road_traffic_density',],values='avg_time',
                     color='std_time', color_continuous_scale='bluered',
                     color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig


# ======================================
# Inicio da EStrutura logica do Código
# ======================================

home_path = os.path.dirname(os.path.abspath(__file__))
#print(os.getcwd())
df = pd.read_csv(os.path.join(home_path, 'datasets', 'train.csv'))

df1 = df.copy()
# Limpando os dados
df1 = clean_code(df1)

date_slider, traffic_options = sidebar()

# Filtros de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ====================================
# Layout no Streamlit
# ====================================
st.header('Marketplace - Visão Restaurante')

with st.container():
    st.title('Overal Mecrics')
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        devery_unique = len(df1.loc[:, 'Delivery_person_ID'].unique())
        col1.metric('Entregadore únicos', devery_unique)

    with col2:
        avg_distance = distance(df1)
        col2.metric('Distancia Média das Entregas',avg_distance)
                                     
    with col3:
        df_aux = avg_std_time_delivery(df1, festival='Yes', op='avg_time')
        col3.metric('Tempo Médio de Entrega Com Festival',df_aux)

    with col4:
        df_aux = avg_std_time_delivery(df1, festival='Yes', op='std_time')
        col4.metric('Desvio Padão Médio de Entrega Com Festival',df_aux)

    with col5:
        df_aux = avg_std_time_delivery(df1, festival='No', op='avg_time')
        col5.metric('Tempo medio de Entrega Sem Festival',df_aux)

    with col6:
        df_aux = avg_std_time_delivery(df1, festival='No', op='std_time')
        col6.metric('Desvio Padão Médio de Entrega Sem Festival',df_aux)



with st.container():
    st.markdown("""---""")
    st.title('Tempo Médio e o Desvio Padrão de Entrega por Cidade')

    fig = avg_std_time_graph(df1)
    st.plotly_chart(fig, use_container_width=True)

   
with st.container():
    st.title('Distribuição do Tempo')

    col1, col2 = st.columns(2)
    with col1:
        fig = distance_fig(df1)
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = avg_std_time_on_traffic(df1)
        st.plotly_chart(fig, use_container_width=True)  
