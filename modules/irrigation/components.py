import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def display_climate_indices(indices_list, time_labels, temp_values, precip_values, manque_water_needs):
    """
    Affiche les indices climatiques, la température, la précipitation et le besoin en eau sous forme de graphiques séparés.

    - indices_list (list): Liste des indices calculés (vegetation_index, soil_moisture).
    - time_labels (list): Labels de temps (dates).
    - temp_values (list): Valeurs de température prédites.
    - precip_values (list): Valeurs de précipitation prédites.
    - daily_water_needs (list): Besoin en eau quotidien (L/m²).
    """
    if not indices_list or not time_labels:
        st.error("Données manquantes pour afficher les indices.")
        return

    # ----- Graphique : Température -----
    st.write("### Évolution de la température")
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(time_labels, temp_values, marker='o', color='orange', label="Température (°C)")
    ax1.set_xlabel("Temps", fontsize=12)
    ax1.set_ylabel("Température (°C)", fontsize=12, color="orange")
    ax1.set_title("Variation de la température", fontsize=14)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc="upper left")
    st.pyplot(fig1)

    # ----- Graphique : Précipitation -----
    st.write("### Évolution de la précipitation")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(time_labels, precip_values, marker='o', color='blue', label="Précipitation (mm)")
    ax2.set_xlabel("Temps", fontsize=12)
    ax2.set_ylabel("Précipitation (mm)", fontsize=12, color="blue")
    ax2.set_title("Variation de la précipitation", fontsize=14)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc="upper left")
    st.pyplot(fig2)

    # ----- Graphique : Indices climatiques -----
    indices_vegetation = [i["vegetation_index"] for i in indices_list]
    indices_soil_moisture = [i["soil_moisture"] for i in indices_list]

    st.write("### Indices climatiques")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.plot(time_labels, indices_vegetation, marker='o', label="Indice de végétation", color='green')
    ax3.plot(time_labels, indices_soil_moisture, marker='o', linestyle='--', label="Humidité du sol (mm)", color='brown')
    ax3.set_xlabel("Temps", fontsize=12)
    ax3.set_ylabel("Indices", fontsize=12)
    ax3.set_title("Évolution des indices climatiques", fontsize=14)
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, linestyle='--', alpha=0.6)
    ax3.legend(loc="upper left")
    st.pyplot(fig3)

    # ----- Graphique : Manque en eau -----
    st.write("### Évolution du manque en eau quotidien")
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.plot(time_labels, manque_water_needs, marker='o', color='purple', label="Manque en Eau (L/m²)")
    ax4.set_xlabel("Temps", fontsize=12)
    ax4.set_ylabel("Manque en Eau (L/m²)", fontsize=12, color="purple")
    ax4.set_title("Variation du manque en eau quotidien", fontsize=14)
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, linestyle='--', alpha=0.6)
    ax4.legend(loc="upper left")
    st.pyplot(fig4)


def display_recommendation(recommendations):
    """
    Affiche les recommandations générées dans un tableau bien structuré.

    - recommendations (list): Liste des recommandations, chaque élément étant un dictionnaire structuré.
    """
    st.markdown("<h3 style='color:#2c3e50;'>Recommandations d'Irrigation</h3>", unsafe_allow_html=True)

    # Préparation des données pour le tableau
    table_data = []
    for idx, recommendation in enumerate(recommendations, start=1):
        table_data.append({
            "Jour": idx,
            "Sol (Type)": f"{recommendation['soil_info']['type']} ({recommendation['soil_info']['composition']})",
            "pH du Sol": recommendation['soil_info']['pH'],
            "Température (°C)": recommendation['weather_forecast']['temperature'],
            "Précipitation (mm)": recommendation['weather_forecast']['precipitation'],
            "Besoin en Eau (L/m²)": recommendation['daily_need_l_per_m2'],
            "Humidité du Sol (mm)": recommendation['soil_moisture'],
            "Recommandation": recommendation['irrigation_message']
        })

    # Conversion en DataFrame
    df = pd.DataFrame(table_data)

    # Affichage dans Streamlit
    st.dataframe(df, use_container_width=True)
