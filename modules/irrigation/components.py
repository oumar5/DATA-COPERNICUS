import streamlit as st

def display_irrigation_recommendations(data):
    """
    Affiche les recommandations d'irrigation.
    """
    if "error" in data:
        st.error(data["error"])
    else:
        st.write("Recommandations :")
        st.write(f"- Température : {data['temperature']}°C")
        st.write(f"- Précipitations : {data['precipitation']} mm")
        if data["irrigation_needed"]:
            st.warning("Irrigation recommandée.")
        else:
            st.success("Pas d'irrigation nécessaire.")
