import streamlit as st
import folium
from streamlit_folium import st_folium
from .service import get_soil_data
from .components import display_soil_data

def show():
    """
    Affiche la page de surveillance des sols avec Folium.
    """
    st.title("Surveillance des sols")
    st.write("Dessinez une zone rectangulaire sur la carte pour obtenir des données sur les sols.")

    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    # Ajouter un outil de dessin pour sélectionner une zone
    from folium.plugins import Draw
    draw = Draw(export=True, draw_options={"rectangle": True, "polyline": False, "polygon": False, "circle": False})
    draw.add_to(m)

    # Intégrer la carte dans Streamlit
    st_data = st_folium(m, width=700, height=500)

    # Vérifier si une zone a été dessinée
    if st_data and "last_active_drawing" in st_data and st_data["last_active_drawing"]:
        geometry = st_data["last_active_drawing"]["geometry"]
        if geometry and "type" in geometry and geometry["type"] == "Polygon":
            bounds = geometry["coordinates"][0]
            lat, lon = bounds[0][1], bounds[0][0]

            # Appeler le service pour récupérer les données des sols
            soil_data = get_soil_data(lat, lon)
            display_soil_data(soil_data)
        else:
            st.warning("Veuillez dessiner une zone valide.")
    else:
        st.info("Aucune zone sélectionnée. Dessinez une zone sur la carte.")
