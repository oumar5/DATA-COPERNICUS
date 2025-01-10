import streamlit as st
from datetime import datetime, timedelta

# Import des modules locaux
from .service import (
    get_climate_data,
    calculate_indices,
    get_soil_info,
    train_multioutput_prediction_model,
    predict_conditions,
    predict_future_climate,
    generate_recommendation,
)
from .components import display_climate_indices, display_recommendation


def set_green_theme():
    """
    Applique un thème vert à l'application Streamlit.
    """
    st.markdown(
        """
        <style>
        .reportview-container {
            background-color: #eaffea;
        }
        .stButton>button {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 0.5em 1em;
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            background-color: #f0fff0;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def load_culture_info(fruit_type):
    """
    Charge des informations statiques sur la culture à analyser en fonction du fruit sélectionné.
    """
    if fruit_type == "Pommier":
        return {
            "nom": "Pommier",
            "temp_optimal_min": 15,
            "temp_optimal_max": 25,
            "besoin_eau_semaine": 20,  # Besoin d'eau en mm par semaine
            "type_sol_prefere": "Loameux",
            "ph_optimal_min": 6.0,
            "ph_optimal_max": 7.0,
            "soil_moisture_optimal": 15  # Humidité du sol en mm
        }
    elif fruit_type == "Poiriers":
        return {
            "nom": "Poiriers",
            "temp_optimal_min": 14,
            "temp_optimal_max": 24,
            "besoin_eau_semaine": 18,
            "type_sol_prefere": "Argileux",
            "ph_optimal_min": 6.0,
            "ph_optimal_max": 7.5,
            "soil_moisture_optimal": 14
        }
    elif fruit_type == "Cerisiers":
        return {
            "nom": "Cerisiers",
            "temp_optimal_min": 16,
            "temp_optimal_max": 26,
            "besoin_eau_semaine": 22,
            "type_sol_prefere": "Sableux",
            "ph_optimal_min": 5.5,
            "ph_optimal_max": 6.5,
            "soil_moisture_optimal": 13
        }
    else:  # Autre ou valeurs par défaut
        return {
            "nom": fruit_type,
            "temp_optimal_min": 15,
            "temp_optimal_max": 25,
            "besoin_eau_semaine": 20,
            "type_sol_prefere": "Loameux",
            "ph_optimal_min": 6.0,
            "ph_optimal_max": 7.0,
            "soil_moisture_optimal": 15
        }


def show():
    """
    Affiche la page principale pour calculer les indices et les recommandations.
    """
    set_green_theme()
    st.title("Indice de Végétation et Humidité du Sol")
    st.write("Analyse climatique pour une région donnée.")

    # Ajout du sélecteur de fruit
    fruit_choice = st.selectbox(
        "Sélectionnez un fruit",
        ["Pommier", "Poiriers", "Cerisiers", "Autre"]
    )

    st.info("Les coordonnées par défaut sont centrées sur la région Auvergne-Rhône-Alpes.")
    lat = st.number_input("Latitude", value=45.764043, format="%.6f")
    lon = st.number_input("Longitude", value=4.835659, format="%.6f")

    today = datetime.today()
    date_range = st.date_input(
        "Sélectionnez la période (dates futures uniquement)",
        value=(today + timedelta(days=1), today + timedelta(days=30)),
        min_value=today,
        max_value=datetime(today.year + 10, today.month, today.day),
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        num_days = (end_date - start_date).days + 1  # Calcul du nombre de jours dans la plage
    else:
        st.error("Veuillez sélectionner une plage de dates valide.")
        st.stop()

    if st.button("Calculer les indices"):
        with st.spinner("Entraînement du modèle..."):
            try:
                model = train_multioutput_prediction_model(lat, lon)
                st.success("Modèle entraîné avec succès.")
            except ValueError as ve:
                st.error(str(ve))
                st.stop()

        with st.spinner("Prédiction des données climatiques futures..."):
            try:
                future_climate_data = predict_future_climate(model, num_days)
                st.success("Prédictions climatiques générées avec succès.")
            except Exception as e:
                st.error(f"Erreur lors de la prédiction : {str(e)}")
                st.stop()

        # Extraire les prévisions
        temp_values = [day["temp"] for day in future_climate_data]
        precip_values = [day["precip"] for day in future_climate_data]
        time_labels = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]

        indices_list = calculate_indices(temp_values, precip_values)
        culture_info = load_culture_info(fruit_choice)  # Utilisation du fruit sélectionné
        soil_info = get_soil_info(lat, lon)

        recommendations = []
        for idx, (temp, precip, indices) in enumerate(zip(temp_values, precip_values, indices_list)):
            rec = generate_recommendation(soil_info, indices, temp, precip, culture_info)
            recommendations.append(rec)

        # Extraire les besoins quotidiens en eau à partir des recommandations
        daily_water_needs = [rec['daily_need_l_per_m2'] for rec in recommendations]

        # Appel de la fonction avec les besoins quotidiens
        display_climate_indices(indices_list, time_labels, temp_values, precip_values, daily_water_needs)
        display_recommendation(recommendations)
