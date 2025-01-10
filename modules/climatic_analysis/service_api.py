import requests
import pandas as pd

def get_weather_climate(lat=45.7772, long=3.0870, start="20250101", end="20250107"):
    
    # URL de l'API NASA POWER
    api_url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

    # Paramètres pour la requête (Clermont-Ferrand)
    params = {
        "parameters": "T2M,PRECTOTCORR",  # Paramètres spécifiques
        "community": "AG",
        "latitude": lat,  # Latitude pour Clermont-Ferrand
        "longitude": long,  # Longitude pour Clermont-Ferrand
        "format": "JSON",
        "start": start,  # Date de début (format AAAAMMJJ)
        "end": end,  # Date de fin (format AAAAMMJJ)
    }

    # Envoyer la requête GET
    response = requests.get(api_url, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        data = response.json()
        
        # Vérification des données
        if 'properties' in data and 'parameter' in data['properties']:
            parameter_data = data['properties']['parameter']
            
            # Création d'un DataFrame avec les données horaires
            df = pd.DataFrame({
                "Datetime": list(parameter_data['T2M'].keys()),
                "Temperature": list(parameter_data['T2M'].values()),
                "Precipitation": list(parameter_data['PRECTOTCORR'].values())
            })
            
            # Conversion de la colonne 'Datetime' en type datetime
            df["Datetime"] = pd.to_datetime(df["Datetime"], format='%Y%m%d%H')
            
            # Extraction de la date sans l'heure pour regrouper les données par jour
            df['Date'] = df["Datetime"].dt.date
            
            # Agrégation des données par jour
            daily_df = df.groupby('Date').agg({
                'Temperature': ['max', 'min', 'mean'],   # Température max, min et moyenne par jour
                'Precipitation': ['max', 'min', 'mean']   # Précipitations max, min et somme par jour
            }).reset_index()
            
            # Renommer les colonnes pour correspondre aux exigences
            daily_df.columns = [
                'Date', 
                'Température Max (°C)', 
                'Température Min (°C)', 
                'Température Moyenne (°C)', 
                'Précipitations Max (mm)', 
                'Précipitations Min (mm)', 
                'Précipitations Moyenne (mm)'
            ]
            
            return daily_df
            
        else:
            return False
           
    else:
        return False


get_weather_climate()