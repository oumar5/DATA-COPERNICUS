import requests

def make_api_request(url, params=None, headers=None):
    """
    Effectue une requête HTTP GET vers une API avec gestion des erreurs.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}
