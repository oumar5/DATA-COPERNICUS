from data.data_loader import fetch_soil_data

def get_soil_data(lat, lon):
    """
    Appelle le service de données pour récupérer les informations sur les sols.
    """
    return fetch_soil_data(lat, lon)
