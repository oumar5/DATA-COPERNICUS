import streamlit as st
from custom_pages import home, about
from modules.soil_monitoring.page import show as show_soil_monitoring
from modules.irrigation.page import show as show_irrigation
from modules.climatic_analysis.page import show as show_climatic_analysis

# Configuration de la barre latérale pour la navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Aller à :",
    ["Accueil", "Analyse climatique","Surveillance des sols", "Recommandations d'irrigation",  "À propos"]
)

# Charger les pages en fonction de la sélection
if page == "Accueil":
    home.show()
elif page == "Surveillance des sols":
    show_soil_monitoring()
elif page == "Recommandations d'irrigation":
    show_irrigation()
elif page == "Analyse climatique":
    show_climatic_analysis()
elif page == "À propos":
    about.show()
