import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime

class util:

    def sidebar():

        util.logo()

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

    def logo():
        image_path = 'logo.png'
        image = Image.open(image_path)
        st.sidebar.image(image,width=120)

        st.sidebar.markdown('# Cury Company')
        st.sidebar.markdown('## Fastest Delivery un Town')
        #st.sidebar.markdown("""---""")

    def clean_code(df):
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
        linhas_selecionadas = df['Delivery_person_Age'] != 'NaN '
        df = df.loc[linhas_selecionadas, :].copy()

        df['Delivery_person_Age'] = df['Delivery_person_Age'].astype(int)

        # 2. convertendo a coluna Ratings de texto para numero decimal (float)
        df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype(float)

        # 3. convertendo a coluna order_date de texto para data
        df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')

        # 4. convertendo multiple_deliveries de texto para numero inteiro (int)
        linhas_selecionadas = df['multiple_deliveries'] != 'NaN '
        df = df.loc[linhas_selecionadas, :].copy()

        df['multiple_deliveries'] = df['multiple_deliveries'].astype(int)


        # 5. Removendo os espacos dentro de strings/texto/object
        df.loc[:, 'ID'] = df.loc[:, 'ID'].str.strip()
        df.loc[:, 'Road_traffic_density'] = df.loc[:, 'Road_traffic_density'].str.strip()
        df.loc[:, 'Type_of_order'] = df.loc[:, 'Type_of_order'].str.strip()
        df.loc[:, 'Type_of_vehicle'] = df.loc[:, 'Type_of_vehicle'].str.strip()
        df.loc[:, 'City'] = df.loc[:, 'City'].str.strip()
        df.loc[:, 'Festival'] = df.loc[:, 'Festival'].str.strip()

        # 6. Removend do NaN
        df = df.loc[df['Road_traffic_density'] != 'NaN', :].copy()
        df = df.loc[df['City'] != 'NaN', :].copy()
        df = df.loc[df['Festival'] != 'NaN ', :].copy()

        # 7. Limpando a coluna de time taken
        df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1])
        df['Time_taken(min)'] = df['Time_taken(min)'].astype(int)

        return df