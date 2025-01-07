### **Rapport : Analyse et Suivi de la Végétation avec Sentinel-2**

---

### **Introduction**
Sentinel-2, une mission du programme européen Copernicus, fournit des données multispectrales essentielles pour surveiller la végétation. Ces données permettent d’évaluer la santé des plantes, détecter le stress hydrique et analyser les écosystèmes à l’aide d’indices de végétation.

---

### **Données Utiles pour la Végétation**

#### **Bandes Spectrales Recommandées**
Les bandes spectrales de Sentinel-2 permettent une analyse détaillée de la végétation :

| **Bande** | **Nom**                  | **Longueur d’onde (nm)** | **Résolution (m)** | **Utilité**                                                             |
|-----------|--------------------------|--------------------------|--------------------|--------------------------------------------------------------------------|
| **B2**    | Bleu                     | 490                      | 10                 | Détection de chlorophylle, qualité de l'eau.                             |
| **B3**    | Vert                     | 560                      | 10                 | Estimation de la couverture végétale.                                    |
| **B4**    | Rouge                    | 665                      | 10                 | Absorption par la chlorophylle (NDVI).                                   |
| **B5**    | Red Edge (Bord rouge 1)  | 705                      | 20                 | Contenu en chlorophylle dans les feuilles.                               |
| **B6**    | Red Edge (Bord rouge 2)  | 740                      | 20                 | Densité végétale.                                                        |
| **B7**    | Red Edge (Bord rouge 3)  | 783                      | 20                 | Stress végétal.                                                          |
| **B8**    | NIR (Proche Infrarouge)  | 842                      | 10                 | Biomasse et indices de végétation (NDVI, EVI).                           |
| **B8A**   | Red Edge (Bord rouge 4)  | 865                      | 20                 | Changements subtils dans la canopée.                                     |
| **B11**   | SWIR 1 (Infrarouge court) | 1610                     | 20                 | Humidité de la végétation, stress hydrique.                              |
| **B12**   | SWIR 2 (Infrarouge court) | 2190                     | 20                 | Zones brûlées, conditions de sécheresse.                                 |

---

### **Indices de Végétation**

1. **NDVI (Normalized Difference Vegetation Index)** :
   - **Formule** :  
     \[
     NDVI = \frac{B8 - B4}{B8 + B4}
     \]
   - **Utilité** : Mesure de la santé de la végétation.
   - **Valeurs** :
     - Près de 1 : Végétation dense.
     - Près de 0 : Sols nus.
     - Négatif : Eau ou surfaces sans végétation.

2. **EVI (Enhanced Vegetation Index)** :
   - **Formule** :  
     \[
     EVI = 2.5 \times \frac{(B8 - B4)}{(B8 + 6 \times B4 - 7.5 \times B2 + 1)}
     \]
   - **Utilité** : Réduction des effets atmosphériques et du sol.

3. **SAVI (Soil Adjusted Vegetation Index)** :
   - **Formule** :  
     \[
     SAVI = \frac{(B8 - B4) \times (1 + 0.5)}{(B8 + B4 + 0.5)}
     \]
   - **Utilité** : Adapté aux zones où le sol est visible.

4. **Red Edge Chlorophyll Index** :
   - **Formule** :  
     \[
     CI_{red\ edge} = \frac{B8}{B5} - 1
     \]
   - **Utilité** : Mesure de la concentration de chlorophylle.

5. **NDWI (Normalized Difference Water Index)** :
   - **Formule** :  
     \[
     NDWI = \frac{B8 - B11}{B8 + B11}
     \]
   - **Utilité** : Indique l'humidité de la végétation.

---

### **Étapes d’Analyse**

1. **Téléchargement des Données** :
   - Téléchargez les images Sentinel-2 sur [Copernicus Open Access Hub](https://scihub.copernicus.eu/dhus).
   - Sélectionnez les bandes nécessaires (B2, B4, B8, etc.).

2. **Traitement des Données** :
   - Corrigez les effets atmosphériques avec **ESA SNAP**.
   - Extraire les bandes d’intérêt.

3. **Calcul des Indices** :
   - Utilisez Python avec des bibliothèques comme `rasterio` et `numpy` :
     ```python
     NDVI = (B8 - B4) / (B8 + B4)
     ```

4. **Visualisation** :
   - Créez des cartes dans **QGIS** ou **matplotlib** pour interpréter les résultats.

---

### **Applications**

1. **Agriculture** :
   - Détection des zones nécessitant une irrigation.
   - Suivi de la croissance des cultures.

2. **Gestion Forestière** :
   - Surveillance du stress végétal.
   - Détection de déforestation.

3. **Écosystèmes Naturels** :
   - Suivi des zones protégées.
   - Évaluation des impacts des changements climatiques.

---

### **Conclusion**
Les données Sentinel-2 offrent des outils puissants pour analyser la végétation et surveiller l’environnement. En utilisant les bandes spectrales et les indices appropriés, vous pouvez répondre à des problématiques agricoles, environnementales et climatiques.

---

