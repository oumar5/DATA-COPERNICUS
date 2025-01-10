import requests
import pandas as pd
from ..climatic_analysis.service_api import get_weather_climate

# Fonction pour calculer l'humidité du sol et l'indice de végétation
def calculate_soil_moisture_and_vegetation_index(lat=45.7, long=3.1, start="20250101", end="20250107"):
    # Calcul de l'humidité du sol : Précipitations - (Température Max - Température Min)
    data = get_weather_climate(lat, long, start, end)
    
    df = pd.DataFrame({
        'Date': data['Date'],
        'Humidité du sol': data.apply(lambda row: max(0, row['Précipitations Moyenne (mm)'] - 0.6 * row['Température Moyenne (°C)']), axis=1),
        'Indice de végétation': data.apply(lambda row: max(0, min(1, 0.5 + 0.05 * (row['Précipitations Moyenne (mm)'] - 10) - 0.02 * (row['Température Moyenne (°C)'] - 25))), axis=1)
    })
    return df

