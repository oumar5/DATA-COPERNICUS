import streamlit as st
import folium
from streamlit_folium import st_folium
from .service import get_irrigation_recommendations
from .components import display_irrigation_recommendations

def show():
    """
    Affiche la page de recommandations d'irrigation avec Folium.
    """
    st.title("Recommandations d'irrigation")
    
    st.write("Sélectionnez un point sur la carte.")
    
    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)
    
    # Ajouter un marqueur initial
    marker = folium.Marker([46.603354, 1.888334], popup="France - Déplacez-moi", draggable=True)
    marker.add_to(m)

    # Afficher la carte interactive dans Streamlit
    st_data = st_folium(m, width=700, height=500)
    
    # Récupérer les coordonnées du marqueur
    if st_data and "last_object_clicked" in st_data:
        lat, lon = st_data["last_object_clicked"]["lat"], st_data["last_object_clicked"]["lng"]
        st.write(f"Coordonnées sélectionnées : Latitude = {lat}, Longitude = {lon}")

        # Appeler le service pour obtenir des recommandations
        irrigation_data = get_irrigation_recommendations(lat, lon)
        display_irrigation_recommendations(irrigation_data)
