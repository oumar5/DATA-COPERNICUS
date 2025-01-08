import streamlit as st
import matplotlib.pyplot as plt

def display_climate_data(data):
    """
    Affiche les données climatiques récupérées sous forme de graphiques.
    """
    if "error" in data:
        st.error(data["error"])
        return
    
    st.success("Données climatiques récupérées avec succès.")
    
    # Vérifier la structure des données
    properties = data.get("properties", {})
    parameter_data = properties.get("parameter", {})

    if not parameter_data:
        st.warning("Aucune donnée climatique disponible.")
        return
    
    for parameter, values in parameter_data.items():
        st.subheader(f"Graphique pour {parameter}")
        
        # Récupération des clés (dates/heures) et valeurs
        times = list(values.keys())
        measurements = list(values.values())
        
        # Obtenir les unités, s'il existe
        parameter_info = properties.get("parameters", {}).get(parameter, {})
        units = parameter_info.get("units", "Valeurs")

        # Tracer un graphique
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(times, measurements, label=parameter, marker='o')
        ax.set_xlabel("Temps (Heure ou Date)", fontsize=12)
        ax.set_ylabel(f"Valeur ({units})", fontsize=12)
        ax.set_title(f"Évolution de {parameter}", fontsize=14)
        ax.grid(True)
        ax.legend()
        
        # Afficher le graphique dans Streamlit
        st.pyplot(fig)
