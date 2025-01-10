

# Guide Complet : Utilisation des Données Climatiques, Informations Statiques et Calculs d’Indices

Ce guide détaille les étapes pour :
1. **Récupérer les données climatiques via l’API NASA POWER.**
2. **Obtenir les informations sur le sol (de façon hypothétique).**
3. **Stocker et utiliser des informations statiques sur une culture** (par exemple : le pommier).
4. **Calculer des indices**, notamment l’humidité du sol et un indice de végétation simplifié.
5. **Générer une recommandation** basée sur ces données.

### Structure des fichiers
Nous structurons le code dans trois fichiers :
- **`service.py`** : appels aux APIs (NASA, API sol).  
- **`component.py`** : gestion des informations statiques et calculs (soil moisture, NDVI simplifié).  
- **`page.py`** : orchestration et génération des recommandations.  

---

## 1. Étapes et Formules

### 1.1 Récupération des données climatiques (NASA POWER)
- Utiliser la fonction `get_climate_data(lat, lon, start_date, end_date)` pour récupérer les données climatiques.  
- Paramètres : latitude, longitude, dates de début et de fin.  
- La réponse contient notamment :
  - **Températures horaires** (`T2M`)  
  - **Précipitations corrigées** (`PRECTOTCORR`).  

---

### 1.2 Récupération des informations sur le sol
- Une API externe pourrait fournir :
  - Composition du sol.
  - pH.
  - Type de sol (ex. : argileux, limoneux).  
- Ici, nous simulons cet appel avec une fonction `get_soil_info(lat, lon)`.

---

### 1.3 Informations statiques sur la culture (Exemple : pommier)
- **Données statiques** : plage de température optimale, besoins en eau, etc.  
- Ces informations sont définies dans un dictionnaire Python.  
- Exemple pour le pommier :
  - Température optimale : 15-25 °C.
  - Besoins en eau : 20 mm/semaine.
  - Type de sol préféré : loameux.  
  - pH optimal : 6.0-7.0.

---

### 1.4 Calcul de l’humidité du sol
- **Formule simplifiée** :  
  \[
  \text{soil\_moisture} = \max(0, \text{precip} - 0.6 \times \text{temp})
  \]
- Remarque : Cette formule approximative ne tient pas compte d'autres facteurs (ex. évapotranspiration).

---

### 1.5 Calcul de l’indice de végétation
- **Formule simplifiée** :  
  \[
  \text{vegetation\_index} = \max(0, \min(1, 0.5 + 0.05 \times (\text{precip} - 10) - 0.02 \times (\text{temp} - 25)))
  \]
- Remarque : Cette formule est une approximation. Le NDVI standard est basé sur des mesures spectrales (proche infrarouge - NIR, rouge - RED) :  
  \[
  NDVI = \frac{\text{NIR} - \text{RED}}{\text{NIR} + \text{RED}}
  \]

---

### 1.6 Recommandation
- En combinant :
  - Données statiques (besoins en eau).  
  - Calculs (humidité du sol, vegetation_index).  
- Vous pouvez recommander :  
  - Une augmentation de l’irrigation si la température est trop élevée.  
  - Une réduction de l’arrosage si l’humidité du sol est correcte.

---

