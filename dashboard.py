import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/fichier_2 .csv')

st.set_page_config(page_title="Tableau de Bord des Performances", layout="wide")

st.title("Tableau de Bord des Performances sur 2000m")

nombre_participants = st.sidebar.selectbox("Nombre de participants à afficher :", [0, 5, 10, 15, 20, 30, 32])

participants = st.sidebar.multiselect("Sélectionner les participants", options=data["participant"].unique())
vitesse_min = st.sidebar.slider("Vitesse moyenne minimale (km/h)", 
                                 min_value=float(data["vitesse_moyenne_2000m_kmh"].min()), 
                                 max_value=float(data["vitesse_moyenne_2000m_kmh"].max()))



df_filtered = data[data["vitesse_moyenne_2000m_kmh"] >= vitesse_min]
if participants:
    df_filtered = df_filtered[df_filtered["participant"].isin(participants)]

data["time_on_2000m"] = data["time_on_2000m"].str.replace('.', ':', regex=False) 
data["time_on_2000m"] = pd.to_timedelta(data["time_on_2000m"], errors='coerce')  
data["time_on_2000m_seconds"] = data["time_on_2000m"].dt.total_seconds()  

data["rang"] = data["time_on_2000m_seconds"].rank(method="min", ascending=True)
df_filtered['rang'] = data['rang']

st.subheader("Ran de chaque Participant")
st.write(data[["participant", "rang"]].set_index("participant").T)
df_filtered = df_filtered.sort_values(by='rang')

st.subheader("Calories Brûlées en Fonction du Rang sur le Temps 2000m")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=data.sort_values("rang"), x="rang", y="calories", ax=ax)
ax.set_title("Calories Brûlées en Fonction du Rang")
ax.set_xlabel("Rang (Temps croissant)")
ax.set_ylabel("Calories Brûlées")
st.pyplot(fig)

st.subheader("Temps et Vitesse Moyenne sur 2000m")
df_top_n = df_filtered.head(nombre_participants)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))

sns.barplot(data=df_top_n, x="rang", y="vitesse_moyenne_2000m_kmh", ax=ax[0])
ax[0].set_title("Vitesse Moyenne (km/h)")

sns.barplot(data=df_top_n, x="rang", y="time_on_2000m", ax=ax[1])
ax[1].set_title("Temps Total (s)")

st.pyplot(fig)

st.subheader("Analyse par Segments de 500m")

for i in range(1, 5):
    st.write(f"**Segment {i}**")
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    sns.barplot(data=df_top_n, x="rang", y=f"vitesse_moyenne_split_{i}_kmh", ax=ax[0])
    ax[0].set_title(f"Vitesse Moyenne sur le Segment {i}")
    
    sns.barplot(data=df_top_n, x="rang", y=f"longueur_moyenne_split_{i}_par_coup", ax=ax[1])
    ax[1].set_title(f"Longueur Moyenne par Coup sur le Segment {i}")
    
    st.pyplot(fig)

st.write(f"Affichage des {min(len(df_filtered), nombre_participants)} premiers participants :")
st.write(df_top_n)
