import pandas as pd

class GraficosEntregadores():

    def __init__(self, df):
        self.df = df
    
    def top_delivers(self, top_asc):
        df = (self.df.loc[:, ['Delivery_person_ID', 'City','Time_taken(min)']]
                  .groupby(['City', 'Delivery_person_ID'])
                  .min()
                  .sort_values(['City','Time_taken(min)'], ascending=top_asc)
                  .reset_index())
        df_aux1 = df.loc[df['City'] == 'Metropolitian', :].head(10)
        df_aux2 = df.loc[df['City'] == 'Urban', :].head(10)
        df_aux3 = df.loc[df['City'] == 'Semi-Urban', :].head(10)
        df2 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop=True)
        
        return df2

    def ratings_per_delivery(self):
        df = (self.df.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
               .groupby('Delivery_person_ID')
               .median()
               .reset_index())
        
        return df
    
    def ranting_by_traffic(self):
    
         df_avg_std_ranting_by_traffic = (self.df.loc[:, ['Delivery_person_Ratings','Road_traffic_density']]
                                             .groupby('Road_traffic_density')
                                             .agg({'Delivery_person_Ratings':['mean', 'std']}))
         
         df_avg_std_ranting_by_traffic.columns = ['delivery_mean', 'delivery_std']
         df_avg_std_ranting_by_traffic = df_avg_std_ranting_by_traffic.reset_index()
         
         return df_avg_std_ranting_by_traffic
    
    def ranting_by_weather(self):
        df_avg_std_ranting_by_weather = (self.df.loc[:, ['Delivery_person_Ratings','Weatherconditions']]
                                            .groupby('Weatherconditions')
                                            .agg({'Delivery_person_Ratings':['mean', 'std']}))
        
        df_avg_std_ranting_by_weather.columns = ['delivery_mean', 'delivery_std']
        df_avg_std_ranting_by_weather = df_avg_std_ranting_by_weather.reset_index()
        
        return df_avg_std_ranting_by_weather