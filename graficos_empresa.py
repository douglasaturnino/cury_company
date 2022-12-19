import folium
import pandas as pd
import plotly.express as px
from streamlit_folium import folium_static

class GraficosEmpresa():

    def __init__(self, df):
        self.df = df

    def order_metric(self):
        # coluna
        cols = ['ID', 'Order_Date']

        # seleção de linhas
        df_aux = self.df.loc[:, cols].groupby('Order_Date').count().reset_index()

        # desenhar o grafico de linhas
        fig = px.bar(df_aux, x='Order_Date', y='ID')
        return fig

    def traffic_order_share(self):
        df_aux = (self.df.loc[:, ['ID', 'Road_traffic_density']]
                     .groupby('Road_traffic_density')
                     .count()
                     .reset_index())

        df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()

        fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
        return fig

    def traffic_order_city(self):
        df_aux = (self.df.loc[:, ['ID', 'City', 'Road_traffic_density']]
                     .groupby(['City', 'Road_traffic_density'])
                     .count()
                     .reset_index())

        fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
        return fig

    def order_by_week(self):
        # criar a coluna de semana
        self.df['week_of_year'] = self.df['Order_Date'].dt.strftime('%U')
        df_aux = self.df.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        fig = px.line(df_aux, x='week_of_year', y='ID')
        return fig

    def order_share_by_week(self):
        # Quantidade de pedidos por semana / Número únicos de entregadores por semana
        df_aux01 = self.df.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
        df_aux02 = self.df.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
        df_aux = pd.merge(df_aux01, df_aux02, how='inner')
        df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        fig = px.line(df_aux, x='week_of_year', y='order_by_deliver')

        return fig

    def country_maps(self):
        cols = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df_aux = self.df.loc[:, cols].groupby(['City', 'Road_traffic_density']).median().reset_index()

        map = folium.Map(
            location=[df_aux['Delivery_location_latitude'].mean(),
                      df_aux['Delivery_location_longitude'].mean()],
            zoom_start=6
        )

        for index, location_info in df_aux.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'],
                           location_info['Delivery_location_longitude']]).add_to(map)

        folium_static(map, width=1024, height=600)