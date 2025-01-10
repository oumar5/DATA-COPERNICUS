import requests
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor

# URL de base pour l'API NASA POWER
BASE_URLS = {
    "nasa_power": "https://power.larc.nasa.gov/api/temporal/daily/point"
}

def get_climate_data(lat, lon, start_date, end_date):
    """
    Récupère les données climatiques (température et précipitation) depuis l'API NASA POWER.

    - lat (float) : Latitude du lieu.
    - lon (float) : Longitude du lieu.
    - start_date (str) : Date de début au format 'YYYYMMDD'.
    - end_date (str) : Date de fin au format 'YYYYMMDD'.

    Retourne :
    - Un dictionnaire contenant les données climatiques si l'appel est réussi.
    - Un dictionnaire contenant une erreur si l'appel échoue.
    """
    url = BASE_URLS["nasa_power"]
    params = {
        "latitude": lat,  # Coordonnée géographique : latitude
        "longitude": lon,  # Coordonnée géographique : longitude
        "parameters": "T2M,PRECTOTCORR",  # Température (T2M) et précipitation corrigée (PRECTOTCORR)
        "format": "JSON",  # Format de la réponse
        "temporalAverage": "daily",  # Moyenne temporelle : journalière
        "start": start_date,  # Date de début
        "end": end_date,  # Date de fin
        "community": "ag"  # Utilisation de la communauté agricole
    }
    try:
        response = requests.get(url, params=params)  # Appel à l'API avec les paramètres
        response.raise_for_status()  # Vérifie si le statut HTTP est correct (200)
        data = response.json()  # Décodage de la réponse JSON

        # Validation de la structure des données
        properties = data.get("properties", {})
        parameters = properties.get("parameter", {})
        if not parameters:
            raise ValueError("Aucune donnée climatique trouvée dans la réponse.")
        return parameters  # Renvoie les données climatiques

    except requests.exceptions.RequestException as e:
        return {"error": f"L'appel API a échoué : {str(e)}"}  # Gestion des erreurs HTTP ou de connexion


def get_soil_info(lat, lon):
    """
    Fournit des informations statiques sur le sol pour une localisation donnée.

    - lat (float) : Latitude du lieu.
    - lon (float) : Longitude du lieu.

    Retourne :
    - Un dictionnaire contenant des informations statiques sur le sol.
    """
    return {"composition": "Argileux", "pH": 6.5, "type": "Loameux"}  # Informations statiques simulées


def calculate_indices(temps, precips):
    """
    Calcule l'indice de végétation et l'humidité du sol à partir des températures et précipitations.

    - temps (list) : Liste des températures journalières en °C.
    - precips (list) : Liste des précipitations journalières en mm.

    Retourne :
    - Une liste de dictionnaires contenant les indices pour chaque jour.
    """
    if len(temps) != len(precips):  # Validation de la taille des listes
        raise ValueError("Les listes de températures et précipitations doivent avoir la même longueur.")

    indices = []
    for temp, precip in zip(temps, precips):
        # Calcul simplifié de l'indice de végétation basé sur température et précipitation
        vegetation_index = max(0, min(1, 0.5 + 0.05 * (precip - 10) - 0.02 * (temp - 25)))

        # Calcul simplifié de l'humidité du sol
        soil_moisture = max(0, precip - 0.6 * temp)

        indices.append({"vegetation_index": vegetation_index, "soil_moisture": soil_moisture})
    return indices


def train_multioutput_prediction_model(lat, lon):
    """
    Entraîne un modèle multi-sorties pour prédire température et précipitation.

    - lat (float) : Latitude du lieu.
    - lon (float) : Longitude du lieu.

    Retourne :
    - Un modèle MultiOutputRegressor basé sur RandomForestRegressor.
    """
    # Déterminer la période d'entraînement : les 2 dernières années
    today = datetime.today()
    end_date_obj = today - timedelta(days=1)  # Hier
    start_date_obj = end_date_obj - timedelta(days=2 * 365)  # Deux ans en arrière

    # Conversion des dates au format 'YYYYMMDD'
    start_date_str = start_date_obj.strftime("%Y%m%d")
    end_date_str = end_date_obj.strftime("%Y%m%d")

    # Récupération des données climatiques pour la période définie
    climate_data = get_climate_data(lat, lon, start_date_str, end_date_str)
    if "error" in climate_data:  # Vérification des erreurs dans la réponse
        raise ValueError(climate_data["error"])

    temps = list(climate_data.get("T2M", {}).values())  # Températures historiques
    precips = list(climate_data.get("PRECTOTCORR", {}).values())  # Précipitations historiques

    if not temps or not precips:  # Vérification de la disponibilité des données
        raise ValueError("Données insuffisantes pour entraîner le modèle.")

    # Préparation des données d'entraînement
    X = np.arange(len(temps)).reshape(-1, 1)  # Index des jours comme variable explicative
    y = np.column_stack((temps, precips))  # Variables cibles : (température, précipitation)

    # Création du modèle multi-sorties basé sur Random Forest
    base_model = RandomForestRegressor(n_estimators=100, random_state=42)
    multi_model = MultiOutputRegressor(base_model)

    # Entraînement du modèle
    multi_model.fit(X, y)

    return multi_model

