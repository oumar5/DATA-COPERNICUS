from data.data_loader import fetch_weather_data

def get_irrigation_recommendations(lat, lon):
    """
    Analyse les données météo pour fournir des recommandations d'irrigation.
    """
    weather_data = fetch_weather_data(lat, lon)
    if "error" in weather_data:
        return {"error": weather_data["error"]}
    
    recommendations = {
        "temperature": weather_data["temperature"],
        "precipitation": weather_data["precipitation"],
        "irrigation_needed": weather_data["precipitation"] < 5
    }
    return recommendations
