import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import folium
from streamlit_folium import folium_static
from collections import Counter
from pygwalker.api.streamlit import StreamlitRenderer


# Ensure `st.set_page_config` is the first Streamlit command
st.set_page_config(
    page_title="Application d'Analyse de Données",
    layout="wide",
    initial_sidebar_state="expanded"
)

data = pd.read_csv("data/licornes_modifiees.csv")


# Sidebar pour la sélection de page
st.sidebar.title("Navigateur")
page = st.sidebar.selectbox("Choisissez une page", ["Accueil", "Visualisation des données", "Statistiques descriptives","Machin learning"])

# Page 1 : Accueil
if page == "Accueil":
    st.title("Analyse des données")
    with st.expander("Exploration et Visualisation des données"):
         st.markdown(""" L'analyse des entreprises licornes dans le monde en 2022 comprend des informations détaillées sur la valorisation de marché, le secteur d'activité et le pays d'origine de ces entreprises. Les entreprises classées selon leur valeur de marché sont réparties comme suit :

         1. **Licorne (Unicorn)** : Une entreprise est considérée comme une licorne lorsqu'elle atteint une valorisation de marché de 1 milliard de dollars US ou plus. Ces entreprises représentent une part importante du marché technologique et d'autres secteurs émergents, et sont généralement considérées comme des success stories de l'innovation.

         2. **Décacorne (Decacorn)** : Les décacornes sont des entreprises dont la valorisation atteint 10 milliards de dollars US ou plus. Ces sociétés sont généralement plus matures que les licornes et ont souvent une portée internationale significative, représentant des leaders dans leur secteur respectif.

         3. **Hectacorne (Hectacorn)** : Une entreprise devient un hectacorne lorsqu'elle atteint une valorisation de 100 milliards de dollars US ou plus. Ces entreprises sont extrêmement rares et sont souvent considérées comme des géants mondiaux, avec une influence majeure dans leurs industries. Elles sont des acteurs clés de l'économie mondiale et des moteurs d'innovation à l'échelle internationale.

         L'analyse de ces catégories fournit un aperçu précieux des tendances du marché, des secteurs qui connaissent une forte croissance, ainsi que des pays qui abritent ces entreprises à forte valorisation. Ce type de classification permet de mieux comprendre la dynamique économique mondiale et d'identifier les entreprises à fort potentiel de croissance à travers le monde..""")


# Page 2 : Analyse des données
elif page == "Visualisation des données":
    st.title("Visualisation des données")
    
    # Scatter Plot Graph by Country
    st.subheader("Scatter Plot Graph par pays")
    countries = data['Country'].unique()
    selected_countries = st.multiselect("Select countries:", countries, default=countries[:2])
    filtered_data = data[data['Country'].isin(selected_countries)]
    agg_data = filtered_data.groupby(['Country', 'Year Joined']).agg({'Valuation ($B)': 'sum'}).reset_index()
    fig1 = px.scatter(agg_data, x='Year Joined', y='Valuation ($B)', color='Country')
    st.plotly_chart(fig1)

    # Bubble graph by industry
    st.subheader("Bubble Graph par industrie")
    industry_data = data.groupby('Industry').agg({'Valuation ($B)': 'sum', 'Total Raised': 'count'}).reset_index()
    fig2 = px.scatter(industry_data, x='Total Raised', y='Valuation ($B)', size='Valuation ($B)', color='Industry', text='Industry')
    fig2.add_hline(y=industry_data['Valuation ($B)'].mean())
    fig2.add_vline(x=industry_data['Total Raised'].mean())
    st.plotly_chart(fig2)

    # Boxplot graph
    st.subheader("Boxplot")
    countries_to_compare = st.multiselect("Select countries to compare:", countries, default=countries[:2])
    boxplot_data = data[data['Country'].isin(countries_to_compare)]
    fig3 = px.box(boxplot_data, x='Country', y='Valuation ($B)', color='Country')
    st.plotly_chart(fig3)
      
    
    
        
# Page 3 : Statistiques descriptives
elif page == "Statistiques descriptives":
    st.title("Statistiques descriptives")
        
    pyg_app = StreamlitRenderer(data)
     
    pyg_app.explorer()


    
    
    
    