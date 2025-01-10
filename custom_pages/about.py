import streamlit as st

def show():
    """
    Affiche la page "À propos" de l'application.
    """
    st.title("À propos du projet 📖")

    st.markdown("""
        ### Contexte et Objectif :
        HydroSense est conçu pour aider les agriculteurs à gérer efficacement l'eau en combinant des données climatiques fiables et des outils d'analyse avancés. 

        ### Technologies Utilisées :
        - **API Climatique** : [NASA POWER](https://power.larc.nasa.gov/api/temporal/hourly/point) pour récupérer les données de température et de précipitations.
        - **Calculs Dynamiques** : 
          - Indices comme l'humidité du sol et des approximations de l'état de la végétation basés uniquement sur les données climatiques.
        - **Outils de Développement** : 
          - **Streamlit** pour l'interface utilisateur.
          - **Pandas**, **NumPy**, **Matplotlib** pour l'analyse et la visualisation.

        ### Membres de l'Équipe :
        - **Oumar Ben Lol**
        - **EFOE Étienne Blavo**
        - **Armel Cyrille Boti**
        - **Ivan Joe Sobgui**
        - **Divengi Nagui**
        - **Sghiouri Mohammed**

        ### Applications Clés :
        - **Optimisation de l'Irrigation** : Réduire la consommation d'eau tout en maximisant les rendements agricoles.
        - **Analyse Climatique** : Anticiper les besoins en eau à partir des données météorologiques.


        Merci d'utiliser HydroSense pour une agriculture durable et responsable ! 🌱
    """)
