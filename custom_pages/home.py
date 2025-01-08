import streamlit as st

def show():
    """
    Affiche la page d'accueil de l'application.
    """
    st.title("Gestion de l'eau en agriculture 🌍")

    st.markdown("""
        ## Bienvenue sur l'application de gestion de l'eau !

        Cette application vise à optimiser la gestion de l'eau en agriculture à l'aide :
        - Des données satellitaires (Sentinel, OneSoil),
        - Des données météorologiques en temps réel (OpenWeatherMap),
        - D'outils d'analyse avancés.

        ### Fonctionnalités principales :
        - **Surveillance des sols** : Obtenez des informations sur l'humidité des sols.
        - **Recommandations d'irrigation** : Recevez des recommandations basées sur les prévisions météorologiques.
        - **Analyse climatique** : Analysez les conditions climatiques actuelles et futures.

        **Naviguez dans l'application en utilisant le menu à gauche !**
    """)

    st.info("Astuce : Utilisez la barre latérale pour explorer les différentes sections.")