def predict_conditions(model, day_index):
    """
    Prédit la température et la précipitation pour un jour donné.

    - model : Modèle MultiOutputRegressor entraîné.
    - day_index (int) : Index du jour à prédire.

    Retourne :
    - (temp_pred, precip_pred) : Tuple contenant la température (°C) et précipitation (mm) prédites.
    """
    X_test = np.array([[day_index]])  # Conversion de l'index en tableau 2D
    y_pred = model.predict(X_test)  # Prédictions
    temp_pred, precip_pred = y_pred[0]

    return temp_pred, max(0, precip_pred)  # Précipitation forcée à être >= 0


def generate_recommendation(soil_info, indices, temp_pred, precip_pred, culture_info):
    """
    Génère une recommandation d'irrigation structurée en litres/m² sous forme de dictionnaire.

    - soil_info (dict) : Informations sur le sol (composition, pH, etc.).
    - indices (dict) : Contient 'soil_moisture' et 'vegetation_index'.
    - temp_pred (float) : Température prédite (°C).
    - precip_pred (float) : Précipitation prédite (mm).
    - culture_info (dict) : Besoins en eau de la culture.

    Retourne :
    - Un dictionnaire contenant les recommandations structurées.
    """
    soil_moisture = indices["soil_moisture"]  # Humidité du sol calculée
    daily_need_mm = culture_info["besoin_eau_semaine"] / 7  # Besoin journalier en mm/jour
    daily_need_l_per_m2 = daily_need_mm  # Conversion directe mm -> litres/m²

    # Calcul des besoins supplémentaires en irrigation
    if precip_pred < daily_need_mm:  # Précipitations insuffisantes
        manque_mm = daily_need_mm - precip_pred  # Besoin supplémentaire en mm
        manque_l_per_m2 = manque_mm  # Conversion mm -> litres/m²
        irrigation_message = f"Précipitations insuffisantes, ajoutez ~{manque_l_per_m2:.2f} L/m²/jour."
    elif soil_moisture > culture_info["soil_moisture_optimal"]:  # Sol déjà humide
        irrigation_message = "Humidité du sol élevée, réduisez l'irrigation."
    else:  # Cas général
        irrigation_message = "Ajustez l'irrigation en fonction des conditions actuelles."

    # Construire le dictionnaire de recommandation
    recommendation = {
        "soil_info": {
            "composition": soil_info["composition"],
            "pH": soil_info["pH"],
            "type": soil_info["type"]
        },
        "weather_forecast": {
            "temperature": round(temp_pred, 1),
            "precipitation": round(precip_pred, 1)
        },
        "daily_need_l_per_m2": round(daily_need_l_per_m2, 2),
        "soil_moisture": round(soil_moisture, 2),
        "irrigation_message": irrigation_message
    }

    return recommendation

def predict_future_climate(model, num_days):
    """
    Prédit les données climatiques (température et précipitation) pour un nombre de jours donné.

    - model : Modèle MultiOutputRegressor entraîné.
    - num_days (int) : Nombre de jours pour lesquels prévoir les données.

    Retourne :
    - Une liste de dictionnaires contenant les prévisions : [{'temp': ..., 'precip': ...}, ...].
    """
    future_indices = np.arange(num_days).reshape(-1, 1)  # Index pour les jours futurs
    predictions = model.predict(future_indices)  # Prédictions pour les indices donnés

    # Formater les prédictions
    future_data = [{"temp": temp, "precip": max(0, precip)} for temp, precip in predictions]
    return future_data
