import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from haversine import haversine




class GraficosRestaurante():
    def __init__(self, df):
        self.df = df

    def distance(self):
        self.df['distance'] = self.distance_havesine()
        avg_distance = np.round(self.df['distance'].mean(),2)

        return avg_distance

    def distance_havesine(self):
        cols = ['Restaurant_latitude','Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude' ]
        self.df['distance'] = self.df.loc[:, cols].apply(lambda x: 
                                                haversine(
                                                    (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
                                                ),axis=1)
        return self.df['distance']

    def avg_std_time_delivery(self, festival, op ):
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
        df_aux = self.df.loc[:, cols].groupby('Festival').agg({'Time_taken(min)':['mean','std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        linhas_selecionadas = df_aux['Festival'] == festival
        df_aux = np.round(df_aux.loc[linhas_selecionadas, op],2)

        return df_aux

    def avg_std_time_graph(self):
        cols = ['City','Time_taken(min)']
        df_aux = self.df.loc[:, cols].groupby('City').agg({'Time_taken(min)':['mean','std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Control',
                             x=df_aux['City'],
                             y=df_aux['avg_time'],
                             error_y=dict(type='data', array=df_aux['std_time'])))
        fig.update_layout(barmode='group')

        return fig

    def distance_fig(self):
        self.df['distance'] = GraficosRestaurante.distance_havesine(self)
        avg_distance = self.df.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
        fig = go.Figure(data=[go.Pie(labels=avg_distance['City'], values=avg_distance['distance'], pull=[0,0.1,0])])

        return fig 

    def avg_std_time_on_traffic(self):
        cols = ['City','Time_taken(min)', 'Road_traffic_density']
        df_aux = self.df.loc[:, cols].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)':['mean','std']})
        df_aux.columns = ['avg_time', 'std_time']

        df_aux = df_aux.reset_index()

        fig =px.sunburst(df_aux,path=['City', 'Road_traffic_density',],values='avg_time',
                         color='std_time', color_continuous_scale='bluered',
                         color_continuous_midpoint=np.average(df_aux['std_time']))
        return fig