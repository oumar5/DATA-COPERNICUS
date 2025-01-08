import streamlit as st
from .service import get_climate_data
from .components import display_climate_data

def show():
    """
    Affiche la page d'analyse climatique avec des graphiques.
    """
    st.title("Analyse climatique")
    
    # Entrée utilisateur pour la latitude et la longitude
    lat = st.number_input("Latitude", value=46.603354, format="%.6f")
    lon = st.number_input("Longitude", value=1.888334, format="%.6f")
    
    # Entrée utilisateur pour les dates de début et de fin
    start_date = st.text_input("Date de début (format YYYYMMDD)", value="20230101")
    end_date = st.text_input("Date de fin (format YYYYMMDD)", value="20230131")
    
    # Bouton pour déclencher l'analyse
    if st.button("Analyser"):
        with st.spinner("Récupération des données climatiques..."):
            climate_data = get_climate_data(lat, lon, start_date, end_date)
        display_climate_data(climate_data)
