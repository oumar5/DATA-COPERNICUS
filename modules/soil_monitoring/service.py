import requests
from config.config import BASE_URLS

def get_climate_data(lat, lon, start_date, end_date):
    """
    Récupère les données climatiques de NASA POWER.

    Parameters:
        lat (float): Latitude de l'emplacement.
        lon (float): Longitude de l'emplacement.
        start_date (str): Date de début au format 'YYYYMMDD'.
        end_date (str): Date de fin au format 'YYYYMMDD'.

    Returns:
        dict: Données climatiques ou erreur.
    """
    url = BASE_URLS["nasa_power"]
    params = {
        "latitude": lat,
        "longitude": lon,
        "parameters": "T2M,PRECTOTCORR",  # Température et précipitations corrigées
        "format": "JSON",
        "temporalAverage": "hourly",  # Données horaires
        "start": start_date,
        "end": end_date,
        "community": "ag"  # Données pour la communauté agricole
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def calculate_indices(temps, precips):
    """
    Calcule l'indice de végétation et l'humidité du sol pour des listes de températures et de précipitations.

    Parameters:
        temps (list): Liste des températures (°C).
        precips (list): Liste des précipitations (mm).

    Returns:
        list: Liste de dictionnaires avec les indices pour chaque période.
    """
    indices = []
    for temp, precip in zip(temps, precips):
        vegetation_index = max(0, min(1, 0.5 + 0.05 * (precip - 10) - 0.02 * (temp - 25)))
        soil_moisture = max(0, precip - 0.6 * temp)

        indices.append({
            "vegetation_index": vegetation_index,
            "soil_moisture": soil_moisture
        })
    
    return indices

