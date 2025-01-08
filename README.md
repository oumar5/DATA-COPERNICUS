# Application Streamlit : Gestion de l'eau en agriculture

Bienvenue dans le projet Streamlit pour optimiser la gestion de l'eau en agriculture. Cette application vise à fournir des outils d'aide à la décision basés sur des données satellitaires et météorologiques afin de surveiller l'humidité des sols, estimer les besoins en irrigation, et fournir des recommandations précises.

---

## Objectifs du projet

- **Surveiller l'humidité des sols** : Analyse en temps réel des conditions de sol pour diverses régions.
- **Optimiser l'irrigation** : Estimation précise des besoins en eau des cultures.
- **Fournir des recommandations** : Proposer des plans d'action basés sur les conditions climatiques et les types de sol.

---

## Architecture du projet

Voici l'organisation des dossiers et fichiers pour une application modulaire et maintenable :

```plaintext
project_root/
│
├── app.py                       # Fichier principal pour lancer l'application Streamlit
├── requirements.txt             # Dépendances Python nécessaires
├── README.md                    # Documentation du projet
│
├── config/                      # Configuration globale et utilitaires
│   ├── __init__.py
│   ├── config.py                # Paramètres globaux (clés API, URLs, etc.)
│   └── utils.py                 # Fonctions utilitaires globales
│
├── data/                        # Gestion des données
│   ├── __init__.py
│   ├── data_loader.py           # Chargement des données (APIs, fichiers, etc.)
│   └── database.py              # Interactions avec la base de données (si nécessaire)
│
├── modules/                     # Modules fonctionnels
│   ├── __init__.py
│   ├── soil_monitoring/         # Module de surveillance des sols
│   │   ├── __init__.py
│   │   ├── page.py              # Page Streamlit pour ce module
│   │   ├── components.py        # Widgets pour ce module
│   │   └── service.py           # Logique métier et traitement des données
│   ├── irrigation/              # Module de recommandations d'irrigation
│   │   ├── __init__.py
│   │   ├── page.py
│   │   ├── components.py
│   │   └── service.py
│   └── climatic_analysis/       # Module d'analyse climatique
│       ├── __init__.py
│       ├── page.py
│       ├── components.py
│       └── service.py
│
├── pages/                       # Pages principales Streamlit
│   ├── __init__.py
│   ├── home.py                  # Page d'accueil
│   └── about.py                 # Page « À propos »
│
├── assets/                      # Fichiers statiques
│   ├── styles.css               # CSS personnalisé pour le design
│   └── logo.png                 # Logo ou images
│
└── tests/                       # Tests unitaires pour valider les modules et services
    ├── __init__.py
    ├── test_soil_monitoring.py
    └── test_utils.py
```

---

## Instructions d'installation

1. **Cloner le dépôt :**
   ```bash
   git clone <URL_du_depot>
   cd project_root
   ```

2. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application :**
   ```bash
   streamlit run app.py
   ```

---

## Fonctionnalités principales

1. **Surveillance des sols :**
   - Données sur l'humidité des sols via les satellites Sentinel-1.
   - Visualisation interactive des régions et des indices d'humidité.

2. **Recommandations d'irrigation :**
   - Calcul des besoins en eau en fonction des prévisions météorologiques et des types de sol.
   - Suggestions adaptées par région et culture.

3. **Analyse climatique :**
   - Données météorologiques locales (précipitations, températures).
   - Prévisions à court et moyen terme.


