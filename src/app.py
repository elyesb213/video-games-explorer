import pandas as pd
import streamlit as st
import plotly.express as px

# Chargement des données
df = pd.read_csv('../vgsales.csv')
df = df[df['Year'].notna()]  # Nettoyage rapide
df['Year'] = df['Year'].astype(int)

st.title("🎮 Explorateur interactif des jeux vidéo")

# Sidebar : filtres
year = st.sidebar.selectbox("Choisir l'année", sorted(df['Year'].unique(), reverse=True))
genre = st.sidebar.selectbox("Choisir le genre", ['Tous'] + sorted(df['Genre'].unique()))
platform = st.sidebar.selectbox("Choisir la plateforme", ['Toutes'] + sorted(df['Platform'].unique()))

# Application des filtres
filtered_df = df[df['Year'] == year]
if genre != 'Tous':
    filtered_df = filtered_df[filtered_df['Genre'] == genre]
if platform != 'Toutes':
    filtered_df = filtered_df[filtered_df['Platform'] == platform]

# Résumé
st.markdown(f"**Nombre de jeux trouvés :** {len(filtered_df)}")

# Graphique : top jeux par ventes
top_games = filtered_df.sort_values(by='Global_Sales', ascending=False).head(10)
fig = px.bar(top_games, x='Name', y='Global_Sales', title='Top 10 jeux - ventes mondiales')
st.plotly_chart(fig)

# Graphique : ventes par région
region_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
region_sales = filtered_df[region_cols].sum().reset_index()
region_sales.columns = ['Région', 'Ventes']

fig2 = px.pie(region_sales, names='Région', values='Ventes', title='Répartition des ventes par région')
st.plotly_chart(fig2)
