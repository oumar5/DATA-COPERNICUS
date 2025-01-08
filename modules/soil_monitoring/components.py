import streamlit as st

def display_soil_data(data):
    """
    Affiche les données sur les sols récupérées.
    """
    if "error" in data:
        st.error(data["error"])
    else:
        st.write("Données sur les sols :", data)
