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
