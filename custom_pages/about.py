import streamlit as st

def show():
    """
    Affiche la page "À propos" de l'application.
    """
    st.title("À propos du projet 📖")

    st.markdown("""
        ### Objectif du projet :
        Ce projet a été conçu pour aider les agriculteurs et les gestionnaires à optimiser l'usage de l'eau en utilisant des outils numériques et des données géospatiales.

        ### Technologies utilisées :
        - **Streamlit** pour l'interface utilisateur.
        - **APIs** : OpenWeatherMap, OneSoil, Google Earth Engine.
        - **Bibliothèques Python** : Pandas, Plotly, Requests.

        ### Développeurs :
        - **Votre Nom** : Développement et intégration des fonctionnalités.
        - **Votre Équipe** : Contribution à l'analyse et à la conception.

        ### Contact :
        - **Email** : votre.email@example.com
        - **Téléphone** : +33 6 12 34 56 78

        Merci d'utiliser cette application ! 🚀
    """)
