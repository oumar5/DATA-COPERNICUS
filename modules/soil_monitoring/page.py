import streamlit as st
from datetime import datetime
from .service import get_climate_data, calculate_indices
from .components import display_climate_indices

def set_green_theme():
    st.markdown(
        """
        <style>
        /* Set background color for the entire app */
        .reportview-container {
            background-color: #eaffea;
        }
        /* Style the buttons with a green background */
        .stButton>button {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 0.5em 1em;
            border-radius: 5px;
        }
        /* Change text input background color */
        .stTextInput>div>div>input {
            background-color: #f0fff0;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show():
    """
    Displays the page to calculate vegetation and soil moisture indices.
    """
    set_green_theme()
    st.title("Indice de végétation et humidité du sol")
    st.write("Analyse climatique pour une région donnée.")

    st.info("Les coordonnées par défaut sont centrées sur la région Auvergne-Rhône-Alpes.")
    lat = st.number_input("Latitude", value=45.764043, format="%.6f")
    lon = st.number_input("Longitude", value=4.835659, format="%.6f")

    date_range = st.date_input(
        "Sélectionnez la période",
        value=(datetime(2023, 1, 1), datetime(2023, 1, 31)),
        min_value=datetime(2000, 1, 1),
        max_value=datetime.today(),
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
    else:
        st.error("Veuillez sélectionner une plage de dates valide.")
        return

    if st.button("Calculer les indices"):
        with st.spinner("Récupération des données climatiques..."):
            climate_data = get_climate_data(lat, lon, start_date_str, end_date_str)

        if "error" in climate_data:
            st.error(climate_data["error"])
            return

        parameters = climate_data.get("properties", {}).get("parameter", {})

        if not parameters:
            st.warning("Aucune donnée disponible pour ces coordonnées et ces dates.")
            return

        try:
            temp_values = list(parameters["T2M"].values())
            precip_values = list(parameters["PRECTOTCORR"].values())
            time_labels = list(parameters["T2M"].keys())

            indices_list = calculate_indices(temp_values, precip_values)
            display_climate_indices(indices_list, time_labels)

        except KeyError as e:
            st.error(f"Erreur de clé manquante : {str(e)}")
