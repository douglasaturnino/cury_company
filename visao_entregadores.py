#Libraries
import folium
import pandas as pd
import plotly.express as px
import os
import streamlit as st
from haversine import haversine
from PIL import Image
from streamlit_folium import folium_static

home_path = os.path.dirname(os.path.abspath(__file__))
#print(os.getcwd())
df = pd.read_csv(os.path.join(home_path, 'datasets', 'train.csv'))

df1 = df.copy()

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
df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

# ====================================
# Barra lateral
# ====================================

st.header('Marketplace - Visão Entregadores')

# image_path = 'logo.png'
# image = Image.open(image_path)
# st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery un Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown("## Selecione uma data limite")

date_slider = st.sidebar.slider(
                'Até qual valor?',
                value=pd.datetime(2022,4,6),
                min_value=pd.datetime(2022,2,11),
                max_value=pd.datetime(2022,4,13),
                format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
                    'Quais as condiçoes de trânsito',
                    ['Low', 'Medium', 'High', 'Jam'], 
                    default=['Low', 'Medium', 'High', 'Jam']
)

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtros de Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de Transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# ====================================
# Layout no Streamlit
# ====================================

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
        df_avg_ratings_per_delivery = (df.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                                         .groupby('Delivery_person_ID')
                                         .median()
                                         .reset_index())

        st.dataframe(df_avg_ratings_per_delivery)


    with col2:
        st.markdown('#### Avaliação media por transito')
        df_avg_std_ranting_by_traffic = (df1.loc[:, ['Delivery_person_Ratings','Road_traffic_density']]
                                            .groupby('Road_traffic_density')
                                            .agg({'Delivery_person_Ratings':['mean', 'std']}))

        df_avg_std_ranting_by_traffic.columns = ['delivery_mean', 'delivery_std']
        df_avg_std_ranting_by_traffic = df_avg_std_ranting_by_traffic.reset_index()
        
        st.dataframe(df_avg_std_ranting_by_traffic)


        st.markdown('#### Avaliação media por clima')
        df_avg_std_ranting_by_weather = (df1.loc[:, ['Delivery_person_Ratings','Weatherconditions']]
                                            .groupby('Weatherconditions')
                                            .agg({'Delivery_person_Ratings':['mean', 'std']}))

        df_avg_std_ranting_by_weather.columns = ['delivery_mean', 'delivery_std']
        df_avg_std_ranting_by_weather = df_avg_std_ranting_by_weather.reset_index()
        
        st.dataframe(df_avg_std_ranting_by_weather)


with st.container():
    st.markdown("""___""")
    st.title('A velocidade de entrega')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Top Entregadores mais rapidos')

        df2 = df1.loc[:, ['Delivery_person_ID', 'City','Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City','Time_taken(min)'], ascending=True).reset_index()

        df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
        df_aux2 = df2.loc[df2['City'] == 'Urban', :].head(10)
        df_aux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

        df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
        st.dataframe(df3)

    with col2:
        st.subheader('Top entregadores mais lentos')
        df2 = df1.loc[:, ['Delivery_person_ID', 'City','Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City','Time_taken(min)'], ascending=True).reset_index()

        df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
        df_aux2 = df2.loc[df2['City'] == 'Urban', :].head(10)
        df_aux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

        df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
        st.dataframe(df3)


