import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
import streamlit as st # type: ignore
sns.set(style='dark')

all_air_quality_df = pd.read_csv('all_air_quality_df.csv')

st.header('Air Quality Dashboard')

st.subheader('Tren PM2.5 dan PM10 per Tahun')

fig, ax = plt.subplots(figsize=(20, 10))

sns.lineplot(
    x='year',
    y='PM2.5',
    data=all_air_quality_df,
    label='PM2.5',
    ax=ax
)

sns.lineplot(
    x='year',
    y='PM10',
    data=all_air_quality_df,
    label='PM10',
    ax=ax
)

ax.set_xlabel('Tahun')
ax.set_ylabel('Konsentrasi (μg/m³)')
ax.legend(fontsize=15)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
ax.set_xticks(range(2013, 2018))

st.pyplot(fig)

st.subheader('Pengaruh RAIN & WSPM Terhadap distribusi Polutan')

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.scatterplot(
        x='RAIN',
        y='PM2.5',
        data=all_air_quality_df,
        label='PM2.5',
        ax=ax
    )

    sns.scatterplot(
        x='RAIN',
        y='NO2',
        data=all_air_quality_df,
        label='NO2',
        ax=ax
    )
ax.set_title('Pengaruh Curah Hujan (RAIN) terhadap Konsentrasi Polutan (PM2.5 & No2)')
ax.set_xlabel('Curah Hujan (mm)')
ax.set_ylabel('Konsentrasi (μg/m³)')
ax.grid(True)
ax.legend(fontsize=15)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.scatterplot(
        x='WSPM',
        y='PM2.5',
        data=all_air_quality_df,
        label='PM2.5',
        ax=ax
    )

    sns.scatterplot(
        x='WSPM',
        y='PM10',
        data=all_air_quality_df,
        label='PM10',
        ax=ax
    )
ax.set_title('Pengaruh WSPM terhadap Distribusi Polutan (Pm2.5 & PM10)')
ax.set_xlabel('WSPM')
ax.set_ylabel('Konsentrasi (μg/m³)')
ax.grid(True)
ax.legend(fontsize=15)
ax.tick_params(axis='x', labelsize=30)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)

air_quality = all_air_quality_df.groupby('station')['PM2.5'].mean().sort_values(ascending=False)

st.subheader('Perbandingan PM2.5 disetiap Stasiun Pengukuran')

fig,ax = plt.subplots(figsize=(20,10))

sns.barplot(x=air_quality.index, y=air_quality.values)

ax.set_xlabel('Stasiun')
ax.set_ylabel('Rata-rata Konsentrasi PM2.5 (μg/m³)')

ax.legend(fontsize=15)
ax.tick_params(axis='x', labelsize=30, rotation=45)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)