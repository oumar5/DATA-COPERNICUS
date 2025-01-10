import streamlit as st

def show():
    """
    Affiche la page d'accueil de l'application.
    """
    st.title("Bienvenue sur HydroSense 🌍")

    st.markdown("""
        ### Gérez efficacement l'eau en agriculture !
        HydroSense est une application innovante qui vous accompagne dans la gestion de l'eau pour une agriculture durable.

        Grâce à l'analyse des données climatiques, cette application vous offre :
        - Une surveillance précise des conditions de sol.
        - Des recommandations personnalisées d'irrigation.
        - Une analyse climatique simplifiée pour anticiper vos besoins.

        #### Pourquoi utiliser HydroSense ?
        - **Précision** : Les recommandations s'appuient sur des données climatiques fiables.
        - **Simplicité** : Une interface intuitive pour un accès rapide à l'information.
        - **Durabilité** : Aidez à préserver les ressources en eau en optimisant leur utilisation.

        **Utilisez le menu à gauche pour naviguer dans les différentes fonctionnalités de l'application.** 🌱
    """)

    st.info("Astuce : Consultez les recommandations quotidiennes pour planifier votre irrigation efficacement.")
