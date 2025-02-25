import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 
import folium 
from streamlit_folium import st_folium
sns.set(style='dark')

def creat_mean_pollutants(df): # Fungsi untuk menghitung nilai rata-rata zat polutan
    # Membuat pivot tabel untuk menghitung rata-rata zat polutan
    mean_pollutants = df.groupby('Date').agg({
                        'PM2.5' : 'mean',
                        'PM10' : 'mean',
                        'SO2' : 'mean',
                        'NO2' : 'mean',
                        'CO' : 'mean',
                        'O3' : 'mean'
                    })
    return mean_pollutants # Mengembalikan nilai mean_pollutants

def comparison_of_PM25_levels_in_each_station(df): # Fungsi untuk membandingkan 
    station_pm25 = df.groupby('station')['PM2.5'].mean() # Pivot table untuk menghitung nilai rata-rata PM2.5
    return station_pm25

def create_aqi_classification(df): # Membuat fungsi untuk mengklasifikasikan aqi berdasarkan PM2,5
    
    # Membuat pivot table untuk menghitung rata_rata PM2,5
    avg_pm25_by_date_station = df.groupby(['Date', 'station', 'longitude', 'latitude'])['PM2.5'].mean().reset_index()

    # Membuat sebuah fungsi untuk klasifikasi AQI berdasarkan pm2.5
    def aqi_classification(PM25):
      if PM25 <= 12:
        return "Good"
      elif PM25 <= 35.4:
        return "Moderate"
      elif PM25 <= 55.4:
        return "Unhealthy for Sensitive Groups"
      elif PM25 <= 150.4:
        return "Unhealthy"
      elif PM25 <= 250.4:
        return "Very Unhealthy"
      else:
        return "Hazardous"
      
    # Menambahkan kolom AQI  
    avg_pm25_by_date_station['AQI'] = avg_pm25_by_date_station['PM2.5'].apply(aqi_classification) 

    return avg_pm25_by_date_station

all_df = pd.read_csv('all_air_quality_df.csv') # load data

# Mengurutkan all_df berdasarkan Date
datetime_columns = ['Date']
all_df.sort_values('Date', inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
   all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df['Date'].min() # Mengambil nilai terkecil data Date
max_date = all_df['Date'].max() # Mengambil nilai terbesar data Date

with st.sidebar:
      # Mengambil start date & end date
      try:
        start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date, value=[min_date,max_date]
        )
      except: # Membuat dashboard tetap berjalan ketika start_date & end_date tidak dipilih 
         start_date = min_date
         end_date = max_date

# Menyimpan filter all_df
main_df = all_df[(all_df['Date'] >= str(start_date))&
                (all_df['Date'] <=str(end_date))]

mean_polutants = creat_mean_pollutants(main_df)
comparison_of_PM25_levels = comparison_of_PM25_levels_in_each_station(main_df)
aqi_classification = create_aqi_classification(main_df)

st.header('Beijing Distric and sub-Distric Air Quality Dashboard (2013-2017)')

st.subheader('Daily AQI')

col1, col2, col3, col4, col5, col6 = st.columns(6) # Membuat 6 column

with col1:
  avg_pm25 = mean_polutants['PM2.5'].mean()
  st.metric('PM2.5', value=f"{avg_pm25:.2f}")
with col2:
  avg_pm10 = mean_polutants['PM10'].mean()
  st.metric('PM10', value=f"{avg_pm10:.2f}")
with col3:
  avg_so2 = mean_polutants['SO2'].mean()
  st.metric('So2', value=f"{avg_so2:.2f}")
with col4:
  avg_no2 = mean_polutants['NO2'].mean()
  st.metric('NO2', value=f"{avg_no2:.2f}")
with col5:
  avg_co = mean_polutants['CO'].mean()
  st.metric('SO', value=f"{avg_co:.1f}")
with col6:
  avg_o3 = mean_polutants['O3'].mean()
  st.metric('O3', value=f"{avg_o3:.2f}")

st.subheader('Comparison of PM2.5 Level in Each Station')

fig, ax = plt.subplots(figsize=(12, 6))

colors_ = ['#de425b', '#f3babc', '#f3babc', '#f3babc', '#f3babc', '#f3babc',
         '#f3babc', '#f3babc', '#f3babc', '#f3babc', '#f3babc', '#f3babc']

sns.barplot(x='PM2.5',
            y='station',
            data=comparison_of_PM25_levels.sort_values(ascending=False).reset_index(),
            palette=colors_,)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.subheader('Mapping AQI')

# Membuat sebuah dictionaries untuk mengelompokan AQI berdasarkan warna
colors = {
    "Good" : 'Green',
    "Moderate" : 'Yellow',
    "Unhealthy for Sensitive Groups" : 'Orange',
    "Unhealthy" : 'Red',
    "Very Unhealthy" : 'Purple',
    "Hazardous" : 'Maroon'
}

# Melakuakn plot clustering AQI menggunakan map
map = folium.Map(location=[aqi_classification['latitude'].mean(), aqi_classification['longitude'].mean()], zoom_start=10)

for _, row in aqi_classification.iterrows():
  folium.CircleMarker(
      location=[row['latitude'], row['longitude']],
      radius=5, color = colors[row['AQI']],
      fill=True, fill_color=colors[row['AQI']],
      fill_opacity=0.7, popup=f"{row['station']}: {row['AQI']}"
  ).add_to(map)

st_folium(map)