import requests
import pandas as pd
from ..climatic_analysis.service_api import get_weather_climate

# Fonction pour calculer l'humidité du sol et l'indice de végétation
def calculate_soil_moisture_and_vegetation_index(lat=45.7, long=3.1, start="20250101", end="20250107"):
    # Calcul de l'humidité du sol : Précipitations - (Température Max - Température Min)
    data = get_weather_climate(lat, long, start, end)
    
    df = pd.DataFrame({
            'Date': data['Date'],
            'Humidité du sol': data['Précipitations Moyenne (mm)'] - (data['Température Max (°C)'] - data['Température Min (°C)']),
            'Indice de végétation': (data['Précipitations Moyenne (mm)'] * (data['Température Max (°C)'] - data['Température Min (°C)'])) / data['Température Max (°C)'],
    })

    return df

